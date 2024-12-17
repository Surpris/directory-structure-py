"""directory_structure_py

get the directory tree
"""

import copy
import datetime
import importlib.resources
import json
from logging import getLogger, config, Logger
import os
from pathlib import Path
import time
import traceback
from typing import Dict, Any, List
from rocrate.rocrate import ROCrate

from directory_structure_py.constants import (
    DEFAULT_OUTPUT_NAME, ENSURE_ASCII, JSON_OUTPUT_INDENT,
    DEFAULT_PREVIEW_TEMPLATE_PATH
)
from directory_structure_py.get_metadata import (
    get_metadata_of_files_in_list_format,
    update_statistical_info_to_metadata_list
)
from directory_structure_py.conversion import (
    list2tree,
    convert_meta_list_json_to_tsv,
    convert_meta_list_json_to_rocrate
)
from directory_structure_py.rocrate_models import Preview, Metadata

LOG_CONF_PATH: str = importlib.resources.files(
    __package__
).joinpath("config/logging.json")
LOG_OUTPUT_PATH: str = os.path.join(
    os.path.dirname(__file__),
    f"log/directory_structure_py_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.log"
)


def set_logger(config_path: str, output_log_path: str) -> Logger:
    """Set a logger"""
    with open(config_path, "r", encoding="utf-8") as ff:
        log_conf = json.load(ff)
        log_conf["handlers"]["fileHandler"]["filename"] = output_log_path
        config.dictConfig(log_conf)

    logger = getLogger("main")
    return logger


def save_dict_to_json(data: Dict[str, Any], dst: str) -> None:
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


def save_nested_list_to_tsv(data: List[List[str]], dst: str) -> None:
    with open(dst, "w", encoding="utf-8") as ff:
        ff.writelines(["\t".join(l) + "\n" for l in data])


def main(
    src: Path | str, dst: Path | str,
    include_root_path: bool,
    in_rocrate: bool = False,
    to_tsv: bool = False,
    in_tree: bool = False,
    structure_only: bool = False,
    log_config_path: str = LOG_CONF_PATH,
    log_output_path: str = LOG_OUTPUT_PATH,
    preview_template_path: str = None
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
    try:
        src = os.path.abspath(src)
        if os.name == "nt" and not str(src).startswith(r"//?/"):
            src = Path(r"//?/" + src)
        logger.info("extract the metadata...")
        data: Dict[str, Any] = get_metadata_of_files_in_list_format(
            src, include_root_path
        )
        data = update_statistical_info_to_metadata_list(data)
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))

        logger.info("save the metadata in a list format...")
        save_dict_to_json(data, dst)

        if in_rocrate:
            logger.info("convert the metadata format from list to the RO-Crate... ")
            root_path_original: str = copy.deepcopy(data["root_path"])
            data["root_path"] = f"{str(Path(src).absolute().as_posix())}"
            crate: ROCrate = convert_meta_list_json_to_rocrate(data)
            data["root_path"] = root_path_original
            _ = crate.add(Preview(crate))
            # crate.write_zip(os.path.dirname(dst))
            # crate.write(os.path.dirname(dst))
            crate.metadata.write(os.path.dirname(dst))
            logger.info("save the metadata in the RO-Crate format... ")
            rocrate_metadata: Metadata = Metadata(crate)
            rocrate_metadata.write(os.path.dirname(dst))
            logger.info("save the preview for the RO-Crate-format metadata... ")
            crate.preview.write(os.path.dirname(dst), preview_template_path)

        if to_tsv:
            logger.info("save the metadata in a TSV format...")
            data_tsv = convert_meta_list_json_to_tsv(data)
            dst_tsv: str = dst.replace(
                os.path.splitext(dst)[-1], ".tsv"
            )
            save_nested_list_to_tsv(data_tsv, dst_tsv)

        if in_tree:
            if structure_only:
                logger.info("extract the directory structure...")
            else:
                logger.info("convert the metadata format from list to tree...")
            data = list2tree(copy.deepcopy(data), structure_only)
            dst_tree: str = dst.replace(
                os.path.splitext(dst)[-1],
                f"_tree{os.path.splitext(dst)[-1]}"
            )
            if structure_only:
                logger.info("save the directory structure...")
            else:
                logger.info("save the metadata in a tree format...")
            save_dict_to_json(data, dst_tree)
    except Exception:
        traceback.print_exc()
        logger.error(traceback.format_exc())
    logger.info("ended.")
    logger.info("elapsed time: %.*f sec.\n", 3, time.time() - st)


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
    parser.add_argument(
        "--preview_template_path", dest="preview_template_path", type=str,
        default=DEFAULT_PREVIEW_TEMPLATE_PATH
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
        args.log_config_path, args.log_output_path,
        args.preview_template_path
    )
