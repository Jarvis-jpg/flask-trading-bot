# 🎛️ JARVIS CLOUD DASHBOARD CONTROLS GUIDE

## 🔍 UNDERSTANDING YOUR CLOUD DASHBOARD

### 🏛️ **LEGACY CONTROLS**
**What it is:**
- Older version of JARVIS system
- Basic trading functionality
- May have limited AI features
- Stable but fewer advanced features

**When to use:**
- ❌ **Don't use for live trading**
- ✅ Use only for testing/comparison
- ✅ Backup system if main system fails

### 🚀 **LIVE CONTROLS** 
**What it is:**
- Current production version
- Full AI capabilities (1M trade dataset)
- Latest risk management features
- Professional-grade system

**When to use:**
- ✅ **USE THIS for live trading**
- ✅ Connected to your OANDA account
- ✅ Receives TradingView webhooks
- ✅ All advanced features active

## 🎯 **RECOMMENDED SETUP**

### **Step 1: Activate LIVE CONTROLS**
1. **Go to your cloud dashboard**: https://jarvis-quant-sys.onrender.com
2. **Click "LIVE CONTROLS"** or similar button
3. **Verify OANDA connection** shows your account (001-001-12623605-001)
4. **Confirm system status** shows "ACTIVE" or "RUNNING"

### **Step 2: Verify Configuration**
Check these settings in LIVE mode:
- ✅ **Account**: 001-001-12623605-001
- ✅ **Mode**: LIVE (not demo)
- ✅ **Risk per trade**: 5%
- ✅ **AI Model**: Active
- ✅ **Webhook**: Listening on /webhook

### **Step 3: Test Webhook**
- **Webhook URL**: `https://jarvis-quant-sys.onrender.com/webhook`
- **Status**: Should show "Ready" or "Listening"
- **Test**: Create a TradingView alert to verify connection

## ⚠️ **IMPORTANT: DON'T RUN BOTH**

### **Choose ONE system only:**
- ✅ **LIVE CONTROLS**: For real trading
- ❌ **Legacy Controls**: Turn OFF (avoid conflicts)
- ❌ **Local System**: Stop if using cloud (avoid duplicate trades)

## 🔧 **ACTIVATION STEPS**

### **If you see both Legacy and Live buttons:**

1. **Turn OFF Legacy:**
   - Click "Stop" or "Disable" on Legacy controls
   - Ensure Legacy system is not running

2. **Turn ON Live:**
   - Click "Start" or "Enable" on Live controls
   - Wait for "ACTIVE" status confirmation

3. **Verify Settings:**
   - Check OANDA connection
   - Verify account balance ($0.95)
   - Confirm webhook is active

## 📊 **WHAT YOU SHOULD SEE**

### **In LIVE mode dashboard:**
```
🟢 System Status: ACTIVE
🏦 OANDA Account: 001-001-12623605-001
💰 Balance: $0.95
🎯 Risk per Trade: 5%
📡 Webhook: LISTENING
🤖 AI Model: LOADED
📈 Ready for Signals: YES
```

### **In Legacy mode (should be OFF):**
```
🔴 System Status: INACTIVE
🏦 OANDA Account: Not Connected
💰 Balance: N/A
📡 Webhook: DISABLED
```

## 🚨 **TROUBLESHOOTING**

### **If you don't see Live Controls:**
- Refresh the dashboard page
- Check you're on the right URL: https://jarvis-quant-sys.onrender.com
- Try clicking "Switch to Live Mode" if available

### **If Live Controls show errors:**
- Check OANDA credentials are configured
- Verify API keys are valid
- Ensure account has sufficient balance ($0.95)

### **If webhook shows offline:**
- Restart Live Controls
- Check system logs for errors
- Verify cloud deployment is running

## 🎯 **FINAL ANSWER**

**YES, use the LIVE CONTROLS to run your system:**

1. ✅ **Enable LIVE CONTROLS** on dashboard
2. ❌ **Disable LEGACY CONTROLS** 
3. ✅ **Use webhook**: `https://jarvis-quant-sys.onrender.com/webhook`
4. ✅ **Monitor LIVE dashboard** for activity
5. ✅ **Create TradingView alerts** pointing to cloud webhook

**The LIVE CONTROLS are your production trading system - that's what will execute real trades with your $0.95 OANDA account!**

## 🚀 **YOU'RE READY!**

Once LIVE CONTROLS are active:
- System runs 24/7 automatically
- Receives TradingView signals
- Executes trades through OANDA
- No need to keep your computer on
- Professional cloud-based operation

**Your autonomous trading system is now fully operational!** 🎉
