"""get_metadata
"""

from collections import Counter
import copy
import datetime
import mimetypes
import os
from pathlib import Path
from typing import Dict, Any, List
import warnings
import hashlib
from directory_structure_py_core.constants import DATETIME_FMT, OUTPUT_ROOT_KEY
from directory_structure_py_core.utils import generate_id


def get_metadata_of_single_file(
    path: Path | str, root_path: Path | str = ""
) -> Dict[str, Any]:
    """Generates metadata for a single file.

    Args:
        path (Path | str): The path to the file.  Can be a Path object or a string.
        root_path (Path | str, optional): The root path to generate relative IDs. Defaults to "".

    Returns:
        Dict[str, Any]: A dictionary containing the file's metadata.  The keys include:
            - `@id`: A unique identifier for the file, relative to `root_path`.
            - `type`: Always "File".
            - `parent`: A dictionary containing the metadata of the parent directory (or an empty dictionary if it's the root).
            - `basename`: The filename including extension.
            - `name`: The filename without extension.
            - `extension`: The file extension (including the leading dot).
            - `mimetype`: The MIME type.
            - `contentSize`: The file size in bytes.
            - `sha256`: The SHA-256 hash value of the file content.
            - `dateCreated`: The creation date and time in ISO 8601 format.
            - `dateModified`: The last modification date and time in ISO 8601 format.

    Raises:
        TypeError: If 'path' is not a file path.
    """
    if isinstance(path, str):
        path = Path(path)
    if not path.is_file():
        raise TypeError(f"{str(path)}: 'path' must be a file path.")

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
    dst["mimetype"] = mimetypes.guess_type(str(path))[0]
    if dst["mimetype"] == "null":
        dst["mimetype"] = "unknown"
    dst["contentSize"] = path.stat().st_size
    with open(path, "rb") as ff:
        dst["sha256"] = hashlib.sha256(ff.read()).hexdigest()
    if os.name == "nt":
        dst["dateCreated"] = datetime.datetime.fromtimestamp(
            path.stat().st_birthtime
        ).strftime(DATETIME_FMT)
    else:
        dst["dateCreated"] = datetime.datetime.fromtimestamp(
            path.stat().st_ctime
        ).strftime(DATETIME_FMT)
    dst["dateModified"] = datetime.datetime.fromtimestamp(
        path.stat().st_mtime
    ).strftime(DATETIME_FMT)

    return dst


def generate_blank_metadata(
    path: Path | str, root_path: Path | str = ""
) -> Dict[str, Any]:
    """Generates a blank metadata for a single path.
    This function is supposed to be used if the type of the path is not specified by the pathlib.

    Args:
        path (Path | str): The path to the file.  Can be a Path object or a string.
        root_path (Path | str, optional): The root path to generate relative IDs. Defaults to "".

    Returns:
        Dict[str, Any]: A dictionary containing the file's metadata.  The keys include:
            - `@id`: A unique identifier for the path, relative to `root_path`.
            - `type`: Always "Unknown".
            - `parent`: A dictionary containing the metadata of the parent directory (or an empty dictionary if it's the root).
            - `basename`: The basename including extension.
            - `name`: The name without extension.
            - `extension`: The extension (including the leading dot).
            - `mimetype`: The MIME type.
            - `contentSize`: The size in bytes.
            - `sha256`: The SHA-256 hash value of the file content.
            - `dateCreated`: The creation date and time in ISO 8601 format.
            - `dateModified`: The last modification date and time in ISO 8601 format.

    """
    if isinstance(path, Path):
        path = str(path)

    dst: Dict[str, Any] = {}
    dst["@id"] = path.replace(os.path.sep, "/")
    dst["type"] = "Unknown"
    parent_id: str = generate_id("/".join(s for s in path.split(os.path.sep)[:-1]), root_path)
    dst["parent"] = {"@id": parent_id}
    dst["basename"] = os.path.basename(path)
    dst["name"] = os.path.splitext(dst["basename"])[0]
    dst["extension"] = os.path.splitext(dst["basename"])[1]
    dst["mimetype"] = "unknown"
    dst["contentSize"] = -1
    dst["sha256"] = ""
    dst["dateCreated"] = "unknown"
    dst["dateModified"] = "unknown"

    return dst


