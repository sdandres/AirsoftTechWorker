@echo off
REM === SETUP ENVIRONMENT ===
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install pyodbc
pip install tk

echo Setup complete.
pause