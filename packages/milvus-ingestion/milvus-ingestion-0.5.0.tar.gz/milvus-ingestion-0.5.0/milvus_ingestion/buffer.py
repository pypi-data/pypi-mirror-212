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
import json
from typing import List

import numpy

from logging import Logger
from threading import Lock

from pymilvus import (
    DataType,
)

from .util import (
    Base,
    default_logger,
    _current_datetime,
)

from .constants import (
    IngestionType,
    TaskState,
    DEFAULT_PARTITION_NAME,
    DYNAMIC_FIELD_NAME,
    COLLECTION_NAME_KEY,
    MB,
    GB,
)

from .data_info import (
    DataInfo,
)

from .exceptions import (
    IngestionException,
    ErrorCode,
)

default_values = {
    DataType.BOOL.name: False,
    DataType.INT8.name: 0,
    DataType.INT16.name: 0,
    DataType.INT32.name: 0,
    DataType.INT64.name: 0,
    DataType.FLOAT.name: 0.0,
    DataType.DOUBLE.name: 0,
    DataType.VARCHAR.name: "",
    DataType.JSON.name: {},
}

type_size = {
    DataType.BOOL.name: 1,
    DataType.INT8.name: 8,
    DataType.INT16.name: 8,
    DataType.INT32.name: 8,
    DataType.INT64.name: 8,
    DataType.FLOAT.name: 8,
    DataType.DOUBLE.name: 8,
}

type_validator = {
    DataType.BOOL.name: lambda x: isinstance(x, bool),
    DataType.INT8.name: lambda x: isinstance(x, int) and -128 <= x <= 127,
    DataType.INT16.name: lambda x: isinstance(x, int) and -32768 <= x <= 32767,
    DataType.INT32.name: lambda x: isinstance(x, int) and -2147483648 <= x <= 2147483647,
    DataType.INT64.name: lambda x: isinstance(x, int),
    DataType.FLOAT.name: lambda x: isinstance(x, float),
    DataType.DOUBLE.name: lambda x: isinstance(x, float),
    DataType.VARCHAR.name: lambda x, l: isinstance(x, str) and len(x) <= l,
    DataType.JSON.name: lambda x: isinstance(x, dict),
    DataType.FLOAT_VECTOR.name: lambda x, dim: isinstance(x, list) and len(x) == dim,
    DataType.BINARY_VECTOR.name: lambda x, dim: isinstance(x, bytes) and len(x) * 8 == dim
}

class Buffer(Base):
    def __init__(
            self,
            collection_schema: dict,
            partition_name: str,
            logger: Logger,
        ):
        super().__init__(logger=logger)
        self._collection_schema = collection_schema
        self._partition_name = partition_name
        self._target_fields = {}
        self._buffer_size = 0
        self._buffer_row_count = 0
        self._sealed = False

        for field in self._collection_schema['fields']:
            self._target_fields[field['name']] = field

    @property
    def collection_schema(self) -> dict:
        return self._collection_schema

    @property
    def partition_name(self) -> str:
        return self._partition_name

    @property
    def collection_name(self) -> str:
        if COLLECTION_NAME_KEY in self._collection_schema:
            return self._collection_schema[COLLECTION_NAME_KEY]
        else:
            return ""

    @property
    def ingestion_type(self):
        msg = "The ingestion_type property is not implemented"
        self._print_err(msg)
        raise Exception(msg)

    @property
    def buffer_size(self)->int:
        return self._buffer_size

    @property
    def buffer_row_count(self)->int:
        return self._buffer_row_count

    @property
    def sealed(self)->bool:
        return self._sealed

    def set_sealed(self):
        self._sealed = True

    def append_row(self, row: dict, partition_name: str = None):
        msg = "The append_row() interface is not implemented"
        self._print_err(msg)
        raise Exception(msg)

    def persist(self, local_path: str):
        msg = "The persist() interface is not implemented"
        self._print_err(msg)
        raise Exception(msg)

    def pop(self, row: int):
        msg = "The pop() interface is not implemented"
        self._print_err(msg)
        raise Exception(msg)

    def _verify_row(self, row: dict, partition_name: str = None)->bool:
        if not isinstance(row, dict):
            self._print_err("The input row must be a dict object")
            return False

        if len(self._target_fields) == 0:
            self._print_err("Target collection schema is empty")
            return False

        if ("enable_dynamic_field" not in self._collection_schema)\
                or (not self._collection_schema["enable_dynamic_field"]):
            for k in row:
                if k not in self._target_fields:
                    self._print_err("Field name '{}' is not defined in collection '{}'. "
                                    "And the collection dynamic field is not enabled."
                                    .format(k, self._collection_schema[COLLECTION_NAME_KEY]))
                    return False

        row_size = 0
        for k in self._target_fields:
            if k not in row:
                self._print_err("'{}' is missed in the row".format(k))
                # TODO: set default value
                return False

            field = self._target_fields[k]
            if 'is_parimary' in field and field['auto_id']:
                self._print_err("The primary key field '{}' is auto-id, no need to provide".format(k))
                return False

            if 'is_partition_key' in field and field['is_partition_key'] and (partition_name is not None):
                self._print_err("The collection has partition key field '{}', not able to insert with partition name"
                                .format(k))
                return False

            dtype = DataType(field['type'])
            validator = type_validator[dtype.name]
            if dtype == DataType.BINARY_VECTOR or dtype == DataType.FLOAT_VECTOR:
                dim = field['params']['dim']
                if not validator(row[k], dim):
                    self._print_err("Illegal vector data for vector field '{}'".format(dtype.name))
                    return False

                vec_size = len(row[k])*4 if dtype == DataType.FLOAT_VECTOR else len(row[k])/8
                row_size = row_size + vec_size
            elif dtype == DataType.VARCHAR:
                max_len = field['params']['max_length']
                if not validator(row[k], max_len):
                    self._print_err("Illegal varchar value for field '{}'".format(dtype.name))
                    return False
                row_size = row_size + len(row[k])
            else:
                if not validator(row[k]):
                    self._print_err("Illegal scalar value for field '{}'".format(dtype.name))
                    return False
                row_size = row_size + type_size[dtype.name]

        self._buffer_size = self._buffer_size + row_size
        self._buffer_row_count = self._buffer_row_count + 1
        return True


