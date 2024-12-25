# directory-structure-py Core

The core functions of `directory-structure-py`.

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

| Function                               | Overview                                                                      |
| :------------------------------------- | :---------------------------------------------------------------------------- |
| `generate_id`                          | Generates a unique ID from a given path, optionally relative to a root path.  |
| `get_metadata_of_single_file`          | Retrieves metadata for a given file.                                          |
| `get_metadata_of_single_directory`     | Retrieves metadata for a given directory.                                     |
| `get_metadata_of_files_in_list_format` | Recursively retrieves metadata for files and directories within a given path. |

`get_metadata_of_files_in_list_format` returns a dict object with the following format:

```json
{
    "root_path": "root path. The value will be '.' if the 'include_root_path' option is not set",
    "@graph": ["metadata returned by get_metadata_of_single_file"]
}
```

# Installation

TBD

# Usage

TBD

# Contributions

Any feedback is welcome via [the Issue section](https://github.com/Surpris/directory-structure-py/issues)!
