@echo off
echo Sourcing from: %~dp0
C:
cd %USERPROFILE%
if not exist BatMenu mkdir BatMenu
cd BatMenu
echo creating virtual environment
python -m venv venv
echo activating virtual environment
call venv\scripts\activate
echo upgrading pip
venv\scripts\python.exe -m pip install --upgrade pip
echo Adding package requirements
venv\scripts\pip.exe install -r "%~dp0\requirements.txt"
deactivate