class RowBuffer(Buffer):
    def __init__(
            self,
            collection_schema: dict,
            partition_name: str = None,
            logger: Logger = default_logger,
        ):
        super().__init__(collection_schema=collection_schema, partition_name=partition_name, logger=logger)
        self._buffer = []

    @property
    def ingestion_type(self)->IngestionType:
        return IngestionType.ROW_BASED

    def append_row(self, row: dict, partition_name: str = None) -> bool:
        if not self._verify_row(row=row, partition_name=partition_name):
            return False

        # expand dynamic values
        # for example:
        # {"id":1, "vec":[], "$meta": {"x": 5}, "y": 1} --> {"id":1, "vec":[], "x": 5, "y": 1}
        if DYNAMIC_FIELD_NAME in row:
            if isinstance(row[DYNAMIC_FIELD_NAME], dict):
                dynamic_values = row[DYNAMIC_FIELD_NAME]
                del row[DYNAMIC_FIELD_NAME]
                row.update(dynamic_values)

        if self.sealed:
            raise IngestionException(code=ErrorCode.BUFFER_SEALED)
        self._buffer.append(row)
        return True

    def persist(self, local_path: str)->DataInfo:
        full_file_name = os.path.join(local_path, "rows.json")

        row_count = len(self._buffer)
        if row_count != self._buffer_row_count:
            self._print_err("Actual row count {} doesn't equal to calculated row count {}"
                            .format(row_count, self._buffer_row_count))

        content = {
            "rows": self._buffer,
        }
        try:
            with open(full_file_name, 'w', encoding='utf-8') as f:
                json.dump(obj=content, fp=f, ensure_ascii=False)
            self._print_info("Successfully persist row-based file {}".format(full_file_name))
        except Exception as e:
            self._print_err("Failed to persist row-based file {}, error: {}".format(full_file_name, e))

        info = DataInfo()
        info.collection_name = self.collection_name
        info.partition_name = self.partition_name
        info.local_folder = local_path
        info.ingestion_type = self.ingestion_type
        info.data_size = self.buffer_size
        info.row_count = self.buffer_row_count
        info.local_files = [full_file_name]
        info.bulkinsert_state = TaskState.Persisted.name
        info.save()
        return info

    def pop(self, row_count: int)->list:
        if row_count <= 0:
            self._print_err("Illegal row_count value: {}".format(row_count))
            return []

        if len(self._buffer) == 0:
            return []

        rows = self._buffer[:row_count]
        self._buffer = self._buffer[row_count:]
        self._buffer_row_count = len(self._buffer)
        return rows


