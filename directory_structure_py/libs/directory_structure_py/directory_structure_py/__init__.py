"""directory_structure_py module.
"""

from typing import Any
from directory_structure_py._version import __version__


def __getattr__(name: str) -> Any:
    if name == "cli_main":
        from directory_structure_py_cli.cli import main as cli_main
        return cli_main
    if name == "get_metadata_of_files_in_list_format":
        from directory_structure_py_core.get_metadata import get_metadata_of_files_in_list_format
        return get_metadata_of_files_in_list_format
    if name == "update_statistical_info_to_metadata_list":
        from directory_structure_py_core.get_metadata import update_statistical_info_to_metadata_list
        return update_statistical_info_to_metadata_list
    if name == "list2tree":
        from directory_structure_py_core.conversion import list2tree
        return list2tree
    if name == "list2tree_from_file":
        from directory_structure_py_core.conversion import list2tree_from_file
        return list2tree_from_file
    if name == "convert_meta_list_json_to_tsv":
        from directory_structure_py_core.conversion import convert_meta_list_json_to_tsv
        return convert_meta_list_json_to_tsv
    if name == "convert_meta_list_json_to_tsv_from_file":
        from directory_structure_py_core.conversion import convert_meta_list_json_to_tsv_from_file
        return convert_meta_list_json_to_tsv_from_file
    if name == "convert_meta_list_json_to_rocrate":
        from directory_structure_py_extension.rocrate.converter import convert_meta_list_json_to_rocrate
        return convert_meta_list_json_to_rocrate
    raise ModuleNotFoundError(f"Could not find: {name}")


__all__ = [
    "cli_main",
    "get_metadata_of_files_in_list_format",
    "update_statistical_info_to_metadata_list",
    "list2tree",
    "list2tree_from_file",
    "convert_meta_list_json_to_tsv",
    "convert_meta_list_json_to_tsv_from_file",
    "convert_meta_list_json_to_rocrate"
]