def get_metadata_of_single_directory(
    path: Path | str, root_path: Path | str = ""
) -> Dict[str, Any]:
    """Generates metadata for a single directory.

    Args:
        path (Path | str): The path to the directory. Can be a Path object or a string.
        root_path (Path | str, optional): The root path to generate relative IDs. Defaults to "".

    Returns:
        Dict[str, Any]: A dictionary containing the directory's metadata.  The keys include:
            - `@id`: A unique identifier for the directory, relative to `root_path`.
            - `type`: Always "Directory".
            - `parent`: A dictionary containing the metadata of the parent directory (or an empty dictionary if it's the root).
            - `basename`: The directory name.
            - `name`: The directory name.
            - `hasPart`: A list of dictionaries, each containing the `@id` of a child item (file or subdirectory).
            - `contentSize`: The total size of files within the directory in bytes.
            - `numberOfContents`: The total number of child items (files and subdirectories).
            - `numberOfFiles`: The number of files within the directory.
            - `numberOfFilesPerExtension`: A dictionary mapping file extensions to their counts.
            - `extension`: A list of file extensions found in the directory.
            - `mimetype`: A list of file MIME types found in the directory. The MIME type.
            - `contentSizeOfAllFiles`: The total size of files within the directory and all its descendant directories in bytes.
            - `numberOfAllContents`: The total number of child items (files and subdirectories) within the directory and all its descendant directories.
            - `numberOfAllFiles`: The total number of files within the directory and all its descendant directories.
            - `numberOfAllFilesPerExtension`: A dictionary mapping file extensions found in the directory and all its descendant directories to their counts.
            - `extensionsOfAllFiles`: A list of file extensions found in the directory and all its descendant directories.
            - `dateCreated`: The creation date and time in ISO 8601 format.
            - `dateModified`: The last modification date and time in ISO 8601 format.

    Raises:
        TypeError: If 'path' is not a directory path.
    """
    if isinstance(path, str):
        path = Path(path)
    if not path.is_dir():
        raise TypeError(f"{str(path)}: 'path' must be a directory path.")

    dst: Dict[str, Any] = {}
    dst["@id"] = generate_id(path, root_path)
    dst["type"] = "Directory"
    if str(path) == str(root_path):
        dst["parent"] = {}
    else:
        dst["parent"] = {"@id": generate_id(path.parent, root_path)}
    dst["basename"] = path.name
    dst["name"] = path.name
    dst["hasPart"] = [
        {"@id": generate_id(p_, root_path)}
        for p_ in path.iterdir()
    ]

    # children only
    dst["contentSize"] = sum(
        p_.stat().st_size for p_ in path.iterdir() if p_.is_file()
    )
    dst["numberOfContents"] = len(dst["hasPart"])
    dst["numberOfFiles"] = len([
        p_ for p_ in path.iterdir() if p_.is_file()
    ])
    dst["numberOfFilesPerExtension"] = dict(Counter(
        os.path.splitext(p_.name)[1] for p_ in path.iterdir()
        if p_.is_file()
    ))
    dst["extension"] = list(dst["numberOfFilesPerExtension"].keys())
    dst["numberOfFilesPerMIMEType"] = dict(Counter(
        mimetypes.guess_type(str(p_))[0] for p_ in path.iterdir()
        if p_.is_file()
    ))
    for key, value in dst["numberOfFilesPerMIMEType"].items():
        if value == "null":
            dst[key] = "unknown"
    dst["mimetype"] = list(dst["numberOfFilesPerMIMEType"].keys())

    # all contents
    dst["contentSizeOfAllFiles"] = sum(
        p_.stat().st_size for p_ in path.iterdir() if p_.is_file()
    )
    dst["numberOfAllContents"] = len(dst["hasPart"])
    dst["numberOfAllFiles"] = len([
        p_ for p_ in path.iterdir() if p_.is_file()
    ])
    dst["numberOfAllFilesPerExtension"] = copy.deepcopy(
        dst["numberOfFilesPerExtension"]
    )
    dst["extensionsOfAllFiles"] = list(
        dst["numberOfAllFilesPerExtension"].keys()
    )
    dst["numberOfAllFilesPerMIMEType"] = copy.deepcopy(
        dst["numberOfFilesPerMIMEType"]
    )
    dst["mimetypesOfAllFiles"] = list(
        dst["numberOfAllFilesPerMIMEType"].keys()
    )

    if os.name == "nt":
        dst["dateCreated"] = datetime.datetime.fromtimestamp(
            path.stat().st_birthtime
        ).strftime(DATETIME_FMT)
    else:
        dst["dateCreated"] = datetime.datetime.fromtimestamp(
            path.stat().st_ctime
        ).strftime(DATETIME_FMT)
    dst["dateModified"] = datetime.datetime.fromtimestamp(
        path.stat().st_mtime
    ).strftime(DATETIME_FMT)

    return dst


