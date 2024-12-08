@echo off
chcp 65001
"%~dp0\src\directory_structure_py.exe" "%~1" --dst "%~dp0output\%~n1\directory_structure_metadata.json" ^
    --in_rocrate ^
    --to_tsv ^
    --in_tree --structure_only ^
    --log_config_path "%~dp0\src\config\logging.json" ^
    --log_output_path "%~dp0\log\app.log" ^
    --preview_template_path "%~dp0\src\templates\preview_template.html.j2"
