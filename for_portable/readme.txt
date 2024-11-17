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
    "hasPart": ["basename of file or directory"],
    "contentSize": "file size (Byte)",
    "creationDatetime": "creation datetime (%Y-%m-%dT%H:%M:%S)",
    "modificationDatetime": "modification datetime (%Y-%m-%dT%H:%M:%S)"
}
```

Please see "# Example" section for the output formats.

# Usage

Drag the directory or file and drop it on the batch file "directory_structure_py.bat".
By default, the following files are output to the `output` directory in the directory where "directory_structure_py.bat" is located.

* `directory_structure_metadata.json`: This file includes a metadata tree with the same structure as the input directory tree.
* `directory_structure_metadata.tsv`: This file includes a metadata list.

# Example

The metadata of the "sample" directory is output in the following JSON format:

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

The metadata is also output in a TSV format:

```tsv
@id	basename	contentSize	creationDatetime	extension	hasPart	modificationDatetime	name	parent	type
.	sample	0	2024-11-10T17:42:42		[{'@id': 'data'}, {'@id': 'hogehoge'}, {'@id': 'readme.md'}]	2024-11-10T17:42:42		{}	Directory
data	data	0	2024-11-10T17:42:42		[{'@id': 'data/data_001.csv'}, {'@id': 'data/data_002.csv'}]	2024-11-10T17:42:42		{'@id': '.'}	Directory
data/data_001.csv	data_001.csv	42	2024-11-10T17:42:42	.csv		2024-09-25T12:18:08	data_001	{'@id': 'data'}	File
data/data_002.csv	data_002.csv	41	2024-11-10T17:42:42	.csv		2024-09-25T12:18:05	data_002	{'@id': 'data'}	File
hogehoge	hogehoge	0	2024-11-10T17:42:42		[{'@id': 'hogehoge/data'}, {'@id': 'hogehoge/fuga.txt'}]	2024-11-10T17:42:42		{'@id': '.'}	Directory
hogehoge/data	data	0	2024-11-10T17:42:42		[{'@id': 'hogehoge/data/data_002.csv'}, {'@id': 'hogehoge/data/data_003.csv'}]	2024-11-10T17:42:42		{'@id': 'hogehoge'}	Directory
hogehoge/data/data_002.csv	data_002.csv	41	2024-11-10T17:42:42	.csv		2024-09-25T12:18:05	data_002	{'@id': 'hogehoge/data'}	File
hogehoge/data/data_003.csv	data_003.csv	47	2024-11-10T17:42:42	.csv		2024-11-10T16:40:30	data_003	{'@id': 'hogehoge/data'}	File
hogehoge/fuga.txt	fuga.txt	6	2024-11-10T17:42:42	.txt		2024-09-25T12:16:55	fuga	{'@id': 'hogehoge'}	File
readme.md	readme.md	187	2024-11-10T17:42:42	.md		2024-11-10T17:42:20	readme	{'@id': '.'}	File

```

# License

Apache License 2.0. Please see the file "LICENSE" in more detail on Apache License 2.0.

# Disclaimer

The developer(s) of this software is not responsible for any incident caused by the users of this software.
