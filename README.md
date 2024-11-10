# directory-structure-py

Python function collecting the metadata of a directory and its contents.

# Requirements

* Python &geq; 3.10 (3.10 \~ 3.12 are tested by the GitHub Actions.)

# Functions

| Function                    | Overview                                                                      |
| :-------------------------- | :---------------------------------------------------------------------------- |
| get_metadata_of_single_file | Retrieves metadata for a given file or directory using the `pathlib` module.  |
| get_metadata_of_files       | Recursively retrieves metadata for files and directories within a given path. |

# Data model of metadata

`get_metadata_of_single_file` returns a dict object with the following format:

```json
// for File
{
    "@id": "id unique in the metadata tree",
    "type": "File",
    "parent": "parent directory info including '@id'",
    "basename": "basename (ex. test.dat)",
    "name": "file name (ex. test.dat -> test)",
    "extension": "file extension (ex. test.dat -> .dat)",
    "contentSize": "file size (Byte)",
    "creationDatetime": "creation datetime (%Y-%m-%dT%H:%M:%S)",
    "modificationDatetime": "modification datetime (%Y-%m-%dT%H:%M:%S)"
}

// for Directory
{
    "@id": "id unique in the metadata tree",
    "type": "Directory",
    "parent": "parent directory info including '@id'",
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
    "root_path": "root path. The value will be '.' if the 'include_root_path' option is not set",
    "contents": ["metadata returned by get_metadata_of_single_file"]
}
```

# Installation

## `pip install` from repository

```sh
pip install git+https://github.com/Surpris/directory-structure-py.git
```

## `git clone` and `pip install`

```sh
git clone https://github.com/Surpris/directory-structure-py.git
cd directory-structure-py
pip install .
```

## portable (only for Windows)

The portable file is also provided only for Windows. You can download it via the release section and decompress it.

# Usage

## CLI

`python -m`:

```sh
python -m directory_structure_py <file_or_directory_path> \
    --dst <output_path> \
    --include_root_path \ // option
    --in_tree \ // option
    --to_tsv // option
```

Options:

| Item                | Type | Description                                                                     |
| :------------------ | :--- | :------------------------------------------------------------------------------ |
| `dst`               | str  | destination path of the json output                                             |
| `include_root_path` | bool | include `file_or_directory_path` with the key `root_path` if this option is set |
| `in_tree`           | bool | output the metadata in a tree format if this option is set                      |
| `to_tsv`            | bool | output a TSV-format file if this option is set                                  |

## Batch file (only for Windows)

Drag the directory or file and drop it on the batch file "directory_structure_py.bat".
By default, the following files are output to the same directory as where "directory_structure_py.bat" is located.

* `directory_structure_metadata.json`: a metadata tree is included.
* `directory_structure_metadata.tsv`: a metadata list is included.

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

## output the metadata in a list

```sh
# at the root directory of this repository
python -m directory_structure_py ./sample --dst sample.json --to_tsv
```

An example of the contents of the `sample.json` is shown below:

