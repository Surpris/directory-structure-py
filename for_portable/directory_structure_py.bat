@echo off
%~dp0\directory_structure_py.exe %1 --dst %~dp0\output\directory_structure_metadata.json --in_tree --to_tsv ^
    --log_config_path %~dp0\logging.json ^
    --log_output_path %~dp0\app.log
