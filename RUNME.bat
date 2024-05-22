@echo off
:: Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python 3.x from https://www.python.org/downloads/
    pause
    exit /b
)

:: Navigate to the script directory
cd %~dp0

:: Run the main Python script
python -m main

:: Pause to keep the command prompt open
pause