def _get_metadata_list(src: Path, root_path: Path | str = "") -> List[Dict[str, Any]]:
    """Recursively generates a list of metadata dictionaries for a given path.

    This function traverses a directory tree, creating metadata for each file and directory encountered.

    Args:
        src (Path): The path to the file or directory to process.
        root_path (Path | str, optional): The root path for relative ID generation. Defaults to "".

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary contains the metadata of a single file or directory.  The structure of each dictionary is defined by `get_metadata_of_single_file` and `get_metadata_of_single_directory`.

    """
    dst: List[Dict[str, Any]] = []
    if src.is_file():
        dst.append(
            get_metadata_of_single_file(src, root_path=root_path)
        )
        return dst
    if not src.is_dir():
        dst.append(
            generate_blank_metadata(src, root_path=root_path)
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
    """Generates metadata for all files and directories within a given path in a list format.

    This function recursively traverses the directory tree starting at the given source path, 
    creating metadata for each file and directory encountered. The metadata is organized in a list.

    Args:
        src (Path | str): The path to the directory or file to process.  Can be a Path object or a string.
        include_root_path (bool, optional): Whether to include the absolute path of the source directory in the output. Defaults to False.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - `"root_path"`: The root path used for relative ID generation (either the absolute path of `src` or "./").
            - `${OUTPUT_ROOT_KEY}`: (Where `OUTPUT_ROOT_KEY` is a constant defined elsewhere) A list of dictionaries, each containing the metadata of a single file or directory.
            - `"dateCreated"`: The date and time the metadata was generated in ISO 8601 format.

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
    """Recursively updates the statistical information of a directory metadata.

    This function updates the statistical information (e.g., `contentSizeOfAllFiles`, `numberOfAllFiles`, etc.) of a directory by recursively traversing its subdirectories and aggregating the statistics of its children.

    Args:
        src (Dict[str, Any]): A dictionary representing the metadata of a directory.  Must contain "type" and "hasPart" keys.
        metadata_list (List[Dict]): A list of metadata dictionaries for all files and directories.  Used to find the children of the directory.

    Returns:
        Dict[str, Any]: The updated directory metadata with aggregated statistical information.

    Warnings:
        If the input `src` is not a directory or if a node in `metadata_list` lacks a "type" property, a warning is issued.
    """
    if src.get("type", "Unknown") != "Directory":
        warnings.warn("'src' must be a Directory metadata. exit.")
        return src
    metadata_list_: List[Dict] = [
        m for m in metadata_list if m.get("type", "Unknown") == "Directory"
    ]
    src_id: str = src["@id"]
    for part in src.get("hasPart", []):
        part_id: str = part["@id"]
        node_list: List[Dict] = [
            node for node in metadata_list_
            if node["@id"] == part_id and node["parent"]["@id"] == src_id
        ]
        for node in node_list:
            node = _update_statistical_info_of_directory(
                node, metadata_list_
            )
            src["contentSizeOfAllFiles"] += node["contentSizeOfAllFiles"]
            src["numberOfAllContents"] += node["numberOfAllContents"]
            src["numberOfAllFiles"] += node["numberOfAllFiles"]
            src["numberOfAllFilesPerExtension"] = dict(
                Counter(src["numberOfAllFilesPerExtension"]) +
                Counter(node["numberOfAllFilesPerExtension"])
            )
            src["extensionsOfAllFiles"] = list(
                src["numberOfAllFilesPerExtension"].keys()
            )
            src["numberOfAllFilesPerMIMEType"] = dict(
                Counter(src["numberOfAllFilesPerMIMEType"]) +
                Counter(node["numberOfAllFilesPerMIMEType"])
            )
            src["mimetypesOfAllFiles"] = list(
                src["numberOfAllFilesPerMIMEType"].keys()
            )
    return src


def update_statistical_info_to_metadata_list(src: Dict[str, Any]) -> Dict[str, Any]:
    """Updates the statistical information in a metadata list.

    This function iterates through a list of file and directory metadata, 
    aggregating statistical information (size, file counts, etc.) for directories.
    It identifies the root directory and recursively updates its statistics based on its children.

    Args:
        src (Dict[str, Any]): A dictionary containing a list of metadata under the key specified by `OUTPUT_ROOT_KEY`.

    Returns:
        Dict[str, Any]: The input dictionary with updated statistical information for directories.  Returns the original dictionary if no root directory is found.

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
    _ = _update_statistical_info_of_directory(root, contents)
    return src
