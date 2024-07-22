



set ANACONDA_ANON_USAGE_DEBUG=1
IF %ERRORLEVEL% NEQ 0 exit /B 1
set PYTHONUNBUFFERED=1
IF %ERRORLEVEL% NEQ 0 exit /B 1
conda create -n testchild1 --yes
IF %ERRORLEVEL% NEQ 0 exit /B 1
conda create -n testchild2 --yes
IF %ERRORLEVEL% NEQ 0 exit /B 1
conda info
IF %ERRORLEVEL% NEQ 0 exit /B 1
conda info --envs
IF %ERRORLEVEL% NEQ 0 exit /B 1
pytest -v tests/unit
IF %ERRORLEVEL% NEQ 0 exit /B 1
python tests/integration/test_config.py
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
