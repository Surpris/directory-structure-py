@echo off
%~dp0\directory_structure_py.exe %1 --dst %~dp0\output\directory_structure_metadata.json ^
    --in_rocrate ^
    --to_tsv ^
    --in_tree --structure_only ^
    --log_config_path %~dp0\logging.json ^
    --log_output_path %~dp0\log\app.log
