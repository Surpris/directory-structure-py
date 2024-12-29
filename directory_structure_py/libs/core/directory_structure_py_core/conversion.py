"""conversion
"""

import json
from pathlib import Path
from typing import Dict, Any, List
import warnings
from directory_structure_py_core.constants import OUTPUT_ROOT_KEY


def convert_meta_list_json_to_tsv(src: Dict[str, Any]) -> List[List[str]]:
    """Converts a list of dictionaries (JSON-like structure) into a TSV-compatible list of lists.

    This function takes a dictionary where one key (specified by OUTPUT_ROOT_KEY) contains a list of dictionaries.  
    Each inner dictionary represents a row.  The function extracts all unique keys across all inner dictionaries 
    to form the column headers.  It then creates a list of lists, where each inner list represents a row, 
    with values corresponding to the column headers.  Missing values are represented as empty strings.

    Args:
        src: A dictionary containing a list of dictionaries under the key OUTPUT_ROOT_KEY.  
             The inner dictionaries represent rows of data, and their keys represent columns.

    Returns:
        A list of lists representing the data in TSV format. The first list contains the column headers.
        Each subsequent list represents a row, with values as strings.  Returns an empty list if input is invalid.

    Raises:
        KeyError: if OUTPUT_ROOT_KEY is not found in the input dictionary `src` or if any inner dictionary is not properly formed.

    """
    buff: List[List[int | str]] = []
    columns: List[str] = []

    # extract all keys
    columns: List[str] = []
    for content in src[OUTPUT_ROOT_KEY]:
        columns.extend(list(content.keys()))
    columns = sorted(list(set(columns)))

    # mapping
    buff: List[List[int | str]] = []
    for content in src[OUTPUT_ROOT_KEY]:
        buff.append([
            str(content.get(key, "")) for key in columns
        ])
    dst: List[str] = [columns]
    dst.extend(buff)
    return dst


def convert_meta_list_json_to_tsv_from_file(src: str) -> List[List[str]]:
    """Converts a JSON file containing a list of dictionaries into a TSV-compatible list of lists.

    This function reads a JSON file from the specified path, parses it, and then uses 
    `convert_meta_list_json_to_tsv` to convert the JSON data into a TSV-compatible format.

    Args:
        src: The path to the JSON file.

    Returns:
        A list of lists representing the data in TSV format. The first list contains the column headers.
        Each subsequent list represents a row, with values as strings. Returns an empty list if there's an error 
        reading the file or if the JSON is invalid or doesn't match the expected structure.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    output: List[str] = []
    with open(src, "r", encoding="utf-8") as ff:
        data: Dict[str, Any] = json.load(ff)
        output = convert_meta_list_json_to_tsv(data)
    return output


def _construct_tree_from_list(
    src: Dict[str, Any], metadata_list: List[Dict[str, Any]],
    structure_only: bool = False
) -> Dict[str, Any]:
    """Recursively constructs a tree structure from a list of nodes.

    This function takes a partially constructed tree and a list of source nodes
    as input and recursively builds a complete tree structure.  It handles
    cases where the tree is initially empty or contains only a root node.
    If `structure_only` is False, it all metadata in the resulting tree;
    otherwise, it only returns the '@id' of leaf nodes.

    Args:
        src: A dictionary representing a partially constructed tree or an empty dictionary.
        metadata_list: A list of dictionaries, where each dictionary represents a node in the tree.
            Each node should have '@id' and 'parent' keys.
        structure_only: A boolean indicating whether to output the structure only.
            in the resulting tree. Defaults to False.

    Returns:
        A dictionary representing the complete tree structure.
            If `include_metadata` is False and the node is a leaf node (type "File"),
            returns only its '@id' as a string.

    """
    if src.get("type", "Unknown") != "Directory":
        if not structure_only:
            return src
        return src.get("@id", "no id")
    buff: List[Dict[str, Any]] = []
    src_id: str = src["@id"]
    for part in src.get("hasPart", []):
        part_id: str = part["@id"]
        node_list: List[Dict] = [
            node for node in metadata_list
            if node["@id"] == part_id and node["parent"]["@id"] == src_id
        ]
        for node in node_list:
            buff.append(
                _construct_tree_from_list(node, metadata_list, structure_only)
            )
    src["hasPart"] = buff
    if structure_only:
        return {src["@id"]: src["hasPart"]}
    return {src["@id"]: src}


def list2tree(src: Dict[str, Any], structure_only: bool = False) -> Dict[str, Any]:
    """
    Constructs a hierarchical tree structure from a metadata dictionary.

    This function takes a metadata dictionary (`src`) containing a OUTPUT_ROOT_KEY key, 
    which holds a list of nodes. Each node is represented as a dictionary with keys
    such as "basename", 
    "parent", "type", and "hasPart". The function uses these nodes to construct a hierarchical tree 
    by calling the helper function `_construct_tree_from_list`.

    Args:
        src (Dict[str, Any]): A metadata dictionary with a OUTPUT_ROOT_KEY key,
            which contains a list of node dictionaries.
        structure_only: A boolean indicating whether to output the structure only.
            in the resulting tree. Defaults to False.

    Returns:
        Dict[str, Any]: A hierarchical tree structure where nodes are nested
            according to their parent-child relationships.

    Example:
        tree = list2tree(metadata_dict)

    Notes:
        - The OUTPUT_ROOT_KEY key in `src` should be a list of dictionaries,
            each representing a node with its metadata.
        - The function relies on `_construct_tree` to recursively build the tree.

    Raises:
        KeyError: If the OUTPUT_ROOT_KEY key is missing in the source dictionary.
    """

    contents: List[Dict[str, Any]] = src[OUTPUT_ROOT_KEY]
    root: Dict[str, Any] = {}
    for node in contents:
        node_parent: Dict[str, Any] = node.get("parent", {})
        if not node_parent:
            root = node
            break
    if not root:
        warnings.warn("No root metadata found. exit.")
        return src
    root = _construct_tree_from_list(root, contents, structure_only)
    dst: Dict[str, Any] = {}
    dst["root_path"] = src["root_path"]
    dst[OUTPUT_ROOT_KEY] = root
    dst["dateCreated"] = src["dateCreated"]
    return dst


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
