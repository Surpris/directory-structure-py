# ポータブルプログラムのバージョン情報

v0.2.2

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

出力形式については "# Example" セクションをご確認ください。

# 使い方

バッチファイル "directory_structure_py.bat" に、メタデータを収集したいディレクトリまたはファイルのパスを drag & drop します。
デフォルトでは以下の名前のファイルが、"directory_structure_py.bat" が配置されているディレクトリ以下にある `output` ディレクトリに出力されます。

* `ro-crate-metadata.json`：メタデータが RO-Crate 形式で含まれます。
* `ro-crate-preview.html`: RO-Crate 形式のメタデータのプレビューファイルです。
* `directory_structure_metadata_tree.json`：ディレクトリツリーが含まれます。
* `directory_structure_metadata.tsv`：メタデータリストが含まれます。

バッチファイル内で設定されているオプションを変えることで出力形式を変更できます。
ただし、v0.2.2 では、RO-Crate 形式でメタデータを出力する場合、`preview_template_path` を必ず設定する必要があります。これは executable file が内在するテンプレートファイルを読み込めないというバグが存在するためです。

# ポータブルプログラムのディレクトリ構造

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

# ライセンス

本ソフトウェアのライセンスは Apache License version 2.0 です。Apache License 2.0 の詳細については "LICENSE" ファイルをご確認ください。

# 免責事項

本ソフトウェア開発者は、本プログラムの利用者によって引き起こされたインシデントに関して一切の責任を負いません。
