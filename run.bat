@echo off
title Tise Scraper Service
echo.
echo ========================================
echo    🛍️ TISE SCRAPER SERVICE STARTUP
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "tise_scraper_env" (
    echo ❌ Virtual environment not found!
    echo Please run setup.bat first to install dependencies.
    echo.
    pause
    exit /b 1
)

REM Check if config.py has profiles configured
findstr /C:"https://tise.com/" config.py >nul
if errorlevel 1 (
    echo ⚠️  No profiles configured!
    echo Please edit config.py and add Tise profile URLs to monitor.
    echo Example: "https://tise.com/username"
    echo.
    pause
    exit /b 1
)

echo ✅ Starting Tise scraper in monitoring mode...
echo ⏰ Will check profiles every few minutes
echo 🛑 Press Ctrl+C to stop the service
echo.
echo ========================================
echo.

REM Activate virtual environment and start monitoring
call tise_scraper_env\Scripts\activate.bat
python main.py --auto

echo.
echo ========================================
echo 🛑 Tise scraper service stopped
echo ========================================
pause
