# Version of the portable program

v0.2.2

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
    "name": "directory name (same as the basename)",
    "hasPart": ["`@id` or metadata of file or directory"],
    "contentSize": "the total size of files included (Byte)",
    "extension": ["unique file extension (ex. test.dat -> .dat)"],
    "numberOfContents": "the number of contents",
    "numberOfFileContents": "the number of files",
    "numberOfFileContentsPerExtension": {"key = extension": "value = the number of files with the extension"},
    "creationDatetime": "creation datetime (%Y-%m-%dT%H:%M:%S)",
    "modificationDatetime": "modification datetime (%Y-%m-%dT%H:%M:%S)"
}
```

Please see "# Example" section for the output formats.

# Usage

Drag the directory or file and drop it on the batch file "directory_structure_py.bat".
By default, the following files are output to the `output` directory in the directory where "directory_structure_py.bat" is located.

* `ro-crate-metadata.json`: a metadata is included in the RO-Crate format.
* `ro-crate-preview.html`: a preview file of the RO-Crate metadata.
* `directory_structure_metadata_tree.json`: the directory tree is included.
* `directory_structure_metadata.tsv`: a metadata list is included.

You can change the output formats by modifying the options set in the batch file. However, in v0.2.2, the option `preview_template_path` must be set when outputting the RO-Crate-format metadata due to a bug that the executable file cannot open the inherent template file because of Permission Error.

# Directory structure of the portable program

```
<root>
│   directory_structure_py.bat: batch file
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
