"""generate_sample_outputs.py

generate sample outputs
"""

import os
from directory_structure_py.constants import DEFAULT_OUTPUT_NAME
from directory_structure_py.main import main

SRC_DIR_PATH: str = os.path.join(os.path.dirname(__file__), "../sample")
DST_DIR_PATH: str = os.path.join(
    os.path.dirname(__file__), f"../output/sample/{DEFAULT_OUTPUT_NAME}"
)

if __name__ == "__main__":
    main(
        SRC_DIR_PATH, DST_DIR_PATH, False,
        in_rocrate=True,
        to_tsv=True,
        in_tree=True,
        structure_only=False
    )
