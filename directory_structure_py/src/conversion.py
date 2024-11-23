"""conversion
"""

import datetime
import json
from pathlib import Path
from typing import Dict, Any, List
from rocrate.rocrate import ROCrate
from directory_structure_py.src.constants import OUTPUT_ROOT_KEY, DATETIME_FMT


def convert_meta_list_json_to_tsv(src: Dict[str, Any]) -> List[List[str]]:
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
    output: List[str] = []
    with open(src, "r", encoding="utf-8") as ff:
        data: Dict[str, Any] = json.load(ff)
        output = convert_meta_list_json_to_tsv(data)
    return output


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
    if structure_only:
        return {tree_["@id"]: tree_["hasPart"]}
    return {tree_["@id"]: tree_}


def list2tree(src: Dict[str, Any], structure_only: bool = False) -> Dict[str, Any]:
    """
    Constructs a hierarchical tree structure from a metadata dictionary.

    This function takes a metadata dictionary (`src`) containing a OUTPUT_ROOT_KEY key, 
    which holds a list of nodes. Each node is represented as a dictionary with keys
    such as "basename", 
    "parent", "type", and "hasPart". The function uses these nodes to construct a hierarchical tree 
    by calling the helper function `_construct_tree`.

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
    tree: Dict[str, Any] = {}
    tree[OUTPUT_ROOT_KEY] = _construct_tree(tree, contents, structure_only)
    tree["dateCreated"] = src["dateCreated"]
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


def convert_mata_list_json_to_rocrate(
    src: Dict[str, str | int | List[Dict[str, Any]]]
) -> ROCrate:
    crate = ROCrate()
    _ = crate.add_tree(src["root_path"])
    meta_list: List[Dict[str, Any]] = src["@graph"]
    for metadata in meta_list:
        properties = {}
        if metadata["type"] == "Directory":
            for k, v in metadata.items():
                if k in ["@id", "parent", "type"]:
                    continue
                if k == "hasPart":
                    properties[k] = [p_["@id"] for p_ in v]
                elif k == "basename":
                    properties["name"] = v
                else:
                    properties[k] = v
        else:
            for k, v in metadata.items():
                if k in ["@id", "parent", "basename", "type"]:
                    continue
                if k == "extension":
                    properties[k] = v
                else:
                    properties[k] = v
        for k, v in properties.items():
            crate.get(metadata['@id'])[k] = v
    crate.datePublished = datetime.datetime.now().strftime(DATETIME_FMT)
    return crate
