# 🚀 JARVIS TRADING SYSTEM - COMPLETE STARTUP GUIDE

## 🎯 PHASE 1: START THE SYSTEM

### Step 1: Open Command Prompt
1. Press `Windows + R`
2. Type `cmd` and press Enter
3. Navigate to your trading bot folder:
   ```
   cd C:\Users\Smith_Family7\flask-trading-bot
   ```

### Step 2: Activate Virtual Environment
```bash
venv\Scripts\activate
```
- You should see `(venv)` at the beginning of your command prompt

### Step 3: Start JARVIS System
```bash
python app.py
```

**✅ EXPECTED OUTPUT:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: off
JARVIS Trading System Started
Live Trading Mode: ACTIVE
OANDA Account Connected: 001-001-12623605-001
Webhook URL: http://127.0.0.1:5000/webhook
```

### Step 4: Verify System is Running
- Open your web browser
- Go to: `http://127.0.0.1:5000`
- You should see the JARVIS dashboard

---

## 🌐 PHASE 2: CONFIGURE TRADINGVIEW

### Step 1: Login to TradingView
1. Go to [TradingView.com](https://tradingview.com)
2. Login to your account
3. Open a chart (EUR/USD, GBP/USD, or USD/JPY)

### Step 2: Create Alert
1. Click the **"Alert"** button (bell icon) on the chart
2. Set up your alert with these settings:

**Alert Settings:**
- **Condition**: Choose your trading strategy indicator
- **Options**: Check "Once Per Bar Close"
- **Expiration**: Never
- **Message**: 
  ```json
  {
    "symbol": "{{ticker}}",
    "action": "{{strategy.order.action}}",
    "price": "{{close}}",
    "time": "{{time}}",
    "strategy": "JARVIS_SIGNAL"
  }
  ```

### Step 3: Configure Webhook
**IMPORTANT: Your webhook URL depends on how you're running the system:**

**For Local Testing (what you're doing now):**
- Webhook URL: `http://127.0.0.1:5000/webhook`
- ⚠️ **Note**: This only works while your computer is on and running the system

**For Production (when you deploy to Render):**
- Webhook URL: `https://flask-trading-bot.onrender.com/webhook`

### Step 4: Test the Alert
1. Click "Create" to save the alert
2. TradingView will now send signals to your system
3. Monitor your command prompt for incoming signals

---

## 🔍 PHASE 3: VERIFY SYSTEM IS WORKING

### Check 1: Command Prompt Activity
**What to look for:**
```
Received webhook from TradingView
Processing trade signal for EUR_USD
Signal validated - confidence: 78.5%
Trade executed successfully
Current balance: $0.95
```

### Check 2: OANDA Account Balance
1. Login to [OANDA Practice Account](https://www.oanda.com)
2. Check your account balance ($0.95 currently)
3. Look for any new trades in "Open Positions" or "Trade History"

### Check 3: System Dashboard
- Visit: `http://127.0.0.1:5000`
- Check recent trades and system status
- Verify connection status shows "CONNECTED"

### Check 4: Log Files
Check these files for activity:
```bash
# View recent system logs
type logs\trading.log
type logs\system.log
```

---

## 💰 PHASE 4: FUNDING YOUR ACCOUNT

### Current Account Status
- **Current Balance**: $0.95
- **Minimum Trade Size**: $1,000 units (about $0.01 per pip)
- **Recommended Balance**: $100+ for meaningful trading

### Adding Funds to OANDA
1. Login to your OANDA account
2. Go to "Fund Account" or "Deposit"
3. Choose your deposit method:
   - **Credit Card**: Instant
   - **Bank Transfer**: 1-3 days
   - **PayPal**: Instant (if available)

### Recommended Starting Amount
- **Conservative**: $100-500
- **Moderate**: $500-1,000
- **Aggressive**: $1,000-5,000

**Risk Per Trade**: System will risk 2% per trade
- $100 account = $2 risk per trade
- $500 account = $10 risk per trade
- $1,000 account = $20 risk per trade

---

## 🛡️ PHASE 5: SAFETY CHECKS

### Before Going Live Checklist
- [ ] System running without errors
- [ ] TradingView alerts configured
- [ ] OANDA account funded
- [ ] Risk settings configured (2% max per trade)
- [ ] Stop losses enabled
- [ ] Daily loss limits set

### Emergency Stop
If you need to stop all trading immediately:
```bash
python emergency_stop.py
```

### Position Monitoring
Check positions every few hours initially:
1. OANDA account dashboard
2. System logs
3. Email notifications (if configured)

---

## 🚨 TROUBLESHOOTING

### Issue: "Insufficient Funds" Error
- **Cause**: Account balance too low
- **Solution**: Add more funds or reduce position size

### Issue: No Trades Executing
1. Check TradingView alerts are firing
2. Verify webhook URL is correct
3. Check system logs for errors
4. Ensure quality filters aren't too strict

### Issue: System Stops Responding
1. Close command prompt
2. Restart system with `python app.py`
3. Check for error messages

### Issue: Trades Not Appearing in OANDA
- **Cause**: Demo mode vs Live mode
- **Solution**: Verify `.env` file has `OANDA_LIVE=true`

---

## 📞 SUPPORT INFORMATION

### System Files to Check
- **Main Application**: `app.py`
- **Configuration**: `.env`
- **Logs**: `logs/` folder
- **Trade History**: Dashboard at `http://127.0.0.1:5000`

### Key Commands
```bash
# Start system
python app.py

# Check system status
python system_monitor.py

# Emergency stop all trades
python emergency_stop.py

# View recent trades
python trade_analyzer.py
```

---

## 🎉 SUCCESS INDICATORS

**✅ System is Working When You See:**
1. **Command Prompt**: Regular webhook notifications
2. **OANDA**: New trades appearing
3. **Balance Changes**: Account balance increasing/decreasing
4. **TradingView**: Alerts firing successfully
5. **Dashboard**: Recent activity showing

**Your JARVIS system is now ready to trade with your $0.95 and any additional funds you add!**

---

*Keep this guide handy and refer to it whenever you start the system. The system will work 24/7 as long as your computer is on and the command prompt window stays open.*
