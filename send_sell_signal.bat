@echo off
echo 📉 SENDING SELL SIGNAL TO JARVIS...
python -c "import requests,datetime; r=requests.post('https://jarvis-quant-sys.onrender.com/webhook', json={'action':'sell','symbol':'EUR_USD','confidence':0.8,'risk_percentage':5.0,'timestamp':datetime.datetime.now().isoformat()}); print('✅ SELL SIGNAL SENT!' if r.status_code==200 else f'❌ Failed: {r.status_code}')"
pause
