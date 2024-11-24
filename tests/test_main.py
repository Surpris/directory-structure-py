"""test_main.py

test code
"""

import pytest
from directory_structure_py.conversion import list2tree


def test_list2tree():
    expected = {
        "@graph": {
            "sample/": {
                "@id": "sample/",
                "type": "Directory",
                "parent": {},
                "basename": "sample",
                "hasPart": [
                    {
                        "sample/data/": {
                            "@id": "sample/data/",
                            "type": "Directory",
                            "parent": {
                                "@id": "sample/"
                            },
                            "basename": "data",
                            "hasPart": [
                                {
                                    "@id": "sample/data/data_001.csv",
                                    "type": "File",
                                    "parent": {
                                        "@id": "sample/data/"
                                    },
                                    "basename": "data_001.csv",
                                    "name": "data_001",
                                    "extension": ".csv",
                                    "contentSize": 42,
                                    "dateCreated": "2024-09-25T12:17:15",
                                    "dateModified": "2024-09-25T12:18:08"
                                },
                                {
                                    "@id": "sample/data/data_002.csv",
                                    "type": "File",
                                    "parent": {
                                        "@id": "sample/data/"
                                    },
                                    "basename": "data_002.csv",
                                    "name": "data_002",
                                    "extension": ".csv",
                                    "contentSize": 41,
                                    "dateCreated": "2024-09-25T12:17:48",
                                    "dateModified": "2024-09-25T12:18:05"
                                }
                            ],
                            "dateCreated": "2024-09-25T12:17:06",
                            "dateModified": "2024-09-25T12:17:53"
                        }
                    },
                    {
                        "sample/hogehoge/": {
                            "@id": "sample/hogehoge/",
                            "type": "Directory",
                            "parent": {
                                "@id": "sample/"
                            },
                            "basename": "hogehoge",
                            "hasPart": [
                                {
                                    "sample/hogehoge/data/": {
                                        "@id": "sample/hogehoge/data/",
                                        "type": "Directory",
                                        "parent": {
                                            "@id": "sample/hogehoge/"
                                        },
                                        "basename": "data",
                                        "hasPart": [
                                            {
                                                "@id": "sample/hogehoge/data/data_002.csv",
                                                "type": "File",
                                                "parent": {
                                                    "@id": "sample/hogehoge/data/"
                                                },
                                                "basename": "data_002.csv",
                                                "name": "data_002",
                                                "extension": ".csv",
                                                "contentSize": 41,
                                                "dateCreated": "2024-11-10T16:40:03",
                                                "dateModified": "2024-09-25T12:18:05"
                                            },
                                            {
                                                "@id": "sample/hogehoge/data/data_003.csv",
                                                "type": "File",
                                                "parent": {
                                                    "@id": "sample/hogehoge/data/"
                                                },
                                                "basename": "data_003.csv",
                                                "name": "data_003",
                                                "extension": ".csv",
                                                "contentSize": 47,
                                                "dateCreated": "2024-11-10T16:40:07",
                                                "dateModified": "2024-11-10T16:40:30"
                                            }
                                        ],
                                        "dateCreated": "2024-11-10T16:39:53",
                                        "dateModified": "2024-11-10T16:40:12"
                                    }
                                },
                                {
                                    "@id": "sample/hogehoge/fuga.txt",
                                    "type": "File",
                                    "parent": {
                                        "@id": "sample/hogehoge/"
                                    },
                                    "basename": "fuga.txt",
                                    "name": "fuga",
                                    "extension": ".txt",
                                    "contentSize": 6,
                                    "dateCreated": "2024-09-25T12:16:51",
                                    "dateModified": "2024-09-25T12:16:55"
                                }
                            ],
                            "dateCreated": "2024-09-25T12:16:46",
                            "dateModified": "2024-11-10T16:39:53"
                        }
                    },
                    {
                        "@id": "sample/readme.md",
                        "type": "File",
                        "parent": {
                            "@id": "sample/"
                        },
                        "basename": "readme.md",
                        "name": "readme",
                        "extension": ".md",
                        "contentSize": 187,
                        "dateCreated": "2024-09-25T12:16:19",
                        "dateModified": "2024-11-10T17:42:20"
                    }
                ],
                "dateCreated": "2024-09-25T12:16:08",
                "dateModified": "2024-11-23T12:15:26"
            }
        },
        "dateCreated": "2024-11-23T19:50:14"
    }
    src = {
        "root_path": "./",
        "@graph": [
            {
                "@id": "sample/",
                "type": "Directory",
                "parent": {},
                "basename": "sample",
                "hasPart": [
                    {
                        "@id": "sample/data/"
                    },
                    {
                        "@id": "sample/hogehoge/"
                    },
                    {
                        "@id": "sample/readme.md"
                    }
                ],
                "dateCreated": "2024-09-25T12:16:08",
                "dateModified": "2024-11-23T12:15:26"
            },
            {
                "@id": "sample/data/",
                "type": "Directory",
                "parent": {
                    "@id": "sample/"
                },
                "basename": "data",
                "hasPart": [
                    {
                        "@id": "sample/data/data_001.csv"
                    },
                    {
                        "@id": "sample/data/data_002.csv"
                    }
                ],
                "dateCreated": "2024-09-25T12:17:06",
                "dateModified": "2024-09-25T12:17:53"
            },
            {
                "@id": "sample/data/data_001.csv",
                "type": "File",
                "parent": {
                    "@id": "sample/data/"
                },
                "basename": "data_001.csv",
                "name": "data_001",
                "extension": ".csv",
                "contentSize": 42,
                "dateCreated": "2024-09-25T12:17:15",
                "dateModified": "2024-09-25T12:18:08"
            },
            {
                "@id": "sample/data/data_002.csv",
                "type": "File",
                "parent": {
                    "@id": "sample/data/"
                },
                "basename": "data_002.csv",
                "name": "data_002",
                "extension": ".csv",
                "contentSize": 41,
                "dateCreated": "2024-09-25T12:17:48",
                "dateModified": "2024-09-25T12:18:05"
            },
            {
                "@id": "sample/hogehoge/",
                "type": "Directory",
                "parent": {
                    "@id": "sample/"
                },
                "basename": "hogehoge",
                "hasPart": [
                    {
                        "@id": "sample/hogehoge/data/"
                    },
                    {
                        "@id": "sample/hogehoge/fuga.txt"
                    }
                ],
                "dateCreated": "2024-09-25T12:16:46",
                "dateModified": "2024-11-10T16:39:53"
            },
            {
                "@id": "sample/hogehoge/data/",
                "type": "Directory",
                "parent": {
                    "@id": "sample/hogehoge/"
                },
                "basename": "data",
                "hasPart": [
                    {
                        "@id": "sample/hogehoge/data/data_002.csv"
                    },
                    {
                        "@id": "sample/hogehoge/data/data_003.csv"
                    }
                ],
                "dateCreated": "2024-11-10T16:39:53",
                "dateModified": "2024-11-10T16:40:12"
            },
            {
                "@id": "sample/hogehoge/data/data_002.csv",
                "type": "File",
                "parent": {
                    "@id": "sample/hogehoge/data/"
                },
                "basename": "data_002.csv",
                "name": "data_002",
                "extension": ".csv",
                "contentSize": 41,
                "dateCreated": "2024-11-10T16:40:03",
                "dateModified": "2024-09-25T12:18:05"
            },
            {
                "@id": "sample/hogehoge/data/data_003.csv",
                "type": "File",
                "parent": {
                    "@id": "sample/hogehoge/data/"
                },
                "basename": "data_003.csv",
                "name": "data_003",
                "extension": ".csv",
                "contentSize": 47,
                "dateCreated": "2024-11-10T16:40:07",
                "dateModified": "2024-11-10T16:40:30"
            },
            {
                "@id": "sample/hogehoge/fuga.txt",
                "type": "File",
                "parent": {
                    "@id": "sample/hogehoge/"
                },
                "basename": "fuga.txt",
                "name": "fuga",
                "extension": ".txt",
                "contentSize": 6,
                "dateCreated": "2024-09-25T12:16:51",
                "dateModified": "2024-09-25T12:16:55"
            },
            {
                "@id": "sample/readme.md",
                "type": "File",
                "parent": {
                    "@id": "sample/"
                },
                "basename": "readme.md",
                "name": "readme",
                "extension": ".md",
                "contentSize": 187,
                "dateCreated": "2024-09-25T12:16:19",
                "dateModified": "2024-11-10T17:42:20"
            }
        ],
        "dateCreated": "2024-11-23T19:50:14"
    }
    dst = list2tree(src)
    assert dst == expected
