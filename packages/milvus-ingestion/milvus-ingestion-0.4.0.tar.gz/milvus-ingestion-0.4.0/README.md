# milvus-ingestion
A tool to help data ingestion for Milvus.

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
field2 = FieldSchema(name="book_intro", dtype=DataType.FLOAT_VECTOR, dim=_128)
field3 = FieldSchema(name="book_name", dtype=DataType.VARCHAR, max_length=64)
schema = CollectionSchema(fields=[field1, field2, field3])
collection = Collection(name="demo", schema=schema)
```

- Declare a DataBuffer object, set the target collection, and specify a local folder to store buffer data.
```python
from milvus_ingestion import (
    DataBuffer,
)

data_buf = DataBuffer(target_collection = "demo", ocal_data_path = "output")
```

- The DataBuffer connect "localhost:19530" by default. Declare a MilvsConnector if you want to specify your Milvus service address.
```python
from milvus_ingestion import (
    DataBuffer,
    MilvusConnector,
)

data_buf = DataBuffer(
    target_collection = "demo",
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

- Upload the local files to MinIO/S3, and call Milvus bulkinsert() interface to import the data.
```python
data_buf.upload()
```

- The uploader connect MinIO/S3 by default address "0.0.0.0:9000", default access key "minioadmin" and default secret key "minioadmin". By default, the tool uses bucket name "a-bucket" to upload files to a remote path "milvus-ingestion". Declare an `MinioUploader` if you want to customize your MinIO/S3 service address. 
```python
from milvus_ingestion import (
    DataBuffer,
    MinioUploader,
)

data_buf = DataBuffer(
    target_collection = "demo",
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

- You can call `list_bulkinsert_tasks()` to list all the tasks that commited by this tool.
```python
print(json.dumps(data_buf.list_bulkinsert_tasks(), indent=2))
```

- You can call to clear the local data folder and remote files uploaded by this tool to save the disk space.
```python
data_buf.clear_data_folder()
```