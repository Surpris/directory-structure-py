"""test_main.py

test code
"""

import pytest
from directory_structure_py.src.main import list2tree


def test_list2tree():
    expected = {
        "contents": {
            ".": [
                {
                    "data": [
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
                    ]
                },
                {
                    "hogehoge": [
                        {
                            "hogehoge/data": [
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
                            ]
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
                    ]
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
                    "contentSize": 187,
                    "creationDatetime": "2024-09-25T12:16:19",
                    "modificationDatetime": "2024-11-10T17:42:20"
                }
            ]
        }
    }
    src = {
        "root_path": ".",
        "contents": [
            {
                "@id": ".",
                "type": "Directory",
                "parent": {},
                "basename": "sample",
                "hasPart": [
                    {
                        "@id": "data"
                    },
                    {
                        "@id": "hogehoge"
                    },
                    {
                        "@id": "readme.md"
                    }
                ],
                "contentSize": 4096,
                "creationDatetime": "2024-09-25T12:16:08",
                "modificationDatetime": "2024-11-23T12:15:26"
            },
            {
                "@id": "data",
                "type": "Directory",
                "parent": {
                    "@id": "."
                },
                "basename": "data",
                "hasPart": [
                    {
                        "@id": "data/data_001.csv"
                    },
                    {
                        "@id": "data/data_002.csv"
                    }
                ],
                "contentSize": 0,
                "creationDatetime": "2024-09-25T12:17:06",
                "modificationDatetime": "2024-09-25T12:17:53"
            },
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
                        "@id": "hogehoge/data"
                    },
                    {
                        "@id": "hogehoge/fuga.txt"
                    }
                ],
                "contentSize": 0,
                "creationDatetime": "2024-09-25T12:16:46",
                "modificationDatetime": "2024-11-10T16:39:53"
            },
            {
                "@id": "hogehoge/data",
                "type": "Directory",
                "parent": {
                    "@id": "hogehoge"
                },
                "basename": "data",
                "hasPart": [
                    {
                        "@id": "hogehoge/data/data_002.csv"
                    },
                    {
                        "@id": "hogehoge/data/data_003.csv"
                    }
                ],
                "contentSize": 0,
                "creationDatetime": "2024-11-10T16:39:53",
                "modificationDatetime": "2024-11-10T16:40:12"
            },
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
                "contentSize": 187,
                "creationDatetime": "2024-09-25T12:16:19",
                "modificationDatetime": "2024-11-10T17:42:20"
            }
        ]
    }
    dst = list2tree(src)
    assert dst == expected
