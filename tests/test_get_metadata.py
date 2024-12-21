"""test_get_metadata.py

test functions for get_metadata.py
"""

import json
import os
from pathlib import Path
from typing import Dict
import pytest
from directory_structure_py.constants import DEFAULT_OUTPUT_NAME
from directory_structure_py.get_metadata import (
    generate_id,
    get_metadata_of_single_file,
    generate_blank_metadata,
    get_metadata_of_single_directory,
    get_metadata_of_files_in_list_format,
    update_statistical_info_to_metadata_list
)


def test_generate_id_wo_root_path():
    """test function for generate_id without root_path"""
    src_path: Path = Path(os.path.join(os.path.dirname(__file__), "../sample"))
    expected: str = str(src_path.absolute().as_posix()) + "/"
    dst: str = generate_id(src_path)
    assert expected == dst


def test_generate_id_w_root_path():
    """test function for generate_id with root_path"""
    root_path: Path = Path(os.path.join(os.path.dirname(__file__)))
    src_path: Path = Path(os.path.join(os.path.dirname(__file__), "../sample"))
    expected: str = f"{
        root_path.name}/{str(src_path.relative_to(root_path).as_posix())}/"
    dst: str = generate_id(src_path, root_path=root_path)
    assert expected == dst


def test_generate_id_w_equal_root_path():
    """test function for generate_id with root_path equal to the source path"""
    src_path: Path = Path(os.path.join(os.path.dirname(__file__), "../sample"))
    root_path: Path = src_path
    expected: str = f"{src_path.name}/"
    dst: str = generate_id(src_path, root_path=root_path)
    assert expected == dst


def test_get_metadata_of_single_file_w_root_path():
    """test function for get_metadata_of_single_file with root_path"""
    src_path: Path = Path(os.path.join(
        os.path.dirname(__file__), "../sample/readme.md"))
    metadata_path: str = os.path.join(
        os.path.dirname(__file__), f"../output/sample/{DEFAULT_OUTPUT_NAME}"
    )
    root_path: Path = Path(os.path.join(
        os.path.dirname(__file__), "../sample")
    )
    metadata: Dict = {}
    with open(metadata_path, "r", encoding="utf-8") as ff:
        metadata = json.loads(ff.read())
    dst: Dict = get_metadata_of_single_file(src_path, root_path)
    expected: Dict = {}
    for meta_ in metadata["@graph"]:
        if meta_["@id"] == dst["@id"]:
            expected = meta_
            break
    properties_existing_only: list = [
        "dateCreated",
        "dateModified",
        "sha256",
    ]
    for k, v in dst.items():
        if k in properties_existing_only:
            assert v is not None
        else:
            assert v == expected[k]


def test_generate_blank_metadata_w_root_path():
    """test function for generate_blank_metadata with root_path"""
    src_path: Path = os.path.join(
        os.path.dirname(__file__), "../sample/readme.md"
    )
    root_path: Path = Path(os.path.join(os.path.dirname(__file__)))
    expected: Dict = {
        "@id": str(src_path).replace(os.path.sep, "/"),
        "type": "Unknown",
        "parent": {
            "@id": generate_id(
                "/".join(s for s in str(src_path).split(os.path.sep)[:-1]),
                root_path
            )
        },
        "basename": "readme.md",
        "name": "readme",
        "extension": ".md",
        "mimetype": "unknown",
        "contentSize": -1,
        "sha256": "",
        "dateCreated": "unknown",
        "dateModified": "unknown"
    }
    dst: Dict = generate_blank_metadata(src_path, root_path=root_path)
    assert expected == dst


def test_get_metadata_of_single_directory_w_root_path():
    """test function for get_metadata_of_single_directory with root_path"""
    src_path: Path = Path(os.path.join(
        os.path.dirname(__file__), "../sample/data"))
    metadata_path: str = os.path.join(
        os.path.dirname(__file__), f"../output/sample/{DEFAULT_OUTPUT_NAME}"
    )
    root_path: Path = Path(os.path.join(
        os.path.dirname(__file__), "../sample")
    )
    metadata: Dict = {}
    with open(metadata_path, "r", encoding="utf-8") as ff:
        metadata = json.loads(ff.read())
    dst: Dict = get_metadata_of_single_directory(src_path, root_path)
    expected: Dict = {}
    for meta_ in metadata["@graph"]:
        if meta_["@id"] == dst["@id"]:
            expected = meta_
            break
    properties_existing_only: list = [
        "dateCreated",
        "dateModified",
        "sha256",
    ]
    for k, v in dst.items():
        if k in properties_existing_only:
            assert v is not None
        else:
            assert v == expected[k]


def test_get_metadata_of_files_in_list_format_w_root_path():
    """test function for get_metadata_of_files_in_list_format with root_path"""
    src_path: Path = Path(os.path.join(os.path.dirname(__file__), "../sample"))
    metadata_path: str = os.path.join(
        os.path.dirname(__file__), f"../output/sample/{DEFAULT_OUTPUT_NAME}"
    )
    expected: Dict = {}
    with open(metadata_path, "r", encoding="utf-8") as ff:
        expected = json.loads(ff.read())
    dst: Dict = get_metadata_of_files_in_list_format(src_path)
    assert expected["root_path"] == dst["root_path"]

    properties_existing_only: list = [
        "contentSizeOfAllFiles",
        "numberOfAllContents",
        "numberOfAllFiles",
        "numberOfAllFilesPerExtension",
        "extensionsOfAllFiles",
        "numberOfAllFilesPerMIMEType",
        "mimetypesOfAllFiles",
        "dateCreated",
        "dateModified",
    ]
    for ii, meta in enumerate(dst["@graph"]):
        meta_ = expected["@graph"][ii]
        for k, v in meta.items():
            if k in properties_existing_only:
                assert v is not None
            else:
                assert v == meta_[k]


def test_update_statistical_info_to_metadata_list():
    """test function for update_statistical_info_to_metadata_list"""
    src_path: Path = Path(os.path.join(os.path.dirname(__file__), "../sample"))
    metadata_path: str = os.path.join(
        os.path.dirname(__file__), f"../output/sample/{DEFAULT_OUTPUT_NAME}"
    )
    expected: Dict = {}
    with open(metadata_path, "r", encoding="utf-8") as ff:
        expected = json.loads(ff.read())
    dst: Dict = get_metadata_of_files_in_list_format(src_path)
    dst: Dict = update_statistical_info_to_metadata_list(dst)
    properties_existing_only: list = [
        "dateCreated",
        "dateModified",
    ]
    for ii, meta in enumerate(dst["@graph"]):
        meta_ = expected["@graph"][ii]
        for k, v in meta.items():
            if k in properties_existing_only:
                assert v is not None
            else:
                assert v == meta_[k]
