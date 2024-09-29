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

    dst["parent"] = path.parent.name
    dst["basename"] = path.name
    if path.is_file():
        dst["name"] = os.path.splitext(path.name)[0]
        dst["extension"] = os.path.splitext(path.name)[1]
    if path.is_dir():
        part: List[str] = [p_.name for p_ in path.iterdir()]
        if part:
            dst["hasPart"] = part
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
    tree_: Dict[str, Any], src: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Recursively constructs a hierarchical tree structure from a flat list of nodes.

    This function takes an existing tree structure (or an empty dictionary) and
    a source list of nodes, 
    each represented as a dictionary with "basename", "parent", and "type" keys,
    and builds a nested tree.
    It looks for nodes that match the "hasPart" attribute of the current tree node,
    attaching child nodes recursively.

    If `tree_` is empty, the function initializes it by searching for the root node, 
    defined as the node where the "parent" key is an empty string.
    The function handles the following cases:
    
    1. If a node has the type "File", it is treated as a leaf node, and recursion terminates.
    2. If a node has children (stored in the "hasPart" key), those children are recursively
    added to the tree.

    Args:
        tree_ (Dict[str, Any]): The current tree or an empty dictionary to initialize the root node.
        src (List[Dict[str, Any]]): A list of nodes, where each node is a dictionary containing
            "basename", "parent", "type", and possibly "hasPart".
    
    Returns:
        Dict[str, Any]: The updated tree structure with all nested nodes attached.

    Example:
        tree = _construct_tree({}, nodes)
    
    Notes:
        - Nodes in `src` should have "basename" and "parent" keys. 
        - Leaf nodes are those with a "type" of "File".
    
    Raises:
        KeyError: If a required key is missing from any node in the source list.
    """
    if not tree_:
        for node in src:
            if node["parent"] == "":
                tree_ = node
                break
    if tree_["type"] == "File":
        return tree_
    buff: List[Dict[str, Any]] = []
    for part in tree_["hasPart"]:
        for node in src:
            if node["basename"] == part and node["parent"] == tree_["basename"]:
                buff.append(
                    _construct_tree(node, src)
                )
    tree_["hasPart"] = buff
    return tree_


def metadata2tree(src: Dict[str, Any]) -> Dict[str, Any]:
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
    
    Returns:
        Dict[str, Any]: A hierarchical tree structure where nodes are nested
            according to their parent-child relationships.
    
    Example:
        tree = metadata2tree(metadata_dict)
    
    Notes:
        - The "contents" key in `src` should be a list of dictionaries,
            each representing a node with its metadata.
        - The function relies on `_construct_tree` to recursively build the tree.
    
    Raises:
        KeyError: If the "contents" key is missing in the source dictionary.
    """

    contents: List[Dict[str, Any]] = src["contents"]
    tree: Dict[str, Any] = {}
    return _construct_tree(tree, contents)


def metadata2tree_from_file(src: Path | str) -> Dict[str, Any]:
    """
    Constructs a hierarchical tree structure from a JSON metadata file.

    This function reads a JSON file from the provided path (`src`), 
    loads its content, and passes it to the `metadata2tree` function to generate 
    a hierarchical tree structure based on the metadata.

    Args:
        src (Path | str): The path to the JSON file containing the metadata. 
                          Can be a `Path` object or a string representing the file path.
    
    Returns:
        Dict[str, Any]: A hierarchical tree structure constructed from the JSON metadata.
    
    Example:
        tree = metadata2tree_from_file("metadata.json")
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
        JSONDecodeError: If the file is not a valid JSON.
        OSError: If an error occurs while reading the file.
    """
    with open(src, "r", encoding="utf-8") as ff:
        return metadata2tree(json.load(ff))


def main(src: Path | str, dst: Path | str, include_root_path: bool, to_tsv: bool = False):
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
    if to_tsv:
        json2tsv(dst)


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
    parser.add_argument(
        "--to_tsv", dest="to_tsv", action="store_true"
    )
    args = parser.parse_args()
    if not args.dst:
        args.dst = os.path.join(args.src, DEFAULT_OUTPUT_NAME)
    main(args.src, args.dst, args.include_root_path, args.to_tsv)
