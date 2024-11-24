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
    """Generates metadata for a single file.

    Args:
        path (Path | str): The path to the file.
        root_path (Path | str, optional): The root path. Defaults to "".

    Raises:
        TypeError: If 'path' is not a file path.

    Returns:
        Dict[str, Any]: A dictionary containing the file's metadata.  The dictionary includes:
            - `@id`: A unique identifier for the file.
            - `type`: Always "File".
            - `parent`: A dictionary containing the parent directory's id
                (or an empty dictionary if it's the root).
            - `basename`: The filename with extension.
            - `name`: The filename without extension.
            - `extension`: The file extension.
            - `contentSize`: The file size in bytes.
            - `dateCreated`: The file creation date and time in ISO 8601 format.
            - `dateModified`: The file last modification date and time in ISO 8601 format.

    """
    if isinstance(path, str):
        path = Path(path)
    if not path.is_file():
        raise TypeError("'path' must be a file path.")

    dst: Dict[str, Any] = {}
    dst["@id"] = generate_id(path, root_path)
    dst["type"] = "File"
    if str(path) == str(root_path):
        dst["parent"] = {}
    else:
        dst["parent"] = {"@id": generate_id(path.parent, root_path)}
    dst["basename"] = path.name
    dst["name"] = os.path.splitext(path.name)[0]
    dst["extension"] = os.path.splitext(path.name)[1]
    dst["contentSize"] = path.stat().st_size
    dst["dateCreated"] = datetime.datetime.fromtimestamp(
        path.stat().st_ctime
    ).strftime(DATETIME_FMT)
    dst["dateModified"] = datetime.datetime.fromtimestamp(
        path.stat().st_mtime
    ).strftime(DATETIME_FMT)

    return dst


def get_metadata_of_single_directory(
    path: Path | str, root_path: Path | str = ""
) -> Dict[str, Any]:
    """Generates metadata for a single directory.

    Args:
        path (Path | str): The path to the directory.
        root_path (Path | str, optional): The root path. Defaults to "".

    Raises:
        TypeError: If 'path' is not a directory path.

    Returns:
        Dict[str, Any]: A dictionary containing the directory's metadata. The dictionary includes:
            - `@id`: A unique identifier for the directory.
            - `type`: Always "Directory".
            - `parent`: A dictionary containing the parent directory's id 
                (or an empty dictionary if it's the root).
            - `basename`: The directory name.
            - `hasPart`: A list of dictionaries, each containing
                the `@id` of a file or subdirectory within this directory.
            - `dateCreated`: The directory creation date and time in ISO 8601 format.
            - `dateModified`: The directory last modification date and time in ISO 8601 format.

    """
    if isinstance(path, str):
        path = Path(path)
    if not path.is_dir():
        raise TypeError("'path' must be a directory path.")

    dst: Dict[str, Any] = {}
    dst["@id"] = generate_id(path, root_path)
    dst["type"] = "Directory"
    if str(path) == str(root_path):
        dst["parent"] = {}
    else:
        dst["parent"] = {"@id": generate_id(path.parent, root_path)}
    dst["basename"] = path.name
    dst["name"] = path.name
    dst["extension"] = [
        os.path.splitext(p_.name)[1] for p_ in path.iterdir()
        if p_.is_file()
    ]
    dst["contentSize"] = sum(
        p_.stat().st_size for p_ in path.iterdir() if p_.is_file()
    )
    dst["hasPart"] = [
        {"@id": generate_id(p_, root_path)}
        for p_ in path.iterdir()
    ]
    dst["numberOfContents"] = len(dst["hasPart"])
    dst["numberOfFileContents"] = len([
        p_ for p_ in path.iterdir() if p_.is_file()
    ])
    dst["dateCreated"] = datetime.datetime.fromtimestamp(
        path.stat().st_ctime
    ).strftime(DATETIME_FMT)
    dst["dateModified"] = datetime.datetime.fromtimestamp(
        path.stat().st_mtime
    ).strftime(DATETIME_FMT)

    return dst


def _get_metadata_list(src: Path, root_path: Path | str = "") -> List[Dict[str, Any]]:
    dst: List[Dict[str, Any]] = []
    if src.is_file():
        dst.append(
            get_metadata_of_single_file(src, root_path=root_path)
        )
        return dst
    dst.append(
        get_metadata_of_single_directory(src, root_path=root_path)
    )
    for path_ in src.iterdir():
        dst.extend(_get_metadata_list(path_, root_path=root_path))
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


def _update_statistical_info_of_directory(
    src: Dict[str, Any], metadata_list: List[Dict]
) -> Dict[str, Any]:
    for part in src["hasPart"]:
        for node in metadata_list:
            if node["type"] == "File":
                continue
            if node["@id"] == part["@id"] and node["parent"]["@id"] == src["@id"]:
                node = _update_statistical_info_of_directory(
                    node, metadata_list
                )
                src["contentSize"] += node["contentSize"]
                src["extension"].extend(node["extension"])
                src["numberOfContents"] += node["numberOfContents"]
                src["numberOfFileContents"] += node["numberOfFileContents"]
    return src


def update_statistical_info_to_metadata_list(src: Dict[str, Any]) -> Dict[str, Any]:
    contents: List[Dict[str, Any]] = src[OUTPUT_ROOT_KEY]
    root: Dict[str, Any] = {}
    for node in contents:
        if not node["parent"]:
            root = node
            break
    _ =  _update_statistical_info_of_directory(root, contents)
    return src
