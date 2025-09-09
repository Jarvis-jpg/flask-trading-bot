import requests
import json
from datetime import datetime

def test_jarvis_live_format():
    """Test the JARVIS Live Pine script format"""
    
    # JARVIS Live format (from Pine script)
    jarvis_live_alert = {
        "pair": "EURUSD",
        "action": "buy",
        "entry": 1.05234,
        "stop_loss": 1.04897,
        "take_profit": 1.06008,
        "confidence": 0.85,
        "strategy": "JARVIS_LIVE",
        "risk_reward": 2.5,
        "position_size": 279,
        "daily_trade_count": 1,
        "account_equity": 10000,
        "timestamp": str(int(datetime.now().timestamp()))
    }
    
    print(f"Testing JARVIS Live webhook format:")
    print(json.dumps(jarvis_live_alert, indent=2))
    
    # Calculate expected distances
    sl_distance = float(jarvis_live_alert['entry']) - float(jarvis_live_alert['stop_loss'])
    tp_distance = float(jarvis_live_alert['take_profit']) - float(jarvis_live_alert['entry'])
    
    print(f"\nExpected Analysis:")
    print(f"SL Distance: {sl_distance:.5f} ({sl_distance * 10000:.1f} pips)")
    print(f"TP Distance: {tp_distance:.5f} ({tp_distance * 10000:.1f} pips)")
    print(f"Risk/Reward: 1:{tp_distance/sl_distance:.2f}")
    
    try:
        response = requests.post(
            'https://jarvis-quant-sys.onrender.com/webhook', 
            json=jarvis_live_alert,
            timeout=30
        )
        print(f"\nProduction webhook response: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error testing webhook: {e}")

def test_jarvis_sell_signal():
    """Test a SELL signal from JARVIS Live"""
    
    jarvis_sell_alert = {
        "pair": "GBPUSD",
        "action": "sell",
        "entry": 1.24567,
        "stop_loss": 1.24890,
        "take_profit": 1.23890,
        "confidence": 0.78,
        "strategy": "JARVIS_LIVE",
        "risk_reward": 2.0,
        "position_size": 250,
        "daily_trade_count": 2,
        "account_equity": 10000,
        "timestamp": str(int(datetime.now().timestamp()))
    }
    
    print(f"\nTesting JARVIS Live SELL signal:")
    print(json.dumps(jarvis_sell_alert, indent=2))
    
    # Calculate expected distances
    sl_distance = float(jarvis_sell_alert['stop_loss']) - float(jarvis_sell_alert['entry'])
    tp_distance = float(jarvis_sell_alert['entry']) - float(jarvis_sell_alert['take_profit'])
    
    print(f"SL Distance: {sl_distance:.5f} ({sl_distance * 10000:.1f} pips)")
    print(f"TP Distance: {tp_distance:.5f} ({tp_distance * 10000:.1f} pips)")
    
    try:
        response = requests.post(
            'https://jarvis-quant-sys.onrender.com/webhook', 
            json=jarvis_sell_alert,
            timeout=30
        )
        print(f"SELL signal response: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error testing SELL signal: {e}")

if __name__ == "__main__":
    print("=== Testing JARVIS Live Webhook Format ===")
    print(f"Test time: {datetime.now()}")
    
    test_jarvis_live_format()
    test_jarvis_sell_signal()
    
    print("\n=== Test Complete ===")
    print("Check OANDA account and logs for trade execution details.")
    print("TP/SL should be added after market orders fill successfully.")
