# directory-structure-py

Python function collecting the metadata of a directory and its contents.

# Requirements

* Python &geq; 3.10

# Functions

| Function                    | Overview                                                                      |
| :-------------------------- | :---------------------------------------------------------------------------- |
| get_metadata_of_single_file | Retrieves metadata for a given file or directory using the `pathlib` module.    |
| get_metadata_of_files       | Recursively retrieves metadata for files and directories within a given path. |

# Data model of metadata

`get_metadata_of_single_file` returns a dict object with the following format:

```json
// for File
{
    "type": "File",
    "basename": "basename (ex. test.dat)",
    "name": "file name (ex. test.dat -> test)",
    "extension": "file extension (ex. test.dat -> .dat)",
    "contentSize": "file size (Byte)",
    "creationDatetime": "creation datetime (%Y-%m-%dT%H:%M:%S)",
    "modificationDatetime": "modification datetime (%Y-%m-%dT%H:%M:%S)"
}

// for Directory
{
    "type": "Directory",
    "basename": "basename (ex. test.dat)",
    "hasPart": ["basename of file or directory"],
    "contentSize": "file size (Byte)",
    "creationDatetime": "creation datetime (%Y-%m-%dT%H:%M:%S)",
    "modificationDatetime": "modification datetime (%Y-%m-%dT%H:%M:%S)"
}
```

`get_metadata_of_files` returns a dict object with the following format:

```json
{
    "root_path": "",
    "contents": ["metadata returned by get_metadata_of_single_file"]
}
```

# Installation

```sh
git clone https://github.com/Surpris/directory-structure-py.git
cd directory-structure-py
pip install .
```

# Usage

`python -m`:

```sh
python -m directory_structure_py <file_or_directory_path> \
    --dst <output_path> \
    --include_root_path // option
```

## python

### get_metadata_of_single_file

```python
from directory_structure_py import get_metadata_of_single_file

fpath: str = "file_or_directory_path"
metadata: dict = get_metadata_of_single_file(fpath)
```

### get_metadata_of_files

```python
from directory_structure_py import get_metadata_of_files

fpath: str = "file_or_directory_path"
metadata: dict = get_metadata_of_files(fpath)
```

# Example

```sh
# at the root directory of this repository
python -m directory_structure_py ./sample --dst sample.json
```

The contents of the `sample.json`:

```json
{
    "contents": [
        {
            "type": "Directory",
            "basename": "sample",
            "hasPart": [
                "data",
                "hogehoge",
                "readme.md"
            ],
            "contentSize": 0,
            "creationDatetime": "2024-09-25T12:16:08",
            "modificationDatetime": "2024-09-25T12:17:06"
        },
        {
            "type": "Directory",
            "basename": "data",
            "hasPart": [
                "data_001.csv",
                "data_002.csv"
            ],
            "contentSize": 0,
            "creationDatetime": "2024-09-25T12:17:06",
            "modificationDatetime": "2024-09-25T12:17:53"
        },
        {
            "type": "File",
            "basename": "data_001.csv",
            "name": "data_001",
            "extension": ".csv",
            "contentSize": 42,
            "creationDatetime": "2024-09-25T12:17:15",
            "modificationDatetime": "2024-09-25T12:18:08"
        },
        {
            "type": "File",
            "basename": "data_002.csv",
            "name": "data_002",
            "extension": ".csv",
            "contentSize": 41,
            "creationDatetime": "2024-09-25T12:17:48",
            "modificationDatetime": "2024-09-25T12:18:05"
        },
        {
            "type": "Directory",
            "basename": "hogehoge",
            "hasPart": [
                "fuga.txt"
            ],
            "contentSize": 0,
            "creationDatetime": "2024-09-25T12:16:46",
            "modificationDatetime": "2024-09-25T12:16:51"
        },
        {
            "type": "File",
            "basename": "fuga.txt",
            "name": "fuga",
            "extension": ".txt",
            "contentSize": 6,
            "creationDatetime": "2024-09-25T12:16:51",
            "modificationDatetime": "2024-09-25T12:16:55"
        },
        {
            "type": "File",
            "basename": "readme.md",
            "name": "readme",
            "extension": ".md",
            "contentSize": 142,
            "creationDatetime": "2024-09-25T12:16:19",
            "modificationDatetime": "2024-09-25T12:27:38"
        }
    ]
}
```
