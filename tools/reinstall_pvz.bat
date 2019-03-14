@echo off

pip uninstall pvz -y

set SRC_DIR=%~dp0..
set PY_DIR=C:\Python37

%~d0
cd %SRC_DIR%\src\

REM test
rd /q /s %PY_DIR%\Lib\site-packages\pvz
del %PY_DIR%\Lib\site-packages\pvz*
python setup.py install
rd /q /s %SRC_DIR%\src\build\
rd /q /s %SRC_DIR%\src\dist\
rd /q /s %SRC_DIR%\src\pvz.egg-info\
del %SRC_DIR%\src\MANIFEST

REM REM publish
REM python setup.py check
REM python setup.py sdist
REM twine upload dist/*

cd %SRC_DIR%\tools\
