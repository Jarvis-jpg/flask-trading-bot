# Sample Trading Strategy Configuration

def custom_signal_logic(indicators, current_price, previous_signals):
    """
    SAMPLE STRATEGY: Simple EMA Crossover
    Replace this with your own trading logic
    """
    
    # Example: Generate buy signal on price momentum
    if len(previous_signals) > 0:
        last_price = previous_signals[-1].get('price', current_price)
        price_change_pct = ((current_price - last_price) / last_price) * 100
        
        # Strong bullish momentum - BUY signal
        if price_change_pct > 0.1:  # 0.1% price increase
            return {
                "action": "buy",
                "confidence": min(0.95, 0.75 + (price_change_pct / 100)),
                "reason": f"Bullish momentum: {price_change_pct:.2f}%"
            }
        
        # Strong bearish momentum - SELL signal  
        elif price_change_pct < -0.1:  # 0.1% price decrease
            return {
                "action": "sell",
                "confidence": min(0.95, 0.75 + (abs(price_change_pct) / 100)),
                "reason": f"Bearish momentum: {price_change_pct:.2f}%"
            }
    
    return None  # No signal

# Customize these settings:
CHART_URL = "https://www.tradingview.com/chart/"  # Your TradingView chart URL
CHECK_INTERVAL_SECONDS = 30  # How often to check for signals
CONFIDENCE_THRESHOLD = 0.75  # Minimum confidence to send signal
DEFAULT_RISK_PERCENTAGE = 5.0  # Risk per trade
