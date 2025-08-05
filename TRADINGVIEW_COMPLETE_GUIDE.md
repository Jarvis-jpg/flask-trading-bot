# 📊 TRADINGVIEW INTEGRATION GUIDE

## 🎯 STEP-BY-STEP TRADINGVIEW SETUP

### STEP 1: Access TradingView
1. Go to [TradingView.com](https://tradingview.com)
2. Login to your account
3. Click "Chart" to open the charting interface

### STEP 2: Choose Your Trading Pair
**JARVIS works best with these pairs:**
- **EUR/USD** (most liquid)
- **GBP/USD** (good volatility)
- **USD/JPY** (Asian session coverage)

### STEP 3: Set Up Chart for Signals
1. Select **1-hour timeframe** (recommended)
2. Add indicators you want to use for signals
3. Look for clear trend patterns

### STEP 4: Create Alert
1. Click the **🔔 Alert** button (top toolbar)
2. Configure these settings:

**ALERT CONFIGURATION:**
```
Condition: [Your chosen indicator/condition]
Options:
  ☑️ Once Per Bar Close
  ☑️ Send Webhook
  ☐ Send Email (optional)
  ☐ Send SMS (optional)

Expiration: Never (keep alert active)

Webhook Settings:
  URL: http://127.0.0.1:5000/webhook
  
Message (copy/paste exactly):
{
  "symbol": "{{ticker}}",
  "action": "BUY",
  "price": {{close}},
  "time": "{{time}}",
  "strategy": "JARVIS_SIGNAL",
  "confidence": 0.75
}
```

### STEP 5: Test Your Alert
1. Click "Create" to save the alert
2. Watch for the alert to trigger
3. Check your JARVIS command prompt for webhook received

---

## 🔍 WEBHOOK VERIFICATION

### What JARVIS Expects to Receive:
```json
{
  "symbol": "EURUSD",
  "action": "BUY" or "SELL", 
  "price": 1.0850,
  "time": "2025-08-05T10:30:00Z",
  "strategy": "JARVIS_SIGNAL",
  "confidence": 0.75
}
```

### Success Indicators in Command Prompt:
```
✅ Webhook received from TradingView
✅ Signal validated for EUR/USD
✅ Confidence level: 75.0%
✅ Risk management passed
✅ Order placed with OANDA
```

---

## ⚡ QUICK SIGNAL STRATEGIES

### Strategy 1: Simple Moving Average Cross
**Alert Condition:**
- When price crosses above 20 SMA → Send BUY signal
- When price crosses below 20 SMA → Send SELL signal

### Strategy 2: RSI Oversold/Overbought
**Alert Condition:**
- RSI crosses above 30 from below → Send BUY signal  
- RSI crosses below 70 from above → Send SELL signal

### Strategy 3: Manual Alerts
**For manual trading:**
- Set alert at key support/resistance levels
- Manually trigger when you see good setups
- JARVIS will validate and execute if criteria met

---

## 🛠️ TROUBLESHOOTING TRADINGVIEW

### Issue: Webhook Not Reaching JARVIS
**Check:**
1. JARVIS system is running (`python app.py`)
2. Webhook URL is correct: `http://127.0.0.1:5000/webhook`
3. TradingView alert is active (green dot)

### Issue: Alerts Not Triggering
**Solutions:**
1. Check alert conditions are being met
2. Verify "Once Per Bar Close" is checked
3. Make sure alert hasn't expired

### Issue: JSON Format Errors
**Common mistakes:**
- Missing quotes around strings
- Wrong bracket types {} vs []
- Comma placement errors

**Correct format:**
```json
{
  "symbol": "{{ticker}}",
  "action": "BUY",
  "price": {{close}}
}
```

---

## 📱 MOBILE MONITORING

### TradingView Mobile App
1. Download TradingView app
2. Login to same account
3. Check "Alerts" tab to see activity
4. Get push notifications when signals fire

### OANDA Mobile App
1. Download OANDA app  
2. Monitor account balance and trades
3. See trade history and P&L
4. Emergency position closing if needed

---

## 🎯 RECOMMENDED SETTINGS FOR YOUR $0.95 ACCOUNT

### Conservative Settings (Recommended):
- **Alerts per day**: 2-5 maximum
- **Risk per trade**: $0.02 (2% of $0.95)
- **Position size**: 100 units
- **Stop loss**: Always enabled

### What This Means:
- Each trade risks about 2 cents
- Need 50+ winning trades to double account  
- Very low risk while learning system
- Perfect for testing and verification

### When to Add Funds:
- After 1 week of successful operation
- When you see consistent profits
- Start with $100-500 additional funding

---

## 🚨 SAFETY REMINDERS

### Before Going Live:
- [ ] Test alerts with small amounts first
- [ ] Verify JARVIS receives webhooks correctly
- [ ] Check OANDA trades are executing
- [ ] Monitor for at least 2-4 hours initially

### Daily Monitoring:
- Check TradingView alerts triggered
- Verify OANDA account balance
- Review JARVIS system logs
- Look for any error messages

**Your TradingView → JARVIS → OANDA pipeline is now ready!** 🚀

Once you add more funds, the same system will scale up proportionally while maintaining the same 2% risk per trade safety.
