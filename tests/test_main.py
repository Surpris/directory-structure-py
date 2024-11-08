"""test_main.py

test code
"""

import pytest
from directory_structure_py.src.main import list2tree


def test_list2tree():
    expected = {
        "contents": {
            "type": "Directory",
            "parent": "",
            "basename": "sample",
            "hasPart": [
                {
                    "type": "Directory",
                    "parent": "sample",
                    "basename": "data",
                    "hasPart": [
                        {
                            "type": "File",
                            "parent": "data",
                            "basename": "data_001.csv",
                            "name": "data_001",
                            "extension": ".csv",
                            "contentSize": 42,
                            "creationDatetime": "2024-09-25T12:17:15",
                            "modificationDatetime": "2024-09-25T12:18:08"
                        },
                        {
                            "type": "File",
                            "parent": "data",
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
                    "type": "Directory",
                    "parent": "sample",
                    "basename": "hogehoge",
                    "hasPart": [
                        {
                            "type": "File",
                            "parent": "hogehoge",
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
                    "modificationDatetime": "2024-09-25T12:16:51"
                },
                {
                    "type": "File",
                    "parent": "sample",
                    "basename": "readme.md",
                    "name": "readme",
                    "extension": ".md",
                    "contentSize": 142,
                    "creationDatetime": "2024-09-25T12:16:19",
                    "modificationDatetime": "2024-09-25T12:27:38"
                }
            ],
            "contentSize": 0,
            "creationDatetime": "2024-09-25T12:16:08",
            "modificationDatetime": "2024-09-25T12:17:06"
        }
    }
    src = {
        "contents": [
            {
                "type": "Directory",
                "parent": "",
                "basename": "sample",
                "hasPart": [
                    "data",
                    "hogehoge",
                    "readme.md"
                ],
                "contentSize": 0,
                "creationDatetime": "2024-09-25T12:16:08",
                "modificationDatetime": "2024-09-25T12:17:06"
            },
            {
                "type": "Directory",
                "parent": "sample",
                "basename": "data",
                "hasPart": [
                    "data_001.csv",
                    "data_002.csv"
                ],
                "contentSize": 0,
                "creationDatetime": "2024-09-25T12:17:06",
                "modificationDatetime": "2024-09-25T12:17:53"
            },
            {
                "type": "File",
                "parent": "data",
                "basename": "data_001.csv",
                "name": "data_001",
                "extension": ".csv",
                "contentSize": 42,
                "creationDatetime": "2024-09-25T12:17:15",
                "modificationDatetime": "2024-09-25T12:18:08"
            },
            {
                "type": "File",
                "parent": "data",
                "basename": "data_002.csv",
                "name": "data_002",
                "extension": ".csv",
                "contentSize": 41,
                "creationDatetime": "2024-09-25T12:17:48",
                "modificationDatetime": "2024-09-25T12:18:05"
            },
            {
                "type": "Directory",
                "parent": "sample",
                "basename": "hogehoge",
                "hasPart": [
                    "fuga.txt"
                ],
                "contentSize": 0,
                "creationDatetime": "2024-09-25T12:16:46",
                "modificationDatetime": "2024-09-25T12:16:51"
            },
            {
                "type": "File",
                "parent": "hogehoge",
                "basename": "fuga.txt",
                "name": "fuga",
                "extension": ".txt",
                "contentSize": 6,
                "creationDatetime": "2024-09-25T12:16:51",
                "modificationDatetime": "2024-09-25T12:16:55"
            },
            {
                "type": "File",
                "parent": "sample",
                "basename": "readme.md",
                "name": "readme",
                "extension": ".md",
                "contentSize": 142,
                "creationDatetime": "2024-09-25T12:16:19",
                "modificationDatetime": "2024-09-25T12:27:38"
            }
        ]
    }
    dst = list2tree(src)
    assert dst == expected
