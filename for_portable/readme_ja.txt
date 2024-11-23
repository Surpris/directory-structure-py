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
    "hasPart": ["`@id` or metadata of file or directory"],
    "contentSize": "file size (Byte)",
    "creationDatetime": "creation datetime (%Y-%m-%dT%H:%M:%S)",
    "modificationDatetime": "modification datetime (%Y-%m-%dT%H:%M:%S)"
}
```

出力形式については "# Example" セクションをご確認ください。

# 使い方

バッチファイル "directory_structure_py.bat" に、メタデータを収集したいディレクトリまたはファイルのパスを drag & drop します。
デフォルトでは以下の名前のファイルが、"directory_structure_py.bat" が配置されているディレクトリ以下にある `output` ディレクトリに出力されます。

* `ro-crate-metadata.json`：メタデータが RO-Crate 形式で含まれます。
* `directory_structure_metadata_tree.json`：ディレクトリツリーが含まれます。
* `directory_structure_metadata.tsv`：メタデータリストが含まれます。

バッチファイル内で設定されているオプションを変えることで出力形式を変更できます。

# Example

本ソフトウェアに付属する "sample" ディレクトリのメタデータ出力結果の一例を以下に示します。

## `ro-crate-metadata.json`

```json
{
    "@context": "https://w3id.org/ro/crate/1.1/context",
    "@graph": [
        {
            "@id": "./",
            "@type": "Dataset",
            "datePublished": "2024-11-23T20:08:04",
            "hasPart": [
                {
                    "@id": "sample/"
                },
                {
                    "@id": "sample/data/"
                },
                {
                    "@id": "sample/data/data_001.csv"
                },
                {
                    "@id": "sample/data/data_002.csv"
                },
                {
                    "@id": "sample/hogehoge/"
                },
                {
                    "@id": "sample/hogehoge/data/"
                },
                {
                    "@id": "sample/hogehoge/data/data_002.csv"
                },
                {
                    "@id": "sample/hogehoge/data/data_003.csv"
                },
                {
                    "@id": "sample/hogehoge/fuga.txt"
                },
                {
                    "@id": "sample/readme.md"
                }
            ]
        },
        {
            "@id": "ro-crate-metadata.json",
            "@type": "CreativeWork",
            "about": {
                "@id": "./"
            },
            "conformsTo": {
                "@id": "https://w3id.org/ro/crate/1.1"
            }
        },
        {
            "@id": "sample/",
            "@type": "Dataset",
            "dateCreated": "2024-11-23T20:07:43",
            "dateModified": "2024-11-23T20:07:43",
            "hasPart": [
                "sample/data/",
                "sample/hogehoge/",
                "sample/readme.md"
            ],
            "name": "sample"
        },
        {
            "@id": "sample/data/",
            "@type": "Dataset",
            "dateCreated": "2024-11-23T20:07:43",
            "dateModified": "2024-11-23T20:07:43",
            "hasPart": [
                "sample/data/data_001.csv",
                "sample/data/data_002.csv"
            ],
            "name": "data"
        },
        {
            "@id": "sample/data/data_001.csv",
            "@type": "File",
            "contentSize": 42,
            "dateCreated": "2024-11-23T11:06:06",
            "dateModified": "2024-11-23T20:07:43",
            "extension": ".csv",
            "name": "data_001"
        },
        {
            "@id": "sample/data/data_002.csv",
            "@type": "File",
            "contentSize": 41,
            "dateCreated": "2024-11-23T11:06:06",
            "dateModified": "2024-11-23T20:07:43",
            "extension": ".csv",
            "name": "data_002"
        },
        {
            "@id": "sample/hogehoge/",
            "@type": "Dataset",
            "dateCreated": "2024-11-23T20:07:43",
            "dateModified": "2024-11-23T20:07:43",
            "hasPart": [
                "sample/hogehoge/data/",
                "sample/hogehoge/fuga.txt"
            ],
            "name": "hogehoge"
        },
        {
            "@id": "sample/hogehoge/data/",
            "@type": "Dataset",
            "dateCreated": "2024-11-23T20:07:43",
            "dateModified": "2024-11-23T20:07:43",
            "hasPart": [
                "sample/hogehoge/data/data_002.csv",
                "sample/hogehoge/data/data_003.csv"
            ],
            "name": "data"
        },
        {
            "@id": "sample/hogehoge/data/data_002.csv",
            "@type": "File",
            "contentSize": 41,
            "dateCreated": "2024-11-23T11:06:06",
            "dateModified": "2024-11-23T20:07:43",
            "extension": ".csv",
            "name": "data_002"
        },
        {
            "@id": "sample/hogehoge/data/data_003.csv",
            "@type": "File",
            "contentSize": 47,
            "dateCreated": "2024-11-23T11:06:06",
            "dateModified": "2024-11-23T20:07:43",
            "extension": ".csv",
            "name": "data_003"
        },
        {
            "@id": "sample/hogehoge/fuga.txt",
            "@type": "File",
            "contentSize": 6,
            "dateCreated": "2024-11-23T11:06:06",
            "dateModified": "2024-11-23T20:07:43",
            "extension": ".txt",
            "name": "fuga"
        },
        {
            "@id": "sample/readme.md",
            "@type": "File",
            "contentSize": 187,
            "dateCreated": "2024-11-23T11:06:06",
            "dateModified": "2024-11-23T20:07:43",
            "extension": ".md",
            "name": "readme"
        }
    ]
}
```

## `directory_structure_metadata_tree.json`

```json
{
    "@graph": {
        "sample/": [
            {
                "sample/data/": [
                    "sample/data/data_001.csv",
                    "sample/data/data_002.csv"
                ]
            },
            {
                "sample/hogehoge/": [
                    {
                        "sample/hogehoge/data/": [
                            "sample/hogehoge/data/data_002.csv",
                            "sample/hogehoge/data/data_003.csv"
                        ]
                    },
                    "sample/hogehoge/fuga.txt"
                ]
            },
            "sample/readme.md"
        ]
    },
    "dateCreated": "2024-11-23T20:08:04"
}
```

## `directory_structure_metadata.tsv`

```tsv
@id	basename	contentSize	dateCreated	dateModified	extension	hasPart	name	parent	type
sample/	sample		2024-11-23T20:07:43	2024-11-23T20:07:43		[{'@id': 'sample/data/'}, {'@id': 'sample/hogehoge/'}, {'@id': 'sample/readme.md'}]		{}	Directory
sample/data/	data		2024-11-23T20:07:43	2024-11-23T20:07:43		[{'@id': 'sample/data/data_001.csv'}, {'@id': 'sample/data/data_002.csv'}]		{'@id': 'sample/'}	Directory
sample/data/data_001.csv	data_001.csv	42	2024-11-23T11:06:06	2024-11-23T20:07:43	.csv		data_001	{'@id': 'sample/data/'}	File
sample/data/data_002.csv	data_002.csv	41	2024-11-23T11:06:06	2024-11-23T20:07:43	.csv		data_002	{'@id': 'sample/data/'}	File
sample/hogehoge/	hogehoge		2024-11-23T20:07:43	2024-11-23T20:07:43		[{'@id': 'sample/hogehoge/data/'}, {'@id': 'sample/hogehoge/fuga.txt'}]		{'@id': 'sample/'}	Directory
sample/hogehoge/data/	data		2024-11-23T20:07:43	2024-11-23T20:07:43		[{'@id': 'sample/hogehoge/data/data_002.csv'}, {'@id': 'sample/hogehoge/data/data_003.csv'}]		{'@id': 'sample/hogehoge/'}	Directory
sample/hogehoge/data/data_002.csv	data_002.csv	41	2024-11-23T11:06:06	2024-11-23T20:07:43	.csv		data_002	{'@id': 'sample/hogehoge/data/'}	File
sample/hogehoge/data/data_003.csv	data_003.csv	47	2024-11-23T11:06:06	2024-11-23T20:07:43	.csv		data_003	{'@id': 'sample/hogehoge/data/'}	File
sample/hogehoge/fuga.txt	fuga.txt	6	2024-11-23T11:06:06	2024-11-23T20:07:43	.txt		fuga	{'@id': 'sample/hogehoge/'}	File
sample/readme.md	readme.md	187	2024-11-23T11:06:06	2024-11-23T20:07:43	.md		readme	{'@id': 'sample/'}	File

```

# ライセンス

本ソフトウェアのライセンスは Apache License version 2.0 です。Apache License 2.0 の詳細については "LICENSE" ファイルをご確認ください。

# 免責事項

本ソフトウェア開発者は、本プログラムの利用者によって引き起こされたインシデントに関して一切の責任を負いません。
