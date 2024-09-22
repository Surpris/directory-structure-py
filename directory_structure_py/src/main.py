"""directory_structure_py

get the directory tree
"""

import datetime
import json
import os
from pathlib import Path
from typing import Dict, Any, List

DATETIME_FMT: str = "%Y-%m-%dT%H:%M:%S"
DEFAULT_OUTPUT_NAME: str = "directory_structure_metadata.json"
JSON_OUTPUT_INDENT: int = 4


def get_metadata_of_single_file(path: Path | str) -> Dict[str, Any]:
    """
    Retrieves metadata for a given file or directory using the Pathlib module.

    Args:
        path (Path or str): The path to the file or directory.
        This can be a Path object or a string representing the path.

    Returns:
        Dict[str, Any]: A dictionary containing metadata for the file or directory.
        The metadata includes:
            - "type": The type of the path, either 'file' or 'directory'.
            - "name": The name of the file or directory.
            - "size": The size of the file in bytes.
            - "creation_datetime": The creation time of the file or directory 
            formatted as a string.
            - "modification_datetime": The last modification time of
            the file or directory formatted as a string.
    """
    if isinstance(path, str):
        path = Path(path)
    dst: Dict[str, Any] = {}
    if path.is_file():
        dst["type"] = "File"
    elif path.is_dir():
        dst["type"] = "Directory"
    else:
        dst["type"] = "Unknown"

    dst["basename"] = path.name
    if path.is_file():
        dst["name"] = os.path.splitext(path.name)[0]
        dst["extension"] = os.path.splitext(path.name)[1]
    if path.is_dir():
        part: List[str] = [p_.name for p_ in path.iterdir()]
        if part:
            dst["hasPart"] =  part
    dst["contentSize"] = path.stat().st_size
    dst["creationDatetime"] = datetime.datetime.fromtimestamp(
        path.stat().st_ctime
    ).strftime(DATETIME_FMT)
    dst["modificationDatetime"] = datetime.datetime.fromtimestamp(
        path.stat().st_mtime
    ).strftime(DATETIME_FMT)
    return dst


def get_metadata_of_files(
    src: Path | str, include_root_path: bool = False
) -> Dict[str, Any]:
    """
    Recursively retrieves metadata for files and directories within a given path.

    This function walks through the directory tree starting at the specified source 
    path (`src`), collecting metadata for each file and directory. The metadata for 
    each file or directory is gathered using the `get_metadata_of_single_file` function.
    Optionally, the root path can be included in the returned metadata.

    Args:
        src (Path | str): The root directory or file path as a `pathlib.Path` object 
        or string, from which to begin the directory traversal.
        include_root_path (bool): If `True`, includes the root path in the result 
        under the key 'root_path'. Default is `False`.

    Returns:
        Dict[str, Any]: A dictionary where each key represents a directory name 
        (or file name if no subdirectories exist), and its value is another dictionary 
        containing the metadata for the files and directories within it. If `include_root_path`
        is `True`, the 'root_path' key will hold the string representation of the root directory.
    """
    def _get_metadata_list(src: Path) -> List[Dict[str, Any]]:
        dst: List[Dict[str, Any]] = []
        dst.append(get_metadata_of_single_file(src))
        if src.is_file():
            return dst
        for path_ in src.iterdir():
            dst.extend(_get_metadata_list(path_))
        return dst

    dst: Dict[str, Any] = {}
    if isinstance(src, str):
        src = Path(src)
    if include_root_path:
        dst["root_path"] = str(src)
    dst["contents"] = _get_metadata_list(src)
    return dst


def main(src: Path | str, dst: Path | str, include_root_path: bool):
    """
    Collects metadata from the source directory and writes it to a JSON file.

    This function retrieves metadata for all files and directories within the 
    specified source directory (`src`) using the `get_metadata_of_files` function. 
    It then writes the collected metadata to the specified destination file (`dst`) 
    in JSON format with UTF-8 encoding. If `include_root_path` is `True`, 'src'
    will be included in the output with the 'root_path' key.

    Args:
        src (Path | str): The path to the source directory from which to collect metadata.
        dst (Path | str): The path to the destination file where the metadata will be saved 
        as a JSON file.
        include_root_path (bool): If `True`, includes the root path in the result 
        under the key 'root_path'. Default is `False`.

    Returns:
        None: The function writes the metadata to a file and does not return anything.
    """
    data: Dict[str, Any] = get_metadata_of_files(src, include_root_path)
    with open(dst, "w", encoding="utf-8") as ff:
        json.dump(data, ff, indent=JSON_OUTPUT_INDENT)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str)
    parser.add_argument(
        "--dst", dest="dst", type=str, default=""
    )
    parser.add_argument(
        "--include_root_path", dest="include_root_path", action="store_true"
    )
    args = parser.parse_args()
    if not args.dst:
        args.dst = os.path.join(args.src, DEFAULT_OUTPUT_NAME)
    main(args.src, args.dst, args.include_root_path)
