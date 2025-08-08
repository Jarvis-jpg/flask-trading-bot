#!/usr/bin/env python3
"""
Fix Stop Loss Validation Issues for OANDA Live Trading
"""
import json
from datetime import datetime

def fix_webhook_data_conversion():
    """Fix webhook data conversion for OANDA live trading"""
    
    print("🔧 FIXING WEBHOOK DATA CONVERSION")
    print("="*50)
    
    # Valid OANDA pairs (major forex pairs)
    VALID_OANDA_PAIRS = {
        'EURUSD': 'EUR_USD',
        'GBPUSD': 'GBP_USD', 
        'USDJPY': 'USD_JPY',
        'USDCHF': 'USD_CHF',
        'AUDUSD': 'AUD_USD',
        'USDCAD': 'USD_CAD',
        'NZDUSD': 'NZD_USD',
        'EURJPY': 'EUR_JPY',
        'GBPJPY': 'GBP_JPY',
        'EURGBP': 'EUR_GBP',
        'AUDJPY': 'AUD_JPY',
        'EURAUD': 'EUR_AUD',
        'EURCAD': 'EUR_CAD'
    }
    
    print("✅ VALID OANDA FOREX PAIRS:")
    for crypto, forex in VALID_OANDA_PAIRS.items():
        print(f"   {crypto} → {forex}")
    
    # Test webhook conversion with valid forex pair
    forex_trade = {
        "pair": "EURUSD",
        "action": "buy", 
        "entry": 1.0856,
        "stop_loss": 1.0806,
        "take_profit": 1.0956,
        "confidence": 0.75,
        "strategy": "MACD+EMA"
    }
    
    print(f"\n📊 FOREX Trade Example:")
    print(json.dumps(forex_trade, indent=2))
    
    # Convert to OANDA format
    oanda_pair = VALID_OANDA_PAIRS.get(forex_trade['pair'], None)
    if not oanda_pair:
        print(f"❌ Invalid pair: {forex_trade['pair']}")
        return None
    
    # Calculate units (position size)
    base_units = 10000  # Standard lot size
    units = base_units if forex_trade['action'] == 'buy' else -base_units
    
    oanda_trade_data = {
        'pair': oanda_pair,
        'units': units,
        'stop_loss': forex_trade['stop_loss'],
        'take_profit': forex_trade['take_profit']
    }
    
    print(f"\n🔄 OANDA Format:")
    print(json.dumps(oanda_trade_data, indent=2))
    
    # Validate stop loss logic
    entry = forex_trade['entry']
    stop_loss = forex_trade['stop_loss'] 
    take_profit = forex_trade['take_profit']
    
    print(f"\n✅ VALIDATION:")
    print(f"   • Entry: {entry}")
    print(f"   • Stop Loss: {stop_loss}")
    print(f"   • Take Profit: {take_profit}")
    print(f"   • Action: {forex_trade['action']}")
    
    if forex_trade['action'] == 'buy':
        sl_valid = stop_loss < entry
        tp_valid = take_profit > entry
        print(f"   • BUY Stop Loss Valid: {sl_valid} (must be < entry)")
        print(f"   • BUY Take Profit Valid: {tp_valid} (must be > entry)")
    else:
        sl_valid = stop_loss > entry  
        tp_valid = take_profit < entry
        print(f"   • SELL Stop Loss Valid: {sl_valid} (must be > entry)")
        print(f"   • SELL Take Profit Valid: {tp_valid} (must be < entry)")
    
    # Calculate risk/reward
    if forex_trade['action'] == 'buy':
        risk = entry - stop_loss
        reward = take_profit - entry
    else:
        risk = stop_loss - entry
        reward = entry - take_profit
    
    rr_ratio = reward / risk if risk > 0 else 0
    print(f"   • Risk/Reward: {rr_ratio:.2f}:1")
    
    return oanda_trade_data

if __name__ == "__main__":
    fix_webhook_data_conversion()
