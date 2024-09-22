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
