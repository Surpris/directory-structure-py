"""converter.py
"""

import datetime
from pathlib import Path
from typing import Dict, List, Any
from rocrate.rocrate import ROCrate
from directory_structure_py_core.constants import DATETIME_FMT


def convert_meta_list_json_to_rocrate(
    src: Dict[str, str | int | List[Dict[str, Any]]]
) -> ROCrate:
    """Converts a metadata list JSON structure into a Research Object Crate (ROCrate).

    This function takes a dictionary representing a metadata list in JSON format and creates a ROCrate object.
    It iterates through the metadata list, extracting relevant properties for each item (files and directories).
    Directories are handled differently than files; specific keys are ignored or renamed ("basename" becomes "name").
    The resulting ROCrate includes a datePublished property reflecting the current time.

    Args:
        src: A dictionary containing the metadata list.  Must contain "@graph" key with a list of dictionaries, and a "root_path" key specifying the root path.  Each dictionary in '@graph' represents a file or directory metadata.

    Returns:
        A ROCrate object populated with the metadata from the input dictionary.  Returns an empty ROCrate if input is invalid.

    Raises:
        KeyError: If the input dictionary does not contain the required keys ("@graph", "root_path").
        TypeError: If the input data is not in the expected format.

    """
    def _get_dictionary_props(meta_: Dict[str, Any]) -> Dict[str, Any]:
        properties = {}
        for k, v in meta_.items():
            if k in ["@id", "parent", "type"]:
                continue
            if k == "hasPart":
                properties[k] = [p_["@id"] for p_ in v]
            elif k == "basename":
                properties["name"] = v
            elif k == "mimetype":
                properties["encodingFormat"] = v
            elif isinstance(v, (int, float)):
                properties[k] = str(v)
            elif isinstance(v, dict) and "@id" not in list(v.keys()):
                properties[k] = str(v)
            else:
                properties[k] = v
        return properties

    def _get_file_props(meta_: Dict[str, Any]) -> Dict[str, Any]:
        properties = {}
        for k, v in meta_.items():
            if k in ["@id", "parent", "basename", "type"]:
                continue
            if k == "extension":
                properties[k] = v
            elif k == "mimetype":
                properties["encodingFormat"] = v
            elif isinstance(v, (int, float)):
                properties[k] = str(v)
            elif isinstance(v, dict) and "@id" not in list(v.keys()):
                properties[k] = str(v)
            else:
                properties[k] = v
        return properties

    crate = ROCrate(gen_preview=False)
    if Path(src["root_path"]).is_dir():
        _ = crate.add_tree(src["root_path"])
    else:
        _ = crate.add_file(src["root_path"])
    crate.name = Path(src["root_path"]).name
    meta_list: List[Dict[str, Any]] = src["@graph"]
    for metadata in meta_list:
        entity: Dict = crate.get(metadata['@id'])
        properties = {}
        if metadata["type"] == "Directory":
            properties = _get_dictionary_props(metadata)
        else:
            properties = _get_file_props(metadata)
        for k, v in properties.items():
            entity[k] = v
    crate.datePublished = src.get(
        "dateCreated", datetime.datetime.now().strftime(DATETIME_FMT)
    )
    return crate
