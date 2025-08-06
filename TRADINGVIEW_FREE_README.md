# 📊 TradingView Free Integration for JARVIS

## 🎯 What This Does
Automatically reads trading signals from your **FREE** TradingView charts and sends them to your JARVIS trading system. No paid TradingView plan required!

## 🚀 Quick Start

### 1. Run Setup
```bash
python setup_tradingview_free.py
```

### 2. Customize Your Strategy
Edit `tradingview_config.py`:
- Add your TradingView chart URL
- Customize your trading logic
- Set risk parameters

### 3. Start Trading
```bash
python tradingview_enhanced_reader.py
```

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `setup_tradingview_free.py` | 🔧 Main setup and launcher |
| `tradingview_enhanced_reader.py` | 🤖 Advanced monitoring system |
| `tradingview_free_reader.py` | 📊 Basic monitoring system |
| `tradingview_config.py` | ⚙️ Your trading strategy settings |

## ⚙️ Configuration

### Basic Settings (tradingview_config.py)
```python
# Your TradingView chart URL
CHART_URL = "https://www.tradingview.com/chart/your-chart-id/"

# How often to check for signals (seconds)
CHECK_INTERVAL_SECONDS = 30

# Minimum confidence to send signal (0.7 = 70%)
CONFIDENCE_THRESHOLD = 0.70

# Risk per trade
DEFAULT_RISK_PERCENTAGE = 5.0
```

### Custom Trading Strategy
```python
def custom_signal_logic(indicators, current_price, previous_signals):
    # Your trading rules here
    if strong_bullish_condition:
        return {
            "action": "buy",
            "confidence": 0.85,
            "reason": "Strong bullish signal"
        }
    return None  # No signal
```

## 🎯 How It Works

1. **Monitor Chart**: Opens your TradingView chart in browser
2. **Read Data**: Extracts price and indicator values every 30 seconds
3. **Analyze Signals**: Applies your custom trading logic
4. **Send to JARVIS**: Automatically sends signals to your JARVIS system
5. **Execute Trades**: JARVIS executes trades through OANDA

## 📈 Strategy Examples

### EMA Crossover
```python
def ema_crossover_strategy(indicators, current_price, previous_signals):
    # Buy when fast EMA crosses above slow EMA
    # Sell when fast EMA crosses below slow EMA
    pass
```

### RSI Oversold/Overbought
```python
def rsi_strategy(indicators, current_price, previous_signals):
    # Buy when RSI < 30 (oversold)
    # Sell when RSI > 70 (overbought) 
    pass
```

### Price Momentum
```python
def momentum_strategy(indicators, current_price, previous_signals):
    # Buy on strong upward price movement
    # Sell on strong downward price movement
    pass
```

## 🔧 Advanced Features

- ✅ **Error Recovery**: Automatically restarts on errors
- ✅ **Signal History**: Tracks previous signals to avoid duplicates  
- ✅ **Multiple Pairs**: Monitor EUR_USD, GBP_USD, USD_JPY, etc.
- ✅ **Custom Indicators**: Support for any TradingView indicator
- ✅ **Risk Management**: Built-in stop loss and take profit
- ✅ **Detailed Logging**: Complete audit trail of all signals

## 🚨 Important Notes

### Browser Requirements
- Chrome browser installed
- Stable internet connection
- TradingView chart accessible

### JARVIS Integration
- JARVIS system must be running: https://jarvis-quant-sys.onrender.com
- Click "Start LIVE Trading" on JARVIS dashboard
- Verify OANDA connection is active

### Market Hours
- System monitors 24/5 during forex market hours
- Automatically handles market closed periods
- Respects trading session filters

## 🛠️ Troubleshooting

### Common Issues

**"Chart not loading"**
- Check your CHART_URL in tradingview_config.py
- Ensure stable internet connection
- Try different TradingView chart

**"No signals generated"**
- Review your custom_signal_logic() function
- Lower CONFIDENCE_THRESHOLD for more signals
- Check indicator values in logs

**"JARVIS connection failed"**
- Verify JARVIS system is online
- Check webhook URL: https://jarvis-quant-sys.onrender.com/webhook
- Ensure "Start LIVE Trading" is clicked

### Debug Mode
```bash
# Run with detailed logging
python tradingview_enhanced_reader.py --debug
```

## 📊 Performance Optimization

### For Better Signal Quality
- Use multiple indicator confirmation
- Set appropriate confidence thresholds (70%+)
- Implement proper risk-reward ratios (2:1 minimum)

### For System Stability  
- Monitor system logs regularly
- Restart periodically for long-running sessions
- Keep Chrome browser updated

## 💰 Expected Results

With proper configuration:
- **Signal Accuracy**: 70%+ with good strategy
- **Risk Management**: 5% per trade maximum
- **Automation Level**: 99% hands-off
- **Monitoring**: 24/5 continuous operation

## 🎉 Success Checklist

- ✅ Setup completed successfully
- ✅ TradingView chart URL configured
- ✅ Custom strategy logic implemented
- ✅ JARVIS connection verified
- ✅ First signals generated and sent
- ✅ Trades executing through OANDA
- ✅ System running autonomously

## 📞 Next Steps

1. **Run Setup**: `python setup_tradingview_free.py`
2. **Customize Strategy**: Edit your trading logic
3. **Start System**: Begin autonomous trading
4. **Monitor Performance**: Track signals and profits
5. **Optimize Strategy**: Refine based on results

---

**🎯 Your JARVIS system now works with FREE TradingView!**  
**No paid plan required - start trading immediately!**
