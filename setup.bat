@echo off
echo Installing Tise Scraper dependencies...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Install required packages
echo Installing Python packages...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install some packages
    echo Try running: pip install --upgrade pip
    pause
    exit /b 1
)

REM Create necessary directories
echo Creating directories...
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "data\downloads" mkdir data\downloads

echo.
echo ✓ Installation completed successfully!
echo.
echo Next steps:
echo 1. Edit config.py to add your Tise profile URLs
echo 2. Run: python main.py
echo.
pause