class ColumnBuffer(Buffer):
    def __init__(
            self,
            collection_schema: dict,
            partition_name: str = None,
            logger: Logger = default_logger,
        ):
        super().__init__(collection_schema=collection_schema, partition_name=partition_name, logger=logger)
        self._buffer = {}
        for field_name in self._target_fields:
            self._buffer[field_name] = []

        # dynamic field, internal name is '$meta'
        if ("enable_dynamic_field" in self._collection_schema) \
                and (self._collection_schema["enable_dynamic_field"]):
            self._buffer[DYNAMIC_FIELD_NAME] = []

    @property
    def ingestion_type(self)->IngestionType:
        return IngestionType.COLUMN_BASED

    def append_row(self, row: dict, partition_name: str = None) -> bool:
        if not self._verify_row(row=row, partition_name=partition_name):
            return False

        dynamic_values = {}
        if DYNAMIC_FIELD_NAME in row:
            if not isinstance(row[DYNAMIC_FIELD_NAME], dict):
                self._print_err("Dynamic field '{}' value should be JSON format".format(DYNAMIC_FIELD_NAME))
                return False

        if self.sealed:
            raise IngestionException(code=ErrorCode.BUFFER_SEALED)

        for k in row:
            if k == DYNAMIC_FIELD_NAME:
                dynamic_values.update(row[k])
                continue

            if k not in self._buffer:
                dynamic_values[k] = row[k]
            else:
                self._buffer[k].append(row[k])

        self._buffer[DYNAMIC_FIELD_NAME].append(json.dumps(dynamic_values))
        return True

    def persist(self, local_path: str)-> DataInfo:
        file_list = []
        row_count = -1
        for k in self._buffer:
            if row_count < 0:
                row_count = len(self._buffer[k])
            elif row_count != len(self._buffer[k]):
                self._print_err("Column `{}` row count {} doesn't equal to the first column row count {}"
                                .format(k, len(self._buffer[k]), row_count))

            full_file_name = os.path.join(local_path, k + ".npy")
            file_list.append(full_file_name)
            try:
                numpy.save(full_file_name, self._buffer[k])
            except Exception as e:
                self._print_err("Failed to persist column-based file {}, error: {}".format(full_file_name, e))
                break

            self._print_info("Successfully persist column-based file {}".format(full_file_name))

        if row_count != self._buffer_row_count:
            self._print_err("Actual row count {} doesn't equal to calculated row count {}"
                            .format(row_count, self._buffer_row_count))

        if len(file_list) != len(self._buffer):
            self._print_err("Some of fields were not persisted successfully, abort the files")
            for f in file_list:
                os.unlink(f)
            os.rmdir(local_path)
            file_list.clear()

        info = DataInfo()
        info.collection_name = self.collection_name
        info.partition_name =self.partition_name
        info.local_folder = local_path
        info.ingestion_type = self.ingestion_type
        info.data_size = self.buffer_size
        info.row_count = self.buffer_row_count
        info.local_files = file_list
        info.bulkinsert_state = TaskState.Persisted.name
        info.save()
        return info

    def pop(self, row_count: int)->list:
        if row_count <= 0:
            self._print_err("Illegal row_count value: {}".format(row_count))
            return []

        if len(self._buffer) == 0:
            return []

        # avoid an unexpected case that row count of fields are unequal
        total_row_count = len(self._buffer[0])
        for k in self._buffer:
            if len(self._buffer[k]) < total_row_count:
                total_row_count = len(self._buffer[k])

        rows = []
        for i in range(row_count):
            if i >= total_row_count:
                break
            row = {}
            for k in self._buffer:
                if k == DYNAMIC_FIELD_NAME:
                    row.update(self._buffer[k])
                else:
                    row[k] = self._buffer[k][i]
            rows.append(row)

        # cut the buffer
        for k in self._buffer:
            self._buffer[k] = self._buffer[k][len(rows):]

        self._buffer_row_count = len(self._buffer[0])
        return rows


