# directory-structure-py

Python function collecting the metadata of a directory and its contents.

[![Release Notes](https://img.shields.io/github/release/Surpris/directory-structure-py?style=flat-square)](https://github.com/Surpris/directory-structure-py/releases)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/directory-structure-py)](https://pypistats.org/packages/directory-structure-py)
[![CI](https://github.com/Surpris/directory-structure-py/actions/workflows/python-package.yml/badge.svg)](https://github.com/Surpris/directory-structure-py/actions/workflows/python-package.yml)
[![License](https://img.shields.io/github/license/Surpris/directory-structure-py?style=flat-square)](https://opensource.org/licenses/Apache-2.0)
[![GitHub star chart](https://img.shields.io/github/stars/Surpris/directory-structure-py?style=flat-square)](https://star-history.com/#Surpris/directory-structure-py)
[![Open Issues](https://img.shields.io/github/issues-raw/Surpris/directory-structure-py?style=flat-square)](https://github.com/Surpris/directory-structure-py/issues)

# Requirements

* Python &geq; 3.12

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
    "mimetype": "MIME type",
    "contentSize": "file size (Byte)",
    "sha256": "SHA-256 hash value",
    "dateCreated": "creation datetime (%Y-%m-%dT%H:%M:%S)",
    "dateModified": "modification datetime (%Y-%m-%dT%H:%M:%S)"
}

// for Directory
{
    "@id": "id unique in the metadata tree",
    "type": "Directory",
    "parent": "parent directory info including '@id'",
    "basename": "basename (ex. test.dat)",
    "name": "directory name (same as the basename)",
    "hasPart": ["`@id` or metadata of file or directory"],
    "contentSize": "the total size of files included (Byte)",
    "extension": ["unique file extension (ex. test.dat -> .dat)"],
    "mimetype": ["unique MIME type"],
    "numberOfContents": "the number of child contents",
    "numberOfFiles": "the number of child files",
    "numberOfFilesPerExtension": {"key = extension": "value = the number of files with the extension"},
    "contentSizeOfAllFiles": "The total size of files within the directory and all its descendant directories in bytes",
    "numberOfAllContents": "The total number of child items (files and subdirectories) within the directory and all its descendant directories",
    "numberOfAllFiles": "The total number of files within the directory and all its descendant directories",
    "numberOfAllFilesPerExtension": {"key = extension": "value = the number of the descendant files with the extension"},
    "extensionsOfAllFiles": ["unique file extension (ex. test.dat -> .dat) extracted from the descendant files"],
    "dateCreated": "creation datetime (%Y-%m-%dT%H:%M:%S)",
    "dateModified": "modification datetime (%Y-%m-%dT%H:%M:%S)",
}
```

# Functions

## In `get_metadata`

| Function                               | Overview                                                                      |
| :------------------------------------- | :---------------------------------------------------------------------------- |
| `generate_id`                          | Generates a unique ID from a given path, optionally relative to a root path.  |
| `get_metadata_of_single_file`          | Retrieves metadata for a given file or directory using the `pathlib` module.  |
| `get_metadata_of_files_in_list_format` | Recursively retrieves metadata for files and directories within a given path. |

`get_metadata_of_files_in_list_format` returns a dict object with the following format:

```json
{
    "root_path": "root path. The value will be '.' if the 'include_root_path' option is not set",
    "@graph": ["metadata returned by get_metadata_of_single_file"]
}
```

## In `conversion`

| Function                                  | Overview                                                                                    |
| :---------------------------------------- | :------------------------------------------------------------------------------------------ |
| `convert_meta_list_json_to_tsv`           | Converts a list of dictionaries (JSON-like structure) into a TSV-compatible list of lists.  |
| `convert_meta_list_json_to_tsv_from_file` | Converts a JSON file containing a list of dictionaries into a TSV-compatible list of lists. |
| `list2tree`                               | Constructs a hierarchical tree structure from a metadata dictionary.                        |
| `list2tree_from_file`                     | Constructs a hierarchical tree structure from a JSON metadata file.                         |
| `convert_meta_list_json_to_rocrate`       | Converts a metadata list JSON structure into a Research Object Crate (ROCrate).             |

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
    --in_rocrate \ // option
    --to_tsv \ // option
    --in_tree \ // option
    --structure_only \ // option
    --log_config_path <log_config_path> \ // option
    --log_output_path <log_output_path> // option
    --preview_template_path <preview_template_path> \\ option
```

Main options:

| Item                    | Type   | Description                                                                                                                      |
| :---------------------- | :----- | :------------------------------------------------------------------------------------------------------------------------------- |
| `dst`                   | str    | destination path of the json output. If empty, the metadata file will be output to the same directory as that of the input file. |
| `include_root_path`     | (bool) | include `file_or_directory_path` with the key `root_path` if this option is set                                                  |
| `in_rocrate`            | (bool) | output an RO-Crate-format file instead of the list format one if this option is set                                              |
| `to_tsv`                | (bool) | output a TSV-format file if this option is set                                                                                   |
| `in_tree`               | (bool) | output the metadata in a tree format if this option is set                                                                       |
| `structure_only`        | (bool) | output only the structure in a tree format if this option is set                                                                 |
| `preview_template_path` | str    | file path of the template for the preview file output by the RO-Crate.                                                           |

Logging options:

| Item              | Type | Description                                                                        |
| :---------------- | :--- | :--------------------------------------------------------------------------------- |
| `log_config_path` | str  | a log config path. See `config/logging.json` for the detail of the content format. |
| `log_output_path` | str  | destination path of the log.                                                       |


## Batch file (Windows and Ubuntu)

Drag the directory or file and drop it on the batch file `directory_structure_py.bat` or on the shell script `directory_structure_py.sh`.
By default, the following files are output to the `output` directory in the directory where the batch file or the shell script is located.

* `directory_structure_metadata.json`: the list-formatted metadata is included.
* `directory_structure_metadata_tree.json`: the directory tree is included.
* `directory_structure_metadata.tsv`: a metadata list is included.
* `ro-crate-metadata.json`: a metadata is included in the RO-Crate format.
* `ro-crate-preview.html`: a preview file of the RO-Crate metadata.

You can change the output formats by modifying the options set in teh batch file.

## python

### get_metadata_of_single_file

```python
from directory_structure_py.src.get_metadata import get_metadata_of_single_file

fpath: str = "file_or_directory_path"
metadata: dict = get_metadata_of_single_file(fpath)
```

### get_metadata_of_files_in_list_format

```python
from directory_structure_py.src.get_metadata import get_metadata_of_files_in_list_format

fpath: str = "file_or_directory_path"
metadata: dict = get_metadata_of_files_in_list_format(fpath)
```

# Output examples

Please see [output/sample](https://github.com/Surpris/directory-structure-py/tree/5dc71273236313cc1935f0204963da6f4c789df5/output/sample) (jump to the GitHub repository).

# Contributions

Any feedback is welcome via the Issue section!
