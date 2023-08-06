# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under
# the License.

from enum import IntEnum

DYNAMIC_FIELD_NAME = "$meta"
DEFAULT_PARTITION_NAME = "_default"
COLLECTION_NAME_KEY = "collection_name"
OUTPUT_FOLDER = "output"

MB = 1024 * 1024
GB = 1024 * MB


class IngestionType(IntEnum):
    ROW_BASED = 1
    COLUMN_BASED = 2


class CleanDataOptions(IntEnum):
    CLEAN_SUCCEED_IMPORT_DATA = 1
    CLEAN_FAILED_IMPORT_DATA = 2
    CLEAN_ALL_DATA = CLEAN_SUCCEED_IMPORT_DATA | CLEAN_FAILED_IMPORT_DATA


class TaskState(IntEnum):
    NoState = 0
    Persisted = 1
    Uploaded = 2
    ImportStarted = 3
    ImportFailed = 4
    ImportSucceed = 5