"""test_main.py

test code
"""

import json
import os
from pathlib import Path
from typing import Dict
from rocrate.rocrate import ROCrate
from rocrate.model import Metadata, Preview
import pytest
from directory_structure_py.constants import DEFAULT_OUTPUT_NAME
from directory_structure_py.conversion import (
    convert_meta_list_json_to_tsv,
    convert_meta_list_json_to_tsv_from_file,
    list2tree,
    list2tree_from_file,
    convert_meta_list_json_to_rocrate
)

def test_convert_meta_list_json_to_tsv():
    """test function for convert_meta_list_json_to_tsv"""
    src_path: str = os.path.join(
        os.path.dirname(__file__), f"../output/sample/{DEFAULT_OUTPUT_NAME}"
    )
    expected_path: str = src_path.replace(
        os.path.splitext(src_path)[-1], ".tsv"
    )
    src: Dict = {}
    with open(src_path, "r", encoding="utf-8") as ff:
        src = json.loads(ff.read())
    expected: list = []
    with open(expected_path, "r", encoding="utf-8") as ff:
        for line in ff:
            expected.append(line.rstrip("\n").split("\t"))
    dst = convert_meta_list_json_to_tsv(src)
    assert dst == expected


def test_convert_meta_list_json_to_tsv_from_file():
    """test function for convert_meta_list_json_to_tsv_from_file"""
    src_path: str = os.path.join(
        os.path.dirname(__file__), f"../output/sample/{DEFAULT_OUTPUT_NAME}"
    )
    expected_path: str = src_path.replace(
        os.path.splitext(src_path)[-1], ".tsv"
    )
    expected: list = []
    with open(expected_path, "r", encoding="utf-8") as ff:
        for line in ff:
            expected.append(line.rstrip("\n").split("\t"))
    dst = convert_meta_list_json_to_tsv_from_file(src_path)
    assert dst == expected

def test_list2tree():
    """test function for list2tree"""
    src_path: str = os.path.join(
        os.path.dirname(__file__), f"../output/sample/{DEFAULT_OUTPUT_NAME}"
    )
    expected_path: str = src_path.replace(
        os.path.splitext(src_path)[-1],
        f"_tree{os.path.splitext(src_path)[-1]}"
    )
    src: Dict = {}
    with open(src_path, "r", encoding="utf-8") as ff:
        src = json.loads(ff.read())
    expected: Dict = {}
    with open(expected_path, "r", encoding="utf-8") as ff:
        expected = json.loads(ff.read())
    dst = list2tree(src)
    assert dst == expected


def test_list2tree_from_file():
    """test function for list2tree_from_file"""
    src_path: str = os.path.join(
        os.path.dirname(__file__), f"../output/sample/{DEFAULT_OUTPUT_NAME}"
    )
    expected_path: str = src_path.replace(
        os.path.splitext(src_path)[-1],
        f"_tree{os.path.splitext(src_path)[-1]}"
    )
    expected: Dict = {}
    with open(expected_path, "r", encoding="utf-8") as ff:
        expected = json.loads(ff.read())
    dst = list2tree_from_file(src_path)
    assert dst == expected


def test_convert_meta_list_json_to_rocrate():
    """test function for convert_meta_list_json_to_rocrate
    """
    src_path: str = os.path.join(
        os.path.dirname(__file__), f"../output/sample/{DEFAULT_OUTPUT_NAME}"
    )
    expected_path: str = os.path.join(
        os.path.dirname(__file__), "../output/sample/ro-crate-metadata.json"
    )
    src: Dict = {}
    with open(src_path, "r", encoding="utf-8") as ff:
        src = json.loads(ff.read())
    root_path: str = os.path.join(os.path.dirname(__file__), "../sample")
    src["root_path"] = f"{str(Path(root_path).absolute().as_posix())}"
    expected: Dict = {}
    with open(expected_path, "r", encoding="utf-8") as ff:
        expected = json.loads(ff.read())
    dst: ROCrate = convert_meta_list_json_to_rocrate(src)
    _ = dst.add(Preview(dst))
    dst_metadata_json: Dict = Metadata(dst).generate()

    for key in expected.keys():
        assert dst_metadata_json.get(key) == expected.get(key)
