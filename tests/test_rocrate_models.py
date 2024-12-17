"""test_rocrate_models.py

test functions for rocrate_models.py
"""

import json
import os
from pathlib import Path
from typing import Dict
from rocrate.rocrate import ROCrate
import pytest
from directory_structure_py.constants import DEFAULT_OUTPUT_NAME, DEFAULT_PREVIEW_TEMPLATE_PATH
from directory_structure_py.conversion import convert_meta_list_json_to_rocrate
from directory_structure_py.rocrate_models import (
    Preview, Metadata
)


def test_metadadta_generate():
    """test function for Metadata.generate()"""
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


def test_preview_generate_html():
    """test function for Preview.generate_html()"""
    src_path: str = os.path.join(
        os.path.dirname(__file__), f"../output/sample/{DEFAULT_OUTPUT_NAME}"
    )
    expected_path: str = os.path.join(
        os.path.dirname(__file__), "../output/sample/ro-crate-preview.html"
    )
    preview_template_path: str = os.path.join(
        os.path.dirname(__file__),
        f"../directory_structure_py/templates/{DEFAULT_PREVIEW_TEMPLATE_PATH}"
    )
    src: Dict = {}
    with open(src_path, "r", encoding="utf-8") as ff:
        src = json.loads(ff.read())
    root_path: str = os.path.join(os.path.dirname(__file__), "../sample")
    src["root_path"] = f"{str(Path(root_path).absolute().as_posix())}"
    expected: str = ""
    with open(expected_path, "r", encoding="utf-8") as ff:
        expected = ff.read()
    dst: ROCrate = convert_meta_list_json_to_rocrate(src)
    _ = dst.add(Preview(dst))
    dst_html: str = dst.preview.generate_html(preview_template_path)

    assert expected == dst_html
