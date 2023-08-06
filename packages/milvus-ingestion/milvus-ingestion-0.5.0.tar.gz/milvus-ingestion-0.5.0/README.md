# milvus-ingestion
A tool to help data ingestion for Milvus.

As we know, Milvus provides two kinds of data ingestion methods: `insert()` and `bulkinsert()`. The bulkinsert command notify the datanodes to read files from MinIO/S3, reduces network transmission across the Milvus client, proxy, Pulsar/Kafka, and data nodes. It is more efficient than the insert command.

But to call `bulkinsert()`, user need to generate data files and upload the files to MinIO/S3 by themselves. We build this tool to encapsulate the bulkinsert usage to reduce the work for users.
Users just append their data rows, this tool help to manage the data rows between memory, local disk, and remote MinIO/S3/Milvus service.

The major workflow of the tool:
1. User appends data rows, the tool helps to split the rows according to partitions, manages data blocks in memory.
2. Once a data block size hit a threshold, the tool flush the data block into local disk with different file format according to column-based or row-based type.
3. The tool can upload the data files to MinIO/S3 service and automatically calls Milvus bulkinsert interface to import the remote files.
5. The tool provides methods to check whether a data block is imported successfully or not. If a task is failed, user can try upload it again after error is fixed.
6. User can clean the local data files and remote files by just one call. 


## From source code
```commandline
git clone git@github.com:yhmo/milvus-ingestion.git
cd milvus-ingestion
pip3 install -r ./requirements.txt
```

## Installation
```commandline
pip3 install milvus-ingestion
```

## Requirement
python >= 3.7

## Compatibility
The following matrix shows Milvus versions and recommended milvus-ingestion versions:

| Milvus | milvus-ingestion |
|:------:|:----------------:|
| v2.2.9 |      v0.4.0      |

## Usage
- Assume you have created a collection in Milvus.
```python
field1 = FieldSchema(name="book_id", dtype=DataType.INT64, is_primary=True, auto_id=False)
field2 = FieldSchema(name="book_intro", dtype=DataType.FLOAT_VECTOR, dim=128)
field3 = FieldSchema(name="book_name", dtype=DataType.VARCHAR, max_length=64)
schema = CollectionSchema(fields=[field1, field2, field3], enable_dynamic_field=True)
collection = Collection(name="ingestion_demo", schema=schema)
```

- Declare a `DataBuffer` object, set the target collection, and specify a local folder to store buffer data.
```python
from milvus_ingestion import (
    DataBuffer,
)

data_buf = DataBuffer(target_collection = "demo", ocal_data_path = "output")
```

- The `DataBuffer` connect "localhost:19530" by default. Declare a `MilvsConnector` if you want to customize your Milvus service address.
```python
from milvus_ingestion import (
    DataBuffer,
    MilvusConnector,
)

data_buf = DataBuffer(
    target_collection = "ingestion_demo",
    local_data_path = "output",
    milvus_connector = MilvusConnector(
        address="xxx.xxx.xxx.xxx:19530",
        user="***",
        password="******",
))
```

- Append rows in JSON format. The rows are accumulated in a buffer. Once the buffer size exceeds 512MB(by default), the tool will flush the buffer to local data folder as JSON files or Numpy files.
```python
data_buf.append_row({
    "book_id": 1,
    "book_intro": [random.random() for _ in range(128)],
    "book_name": "this is my first book",
})

data_buf.append_row({
    "book_id": 2,
    "book_intro": [random.random() for _ in range(128)],
    "book_name": "this is my second book",
})
```

- Reset buffer limit size at your will. (Units: byte)
```python
data_buf.set_buffer_max_size(1024*1024*1024)
```

- Flush the buffer to local files. As the `local_data_path = "output"`, the files are stored into local folder "./output".
```python
data_buf.persist()
```
After `persist()`, the directory tree of "./output" is like this:
```shell
./output
└── ingestion_demo
    └── _default
        ├── 2023-06-05_10:23:41.189996
        │   ├── $meta.npy
        │   ├── book_id.npy
        │   ├── book_intro.npy
        │   ├── book_name.npy
        │   └── info.json
        └── 2023-06-05_10:23:41.608843
            ├── $meta.npy
            ├── book_id.npy
            ├── book_intro.npy
            ├── book_name.npy
            └── info.json
```
Each data block is put into a folder which is named by the timestamp when it created. Column-based data files are Numpy format. Row-based data files format  is JSON. There is a "info.json" for each data block to record necessary information for bulkinsert task.


