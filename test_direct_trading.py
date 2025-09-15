#!/usr/bin/env python3
"""
Simple webhook test - bypasses Flask to test the core logic directly
"""

import sys
sys.path.append('c:\\Users\\Smith_Family7\\flask-trading-bot')

import json
from oanda_client import OandaClient
from datetime import datetime
import traceback

def calculate_position_size(price, stop_loss, account_balance=25000, risk_percent=4.0):
    try:
        risk_amount = account_balance * (risk_percent / 100)
        price_difference = abs(float(price) - float(stop_loss))
        if price_difference == 0:
            return 500  # Conservative default for small account
        position_size = round(risk_amount / price_difference)
        return max(1, min(position_size, 1000))  # Cap at 1000 for small account
    except Exception as e:
        print(f"Error calculating position size: {e}")
        return 500

def test_trade_execution():
    """Test trade execution directly"""
    print("🚀 Testing Trade Execution Directly")
    print("=" * 50)
    
    try:
        # Initialize OANDA client
        oanda = OandaClient()
        print("✅ OANDA client initialized")
        
        # Test data (realistic SevenSYS format)
        test_data = {
            "ticker": "EURUSD",
            "strategy.order.action": "buy",
            "close": 1.0850,
            "strategy": "SevenSYS",
            "signal_strength": 58.4,
            "news_bias": 8.5,
            "trend_strength": 12.3,
            "stop_loss": 1.0825,
            "take_profit": 1.0900
        }
        
        print(f"\n📊 Processing webhook data:")
        print(json.dumps(test_data, indent=2))
        
        # Extract data (same logic as Flask app)
        symbol = test_data.get("ticker") or test_data.get("symbol", "")
        action = test_data.get("strategy.order.action") or test_data.get("action", "")
        price = test_data.get("close") or test_data.get("price", 0)
        stop_loss = test_data.get("stop_loss", 0)
        take_profit = test_data.get("take_profit", 0)
        
        print(f"\n🔍 Extracted data:")
        print(f"   Symbol: {symbol}")
        print(f"   Action: {action}")
        print(f"   Price: {price}")
        print(f"   Stop Loss: {stop_loss}")
        print(f"   Take Profit: {take_profit}")
        
        # Validate data
        if not all([symbol, action, price, stop_loss, take_profit]):
            missing = [k for k, v in {"symbol": symbol, "action": action, "price": price, "stop_loss": stop_loss, "take_profit": take_profit}.items() if not v]
            print(f"❌ Missing required fields: {missing}")
            return
        
        # Convert to numeric
        price_float = float(price)
        stop_loss_float = float(stop_loss) 
        take_profit_float = float(take_profit)
        
        print(f"\n💰 Price Analysis:")
        sl_distance = abs(stop_loss_float - price_float)
        tp_distance = abs(take_profit_float - price_float)
        tp_sl_ratio = tp_distance / sl_distance if sl_distance > 0 else 0
        
        print(f"   SL Distance: {sl_distance:.5f} ({sl_distance * 10000:.1f} pips)")
        print(f"   TP Distance: {tp_distance:.5f} ({tp_distance * 10000:.1f} pips)")
        print(f"   Risk/Reward: 1:{tp_sl_ratio:.2f}")
        
        # Calculate position size
        position_size = calculate_position_size(price, stop_loss, account_balance=45.0, risk_percent=2.0)
        units = position_size if action.lower() == "buy" else -position_size
        
        # Convert symbol to OANDA format
        oanda_symbol = symbol
        if len(symbol) == 6 and '_' not in symbol:
            oanda_symbol = symbol[:3] + '_' + symbol[3:]
        
        trade_data = {
            "symbol": oanda_symbol,
            "units": units,
            "close_price": price_float,
            "stop_loss": round(stop_loss_float, 5),
            "take_profit": round(take_profit_float, 5)
        }
        
        print(f"\n🎯 Trade Data:")
        print(f"   Symbol: {trade_data['symbol']}")
        print(f"   Units: {trade_data['units']}")
        print(f"   Close Price: {trade_data['close_price']}")
        print(f"   Stop Loss: {trade_data['stop_loss']}")
        print(f"   Take Profit: {trade_data['take_profit']}")
        
        print(f"\n🚀 Placing trade...")
        trade_result = oanda.place_trade(trade_data)
        
        print(f"✅ Trade Result:")
        print(json.dumps(trade_result, indent=2))
        
        if isinstance(trade_result, dict) and trade_result.get('status') == 'success':
            print(f"\n🎉 SUCCESS! Trade placed successfully")
            print(f"   Order ID: {trade_result.get('order_id')}")
            print(f"   Fill Price: {trade_result.get('filled_price')}")
            return True
        else:
            print(f"❌ Trade failed: {trade_result}")
            return False
            
    except Exception as e:
        print(f"💥 Error: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_trade_execution()
