#!/usr/bin/env python3
"""
Debug Webhook Data - Check what TradingView is actually sending
"""
import json
from datetime import datetime

def debug_webhook_data():
    """Check webhook data format from logs"""
    
    print("🔍 ANALYZING WEBHOOK DATA FORMAT")
    print("="*50)
    
    # Sample webhook data from logs
    sample_trade = {
        "pair": "ETHUSDT", 
        "action": "buy", 
        "entry": 2288.73, 
        "stop_loss": 2246.55, 
        "take_profit": 2357.76, 
        "confidence": 0.91, 
        "strategy": "MACD+EMA"
    }
    
    print(f"📊 Sample Trade Data:")
    print(json.dumps(sample_trade, indent=2))
    
    # Check OANDA format requirements
    print(f"\n🔄 OANDA Trade Format Conversion:")
    
    # Convert to OANDA format
    oanda_units = 10000 if sample_trade['action'] == 'buy' else -10000
    oanda_trade = {
        'pair': sample_trade['pair'].replace('USDT', '_USD'),  # Fix pair format
        'units': oanda_units,
        'stop_loss': sample_trade['stop_loss'],
        'take_profit': sample_trade['take_profit']
    }
    
    print(json.dumps(oanda_trade, indent=2))
    
    # Validate stop loss format
    print(f"\n✅ VALIDATION CHECKS:")
    print(f"   • Pair format: {oanda_trade['pair']}")
    print(f"   • Stop loss: {oanda_trade['stop_loss']} (float)")
    print(f"   • Stop loss str: '{str(oanda_trade['stop_loss'])}'")
    print(f"   • Units: {oanda_trade['units']} ({'BUY' if oanda_trade['units'] > 0 else 'SELL'})")
    
    # Check for potential issues
    issues = []
    
    # Issue 1: Crypto pairs vs Forex pairs
    if 'USDT' in sample_trade['pair']:
        issues.append("❌ CRYPTO pair format - OANDA expects FOREX (EUR_USD, GBP_USD, etc.)")
    
    # Issue 2: Stop loss validation
    entry = sample_trade['entry']
    stop_loss = sample_trade['stop_loss']
    if sample_trade['action'] == 'buy' and stop_loss >= entry:
        issues.append("❌ BUY order: Stop loss must be BELOW entry price")
    elif sample_trade['action'] == 'sell' and stop_loss <= entry:
        issues.append("❌ SELL order: Stop loss must be ABOVE entry price")
    else:
        issues.append("✅ Stop loss direction is correct")
    
    # Issue 3: Price precision
    if len(str(stop_loss).split('.')[-1]) > 5:
        issues.append("❌ Stop loss precision too high (>5 decimals)")
    else:
        issues.append("✅ Stop loss precision acceptable")
    
    print(f"\n🚨 POTENTIAL ISSUES:")
    for issue in issues:
        print(f"   {issue}")
    
    return oanda_trade, issues

if __name__ == "__main__":
    debug_webhook_data()
