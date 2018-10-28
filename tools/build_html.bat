@echo off

set SRC_DIR=D:\work\pvzscripts

pythonw %SRC_DIR%\tools\md2html.py %SRC_DIR%\markdown\anjian.md %SRC_DIR%\html\anjian.html
pythonw %SRC_DIR%\tools\md2html.py %SRC_DIR%\markdown\python.md %SRC_DIR%\html\python.html
