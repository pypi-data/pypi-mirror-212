# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under
# the License.

import time

from typing import List
from logging import Logger

from pymilvus import (
    connections,
    Collection,
    utility,
    DefaultConfig,
    BulkInsertState,
)
from pymilvus.client.types import LoadState

from .util import (
    Base,
    default_logger,
)


class MilvusConnector(Base):
    def __init__(
            self,
            address: str,
            alias: str = DefaultConfig.MILVUS_CONN_ALIAS,
            user: str = "",
            password: str = "",
            db_name: str = "",
            token: str = "",
            uri: str = None,
            host: str = None,
            port: str = None,
            secure: bool = False,
            client_key_path: str = None,
            ca_pem_path: str = None,
            server_pem_path: str = None,
            server_name: str = None,
            logger: Logger = default_logger,
        ):
        super().__init__(logger=logger)
        self._address = address
        self._alias = alias
        self._user = user
        self._password = password
        self._db_name = db_name
        self._token = token
        self._uri = uri
        self._host = host
        self._port = port
        self._secure = secure
        self._client_key_path = client_key_path
        self._ca_pem_path = ca_pem_path
        self._server_pem_path = server_pem_path
        self._server_name = server_name

    def __connect(self)->bool:
        try:
            if not connections.has_connection(alias=self._alias):
                connections.connect(address=self._address,
                                    alias=self._alias,
                                    user=self._user,
                                    password=self._password,
                                    db_name=self._db_name,
                                    token=self._token,
                                    uri=self._uri,
                                    host=self._host,
                                    port=self._port,
                                    secure=self._secure,
                                    client_key_path=self._client_key_path,
                                    ca_pem_path=self._ca_pem_path,
                                    server_pem_path=self._server_pem_path,
                                    server_name=self._server_name)
            return True
        except Exception as e:
            self._print_err("Failed to connect milvus with address '{}', error: {}".format(self._address, e))
            return False

    def collection_schema(self, collection_name: str)->{}:
        if not self.__connect():
            return None

        if not utility.has_collection(collection_name=collection_name, using=self._alias):
            self._print_err("Collection '{}' doesn't exist".format(collection_name))
            return None

        collection = Collection(name=collection_name, using=self._alias)
        return collection.describe()

    def verify_input(self, collection_name: str, partition_name: str)->(bool, str):
        if not self.__connect():
            return False, "Connection is not ok"

        if not utility.has_collection(collection_name=collection_name, using=self._alias):
            msg = "Collection '{}' doesn't exist".format(collection_name)
            self._print_err(msg)
            return False, msg

        if partition_name is not None:
            if not utility.has_partition(collection_name=collection_name,
                                         partition_name=partition_name,
                                         using=self._alias):
                msg = "Partition '{}' doesn't exist".format(partition_name)
                self._print_err(msg)
                return False, msg

        return True, ""

    def flush(self, collection_name: str):
        if utility.has_collection(collection_name=collection_name):
            collection = Collection(name=collection_name, using=self._alias)
            collection.flush()

    def insert(self, data, collection_name: str, partition_name: str=None)->list:
        ok, msg = self.verify_input(collection_name, partition_name)
        if not ok:
            return []

        collection = Collection(name=collection_name, using=self._alias)
        res = collection.insert(data=data, partition_name=partition_name)
        return res.primary_keys

    def bulk_insert(self, files: list, collection_name: str, partition_name: str=None)->(int, str):
        ok, msg = self.verify_input(collection_name, partition_name)
        if not ok:
            return 0, msg

        id = utility.do_bulk_insert(files=files, collection_name=collection_name, partition_name=partition_name)
        self._print_info("Bulkinsert to milvus, task id: {}, files: {}, ".format(id, files))
        return id, ""

    def wait_bulkinsert_task(self, task_id: int)->BulkInsertState:
        while True:
            self._print_info("Waiting for bulkinsert task {} ...".format(task_id))
            try:
                state = utility.get_bulk_insert_state(task_id=task_id)
                if state.state == BulkInsertState.ImportFailed \
                        or state.state == BulkInsertState.ImportFailedAndCleaned:
                    self._print_err("The bulkinsert task {} failed, reason: {}"
                                    .format(state.task_id, state.failed_reason))
                    return state
                elif state.state == BulkInsertState.ImportCompleted:
                    self._print_info("The bulkinsert task {} is done, {} rows were imported into collection '{}' partition '{}'"
                                     .format(task_id, state.row_count, state.collection_name, state.partition_name))
                    return state
            except Exception as e:
                self._print_err("Failed to get state of bulkinsert task {}, error: {}".format(task_id, e))
                break

            time.sleep(1)
        return None

    def refresh_load(self, collection_list: List[str]):
        for collection_name in collection_list:
            state = utility.load_state(collection_name=collection_name)
            if state == LoadState.Loaded:
                self._print_info("Waiting for the new data be fully indexed in collection '{}' ..."
                                 .format(collection_name))
                utility.wait_for_index_building_complete(collection_name=collection_name)
                self._print_info("Waiting for collection '{}' loading the new data ...".format(collection_name))
                collection = Collection(name=collection_name)
                collection.load(_refresh=True)
                self._print_info("Collection '{}' finished loading, {} rows"
                                 .format(collection_name, collection.num_entities))

    def num_entities(self, collection_name: str):
        if utility.has_collection(collection_name=collection_name):
            collection = Collection(name=collection_name)
            return collection.num_entities
        return 0

default_milvus = MilvusConnector(address="localhost:19530")
