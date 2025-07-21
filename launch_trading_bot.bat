@echo off
echo ========================================================
echo  JARVIS AUTONOMOUS TRADING BOT - WINDOWS LAUNCHER
echo ========================================================
echo.

REM Check if Python virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo ERROR: Python virtual environment not found!
    echo Please run setup first or activate your Python environment.
    pause
    exit /b 1
)

echo [1/4] Activating Python environment...
call venv\Scripts\activate.bat

echo [2/4] Running system validation...
venv\Scripts\python.exe validate_system.py
if errorlevel 1 (
    echo.
    echo ERROR: System validation failed!
    echo Please check the validation report and fix any issues.
    pause
    exit /b 1
)

echo.
echo [3/4] System validation passed! 
echo [4/4] Starting Jarvis Trading Bot...
echo.
echo =========================================================
echo  JARVIS TRADING BOT IS STARTING
echo =========================================================
echo  Dashboard will be available at: http://localhost:5000
echo  Press Ctrl+C to stop the bot
echo =========================================================
echo.

REM Start the trading bot
venv\Scripts\python.exe start_trading_bot.py

echo.
echo =========================================================
echo  JARVIS TRADING BOT HAS STOPPED
echo =========================================================
pause
