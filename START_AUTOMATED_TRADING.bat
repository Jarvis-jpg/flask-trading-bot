@echo off
echo 🚀 STARTING FULLY AUTOMATED SEVENSYS TRADING SYSTEM
echo =====================================================
echo ✅ 100%% Automated - Watches news headlines automatically
echo ✅ Applies news data to strategy automatically  
echo ✅ Executes trades automatically
echo ✅ NO MANUAL INTERVENTION REQUIRED
echo.

cd /d "C:\Users\Smith_Family7\flask-trading-bot"

echo 🔧 Activating Python environment...
call .venv\Scripts\activate.bat

echo 📰 Starting news-integrated automated trader...
python fully_automated_sevensys.py

echo.
echo 🛑 Automated trading stopped
pause
