# URGENT: TradingView Alert Setup for SevenSYS

## 🚨 WHY NO SIGNALS: Missing TradingView Webhook Configuration

Your system is working, but TradingView isn't sending signals to your Render deployment.

## ✅ IMMEDIATE FIX - SET UP TRADINGVIEW ALERTS:

### Step 1: Open TradingView
1. Go to TradingView.com
2. Open a chart with EUR/USD, GBP/USD, or any major forex pair
3. Add the SevenSYS_Complete.pine strategy to your chart

### Step 2: Create Alert
1. Right-click on chart → "Add Alert"
2. Condition: Select "SevenSYS_Complete" → "Any alert() function call"
3. Options: Leave default settings
4. Actions: Check "Webhook URL"

### Step 3: Configure Webhook
**Webhook URL:** 
```
https://jarvis-quant-sys.onrender.com/webhook
```

**Message (copy exactly):**
```json
{"ticker": "{{ticker}}", "strategy.order.action": "{{strategy.order.action}}", "close": {{close}}, "strategy": "SevenSYS", "signal_strength": 40.0, "news_bias": 0.0, "trend_strength": 5.0}
```

### Step 4: Save Alert
1. Name: "SevenSYS Live Trading"
2. Click "Create"
3. Ensure alert shows as "Active" (green dot)

## 🎛️ ADJUST SIGNAL SENSITIVITY (If Still No Signals):

### In Pine Script Settings:
- **Minimum Signal Strength**: Change from 35.0 to **25.0**
- **News Sentiment Bias**: Set based on current market (e.g., +3 for bullish, -3 for bearish)
- **Enable News Filter**: Keep checked
- **Major Event Mode**: Uncheck unless there's a major event

## 🔍 VERIFY SYSTEM IS WORKING:

### Test Webhook Manually:
```python
python -c "
import requests
r = requests.post('https://jarvis-quant-sys.onrender.com/webhook', 
json={'ticker':'EUR_USD','strategy.order.action':'buy','close':1.0850,'strategy':'SevenSYS'}, 
timeout=30)
print('Test Result:', r.status_code, r.text[:200])
"
```

### Check Render Logs:
1. Go to Render dashboard
2. Select your flask-trading-bot service
3. Check logs for webhook activity

## 📊 Expected Behavior After Setup:

1. **Pine Script Dashboard** shows signal strength ≥ 25
2. **TradingView Alert** fires and shows notification
3. **Render Logs** show "Webhook received" messages
4. **OANDA Account** shows new trades being placed

## ⏰ Market Session Requirements:

SevenSYS only trades during active sessions:
- **London**: 8:00-16:00 GMT
- **New York**: 13:00-22:00 GMT  
- **Asian**: 22:00-06:00 GMT

## 🚀 GUARANTEED SIGNAL TEST:

If you want to force a test signal, temporarily change in Pine Script:
```pinescript
minSignalStrength = input.float(5.0, "Minimum Signal Strength", minval=1.0, maxval=65.0, step=1.0)
```

This will make signals fire much more frequently for testing.

## 📱 Success Indicators:

✅ TradingView alert shows "Triggered" in alert list  
✅ Render logs show POST requests to /webhook  
✅ OANDA account shows new positions  
✅ Memory database (sevensys_memory.db) logs trades

---

## 🎯 BOTTOM LINE: 

Your trading system is fully functional. You just need to **create the TradingView alert** that connects Pine Script signals to your Render webhook endpoint.

**Webhook URL:** https://jarvis-quant-sys.onrender.com/webhook
