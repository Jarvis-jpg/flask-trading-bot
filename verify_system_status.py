#!/usr/bin/env python3
"""
Quick system status verification - no file changes
"""

import requests
import json

def verify_system_status():
    """Verify current system status"""
    print("🔍 SYSTEM STATUS VERIFICATION")
    print("=" * 50)
    
    # Test production webhook with exact JARVIS signal format
    test_signal = {
        "symbol": "EURUSD",
        "action": "BUY", 
        "confidence": 85.0,
        "price": 1.0850,
        "risk_percentage": 5.0,
        "stop_loss_pips": 20,
        "take_profit_pips": 40,
        "source": "ultra_reliable_automated"
    }
    
    url = "https://jarvis-quant-sys.onrender.com/webhook"
    
    print("📊 Testing production webhook...")
    try:
        response = requests.post(url, json=test_signal, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            status = result.get('status', 'unknown')
            
            if status == 'executed':
                print("✅ SUCCESS: Trade would be executed!")
                print("🎯 System is working - trades should appear!")
                return True
            elif status == 'rejected':
                reason = result.get('reason', 'unknown')
                print(f"⚠️  TRADE REJECTED: {reason}")
                
                if 'market_closed' in reason:
                    print("💡 Market is closed - normal behavior")
                elif 'unfavorable_analysis' in reason:
                    print("💡 Analysis rejected trade - system is cautious")
                elif 'balance' in reason.lower():
                    print("💡 Insufficient balance - $0.95 might be too low")
                    
                return False
        else:
            print(f"❌ ERROR: {response.text[:200]}...")
            
            if "EUR_USD" in response.text or "instrument" in response.text:
                print("🔧 OANDA instrument format issue")
            elif "units" in response.text:
                print("🔧 Position sizing issue") 
            elif "balance" in response.text.lower():
                print("💰 Account balance issue ($0.95 too low?)")
            else:
                print("🔧 Other technical issue")
                
            return False
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

if __name__ == "__main__":
    verify_system_status()
