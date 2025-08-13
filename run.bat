@echo off
REM Windows batch script to run DevTerm

echo Starting DevTerm...

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run the application
echo Launching DevTerm...
python main.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo DevTerm exited with an error
    pause
)