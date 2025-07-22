@echo off
REM JARVIS Trading System Startup Script for Windows

echo Starting JARVIS AI Trading System...

REM Check if emergency stop flag exists
if exist "EMERGENCY_STOP.flag" (
    echo Emergency stop flag detected! Remove flag file to start.
    pause
    exit /b 1
)

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Virtual environment activated
)

REM Run system validation
echo Running system validation...
python validate_system.py
if %errorlevel% neq 0 (
    echo System validation failed!
    pause
    exit /b 1
)

REM Start health monitor in background
echo Starting health monitor...
start /b python health_monitor.py --continuous 300

REM Start trading system
echo Starting trading system...
python start_trading_bot.py

echo JARVIS Trading System stopped
pause
