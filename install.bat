@echo off
echo Sourcing from: %~dp0
echo Installing Python 3.11.5
"%~dp0\python-3.11.5-amd64.exe" /passive
echo upgrading pip
%LocalAppData%\Programs\Python\Python311\python.exe -m pip install --upgrade pip
echo Adding package requirements
%LocalAppData%\Programs\Python\Python311\Scripts\pip.exe install -r "%~dp0\requirements.txt"
