#!/bin/bash

# Get the filename and extension from the argument
FILENAME=$(basename "$1")
DIRNAME="${FILENAME}"

# Get the current directory
SCRIPT_DIR=$(dirname "$0")
SCRIPT_DIR=$(cd "$SCRIPT_DIR" && pwd)

# Path to the executable file
EXE_PATH="$SCRIPT_DIR/src/directory_structure_py"
# Path to the output directory
OUTPUT_DIR="$SCRIPT_DIR/output/$DIRNAME"
# Path to the log directory
LOG_DIR="$SCRIPT_DIR/log"
# Path to the configuration file
CONFIG_PATH="$SCRIPT_DIR/src/config/logging.json"
# Path to the preview template file
TEMPLATE_PATH="$SCRIPT_DIR/src/templates/preview_template.html.j2"

# Create the directories
mkdir -p "$OUTPUT_DIR"
mkdir -p "$LOG_DIR"

# Execute the command
"$EXE_PATH" "$1" --dst "$OUTPUT_DIR/directory_structure_metadata.json" \
    --in_rocrate \
    --to_tsv \
    --in_tree --structure_only \
    --log_config_path "$CONFIG_PATH" \
    --log_output_path "$LOG_DIR/app.log" \
    --preview_template_path "$TEMPLATE_PATH"
