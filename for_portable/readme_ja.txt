# 何をしてくれるか

入力されたパスについて、ディレクトリツリーと以下のメタデータを取り出して JSON 形式で出力します。
収集されるメタデータは次の通りです。

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

出力形式については "# Example" セクションをご確認ください。

# 使い方

バッチファイル "directory_structure_py.bat" に、メタデータを収集したいディレクトリまたはファイルのパスを drag & drop します。
デフォルトでは以下の名前のファイルが、"directory_structure_py.bat" と同じディレクトリに出力されます。

* `directory_structure_metadata.json`：ディレクトリツリーと同じ構造を持つメタデータツリーが含まれます。
* `directory_structure_metadata.tsv`: メタデータリストが含まれます。


# Example

本ソフトウェアに付属する "sample" ディレクトリのメタデータ出力結果の一例を以下に示します。

## `directory_structure_metadata.json`

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

## `directory_structure_metadata.tsv`

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

# ライセンス

本ソフトウェアのライセンスは Apache License 2.0 です。Apache License 2.0 の詳細については "LICENSE" ファイルをご確認ください。

# 免責事項

本ソフトウェア開発者は、本プログラムの利用者によって引き起こされたインシデントに関して一切の責任を負いません。
