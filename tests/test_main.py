"""test_main.py

test code
"""

import pytest
from directory_structure_py.conversion import list2tree


def test_list2tree():
    expected = {
        "root_path": "./",
        "@graph": {
            "sample/": {
                "@id": "sample/",
                "type": "Directory",
                "parent": {},
                "basename": "sample",
                "name": "sample",
                "hasPart": [
                    {
                        "sample/data/": {
                            "@id": "sample/data/",
                            "type": "Directory",
                            "parent": {
                                "@id": "sample/"
                            },
                            "basename": "data",
                            "name": "data",
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
                                    "mimetype": "application/vnd.ms-excel",
                                    "contentSize": 42,
                                    "sha256": "81bd6ceb41ba6005e367ea487055b61bf177010d60b6354ab21c469dff22cfcd",
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
                                    "mimetype": "application/vnd.ms-excel",
                                    "contentSize": 41,
                                    "sha256": "a8681eaa42ac69b9281ce9d0c75221084336d2fc2f1b3d8b9807eb2bb6e0ac5b",
                                    "dateCreated": "2024-09-25T12:17:48",
                                    "dateModified": "2024-09-25T12:18:05"
                                }
                            ],
                            "contentSize": 83,
                            "numberOfContents": 2,
                            "numberOfFiles": 2,
                            "numberOfFilesPerExtension": {
                                ".csv": 2
                            },
                            "extension": [
                                ".csv"
                            ],
                            "numberOfFilesPerMIMEType": {
                                "application/vnd.ms-excel": 2
                            },
                            "mimetype": [
                                "application/vnd.ms-excel"
                            ],
                            "contentSizeOfAllFiles": 83,
                            "numberOfAllContents": 2,
                            "numberOfAllFiles": 2,
                            "numberOfAllFilesPerExtension": {
                                ".csv": 2
                            },
                            "extensionsOfAllFiles": [
                                ".csv"
                            ],
                            "numberOfAllFilesPerMIMEType": {
                                "application/vnd.ms-excel": 2
                            },
                            "mimetypesOfAllFiles": [
                                "application/vnd.ms-excel"
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
                            "name": "hogehoge",
                            "hasPart": [
                                {
                                    "sample/hogehoge/data/": {
                                        "@id": "sample/hogehoge/data/",
                                        "type": "Directory",
                                        "parent": {
                                            "@id": "sample/hogehoge/"
                                        },
                                        "basename": "data",
                                        "name": "data",
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
                                                "mimetype": "application/vnd.ms-excel",
                                                "contentSize": 41,
                                                "sha256": "a8681eaa42ac69b9281ce9d0c75221084336d2fc2f1b3d8b9807eb2bb6e0ac5b",
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
                                                "mimetype": "application/vnd.ms-excel",
                                                "contentSize": 47,
                                                "sha256": "885135f677ffdb7d34bdb7294669b7310f63fc13ee29d7fe29b80267e16f09a2",
                                                "dateCreated": "2024-11-10T16:40:07",
                                                "dateModified": "2024-11-10T16:40:30"
                                            }
                                        ],
                                        "contentSize": 88,
                                        "numberOfContents": 2,
                                        "numberOfFiles": 2,
                                        "numberOfFilesPerExtension": {
                                            ".csv": 2
                                        },
                                        "extension": [
                                            ".csv"
                                        ],
                                        "numberOfFilesPerMIMEType": {
                                            "application/vnd.ms-excel": 2
                                        },
                                        "mimetype": [
                                            "application/vnd.ms-excel"
                                        ],
                                        "contentSizeOfAllFiles": 88,
                                        "numberOfAllContents": 2,
                                        "numberOfAllFiles": 2,
                                        "numberOfAllFilesPerExtension": {
                                            ".csv": 2
                                        },
                                        "extensionsOfAllFiles": [
                                            ".csv"
                                        ],
                                        "numberOfAllFilesPerMIMEType": {
                                            "application/vnd.ms-excel": 2
                                        },
                                        "mimetypesOfAllFiles": [
                                            "application/vnd.ms-excel"
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
                                    "mimetype": "text/plain",
                                    "contentSize": 6,
                                    "sha256": "487e0520fb988a5475fae2cd9abdcc2454cc96b5540ef1847ac3115265c02038",
                                    "dateCreated": "2024-09-25T12:16:51",
                                    "dateModified": "2024-09-25T12:16:55"
                                }
                            ],
                            "contentSize": 6,
                            "numberOfContents": 2,
                            "numberOfFiles": 1,
                            "numberOfFilesPerExtension": {
                                ".txt": 1
                            },
                            "extension": [
                                ".txt"
                            ],
                            "numberOfFilesPerMIMEType": {
                                "text/plain": 1
                            },
                            "mimetype": [
                                "text/plain"
                            ],
                            "contentSizeOfAllFiles": 94,
                            "numberOfAllContents": 4,
                            "numberOfAllFiles": 3,
                            "numberOfAllFilesPerExtension": {
                                ".txt": 1,
                                ".csv": 2
                            },
                            "extensionsOfAllFiles": [
                                ".txt",
                                ".csv"
                            ],
                            "numberOfAllFilesPerMIMEType": {
                                "text/plain": 1,
                                "application/vnd.ms-excel": 2
                            },
                            "mimetypesOfAllFiles": [
                                "text/plain",
                                "application/vnd.ms-excel"
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
                        "mimetype": "text/markdown",
                        "contentSize": 187,
                        "sha256": "0252adf6bb7bf5c8882f666bf0539acfe19eb372fc90739b86e14df92eef79a6",
                        "dateCreated": "2024-09-25T12:16:19",
                        "dateModified": "2024-11-10T17:42:20"
                    }
                ],
                "contentSize": 187,
                "numberOfContents": 3,
                "numberOfFiles": 1,
                "numberOfFilesPerExtension": {
                    ".md": 1
                },
                "extension": [
                    ".md"
                ],
                "numberOfFilesPerMIMEType": {
                    "text/markdown": 1
                },
                "mimetype": [
                    "text/markdown"
                ],
                "contentSizeOfAllFiles": 364,
                "numberOfAllContents": 9,
                "numberOfAllFiles": 6,
                "numberOfAllFilesPerExtension": {
                    ".md": 1,
                    ".csv": 4,
                    ".txt": 1
                },
                "extensionsOfAllFiles": [
                    ".md",
                    ".csv",
                    ".txt"
                ],
                "numberOfAllFilesPerMIMEType": {
                    "text/markdown": 1,
                    "application/vnd.ms-excel": 4,
                    "text/plain": 1
                },
                "mimetypesOfAllFiles": [
                    "text/markdown",
                    "application/vnd.ms-excel",
                    "text/plain"
                ],
                "dateCreated": "2024-09-25T12:16:08",
                "dateModified": "2024-11-23T12:15:26"
            }
        },
        "dateCreated": "2024-12-15T23:25:03"
    }
    src = {
        "root_path": "./",
        "@graph": [
            {
                "@id": "sample/",
                "type": "Directory",
                "parent": {},
                "basename": "sample",
                "name": "sample",
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
                "contentSize": 187,
                "numberOfContents": 3,
                "numberOfFiles": 1,
                "numberOfFilesPerExtension": {
                    ".md": 1
                },
                "extension": [
                    ".md"
                ],
                "numberOfFilesPerMIMEType": {
                    "text/markdown": 1
                },
                "mimetype": [
                    "text/markdown"
                ],
                "contentSizeOfAllFiles": 364,
                "numberOfAllContents": 9,
                "numberOfAllFiles": 6,
                "numberOfAllFilesPerExtension": {
                    ".md": 1,
                    ".csv": 4,
                    ".txt": 1
                },
                "extensionsOfAllFiles": [
                    ".md",
                    ".csv",
                    ".txt"
                ],
                "numberOfAllFilesPerMIMEType": {
                    "text/markdown": 1,
                    "application/vnd.ms-excel": 4,
                    "text/plain": 1
                },
                "mimetypesOfAllFiles": [
                    "text/markdown",
                    "application/vnd.ms-excel",
                    "text/plain"
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
                "name": "data",
                "hasPart": [
                    {
                        "@id": "sample/data/data_001.csv"
                    },
                    {
                        "@id": "sample/data/data_002.csv"
                    }
                ],
                "contentSize": 83,
                "numberOfContents": 2,
                "numberOfFiles": 2,
                "numberOfFilesPerExtension": {
                    ".csv": 2
                },
                "extension": [
                    ".csv"
                ],
                "numberOfFilesPerMIMEType": {
                    "application/vnd.ms-excel": 2
                },
                "mimetype": [
                    "application/vnd.ms-excel"
                ],
                "contentSizeOfAllFiles": 83,
                "numberOfAllContents": 2,
                "numberOfAllFiles": 2,
                "numberOfAllFilesPerExtension": {
                    ".csv": 2
                },
                "extensionsOfAllFiles": [
                    ".csv"
                ],
                "numberOfAllFilesPerMIMEType": {
                    "application/vnd.ms-excel": 2
                },
                "mimetypesOfAllFiles": [
                    "application/vnd.ms-excel"
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
                "mimetype": "application/vnd.ms-excel",
                "contentSize": 42,
                "sha256": "81bd6ceb41ba6005e367ea487055b61bf177010d60b6354ab21c469dff22cfcd",
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
                "mimetype": "application/vnd.ms-excel",
                "contentSize": 41,
                "sha256": "a8681eaa42ac69b9281ce9d0c75221084336d2fc2f1b3d8b9807eb2bb6e0ac5b",
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
                "name": "hogehoge",
                "hasPart": [
                    {
                        "@id": "sample/hogehoge/data/"
                    },
                    {
                        "@id": "sample/hogehoge/fuga.txt"
                    }
                ],
                "contentSize": 6,
                "numberOfContents": 2,
                "numberOfFiles": 1,
                "numberOfFilesPerExtension": {
                    ".txt": 1
                },
                "extension": [
                    ".txt"
                ],
                "numberOfFilesPerMIMEType": {
                    "text/plain": 1
                },
                "mimetype": [
                    "text/plain"
                ],
                "contentSizeOfAllFiles": 94,
                "numberOfAllContents": 4,
                "numberOfAllFiles": 3,
                "numberOfAllFilesPerExtension": {
                    ".txt": 1,
                    ".csv": 2
                },
                "extensionsOfAllFiles": [
                    ".txt",
                    ".csv"
                ],
                "numberOfAllFilesPerMIMEType": {
                    "text/plain": 1,
                    "application/vnd.ms-excel": 2
                },
                "mimetypesOfAllFiles": [
                    "text/plain",
                    "application/vnd.ms-excel"
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
                "name": "data",
                "hasPart": [
                    {
                        "@id": "sample/hogehoge/data/data_002.csv"
                    },
                    {
                        "@id": "sample/hogehoge/data/data_003.csv"
                    }
                ],
                "contentSize": 88,
                "numberOfContents": 2,
                "numberOfFiles": 2,
                "numberOfFilesPerExtension": {
                    ".csv": 2
                },
                "extension": [
                    ".csv"
                ],
                "numberOfFilesPerMIMEType": {
                    "application/vnd.ms-excel": 2
                },
                "mimetype": [
                    "application/vnd.ms-excel"
                ],
                "contentSizeOfAllFiles": 88,
                "numberOfAllContents": 2,
                "numberOfAllFiles": 2,
                "numberOfAllFilesPerExtension": {
                    ".csv": 2
                },
                "extensionsOfAllFiles": [
                    ".csv"
                ],
                "numberOfAllFilesPerMIMEType": {
                    "application/vnd.ms-excel": 2
                },
                "mimetypesOfAllFiles": [
                    "application/vnd.ms-excel"
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
                "mimetype": "application/vnd.ms-excel",
                "contentSize": 41,
                "sha256": "a8681eaa42ac69b9281ce9d0c75221084336d2fc2f1b3d8b9807eb2bb6e0ac5b",
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
                "mimetype": "application/vnd.ms-excel",
                "contentSize": 47,
                "sha256": "885135f677ffdb7d34bdb7294669b7310f63fc13ee29d7fe29b80267e16f09a2",
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
                "mimetype": "text/plain",
                "contentSize": 6,
                "sha256": "487e0520fb988a5475fae2cd9abdcc2454cc96b5540ef1847ac3115265c02038",
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
                "mimetype": "text/markdown",
                "contentSize": 187,
                "sha256": "0252adf6bb7bf5c8882f666bf0539acfe19eb372fc90739b86e14df92eef79a6",
                "dateCreated": "2024-09-25T12:16:19",
                "dateModified": "2024-11-10T17:42:20"
            }
        ],
        "dateCreated": "2024-12-15T23:25:03"
    }
    dst = list2tree(src)
    assert dst == expected