class MultiBuffer(Buffer):
    def __init__(
            self,
            collection_schema: dict,
            ingestion_type: IngestionType,
            buffer_max_size: int = 512*MB,
            logger: Logger = default_logger,
        ):
        super().__init__(collection_schema=collection_schema,
                         partition_name=None,
                         logger=logger)
        self._ingestion_type = ingestion_type
        self._buffers = {}
        self._buffer_max_size = buffer_max_size
        self._buffer_lock = Lock()

    def set_buffer_max_size(self, max_size: int):
        if max_size <= 0:
            max_size = 512*MB
        self._buffer_max_size = max_size

    @property
    def ingestion_type(self)->IngestionType:
        return self._ingestion_type

    @property
    def buffer_row_count(self) -> int:
        total_count = 0
        with self._buffer_lock:
            for k in self._buffers:
                total_count = total_count + self._buffers[k].buffer_row_count
        return total_count

    @property
    def buffer_size(self) -> int:
        total_size = 0
        with self._buffer_lock:
            for k in self._buffers:
                total_size = total_size + self._buffers[k].buffer_size
        return total_size

    def _new_buffer(self, partition_name: str):
        # here we always create RowBuffer because the append() method of RowBuffer is thread-safe,
        # we convert RowBuffer to ColumnBuffer when persist() is called.
        return RowBuffer(collection_schema=self._collection_schema,
                         partition_name=partition_name,
                         logger=self._logger)

    def append_row(self, row: dict, partition_name: str = None) -> bool:
        if self._collection_schema is None:
            self._print_err("Failed to append row, collection not specified")
            return False

        if partition_name is None:
            partition_name = DEFAULT_PARTITION_NAME

        with self._buffer_lock:
            if partition_name not in self._buffers:
                self._buffers[partition_name] = self._new_buffer(partition_name=partition_name)

        try:
            ok = self._buffers[partition_name].append_row(row=row)
            return ok
        except IngestionException as e:
            # sealed buffer not allow append, might be in persist process, retry again
            if e.code == ErrorCode.BUFFER_SEALED:
                return self._buffers[partition_name].append_row(row=row)

    def has_large_buffer(self)->bool:
        with self._buffer_lock:
            for k in self._buffers:
                if self._buffers[k].buffer_size >= self._buffer_max_size:
                    return True
        return False

    def _convert_buffer(self, row_buffer: RowBuffer)->ColumnBuffer:
        if row_buffer.buffer_row_count <= 0:
            return None

        size_per_row = row_buffer.buffer_size/row_buffer.buffer_row_count
        if size_per_row < 1:
            size_per_row = 1
        batch_row_count = int(8*MB/size_per_row)
        if batch_row_count < 1:
            batch_row_count = 1

        new_buffer = ColumnBuffer(collection_schema=row_buffer.collection_schema,
                                  partition_name=row_buffer.partition_name,
                                  logger=self._logger)
        while True:
            rows = row_buffer.pop(batch_row_count)
            if len(rows) == 0:
                break
            for row in rows:
                new_buffer.append_row(row)

        return new_buffer

    def persist(self, local_path: str, force: bool=False)->List[DataInfo]:
        os.makedirs(name=local_path, exist_ok=True)

        to_persist_buffers = []
        with self._buffer_lock:
            for k in self._buffers:
                if (not force) and (self._buffers[k].buffer_size < self._buffer_max_size):
                    continue

                if force:
                    self._print_info("Force to persist buffer to local data path"
                                     .format(self._buffers[k].buffer_size, self._buffer_max_size))
                else:
                    self._print_info("Buffer size({} bytes) exceeds max size({} bytes), persist to local data path"
                                     .format(self._buffers[k].buffer_size, self._buffer_max_size))
                to_persist_buffers.append(self._buffers[k])
                self._buffers[k].set_sealed()
                self._buffers[k] = self._new_buffer(partition_name=k)

        info_list = []
        for buffer in to_persist_buffers:
            if self.ingestion_type == IngestionType.COLUMN_BASED and isinstance(buffer, RowBuffer):
                new_buffer = self._convert_buffer(buffer)
                if new_buffer is None:
                    continue
                buffer = new_buffer

            # create path [local_data_path]/[collection_name]/[partition_name]/[datetime]/
            collection_folder = os.path.join(local_path, self._collection_schema[COLLECTION_NAME_KEY])
            os.makedirs(name=collection_folder, exist_ok=True)
            partition_folder = os.path.join(collection_folder, buffer.partition_name)
            os.makedirs(name=partition_folder, exist_ok=True)
            dt_folder = os.path.join(partition_folder, _current_datetime())
            os.makedirs(name=dt_folder, exist_ok=True)
            info = buffer.persist(dt_folder)
            info_list.append(info)

            self._print_info("Successfully persist files: {} with row count {}".format(info.local_files, info.row_count))

        return info_list

    def pop(self, row_count: int)->(str, list):
        empty_buffers = []
        partition_name = ""
        pop_rows = []
        for k in self._buffers:
            buffer = self._buffers[k]
            rows = buffer.pop(row_count)
            if len(rows) > 0:
                partition_name = k
                pop_rows = rows
                break
            else:
                empty_buffers.append(k)

        for k in empty_buffers:
            del self._buffers[k]
        return partition_name, pop_rows

