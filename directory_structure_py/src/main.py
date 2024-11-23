"""directory_structure_py

get the directory tree
"""

import datetime
import json
from logging import getLogger, config, Logger
import os
from pathlib import Path
import time
from typing import Dict, Any
from directory_structure_py.src.constants import (
    DEFAULT_OUTPUT_NAME, ENSURE_ASCII, JSON_OUTPUT_INDENT
)
from directory_structure_py.src.get_metadata import (
    get_metadata_of_files_in_list_format,
)
from directory_structure_py.src.conversion import (
    list2tree,
    convert_meta_list_json_to_tsv,
    convert_mata_list_json_to_rocrate
)
from rocrate.rocrate import ROCrate

LOG_CONF_PATH: str = os.path.join(
    os.path.dirname(__file__), "../config/logging.json"
)
LOG_OUTPUT_PATH: str = os.path.join(
    os.path.dirname(__file__),
    f"../log/directory_structure_py_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.log"
)


def set_logger(config_path: str, output_log_path: str) -> Logger:
    """Set a logger"""
    with open(config_path, "r", encoding="utf-8") as ff:
        log_conf = json.load(ff)
        log_conf["handlers"]["fileHandler"]["filename"] = output_log_path
        config.dictConfig(log_conf)

    logger = getLogger("main")
    return logger


def save(data: Dict[str, Any], dst: str) -> None:
    """Saves a dictionary to a JSON file.

    Args:
        data: The dictionary to be saved.
        dst: The path to the output JSON file.
            The file will be overwritten if it already exists.
    """
    with open(dst, "w", encoding="utf-8") as ff:
        json.dump(
            data, ff,
            indent=JSON_OUTPUT_INDENT,
            ensure_ascii=ENSURE_ASCII
        )


def main(
    src: Path | str, dst: Path | str,
    include_root_path: bool,
    in_rocrate: bool = False,
    to_tsv: bool = False,
    in_tree: bool = False,
    structure_only: bool = False,
    log_config_path: str = LOG_CONF_PATH,
    log_output_path: str = LOG_OUTPUT_PATH
):
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
        structure_only: A boolean indicating whether to output the structure only.
            in the resulting tree. Defaults to False.
        in_tree (bool): If `True`, output the metadata in a tree format.
        to_tsv (bool): If `True`, output the metadata a TSV format as well as a JSON one.

    Returns:
        None: The function writes the metadata to a file and does not return anything.
    """
    st = time.time()
    if not os.path.exists(os.path.dirname(log_output_path)):
        os.makedirs(os.path.dirname(log_output_path))
    logger: Logger = set_logger(log_config_path, log_output_path)
    logger.info("starts.")
    logger.info("source path: '%s'.", str(src))
    data: Dict[str, Any] = get_metadata_of_files_in_list_format(
        src, include_root_path
    )
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))
    if not in_rocrate:
        save(data, dst)
    else:
        data["root_path"] = f"{str(Path(src).absolute().as_posix())}"
        crate: ROCrate = convert_mata_list_json_to_rocrate(data)
        crate.metadata.write(os.path.dirname(dst))
        if os.path.exists(dst):
            os.remove(dst)
        os.rename(
            os.path.join(os.path.dirname(dst), crate.metadata.BASENAME),
            dst
        )
    if to_tsv:
        logger.info("generate a TSV-format file.")
        convert_meta_list_json_to_tsv(dst)
    if in_tree:
        logger.info("convert the metadata format from list to tree.")
        data = list2tree(data, structure_only)
        dst_tree: str = dst.replace(
            os.path.splitext(dst)[-1],
            f"_tree{os.path.splitext(dst)[-1]}"
        )
        with open(dst_tree, "w", encoding="utf-8") as ff:
            json.dump(
                data, ff,
                indent=JSON_OUTPUT_INDENT,
                ensure_ascii=ENSURE_ASCII
            )
    logger.info("ended.")
    logger.info("elapsed time: %.*f sec.", 3, time.time() - st)


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
        "--in_rocrate", dest="in_rocrate", action="store_true"
    )
    parser.add_argument(
        "--to_tsv", dest="to_tsv", action="store_true"
    )
    parser.add_argument(
        "--in_tree", dest="in_tree", action="store_true"
    )
    parser.add_argument(
        "--structure_only", dest="structure_only", action="store_true"
    )
    parser.add_argument(
        "--log_config_path", dest="log_config_path", type=str, default=LOG_CONF_PATH
    )
    parser.add_argument(
        "--log_output_path", dest="log_output_path", type=str, default=LOG_OUTPUT_PATH
    )
    args = parser.parse_args()
    if not args.dst:
        if os.path.isdir(args.src):
            args.dst = os.path.join(args.src, DEFAULT_OUTPUT_NAME)
        else:
            args.dst = os.path.join(
                os.path.dirname(args.src), DEFAULT_OUTPUT_NAME
            )
    elif os.path.isdir(args.dst):
        args.dst = os.path.join(args.dst, DEFAULT_OUTPUT_NAME)
    main(
        args.src, args.dst, args.include_root_path,
        args.in_rocrate, args.to_tsv,
        args.in_tree, args.structure_only,
        args.log_config_path, args.log_output_path
    )
