"""get_metadata
"""

import datetime
import json
import os
from pathlib import Path
from typing import Dict, Any, List

from directory_structure_py.src.constants import DATETIME_FMT


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
    if not root_path:
        return str(path.absolute().as_posix())
    if path == root_path:
        return "."
    return str(path.relative_to(root_path).as_posix())


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
    dst["contentSize"] = path.stat().st_size
    dst["creationDatetime"] = datetime.datetime.fromtimestamp(
        path.stat().st_ctime
    ).strftime(DATETIME_FMT)
    dst["modificationDatetime"] = datetime.datetime.fromtimestamp(
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
        dst.append(get_metadata_of_single_file(src, root_path=root_path))
        if src.is_file():
            return dst
        for path_ in src.iterdir():
            dst.extend(_get_metadata_list(path_, root_path=root_path))
        return dst

    dst: Dict[str, Any] = {}
    if isinstance(src, str):
        src = Path(src)
    if include_root_path:
        dst["root_path"] = str(src)
    else:
        dst["root_path"] = "."
    dst["contents"] = _get_metadata_list(src, root_path=src)
    return dst


def json2tsv(src: str, dst: str = "") -> None:
    """
    Converts a JSON file to a TSV (Tab-Separated Values) file.

    The function reads a JSON file specified by `src`, extracts its contents,
    and writes them into a TSV file. 
    If the `dst` (destination) parameter is not provided, the output TSV file will
    have the same name as the source file but with a `.tsv` extension.

    The JSON structure is expected to contain a "contents" key, which holds a list of dictionaries. 
    The function gathers all the unique keys from these dictionaries to form the columns of
    the TSV file. 
    For each row (content), it writes values corresponding to these keys. If a key is missing in
    a particular row, an empty string is used.

    Args:
        src (str): Path to the source JSON file.
        dst (str, optional): Path to the destination TSV file.
            Defaults to a file with the same name as `src` but with a `.tsv` extension.

    Returns:
        None: The function writes directly to a file and does not return a value.

    Raises:
        FileNotFoundError: If the source file does not exist.
        JSONDecodeError: If the source file is not a valid JSON.
        OSError: If there are issues reading from or writing to the file system.

    Example:
        json2tsv("data.json", "output.tsv")
    """

    buff: List[List[int | str]] = []
    columns: List[str] = []
    with open(src, "r", encoding="utf-8") as ff:
        data: Dict[str, Any] = json.load(ff)
        # extract all keys
        columns: List[str] = []
        for content in data["contents"]:
            columns.extend(list(content.keys()))
        columns = sorted(list(set(columns)))
        # mapping
        buff: List[List[int | str]] = []
        for content in data["contents"]:
            buff.append([str(content.get(key, "")) for key in columns])
    if not dst:
        dst = src.replace(os.path.splitext(src)[-1], ".tsv")
    with open(dst, "w", encoding="utf-8") as ff:
        ff.write("\t".join(columns) + "\n")
        ff.writelines(["\t".join(l) + "\n" for l in buff])


def _construct_tree(
    tree_: Dict[str, Any], src: List[Dict[str, Any]],
    structure_only: bool = False
) -> Dict[str, Any]:
    """Recursively constructs a tree structure from a list of nodes.

    This function takes a partially constructed tree and a list of source nodes
    as input and recursively builds a complete tree structure.  It handles
    cases where the tree is initially empty or contains only a root node.
    If `structure_only` is False, it all metadata in the resulting tree;
    otherwise, it only returns the '@id' of leaf nodes.

    Args:
        tree_: A dictionary representing a partially constructed tree or an empty dictionary.
        src: A list of dictionaries, where each dictionary represents a node in the tree.
            Each node should have '@id' and 'parent' keys.
        structure_only: A boolean indicating whether to output the structure only.
            in the resulting tree. Defaults to False.

    Returns:
        A dictionary representing the complete tree structure.
            If `include_metadata` is False and the node is a leaf node (type "File"),
            returns only its '@id' as a string.

    """
    if not tree_:
        for node in src:
            if not node["parent"]:
                tree_ = node
                break
    if tree_["type"] == "File":
        if not structure_only:
            return tree_
        return tree_["@id"]
    buff: List[Dict[str, Any]] = []
    for part in tree_["hasPart"]:
        for node in src:
            if node["@id"] == part["@id"] and node["parent"]["@id"] == tree_["@id"]:
                buff.append(
                    _construct_tree(node, src, structure_only)
                )
    tree_["hasPart"] = buff
    return {tree_["@id"]: tree_["hasPart"]}


def list2tree(src: Dict[str, Any], structure_only: bool = False) -> Dict[str, Any]:
    """
    Constructs a hierarchical tree structure from a metadata dictionary.

    This function takes a metadata dictionary (`src`) containing a "contents" key, 
    which holds a list of nodes. Each node is represented as a dictionary with keys
    such as "basename", 
    "parent", "type", and "hasPart". The function uses these nodes to construct a hierarchical tree 
    by calling the helper function `_construct_tree`.

    Args:
        src (Dict[str, Any]): A metadata dictionary with a "contents" key,
            which contains a list of node dictionaries.
        structure_only: A boolean indicating whether to output the structure only.
            in the resulting tree. Defaults to False.

    Returns:
        Dict[str, Any]: A hierarchical tree structure where nodes are nested
            according to their parent-child relationships.

    Example:
        tree = list2tree(metadata_dict)

    Notes:
        - The "contents" key in `src` should be a list of dictionaries,
            each representing a node with its metadata.
        - The function relies on `_construct_tree` to recursively build the tree.

    Raises:
        KeyError: If the "contents" key is missing in the source dictionary.
    """

    contents: List[Dict[str, Any]] = src["contents"]
    tree: Dict[str, Any] = {}
    tree["contents"] = _construct_tree(tree, contents, structure_only)
    return tree


def list2tree_from_file(src: Path | str, structure_only: bool = False) -> Dict[str, Any]:
    """
    Constructs a hierarchical tree structure from a JSON metadata file.

    This function reads a JSON file from the provided path (`src`), 
    loads its content, and passes it to the `list2tree` function to generate 
    a hierarchical tree structure based on the metadata.

    Args:
        src (Path | str): The path to the JSON file containing the metadata. 
                          Can be a `Path` object or a string representing the file path.
        structure_only: A boolean indicating whether to output the structure only.
            in the resulting tree. Defaults to False.

    Returns:
        Dict[str, Any]: A hierarchical tree structure constructed from the JSON metadata.

    Example:
        tree = list2tree_from_file("metadata.json")

    Raises:
        FileNotFoundError: If the specified file does not exist.
        JSONDecodeError: If the file is not a valid JSON.
        OSError: If an error occurs while reading the file.
    """
    with open(src, "r", encoding="utf-8") as ff:
        return list2tree(json.load(ff), structure_only)