- Upload the local files to MinIO/S3, and call Milvus `bulkinsert()` interface to import the data.
```python
data_buf.upload()
```
After `upload()`, you will see data files are uploaded to the MinIO server under the path "a-bucket/milvus-ingestion/ingestion_demo". And the Milvus server begins to import these files shortly.

- The uploader connect MinIO/S3 by default address "0.0.0.0:9000", default access key "minioadmin" and default secret key "minioadmin". By default, the tool uses bucket name "a-bucket" to upload files to a remote path "milvus-ingestion". Declare an `MinioUploader` if you want to customize your MinIO/S3 service address. 
```python
from milvus_ingestion import (
    DataBuffer,
    MinioUploader,
)

data_buf = DataBuffer(
    target_collection = "ingestion_demo",
    local_data_path = "output",
    uploader = MinioUploader(
        address="xxx.xxx.xxx.xxx:9000",
        access_key="***",
        secret_key="******",
        bucket_name="xxxxx",
        remote_path="xxxxx"
))
```

- The uploaded data is not visible immediately, call `wait_upload_finish()` before you search the data.
```python
data_buf.wait_upload_finish()
```

- You can call `list_bulkinsert_tasks()` to list all the tasks that committed by this tool.
```python
print(json.dumps(data_buf.list_bulkinsert_tasks(), indent=2))
```
A task infomation example:
```JSON
{
    "collection_name": "ingestion_demo",
    "partition_name": "_default",
    "ingestion_type": 2,
    "row_count": 2000,
    "data_size": 309778,
    "local_folder": "output/ingestion_demo/p1/2023-06-05_18:47:52.970121",
    "local_files": [
      "output/ingestion_demo/p1/2023-06-05_18:47:52.970121/book_id.npy",
      "output/ingestion_demo/p1/2023-06-05_18:47:52.970121/book_intro.npy",
      "output/ingestion_demo/p1/2023-06-05_18:47:52.970121/book_name.npy",
      "output/ingestion_demo/p1/2023-06-05_18:47:52.970121/$meta.npy"
    ],
    "remote_files": [
      "milvus-ingestion/ingestion_demo/p1/2023-06-05_18:47:52.970121/book_id.npy",
      "milvus-ingestion/ingestion_demo/p1/2023-06-05_18:47:52.970121/book_intro.npy",
      "milvus-ingestion/ingestion_demo/p1/2023-06-05_18:47:52.970121/book_name.npy",
      "milvus-ingestion/ingestion_demo/p1/2023-06-05_18:47:52.970121/$meta.npy"
    ],
    "bulkinsert_id": 441963163085003029,
    "bulkinsert_done": true,
    "bulkinsert_err": null,
    "bulkinsert_pk_ranges": []
}
```

- You can call `clear_data_folder()` to clear the local data folder and remote files uploaded by this tool to save the disk space.
```python
data_buf.clear_data_folder()
```

## API Reference

### Enums 
#### CleanDataOptions
As parameter of `DataBuffer.clear_data_folder()` method.
<table class="language-python">
	<thead>
        <tr>
            <th>Option</th>
            <th>Code</th>
            <th>Description</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>CLEAN_SUCCEED_IMPORT_DATA</code></td>
            <td>1</td>
            <td>Only delete the data files that have been uploaded and imported successfully to Milvus.</td>
        </tr>
        <tr>
            <td><code>CLEAN_FAILED_IMPORT_DATA</code></td>
            <td>2</td>
            <td>Delete the data files that failed to upload.</td>
        </tr>
        <tr>
            <td><code>CLEAN_ALL_DATA</code></td>
            <td><code>CLEAN_SUCCEED_IMPORT_DATA|CLEAN_FAILED_IMPORT_DATA</code></td>
            <td>Delete all data files under the local data path.</td>
        </tr>
	</tbody>
</table>

#### IngestionType
As a parameter to declare a `DataBuffer` object.
<table class="language-python">
	<thead>
        <tr>
            <th>Type</th>
            <th>Code</th>
            <th>Description</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>ROW_BASED</code></td>
            <td>1</td>
            <td>Persist data in a row-based JSON format file.</td>
        </tr>
        <tr>
            <td><code>COLUMN_BASED</code></td>
            <td>2</td>
            <td>Persist data in column-based Numpy format files.</td>
        </tr>
	</tbody>
