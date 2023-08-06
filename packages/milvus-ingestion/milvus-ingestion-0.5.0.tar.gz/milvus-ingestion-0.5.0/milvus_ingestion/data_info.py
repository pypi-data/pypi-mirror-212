# Copyright (C) 2019-2021 Zilliz. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under
# the License.

import json
import os

from .util import (
    Base,
)

from .constants import (
    TaskState,
)

DATAINFO_FILE_NAME = "info.json"


class DataInfo(Base):
    def __init__(self):
        self.collection_name = ""
        self.partition_name = None
        self.ingestion_type = None
        self.row_count = 0
        self.data_size = 0
        self.local_folder = ""
        self.local_files = []
        self.remote_files = []
        self.bulkinsert_id = None
        self.bulkinsert_state = TaskState.NoState.name
        self.bulkinsert_err = None
        self.bulkinsert_pk_ranges = None

    def to_dict(self):
        return self.__dict__

    def save(self)->(bool, str):
        if len(self.local_folder) == 0:
            return False, "DataInfo's local folder is not specified"
        try:
            full_name = os.path.join(self.local_folder, DATAINFO_FILE_NAME)
            with open(full_name, 'w', encoding='utf-8') as f:
                json.dump(obj=self.to_dict(), fp=f, indent=2, ensure_ascii=False)
            return True, ""
        except Exception as e:
            return False, "Failed to save DataInfo to {}, error: {}".format(self.local_folder, e)

    def load(self, local_folder: str)->(bool, str):
        try:
            full_name = os.path.join(local_folder, DATAINFO_FILE_NAME)
            with open(full_name, 'r', encoding='utf-8') as f:
                a = json.load(f)
                if not isinstance(a, dict):
                    return False, "The content in file {} is invalid to DataInfo".format(full_name)
                self.collection_name = a["collection_name"] if "collection_name" in a else ""
                self.partition_name = a["partition_name"] if "partition_name" in a else None
                self.ingestion_type = a["ingestion_type"] if "ingestion_type" in a else None
                self.row_count = a["row_count"] if "row_count" in a else 0
                self.data_size = a["data_size"] if "data_size" in a else 0
                self.local_folder = local_folder
                self.local_files = a["local_files"] if "local_files" in a else []
                self.remote_files = a["remote_files"] if "remote_files" in a else []
                self.bulkinsert_id = a["bulkinsert_id"] if "bulkinsert_id" in a else None
                self.bulkinsert_state = a["bulkinsert_state"] if "bulkinsert_state" in a else TaskState.NoState.name
                self.bulkinsert_err = a["bulkinsert_err"] if "bulkinsert_err" in a else None
                self.bulkinsert_pk_ranges = a["bulkinsert_pk_ranges"] if "bulkinsert_pk_ranges" in a else None
            return True, ""
        except Exception as e:
            return False, "Failed to load DataInfo, error: {}".format(e)
