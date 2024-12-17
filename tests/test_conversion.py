"""test_main.py

test code
"""

import json
import os
from typing import Dict
import pytest
from directory_structure_py.constants import DEFAULT_OUTPUT_NAME
from directory_structure_py.conversion import list2tree


def test_list2tree():
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