```json
{
    "root_path": ".",
    "contents": [
        {
            "@id": ".",
            "type": "Directory",
            "parent": {},
            "basename": "sample",
            "hasPart": [
                {
                    "@id": "data"
                },
                {
                    "@id": "directory_structure_metadata.json"
                },
                {
                    "@id": "directory_structure_metadata.tsv"
                },
                {
                    "@id": "hogehoge"
                },
                {
                    "@id": "readme.md"
                }
            ],
            "contentSize": 4096,
            "creationDatetime": "2024-09-25T12:16:08",
            "modificationDatetime": "2024-11-10T17:29:03"
        },
        {
            "@id": "data",
            "type": "Directory",
            "parent": {
                "@id": "."
            },
            "basename": "data",
            "hasPart": [
                {
                    "@id": "data/data_001.csv"
                },
                {
                    "@id": "data/data_002.csv"
                }
            ],
            "contentSize": 0,
            "creationDatetime": "2024-09-25T12:17:06",
            "modificationDatetime": "2024-09-25T12:17:53"
        },
        {
            "@id": "data/data_001.csv",
            "type": "File",
            "parent": {
                "@id": "data"
            },
            "basename": "data_001.csv",
            "name": "data_001",
            "extension": ".csv",
            "contentSize": 42,
            "creationDatetime": "2024-09-25T12:17:15",
            "modificationDatetime": "2024-09-25T12:18:08"
        },
        {
            "@id": "data/data_002.csv",
            "type": "File",
            "parent": {
                "@id": "data"
            },
            "basename": "data_002.csv",
            "name": "data_002",
            "extension": ".csv",
            "contentSize": 41,
            "creationDatetime": "2024-09-25T12:17:48",
            "modificationDatetime": "2024-09-25T12:18:05"
        },
        {
            "@id": "directory_structure_metadata.json",
            "type": "File",
            "parent": {
                "@id": "."
            },
            "basename": "directory_structure_metadata.json",
            "name": "directory_structure_metadata",
            "extension": ".json",
            "contentSize": 5286,
            "creationDatetime": "2024-11-10T17:29:03",
            "modificationDatetime": "2024-11-10T17:29:03"
        },
        {
            "@id": "directory_structure_metadata.tsv",
            "type": "File",
            "parent": {
                "@id": "."
            },
            "basename": "directory_structure_metadata.tsv",
            "name": "directory_structure_metadata",
            "extension": ".tsv",
            "contentSize": 1366,
            "creationDatetime": "2024-11-10T17:29:03",
            "modificationDatetime": "2024-11-10T17:29:03"
        },
        {
            "@id": "hogehoge",
            "type": "Directory",
            "parent": {
                "@id": "."
            },
            "basename": "hogehoge",
            "hasPart": [
                {
                    "@id": "hogehoge/data"
                },
                {
                    "@id": "hogehoge/fuga.txt"
                }
            ],
            "contentSize": 0,
            "creationDatetime": "2024-09-25T12:16:46",
            "modificationDatetime": "2024-11-10T16:39:53"
        },
        {
            "@id": "hogehoge/data",
            "type": "Directory",
            "parent": {
                "@id": "hogehoge"
            },
            "basename": "data",
            "hasPart": [
                {
                    "@id": "hogehoge/data/data_002.csv"
                },
                {
                    "@id": "hogehoge/data/data_003.csv"
                }
            ],
            "contentSize": 0,
            "creationDatetime": "2024-11-10T16:39:53",
            "modificationDatetime": "2024-11-10T16:40:12"
        },
        {
            "@id": "hogehoge/data/data_002.csv",
            "type": "File",
            "parent": {
                "@id": "hogehoge/data"
            },
            "basename": "data_002.csv",
            "name": "data_002",
            "extension": ".csv",
            "contentSize": 41,
            "creationDatetime": "2024-11-10T16:40:03",
            "modificationDatetime": "2024-09-25T12:18:05"
        },
        {
            "@id": "hogehoge/data/data_003.csv",
            "type": "File",
            "parent": {
                "@id": "hogehoge/data"
            },
            "basename": "data_003.csv",
            "name": "data_003",
            "extension": ".csv",
            "contentSize": 47,
            "creationDatetime": "2024-11-10T16:40:07",
            "modificationDatetime": "2024-11-10T16:40:30"
        },
        {
            "@id": "hogehoge/fuga.txt",
            "type": "File",
            "parent": {
                "@id": "hogehoge"
            },
            "basename": "fuga.txt",
            "name": "fuga",
            "extension": ".txt",
            "contentSize": 6,
            "creationDatetime": "2024-09-25T12:16:51",
            "modificationDatetime": "2024-09-25T12:16:55"
        },
        {
            "@id": "readme.md",
            "type": "File",
            "parent": {
                "@id": "."
            },
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

An example of the contents of `sample.tsv` is shown below:

```tsv
basename	contentSize	creationDatetime	extension	hasPart	modificationDatetime	@id	basename	contentSize	creationDatetime	extension	hasPart	modificationDatetime	name	parent	type
.	sample	4096	2024-09-25T12:16:08		[{'@id': 'data'}, {'@id': 'directory_structure_metadata.json'}, {'@id': 'directory_structure_metadata.tsv'}, {'@id': 'hogehoge'}, {'@id': 'readme.md'}]	2024-11-10T17:29:03		{}	Directory
data	data	0	2024-09-25T12:17:06		[{'@id': 'data/data_001.csv'}, {'@id': 'data/data_002.csv'}]	2024-09-25T12:17:53		{'@id': '.'}	Directory
data/data_001.csv	data_001.csv	42	2024-09-25T12:17:15	.csv		2024-09-25T12:18:08	data_001	{'@id': 'data'}	File
data/data_002.csv	data_002.csv	41	2024-09-25T12:17:48	.csv		2024-09-25T12:18:05	data_002	{'@id': 'data'}	File
directory_structure_metadata.json	directory_structure_metadata.json	5286	2024-11-10T17:29:03	.json		2024-11-10T17:29:03	directory_structure_metadata	{'@id': '.'}	File
directory_structure_metadata.tsv	directory_structure_metadata.tsv	1366	2024-11-10T17:29:03	.tsv		2024-11-10T17:29:03	directory_structure_metadata	{'@id': '.'}	File
hogehoge	hogehoge	0	2024-09-25T12:16:46		[{'@id': 'hogehoge/data'}, {'@id': 'hogehoge/fuga.txt'}]	2024-11-10T16:39:53		{'@id': '.'}	Directory
hogehoge/data	data	0	2024-11-10T16:39:53		[{'@id': 'hogehoge/data/data_002.csv'}, {'@id': 'hogehoge/data/data_003.csv'}]	2024-11-10T16:40:12		{'@id': 'hogehoge'}	Directory
hogehoge/data/data_002.csv	data_002.csv	41	2024-11-10T16:40:03	.csv		2024-09-25T12:18:05	data_002	{'@id': 'hogehoge/data'}	File
hogehoge/data/data_003.csv	data_003.csv	47	2024-11-10T16:40:07	.csv		2024-11-10T16:40:30	data_003	{'@id': 'hogehoge/data'}	File
hogehoge/fuga.txt	fuga.txt	6	2024-09-25T12:16:51	.txt		2024-09-25T12:16:55	fuga	{'@id': 'hogehoge'}	File
readme.md	readme.md	142	2024-09-25T12:16:19	.md		2024-09-25T12:27:38	readme	{'@id': '.'}	File

