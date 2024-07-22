



pip check
IF %ERRORLEVEL% NEQ 0 exit /B 1
pytest tests/ -vvv --ignore=tests/test_schema.py --ignore=tests/test_elevation.py
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
