"""get_metadata
"""

import datetime
import os
from pathlib import Path
from typing import Dict, Any, List
from directory_structure_py.src.constants import DATETIME_FMT, OUTPUT_ROOT_KEY


def generate_id(path: Path | str, root_path: Path | str = "") -> str:
    """Generates a unique ID from a given path, optionally relative to a root path.

    The generated ID is a string representation of the path, either absolute or relative
    to the `root_path`.  It uses a POSIX-style path representation (forward slashes).

    Args:
        path: The path to generate an ID from. Can be a `pathlib.Path` object or a string.
        root_path: An optional root path. If provided, the generated ID will be relative
            to this path. Can be a `pathlib.Path` object or a string.  If not provided
            or an empty string, the absolute path is used.

    Returns:
        A string representing the unique ID of the path.
    """
    if isinstance(path, str):
        path = Path(path)

    if not root_path:
        if path.is_dir():
            return str(path.absolute().as_posix()) + "/"
        return str(path.absolute().as_posix())
    if isinstance(root_path, str):
        root_path = Path(root_path)
    if path == root_path:
        if path.is_dir():
            return f"{path.name}/"
        return path.name
    if path.is_dir():
        return f"{root_path.name}/{str(path.relative_to(root_path).as_posix())}/"
    return f"{root_path.name}/{str(path.relative_to(root_path).as_posix())}"


def get_metadata_of_single_file(path: Path | str, root_path: Path | str = "") -> Dict[str, Any]:
    """
    Retrieves metadata for a given file or directory using the Pathlib module.

    Args:
        path (Path or str): The path to the file or directory.
            This can be a Path object or a string representing the path.
        root_path (Path or str): The root path to which the path is relative.
            This is used to set '@id.'
            If blank, then the absolute path of 'path' is set as '@id.'

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

    dst["@id"] = generate_id(path, root_path)

    if path.is_file():
        dst["type"] = "File"
    elif path.is_dir():
        dst["type"] = "Directory"
    else:
        dst["type"] = "Unknown"

    if str(path) == str(root_path):
        dst["parent"] = {}
    else:
        dst["parent"] = {"@id": generate_id(path.parent, root_path)}
    dst["basename"] = path.name
    if path.is_file():
        dst["name"] = os.path.splitext(path.name)[0]
        dst["extension"] = os.path.splitext(path.name)[1]
    if path.is_dir():
        part: List[str] = [generate_id(p_, root_path) for p_ in path.iterdir()]
        if part:
            dst["hasPart"] = [{"@id": p_} for p_ in part]
    if path.is_file():
        dst["contentSize"] = path.stat().st_size
    dst["dateCreated"] = datetime.datetime.fromtimestamp(
        path.stat().st_ctime
    ).strftime(DATETIME_FMT)
    dst["dateModified"] = datetime.datetime.fromtimestamp(
        path.stat().st_mtime
    ).strftime(DATETIME_FMT)
    return dst


def get_metadata_of_files_in_list_format(
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
    def _get_metadata_list(src: Path, root_path: Path | str = "") -> List[Dict[str, Any]]:
        dst: List[Dict[str, Any]] = []
        dst.append(
            get_metadata_of_single_file(src, root_path=root_path)
        )
        if src.is_file():
            return dst
        for path_ in src.iterdir():
            dst.extend(_get_metadata_list(path_, root_path=root_path))
        return dst

    dst: Dict[str, Any] = {}
    if isinstance(src, str):
        src = Path(src)
    if include_root_path:
        dst["root_path"] = f"{str(Path(src).as_posix())}/"
    else:
        dst["root_path"] = "./"
    dst[OUTPUT_ROOT_KEY] = _get_metadata_list(src, root_path=src)
    dst["dateCreated"] = datetime.datetime.now().strftime(DATETIME_FMT)
    return dst