</table>

### Classes
#### DataBuffer
- **Constructor**

DataBuffer is the major functional class for users. A collection name is required, each DataBuffer object can only serve one collection.
```python
    def __init__(
            self,
            target_collection: str,
            local_data_path: str = OUTPUT_FOLDER,
            milvus_connector: MilvusConnector = default_milvus,
            uploader: Uploader = default_uploader,
            ingestion_type: IngestionType = IngestionType.COLUMN_BASED,
            logger: Logger = default_logger,
        )
```
Parameters list:
<table class="language-python">
	<thead>
        <tr>
            <th>Parameter</th>
            <th>Default Value</th>
            <th>Description</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>target_collection</code></td>
            <td>N/A</td>
            <td>A collection name is required, each DataBuffer object can only serve one collection. If the collection doesn't exist, the constructor will throw an exception.</td>
        </tr>
        <tr>
            <td><code>local_data_path</code></td>
            <td>"output"</td>
            <td>DataBuffer persists data files into this local folder. Make sure this path is accessible.</td>
        </tr>
        <tr>
            <td><code>milvus_connector</code></td>
            <td>A pymilvus connection to "localhost:19530"</td>
            <td>A MilvusConnector object to interact with Milvus server. The underlying API is pymilvus.</td>
        </tr>
        <tr>
            <td><code>uploader</code></td>
            <td>A MinIO client to "0.0.0.0:9000" with access_key="minioadmin" and secret_key="minioadmin".</td>
            <td>A MinIO client to interact with MinIO/S3 server. The underlying API is MinIO python client.</td>
        </tr>
        <tr>
            <td><code>ingestion_type</code></td>
            <td><code>IngestionType.COLUMN_BASED</code></td>
            <td>Decide which file format for the data files. Column-based using Numpy format, row-based using JSON format.</td>
        </tr>
        <tr>
            <td><code>logger</code></td>
            <td>A logging.Logger object prints log onto the console</td>
            <td>A logging.Logger object to print log, you can replace it with your logger object.</td>
        </tr>
	</tbody>
</table>

- **append_row()**

Append data by row in JSON format. The rows are accumulated in an in-memory buffer, split into data blocks for different partitions.
Once a data block size is larger or equal to a threshold, the data block will be flushed into local data folder.
This method returns `False` if the input row or `partition_name` is illegal.
```python
def append_row(self, row: dict, partition_name: str = None)->bool
```

Parameters list:
<table class="language-python">
	<thead>
        <tr>
            <th>Parameter</th>
            <th>Default Value</th>
            <th>Description</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>row</code></td>
            <td>N/A</td>
            <td>A data row in JSON format with each field's name as key, field's value as value. For dynamic field enabled collection, you can add extra key-value pairs at your will.</td>
        </tr>
        <tr>
            <td><code>partition_name</code></td>
            <td><code>None</code></td>
            <td>Specify which partition this row should be inserted in. If not specified, the row will be inserted into the default partition. For partition key enabled collection, you could not specify partition name.</td>
        </tr>
	</tbody>
</table>

- **clear_data_folder()**

Delete data files under the local data folder along with the remotes files accordingly.
```python
def clear_data_folder(self, options: CleanDataOptions=CleanDataOptions.CLEAN_SUCCEED_IMPORT_DATA)
```

Parameters list:
<table class="language-python">
	<thead>
        <tr>
            <th>Parameter</th>
            <th>Default Value</th>
            <th>Description</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>options</code></td>
            <td><code>CleanDataOptions.CLEAN_SUCCEED_IMPORT_DATA</code></td>
            <td>An option to decide which data files ought to be deleted. The default option only delete the data files that successfully uploaded to Milvus. With the option you can choose to keep the data files that failed to upload so that you can retry upload them later.</td>
        </tr>
	</tbody>
</table>

- **current_row_count()**

This method returns the current row count in the in-memory buffer. Once a data block is persisted to local files, its rows will not be counted in.
```python
def current_row_count(self)->int
```

- **direct_insert()**

This method calls the Milvus `insert()` interface to insert data directly. It inserts the data batch by batch with 8MB bytes per batch.
This method returns the auto-generated primary keys if the primary key is auto-id.
```python
def direct_insert(self)->List[int]
```

