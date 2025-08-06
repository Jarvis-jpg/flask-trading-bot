@echo off
echo.
echo ==========================================
echo  JARVIS TRADING SYSTEM STATUS CHECK
echo ==========================================
echo.

echo 1. Testing JARVIS Connection...
python -c "import requests; r=requests.get('https://jarvis-quant-sys.onrender.com/status', timeout=10); print('✅ JARVIS ONLINE:', r.json() if r.status_code==200 else '❌ OFFLINE')" 2>nul || echo ❌ Connection failed

echo.
echo 2. Testing Webhook...
python -c "import requests,json,datetime; r=requests.post('https://jarvis-quant-sys.onrender.com/webhook', json={'test':'ping','timestamp':datetime.datetime.now().isoformat()}, timeout=10); print('✅ Webhook OK:', r.status_code==200)" 2>nul || echo ❌ Webhook failed

echo.
echo 3. Checking Python processes...
tasklist /FI "IMAGENAME eq python.exe" /FO TABLE 2>nul || echo ❌ No Python processes

echo.
echo ==========================================
echo  MANUAL VERIFICATION STEPS:
echo ==========================================
echo.
echo ✅ Step 1: Confirm TradingView is open with Pine Script
echo ✅ Step 2: Run: python manual_tradingview_input.py  
echo ✅ Step 3: Input signals when you see BUY/SELL
echo ✅ Step 4: Check dashboard: https://jarvis-quant-sys.onrender.com
echo.
echo Press any key to continue...
pause >nul
