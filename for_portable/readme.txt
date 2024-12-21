# Version of the portable program

v0.2.5

# What is for?

This program output the metadata of the files and directories stored in the input path.
The following metadata items are collected:

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

Please see "# Example" section for the output formats.

# Usage

Drag the directory or file and drop it on the batch file `directory_structure_py.bat` or on the shell script `directory_structure_py.sh`.
By default, the following files are output to the `output` directory in the directory where the batch file or the shell script is located.

* `directory_structure_metadata.json`: the list-formatted metadata is included.
* `directory_structure_metadata_tree.json`: the directory tree is included.
* `directory_structure_metadata.tsv`: a metadata list is included.
* `ro-crate-metadata.json`: a metadata is included in the RO-Crate format.
* `ro-crate-preview.html`: a preview file of the RO-Crate metadata.

You can change the output formats by modifying the options set in the batch file.

## options

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

# Directory structure of the portable program

```
<root>
│   directory_structure_py.bat or .sh: batch file or shell script
│   readme.txt: this file
│   readme_ja.txt: Japanese readme
│
├───sample: the sample file(s)
│   │   readme.md: readme of the sample file(s)
│   │
│   ├───data
│   │       data_001.csv
│   │       data_002.csv
│   │
│   └───hogehoge
│       │   fuga.txt
│       │
│       └───data
│               data_002.csv
│               data_003.csv
│
└───src: the source directory
    │   directory_structure_py.exe: the executable file
    │
    ├───config: config directory
    │       logging.json: the config file for logging
    │
    └───templates: templates directory
            preview_template.html.j2: the template file for the RO-Crate HTML preview
```

# License

Apache License version 2.0. Please see the file "LICENSE" in more detail on Apache License 2.0.

# Disclaimer

The developer(s) of this software is not responsible for any incident caused by the users of this software.
