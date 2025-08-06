@echo off
cls
echo.
echo ==========================================
echo   JARVIS SYSTEM - COMPLETE FRESH START
echo ==========================================
echo.

echo Step 1: Cleaning all processes...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im chrome.exe >nul 2>&1
echo ✅ Processes cleaned

timeout /t 5 >nul

echo.
echo Step 2: Installing required packages...
pip install selenium webdriver-manager --quiet --upgrade
echo ✅ Packages ready

echo.
echo Step 3: Starting fresh automated system...
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🚀 JARVIS AUTOMATED SYSTEM                               ║
echo ║                         100%% Automated Trading                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo 🎯 WHAT WILL HAPPEN:
echo    ✅ Chrome opens to TradingView automatically
echo    ✅ You login ONCE with your reset password  
echo    ✅ Add your Pine Script to EUR/USD chart
echo    ✅ System reads signals automatically
echo    ✅ Trades executed with 5%% risk automatically
echo    ✅ Monitors 24/7 continuously
echo.
echo 📊 Dashboard: https://jarvis-quant-sys.onrender.com
echo.
echo Press any key to start the automated system...
pause >nul

echo.
echo 🚀 Launching...
python simple_jarvis_reader.py

echo.
echo System finished. Press any key to exit...
pause >nul
