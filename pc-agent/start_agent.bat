@echo off
echo ==========================================
echo KOPU PC Activity Monitoring Agent
echo ==========================================
echo Starting agent in background...
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Install requirements if needed
if not exist "requirements_installed.txt" (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install requirements
        pause
        exit /b 1
    )
    echo Requirements installed > requirements_installed.txt
)

REM Start the agent
echo Starting PC Activity Monitoring Agent...
echo Press Ctrl+C to stop
echo.
python main.py

pause