- **list_bulkinsert_tasks()**

Each data block will be uploaded to Milvus by a bulkinsert call. Bulkinsert tasks are running asynchronously. This method is used to check bulkinsert tasks states.
This method returns a list of JSON format dict to show the information of all the bulkinsert tasks committed by this DataBuffer.
```python
def list_bulkinsert_tasks(self) -> List[dict]
```

- **persist()**

The `append_row()` method can automatically persist data blocks to local disk, but sometimes user might need to call this method after he finished data ingestion.
This method will flush all the in-memory data blocks to local files, then upload them to MinIO and Milvus, finally returns a list of bulkinsert tasks ID. 
```python
def persist(self) -> List[str]
```

- **upload()**

Sometimes a data block is failed to upload to Milvus, this method allows user to retry upload the failed data files again and returns list of new bulkinsert tasks ID.
Internally, the method searches the "info.json" files under a local folder, and picks the failed tasks by reading the key "bulkinsert_done" in the "info.json" file.
```python
def upload(self, data_folder: str=None)->List[int]
```

Parameters list:
<table class="language-python">
	<thead>
        <tr>
            <th>Parameter</th>
            <th>Default Value</th>
            <th>Description</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>data_folder</code></td>
            <td><code>None</code></td>
            <td>Specify which local folder to be checked.</td>
        </tr>
	</tbody>
</table>


- **wait_upload_finish()**

Since Milvus bulkinsert tasks are running asynchronously, this method checks each task's state with an interval of 1 second.
This method returns `True` only when all the bulkinsert tasks are finished and the new data is fully indexed and loaded in Milvus.
Internal, this method calls `utility.get_bulk_insert_state()`, `utility.wait_for_index_building_complete()` and `collection.load(_refresh=True)` to check tasks.
```python
def wait_upload_finish(self, task_list: List[int]=None)->bool
```

Parameters list:
<table class="language-python">
	<thead>
        <tr>
            <th>Parameter</th>
            <th>Default Value</th>
            <th>Description</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>task_list</code></td>
            <td><code>None</code></td>
            <td>Specify which bulkinsert task to be waited. If this parameter is None, this method will search the entire local data path.</td>
        </tr>
	</tbody>
</table>

#### MilvusConnector
- **Constructor**

```python
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
        )
```

Parameters list:
<table class="language-python">
	<thead>
        <tr>
            <th>Parameter</th>
            <th>Default Value</th>
            <th>Description</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>logger</code></td>
            <td>A logging.Logger object prints log onto the console</td>
            <td>A logging.Logger object to print log, you can replace it with your logger object.</td>
        </tr>
	</tbody>
</table>

Note: for the other parameters' usage, following the [pymilvus connections.connect() API](https://github.com/milvus-io/pymilvus/blob/932fc82b247cc7e186da5e5124aa3c78ead760ff/pymilvus/orm/connections.py#L222).


#### MinioUploader
- **Constructor**

```python
    def __init__(
            self,
            bucket_name: str=DEFAULT_BUCKET_NAME,
            remote_path: str=DEFAULT_REMOTE_PATH,
            endpoint: str=None,
            access_key: str=None,
            secret_key: str=None,
            secure: bool=True,
            session_token: str=None,
            region: str=None,
            http_client=None,
            credentials=None,
            logger: Logger = default_logger
         )
```

Parameters list:
<table class="language-python">
	<thead>
        <tr>
            <th>Parameter</th>
            <th>Default Value</th>
            <th>Description</th>
        </tr>
	</thead>
	<tbody>
        <tr>
            <td><code>bucket_name</code></td>
            <td>"a-bucket"</td>
            <td>Specify the bucket name where the data files be uploaded to. Currently, we require it must be the bucket which the Milvus server depends on.</td>
        </tr>
        <tr>
            <td><code>remote_path</code></td>
            <td>"milvus-ingestion"</td>
            <td>A remote root path for the uploaded data files.</td>
        </tr>
        <tr>
            <td><code>logger</code></td>
            <td>A logging.Logger object prints log onto the console</td>
            <td>A logging.Logger object to print log, you can replace it with your logger object.</td>
        </tr>
	</tbody>
</table>

Note: for the other parameters' usage, following the [MinIO client API](https://github.com/minio/minio-py/blob/d67d8fb59167c75005b62d2c3256f16b9e316e2b/minio/api.py#L117).
