#!/usr/bin/env python3
"""
TradingView Free Signal Configuration
Customize your trading strategy and chart settings
"""

# ========================================
# TRADINGVIEW CONFIGURATION
# ========================================

# Your TradingView chart URL (customize this)
CHART_URL = "https://www.tradingview.com/chart/your-chart-id/"

# TradingView login (optional for free charts)
TRADINGVIEW_USERNAME = None  # Set to your username if you want to login
TRADINGVIEW_PASSWORD = None  # Set to your password if you want to login

# ========================================
# JARVIS INTEGRATION
# ========================================

# JARVIS webhook URL (your cloud system)
JARVIS_WEBHOOK_URL = "https://jarvis-quant-sys.onrender.com/webhook"

# ========================================
# SIGNAL GENERATION SETTINGS
# ========================================

# How often to check for signals (seconds)
CHECK_INTERVAL_SECONDS = 30

# Minimum confidence required to send signal (0.0 to 1.0)
CONFIDENCE_THRESHOLD = 0.70

# Currency pairs to monitor
CURRENCY_PAIRS = [
    "EUR_USD",
    "GBP_USD", 
    "USD_JPY",
    "AUD_USD",
    "USD_CAD"
]

# Risk management
DEFAULT_RISK_PERCENTAGE = 5.0
DEFAULT_STOP_LOSS_PIPS = 20
DEFAULT_TAKE_PROFIT_PIPS = 40

# ========================================
# INDICATOR THRESHOLDS
# ========================================

# EMA Settings
EMA_FAST_PERIOD = 12
EMA_SLOW_PERIOD = 26

# RSI Settings  
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70

# MACD Settings
MACD_SIGNAL_THRESHOLD = 0.0001

# ========================================
# CHART ELEMENT SELECTORS
# ========================================
# These CSS selectors help read data from TradingView
# You may need to customize these based on your chart setup

SELECTORS = {
    'price': "[data-name='legend-source-item']",
    'volume': ".chart-markup-table .apply-common-tooltip",
    'indicators': ".legend-source-item",
    'chart_container': ".chart-container",
    'loading_indicator': ".tv-spinner"
}

# ========================================
# SIGNAL LOGIC CONFIGURATION
# ========================================

def jarvis_pine_script_logic(indicators, current_price, previous_signals):
    """
    JARVIS Pine Script Logic - Uses your existing strategy
    This reads the same indicators your Pine Script uses:
    - EMA (12, 26)
    - MACD 
    - RSI
    - Bollinger Bands
    """
    
    # Extract indicator values (these match your Pine Script)
    try:
        # Get indicator values from TradingView chart
        ema_12 = indicators.get('ema_12', current_price)
        ema_26 = indicators.get('ema_26', current_price) 
        rsi = indicators.get('rsi', 50)
        macd = indicators.get('macd', 0)
        macd_signal = indicators.get('macd_signal', 0)
        bb_upper = indicators.get('bb_upper', current_price * 1.02)
        bb_lower = indicators.get('bb_lower', current_price * 0.98)
        
        # JARVIS Pine Script Strategy Logic (same as your existing Pine Script)
        
        # BUY CONDITIONS (matching your Pine Script)
        buy_condition = (
            current_price > ema_12 and           # Price above fast EMA
            ema_12 > ema_26 and                 # EMA bullish alignment
            rsi < 70 and rsi > 30 and           # RSI in tradeable range
            macd > macd_signal and              # MACD bullish
            current_price < bb_upper * 0.98     # Not overbought on Bollinger
        )
        
        # SELL CONDITIONS (matching your Pine Script)
        sell_condition = (
            current_price < ema_12 and          # Price below fast EMA
            ema_12 < ema_26 and                # EMA bearish alignment  
            rsi > 30 and rsi < 70 and          # RSI in tradeable range
            macd < macd_signal and             # MACD bearish
            current_price > bb_lower * 1.02    # Not oversold on Bollinger
        )
        
        # Calculate confidence based on indicator strength (like your Pine Script)
        if buy_condition:
            # Calculate confidence based on indicator alignment
            ema_strength = min((ema_12 - ema_26) / ema_26 * 100, 0.2)  # Max 20% contribution
            rsi_strength = min(abs(50 - rsi) / 50, 0.2)  # Distance from neutral
            macd_strength = min(abs(macd - macd_signal) * 1000, 0.2)  # MACD divergence
            
            base_confidence = 0.75  # Base confidence for signal
            confidence = min(0.95, base_confidence + ema_strength + rsi_strength + macd_strength)
            
            return {
                "action": "buy",
                "confidence": confidence,
                "reason": f"JARVIS Pine Script BUY: EMA({ema_12:.4f}>{ema_26:.4f}), RSI({rsi:.1f}), MACD({macd:.4f})"
            }
            
        elif sell_condition:
            # Calculate confidence for sell signal
            ema_strength = min((ema_26 - ema_12) / ema_12 * 100, 0.2)
            rsi_strength = min(abs(50 - rsi) / 50, 0.2)
            macd_strength = min(abs(macd_signal - macd) * 1000, 0.2)
            
            base_confidence = 0.75
            confidence = min(0.95, base_confidence + ema_strength + rsi_strength + macd_strength)
            
            return {
                "action": "sell", 
                "confidence": confidence,
                "reason": f"JARVIS Pine Script SELL: EMA({ema_12:.4f}<{ema_26:.4f}), RSI({rsi:.1f}), MACD({macd:.4f})"
            }
        
        return None  # No signal
        
    except Exception as e:
        print(f"Error in JARVIS Pine Script logic: {e}")
        return None

# Use your existing Pine Script logic
custom_signal_logic = jarvis_pine_script_logic

# ========================================
# ADVANCED SETTINGS
# ========================================

# Browser settings
BROWSER_SETTINGS = {
    'headless': False,  # Set True to run browser in background
    'window_width': 1920,
    'window_height': 1080,
    'page_load_timeout': 30,
    'implicit_wait': 10
}

# Logging settings
LOGGING_SETTINGS = {
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR
    'log_to_file': True,
    'log_file': 'tradingview_reader.log'
}

# Error handling
ERROR_SETTINGS = {
    'max_retries': 3,
    'retry_delay': 5,  # seconds
    'restart_on_error': True
}
