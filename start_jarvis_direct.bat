@echo off
echo.
echo ==========================================
echo  JARVIS AUTOMATED SYSTEM - DIRECT START
echo ==========================================
echo.

echo Stopping any existing processes...
taskkill /f /im chrome.exe /t >nul 2>&1
taskkill /f /im python.exe /fi "WINDOWTITLE eq *jarvis*" >nul 2>&1
timeout /t 3 >nul

echo.
echo Starting JARVIS Automated Pine Script Reader...
echo.
echo WHAT WILL HAPPEN:
echo 1. Chrome opens to TradingView
echo 2. Login with your RESET password
echo 3. Add Pine Script to EUR/USD chart  
echo 4. System reads signals automatically
echo 5. Trades executed automatically (5%% risk)
echo.
echo Press any key to start...
pause >nul

echo.
echo Launching automated system...
start "JARVIS Automated Reader" python jarvis_pine_script_reader.py

echo.
echo ✅ JARVIS Automated System Started!
echo.
echo 📊 Dashboard: https://jarvis-quant-sys.onrender.com
echo 🔄 System will monitor and trade automatically
echo 💰 Risk per trade: 5%%
echo.
echo Keep this window open to monitor status...
echo Press any key to close launcher...
pause >nul
