🚀 TRADINGVIEW WEBHOOK SETUP FOR LIVE TRADING
==============================================

Your Render webhook URL: https://your-app-name.onrender.com/webhook

## REQUIRED TRADINGVIEW ALERT MESSAGE FORMAT:

```json
{
    "action": "{{strategy.order.action}}",
    "symbol": "{{ticker}}",
    "price": "{{close}}",
    "quantity": "1000",
    "timestamp": "{{time}}",
    "strategy": "JARVIS_AI",
    "confidence": "0.85",
    "risk_reward": "2.5"
}
```

## SETUP STEPS:

### 1. TRADINGVIEW STRATEGY SETUP:
- Open your TradingView chart
- Add your trading strategy/indicator
- Go to "Alerts" tab
- Click "Create Alert"

### 2. WEBHOOK CONFIGURATION:
- Alert Type: "Strategy Alert"  
- Message: Copy the JSON format above
- Webhook URL: https://your-app-name.onrender.com/webhook
- Method: POST

### 3. REQUIRED ALERT CONDITIONS:
- Trigger: "Once Per Bar Close"
- Expiration: Never
- Enable "Webhook URL"

### 4. SUPPORTED ACTIONS:
- "buy" - Opens long position
- "sell" - Opens short position  
- "close_buy" - Closes long position
- "close_sell" - Closes short position

### 5. SUPPORTED SYMBOLS:
- EUR_USD
- GBP_USD  
- USD_JPY
- AUD_USD
- USD_CAD
- NZD_USD
- EUR_GBP
- EUR_JPY
- GBP_JPY
- AUD_JPY

### 6. SAFETY FEATURES ACTIVE:
✅ Maximum position size: $1000 per trade
✅ Stop loss: Automatic based on risk_reward ratio
✅ Take profit: Automatic based on confidence level
✅ Maximum daily trades: 10
✅ Emergency kill switch available
✅ Real-time monitoring dashboard

### 7. TESTING BEFORE LIVE:
1. Send test webhook to verify connection
2. Check dashboard shows received signal
3. Verify OANDA account connection
4. Test with small position first

## 🎯 SYSTEM STATUS: READY FOR LIVE TRADING!

Your autonomous trading system is fully deployed and ready.
The AI is currently training on realistic market data.
All safety systems are active and monitoring.

Next step: Configure your TradingView alerts using the format above.
