#!/usr/bin/env python3
"""
Debug script to check the trade realism assessment logic
"""

import json
import os

def debug_trade_realism():
    """Debug the trade realism assessment"""
    print("🔍 DEBUGGING TRADE REALISM ASSESSMENT")
    print("=" * 50)
    
    if not os.path.exists("jarvis_ai_memory_mega.json"):
        print("❌ File not found")
        return
    
    try:
        with open("jarvis_ai_memory_mega.json", 'r') as f:
            data = json.load(f)
        
        trades = data.get('trades', [])
        print(f"📊 Total trades found: {len(trades):,}")
        
        if not trades:
            print("❌ No trades in dataset")
            return
        
        # Check first few trades
        sample_size = min(10, len(trades))
        sample_trades = trades[:sample_size]
        
        print(f"\n🔍 Analyzing first {sample_size} trades:")
        print("-" * 50)
        
        realistic_count = 0
        
        for i, trade in enumerate(sample_trades):
            print(f"\nTrade {i+1}:")
            print(f"   Keys: {list(trade.keys())}")
            
            # Check different possible key names
            confidence = (trade.get('confidence') or 
                         trade.get('confidence_score') or 
                         trade.get('probability') or 0)
            
            risk_reward = (trade.get('risk_reward_ratio') or 
                          trade.get('risk_reward') or 
                          trade.get('rr_ratio') or 0)
            
            print(f"   Confidence: {confidence}")
            print(f"   Risk/Reward: {risk_reward}")
            print(f"   Outcome: {trade.get('outcome', 'N/A')}")
            print(f"   Pair: {trade.get('pair', 'N/A')}")
            
            # Apply realism check (CORRECTED LOGIC)
            confidence_realistic = 0.5 <= confidence <= 0.95
            rr_realistic = 1.0 <= risk_reward <= 5.0
            
            print(f"   Confidence realistic (0.5-0.95): {confidence_realistic}")
            print(f"   Risk/Reward realistic (1.0-5.0): {rr_realistic}")
            
            if confidence_realistic and rr_realistic:
                realistic_count += 1
                print("   ✅ REALISTIC")
            else:
                print("   ❌ NOT REALISTIC")
        
        realism_percentage = (realistic_count / sample_size) * 100
        print(f"\n📊 REALISM ASSESSMENT:")
        print(f"   Realistic trades: {realistic_count}/{sample_size}")
        print(f"   Realism percentage: {realism_percentage:.1f}%")
        
        if realism_percentage >= 80:
            print("✅ CONCLUSION: Training data appears realistic")
        elif realism_percentage >= 50:
            print("⚠️ CONCLUSION: Training data partially realistic")
        else:
            print("❌ CONCLUSION: Training data may be synthetic")
        
        # Check if the original assessment had wrong key names
        print(f"\n🔍 DEBUGGING ORIGINAL ASSESSMENT ISSUE:")
        first_trade = trades[0]
        print(f"   Original logic expected 'risk_reward_ratio' key")
        print(f"   Actual key in data: '{list(first_trade.keys())}'")
        print(f"   This explains the 0.0% realism - wrong key names!")
        
        return realism_percentage
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 0

if __name__ == "__main__":
    debug_trade_realism()