```

## output the metadata in a tree

```sh
# at the root directory of this repository
python -m directory_structure_py ./sample --dst sample.json --to_tsv --in_tree
```

An example of the contents of the `sample.json` is shown below:

```json
{
    "contents": {
        "@id": ".",
        "type": "Directory",
        "parent": {},
        "basename": "sample",
        "hasPart": [
            {
                "@id": "data",
                "type": "Directory",
                "parent": {
                    "@id": "."
                },
                "basename": "data",
                "hasPart": [
                    {
                        "@id": "data/data_001.csv",
                        "type": "File",
                        "parent": {
                            "@id": "data"
                        },
                        "basename": "data_001.csv",
                        "name": "data_001",
                        "extension": ".csv",
                        "contentSize": 42,
                        "creationDatetime": "2024-09-25T12:17:15",
                        "modificationDatetime": "2024-09-25T12:18:08"
                    },
                    {
                        "@id": "data/data_002.csv",
                        "type": "File",
                        "parent": {
                            "@id": "data"
                        },
                        "basename": "data_002.csv",
                        "name": "data_002",
                        "extension": ".csv",
                        "contentSize": 41,
                        "creationDatetime": "2024-09-25T12:17:48",
                        "modificationDatetime": "2024-09-25T12:18:05"
                    }
                ],
                "contentSize": 0,
                "creationDatetime": "2024-09-25T12:17:06",
                "modificationDatetime": "2024-09-25T12:17:53"
            },
            {
                "@id": "directory_structure_metadata.json",
                "type": "File",
                "parent": {
                    "@id": "."
                },
                "basename": "directory_structure_metadata.json",
                "name": "directory_structure_metadata",
                "extension": ".json",
                "contentSize": 5990,
                "creationDatetime": "2024-11-10T17:29:03",
                "modificationDatetime": "2024-11-10T17:34:06"
            },
            {
                "@id": "directory_structure_metadata.tsv",
                "type": "File",
                "parent": {
                    "@id": "."
                },
                "basename": "directory_structure_metadata.tsv",
                "name": "directory_structure_metadata",
                "extension": ".tsv",
                "contentSize": 1790,
                "creationDatetime": "2024-11-10T17:29:03",
                "modificationDatetime": "2024-11-10T17:34:06"
            },
            {
                "@id": "hogehoge",
                "type": "Directory",
                "parent": {
                    "@id": "."
                },
                "basename": "hogehoge",
                "hasPart": [
                    {
                        "@id": "hogehoge/data",
                        "type": "Directory",
                        "parent": {
                            "@id": "hogehoge"
                        },
                        "basename": "data",
                        "hasPart": [
                            {
                                "@id": "hogehoge/data/data_002.csv",
                                "type": "File",
                                "parent": {
                                    "@id": "hogehoge/data"
                                },
                                "basename": "data_002.csv",
                                "name": "data_002",
                                "extension": ".csv",
                                "contentSize": 41,
                                "creationDatetime": "2024-11-10T16:40:03",
                                "modificationDatetime": "2024-09-25T12:18:05"
                            },
                            {
                                "@id": "hogehoge/data/data_003.csv",
                                "type": "File",
                                "parent": {
                                    "@id": "hogehoge/data"
                                },
                                "basename": "data_003.csv",
                                "name": "data_003",
                                "extension": ".csv",
                                "contentSize": 47,
                                "creationDatetime": "2024-11-10T16:40:07",
                                "modificationDatetime": "2024-11-10T16:40:30"
                            }
                        ],
                        "contentSize": 0,
                        "creationDatetime": "2024-11-10T16:39:53",
                        "modificationDatetime": "2024-11-10T16:40:12"
                    },
                    {
                        "@id": "hogehoge/fuga.txt",
                        "type": "File",
                        "parent": {
                            "@id": "hogehoge"
                        },
                        "basename": "fuga.txt",
                        "name": "fuga",
                        "extension": ".txt",
                        "contentSize": 6,
                        "creationDatetime": "2024-09-25T12:16:51",
                        "modificationDatetime": "2024-09-25T12:16:55"
                    }
                ],
                "contentSize": 0,
                "creationDatetime": "2024-09-25T12:16:46",
                "modificationDatetime": "2024-11-10T16:39:53"
            },
            {
                "@id": "readme.md",
                "type": "File",
                "parent": {
                    "@id": "."
                },
                "basename": "readme.md",
                "name": "readme",
                "extension": ".md",
                "contentSize": 142,
                "creationDatetime": "2024-09-25T12:16:19",
                "modificationDatetime": "2024-09-25T12:27:38"
            }
        ],
        "contentSize": 4096,
        "creationDatetime": "2024-09-25T12:16:08",
        "modificationDatetime": "2024-11-10T17:29:03"
    }
}
```

An example of the contents of `sample.tsv` is the same as that in outputting the metadata in a list.

# Contributions

Any feedback is welcome via the Issue section!
