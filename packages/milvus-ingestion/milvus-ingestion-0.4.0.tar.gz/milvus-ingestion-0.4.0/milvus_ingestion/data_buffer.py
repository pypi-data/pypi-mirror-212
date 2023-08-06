# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under
# the License.

import os
import shutil
from typing import List

from logging import Logger
from threading import Lock

from pymilvus import BulkInsertState

from .util import (
    Base,
    default_logger,
)

from .constants import (
    IngestionType,
    CleanDataOptions,
    OUTPUT_FOLDER,
    DEFAULT_PARTITION_NAME,
    MB,
    GB,
)

from .milvus_connector import (
    MilvusConnector,
    default_milvus,
)

from .uploader import (
    Uploader,
    default_uploader,
)

from.buffer import (
    MultiBuffer,
)

from .data_info import (
    DATAINFO_FILE_NAME,
    DataInfo,
)


class DataBuffer(Base):
    def __init__(
            self,
            target_collection: str,
            local_data_path: str = OUTPUT_FOLDER,
            milvus_connector: MilvusConnector = default_milvus,
            uploader: Uploader = default_uploader,
            ingestion_type: IngestionType = IngestionType.COLUMN_BASED,
            logger: Logger = default_logger(),
        ):
        self._args_check(target_collection, local_data_path, milvus_connector, uploader, ingestion_type)
        super().__init__(logger=logger)
        self._local_data_path = local_data_path
        self._milvus_connector = milvus_connector
        self._uploader = uploader
        self._ingestion_type = ingestion_type
        self._buffer_max_size = 512*MB
        self._buffer:MultiBuffer = None # RowBuffer or ColumnBuffer

        self._collection_schema = None
        self._set_target_collection(target_collection)

        self._upload_lock = Lock()

    def _args_check(self,
                    target_collection: str,
                    local_data_path: str,
                    milvus_connector: MilvusConnector,
                    uploader: Uploader,
                    ingestion_type: IngestionType,
                    ):
        def _raise_err(msg: str):
            self._print_err(msg)
            raise Exception(msg)

        if target_collection is None or len(target_collection) == 0:
            _raise_err("Target collection name cannot be null or empty")
        if local_data_path is None or len(local_data_path) == 0:
            _raise_err("Local data path be null or empty")
        if milvus_connector is None:
            _raise_err("Milvus connector cannot be null")
        if uploader is None:
            _raise_err("Uploader cannot be null")
        if not isinstance(ingestion_type, IngestionType):
            _raise_err("illegal ingestion type: {}".format(ingestion_type))

    def set_buffer_max_size(self, max_size: int):
        if max_size <= 0:
            max_size = 512*MB
        self._buffer_max_size = max_size
        if self._buffer is not None:
            self._buffer.set_buffer_max_size(self._buffer_max_size)

    def _set_target_collection(self, collection_name: str):
        if self._milvus_connector is None:
            msg = "Milvus connector is None"
            self._print_err(msg)
            raise Exception(msg)

        collection_schema = self._milvus_connector.collection_schema(collection_name=collection_name)
        if collection_schema is None:
            msg = "Failed to get schema for collection '{}'".format(collection_name)
            self._print_err()
            raise Exception(msg)

        self._collection_schema = collection_schema
        self._buffer = MultiBuffer(collection_schema=self._collection_schema,
                                   ingestion_type=self._ingestion_type,
                                   buffer_max_size=self._buffer_max_size,
                                   logger=self._logger)

    def append_row(self, row: dict, partition_name: str = None)->bool:
        if self._buffer is None:
            msg = "Failed to append row, collection not specified"
            self._print_err(msg)
            raise Exception(msg)

        if not self._buffer.append_row(row=row, partition_name=partition_name):
            return False

        if self._buffer.has_large_buffer():
            info_list = self._persist(force=False)
            for info in info_list:
                self._upload_import(info)

        return True

    def current_row_count(self):
        return self._buffer.buffer_row_count

    def _persist(self, force: bool)->List[DataInfo]:
        os.makedirs(name=self._local_data_path, exist_ok=True)

        to_persist_buffer = self._buffer
        self._buffer = MultiBuffer(collection_schema=self._collection_schema,
                                   ingestion_type=self._ingestion_type,
                                   logger=self._logger)

        info_list = to_persist_buffer.persist(local_path=self._local_data_path, force=force)
        if len(info_list) == 0:
            self._print_info("Nothing to persist")
            return []

        self._print_info("Successfully persist, buffer is reset")
        return info_list

    def persist(self) -> List[str]:
        info_list = self._persist(force=True)
        return [info.local_folder for info in info_list]

    def _update_info(self, info: DataInfo):
        ok, msg = info.save()
        if not ok:
            self._print_err(msg)

    def _upload_import(self, info: DataInfo)->int:
        if len(info.local_files) == 0:
            self._print_err("No local data files to upload")
            return 0

        if self._uploader is None:
            self._print_err("Uploader is None")
            return 0

        if self._milvus_connector is not None:
            ok, msg = self._milvus_connector.verify_input(info.collection_name, info.partition_name)
            if not ok:
                msg = "Unable to import files {}, error: {}".format(info.local_files, msg)
                self._print_err(msg)
                info.bulkinsert_done = False
                info.bulkinsert_err = msg
                self._update_info(info)
                return 0

        # upload files
        ok, remote_files = self._uploader.upload(files=info.local_files, relative_path=self._local_data_path)
        if not ok:
            msg = "Failed to upload files {}".format(info.local_files)
            self._print_err(msg)
            info.bulkinsert_done = False
            info.bulkinsert_err = msg
            self._update_info(info)
            return 0

        if self._milvus_connector is None:
            self._print_err("Milvus connector is None")
            return 0

        # call bulkinsert
        partition_name = None if info.partition_name == DEFAULT_PARTITION_NAME else info.partition_name
        task_id, msg = self._milvus_connector.bulk_insert(files=remote_files,
                                                          collection_name=info.collection_name,
                                                          partition_name=partition_name)
        if task_id == 0:
            self._print_err("Failed to import to collection '{}', partition '{}', error: {}"
                            .format(info.collection_name, partition_name, msg))
            info.bulkinsert_done = False
            info.bulkinsert_err = msg
            return 0
        self._print_info("Start a bulkinsert task to import files {}, task id: {}".format(remote_files, task_id))

        # write infomation into a json file
        info.bulkinsert_id = task_id
        info.remote_files = remote_files
        ok, msg = info.save()
        if not ok:
            self._print_err(msg)

        return task_id

    def upload(self, data_folder: str=None)->List[int]:
        if self._uploader is None:
            self._print_err("Uploader is None")
            return []

        if data_folder is None:
            data_folder = self._local_data_path

        task_list = []
        info_list = self._list_bulkinsert_tasks(data_folder)
        for info in info_list:
            if info.bulkinsert_done:
                continue

            task_id = self._upload_import(info)
            if task_id > 0:
                task_list.append(task_id)

        return task_list

    def wait_upload_finish(self, task_list: List[int]=None)->bool:
        if self._milvus_connector is None:
            self._print_err("Milvus connector is None")
            return False

        wait_info_list = []
        # find out the unfinished tasks
        all_info_list = self._list_bulkinsert_tasks()
        for info in all_info_list:
            if info.bulkinsert_id is None or info.bulkinsert_done:
                continue
            if task_list is not None:
                if info.bulkinsert_id in task_list:
                    wait_info_list.append(info)
            else:
                wait_info_list.append(info)

        # wait the unfinished tasks
        collection_list = []
        for info in wait_info_list:
            if info.collection_name not in collection_list:
                collection_list.append(info.collection_name)
            state = self._milvus_connector.wait_bulkinsert_task(info.bulkinsert_id)
            if state.state == BulkInsertState.ImportCompleted:
                self._print_info("Bulklinsert task {} completed".format(info.bulkinsert_id))
                info.bulkinsert_done = True
                info.bulkinsert_pk_ranges = list(state.id_ranges)
            elif state.state == BulkInsertState.ImportFailed or state.state == BulkInsertState.ImportFailedAndCleaned:
                self._print_err("Bulklinsert task {} failed with reason: {}"
                                .format(info.bulkinsert_id, info.bulkinsert_err))
                info.bulkinsert_done = False
                info.bulkinsert_err = state.failed_reason

            # update the info
            ok, msg = info.save()
            if not ok:
                self._print_err(msg)

        # refresh load the collections
        self._milvus_connector.refresh_load(collection_list)
        return True

    def _list_bulkinsert_tasks(self, data_folder: str=None)->List[DataInfo]:
        if data_folder is None:
            data_folder = self._local_data_path

        info_list = []
        for root, _, files in os.walk(data_folder):
            if DATAINFO_FILE_NAME in files:
                info = DataInfo()
                ok, msg = info.load(root)
                if not ok:
                    self._print_err(msg)
                    continue
                info_list.append(info)
        return info_list

    def list_bulkinsert_tasks(self) -> List[dict]:
        info_list = self._list_bulkinsert_tasks(self._local_data_path)
        return [info.to_dict() for info in info_list]

    def clear_data_folder(self, options: CleanDataOptions=CleanDataOptions.CLEAN_SUCCEED_IMPORT_DATA):
        self._print_warn("Clear the data folder '{}', all the local data will be deleted".format(self._local_data_path))

        def _remove_files(info: DataInfo):
            if len(info.local_files) > 0:
                for file in info.local_files:
                    os.remove(file)
            if len(info.remote_files) > 0:
                if self._uploader != None:
                    self._uploader.remove(info.remote_files)
            shutil.rmtree(info.local_folder)

        sub_paths = os.listdir(self._local_data_path)
        for p in sub_paths:
            full_path = os.path.join(self._local_data_path, p)
            if os.path.isdir(full_path):
                if options == CleanDataOptions.CLEAN_ALL_DATA:
                    shutil.rmtree(full_path)
                    continue

                info_list = self._list_bulkinsert_tasks(full_path)
                for info in info_list:
                    if info.bulkinsert_done and (options & CleanDataOptions.CLEAN_SUCCEED_IMPORT_DATA):
                        _remove_files(info)
                    if (not info.bulkinsert_done) and (options & CleanDataOptions.CLEAN_FAILED_IMPORT_DATA):
                        _remove_files(info)

    def direct_insert(self)->list:
        if self._milvus_connector is None:
            self._print_err("Milvus connector is None")
            return []

        row_count = self._buffer.buffer_row_count
        if self._buffer is None or row_count == 0:
            self._print_err("Buffer is empty")
            return []

        # reset the buffer
        to_persist_buffer = self._buffer
        self._buffer = MultiBuffer(collection_schema=self._collection_schema,
                                   ingestion_type=self._ingestion_type,
                                   logger=self._logger)

        size_per_row = to_persist_buffer.buffer_size/row_count
        batch = int(8*MB/size_per_row)
        if batch > row_count:
            batch = row_count

        self._print_info("{} rows in buffer, prepare to insert batch by batch, {} rows per batch"
                         .format(row_count, batch))

        collection_name = to_persist_buffer.collection_name
        primary_ids = []
        while True:
            partition_name, rows = to_persist_buffer.pop(batch)
            if len(rows) == 0:
                break

            if (partition_name == DEFAULT_PARTITION_NAME) or (len(partition_name) == 0):
                partition_name = None
            ids = self._milvus_connector.insert(data=rows,
                                                collection_name=collection_name,
                                                partition_name=partition_name)
            primary_ids.extend(ids)
            self._print_info("Finish insert {} rows into collection '{}' partition '{}'"
                             .format(len(rows), collection_name, partition_name))

        self._milvus_connector.flush(collection_name=collection_name)
        self._print_info("{} rows were inserted to collection '{}', the collection currently has {} rows"
                         .format(row_count, collection_name, self._milvus_connector.num_entities(collection_name)))
        return primary_ids

