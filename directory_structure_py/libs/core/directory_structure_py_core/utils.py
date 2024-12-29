"""utils.py
"""

from pathlib import Path
from directory_structure_py_core.base_class import FilePathType


def generate_id(path: FilePathType, root_path: FilePathType = "") -> str:
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
