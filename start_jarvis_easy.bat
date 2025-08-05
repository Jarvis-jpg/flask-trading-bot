@echo off
echo 🚀 STARTING JARVIS TRADING SYSTEM
echo =====================================
echo.

:: Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Please run setup first.
    pause
    exit /b 1
)

:: Activate virtual environment
echo 📦 Activating virtual environment...
call venv\Scripts\activate.bat

:: Check if .env file exists
if not exist ".env" (
    echo ❌ Configuration file (.env) not found!
    echo Please check your OANDA settings.
    pause
    exit /b 1
)

:: Display account info
echo.
echo 💰 ACCOUNT INFORMATION:
echo ========================
findstr "ACCOUNT_ID" .env
findstr "LIVE" .env
echo.

:: Display important URLs
echo 🌐 IMPORTANT URLS:
echo ===================
echo Dashboard: http://127.0.0.1:5000
echo Webhook: http://127.0.0.1:5000/webhook
echo.

:: Warning about funding
echo ⚠️  CURRENT BALANCE: $0.95
echo Consider adding funds for meaningful trading
echo.

echo 🎯 Starting JARVIS system...
echo Press Ctrl+C to stop the system
echo.
echo =====================================

:: Start the main application
python app.py

echo.
echo ❌ JARVIS system has stopped
pause
