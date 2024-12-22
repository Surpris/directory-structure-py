# ポータブルプログラムのバージョン情報

v0.2.6

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

出力形式については "# Example" セクションをご確認ください。

# 使い方

バッチファイル "directory_structure_py.bat" に、メタデータを収集したいディレクトリまたはファイルのパスを drag & drop します。
デフォルトでは以下の名前のファイルが、"directory_structure_py.bat" が配置されているディレクトリ以下にある `output` ディレクトリに出力されます。

* `directory_structure_metadata.json`：リスト形式で収集されたメタデータが含まれます。
* `directory_structure_metadata_tree.json`：ディレクトリツリーが含まれます。
* `directory_structure_metadata.tsv`：メタデータリストが含まれます。
* `ro-crate-metadata.json`：メタデータが RO-Crate 形式で含まれます。
* `ro-crate-preview.html`: RO-Crate 形式のメタデータのプレビューファイルです。

バッチファイル内で設定されているオプションを変えることで出力形式を変更できます。

## バッチファイルのオプション

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

# ポータブルプログラムのディレクトリ構造

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

# ライセンス

本ソフトウェアのライセンスは Apache License version 2.0 です。Apache License 2.0 の詳細については "LICENSE" ファイルをご確認ください。

# 免責事項

本ソフトウェア開発者は、本プログラムの利用者によって引き起こされたインシデントに関して一切の責任を負いません。
