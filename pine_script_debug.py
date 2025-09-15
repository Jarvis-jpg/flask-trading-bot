#!/usr/bin/env python3
"""
Pine Script Debug Helper
Check why no signals are generated
"""

def analyze_signal_requirements():
    print("🔍 PINE SCRIPT SIGNAL ANALYSIS")
    print("=" * 60)
    
    print("📊 ORIGINAL EMERGENCY FIX ISSUES:")
    print("• Minimum signal strength: 65 (very high)")
    print("• Required ALL EMAs aligned (ema8>ema21>ema50>ema200)")
    print("• Required London-NY overlap ONLY (limited time)")
    print("• Required trend_strength >= 5.0 or <= -5.0")
    print("• Required momentum_score > 0 or < 0")
    print("• Required above/below VWAP")
    print("• Required normal volatility")
    print()
    
    print("🎯 NEW BALANCED VERSION CHANGES:")
    print("• Minimum signal strength: 55 (more reasonable)")
    print("• EMA alignment: More flexible (ema8>ema21>ema50 OR strong version)")
    print("• Sessions: London, NY, Asian (more trading hours)")
    print("• Trend strength: >= 0 for basic, > 5 for strong")
    print("• RSI FIXED: 40-80 bullish, 20-60 bearish")
    print("• Multiple entry conditions (basic OR strong)")
    print()
    
    print("🚨 CRITICAL RSI FIX:")
    print("OLD (WRONG): rsi < 60 considered bearish")
    print("NEW (FIXED): rsi > 40 and rsi < 80 considered bullish")
    print("           : rsi < 60 and rsi > 20 considered bearish")
    print()
    
    print("🔧 TESTING RECOMMENDATIONS:")
    print("1. Use SevenSYS_BALANCED.pine (more signals)")
    print("2. Check on 1H or 4H timeframe first")
    print("3. Look for EMA 8 > EMA 21 alignment")
    print("4. Verify RSI between 40-80 for longs")
    print("5. Check dashboard shows 'READY' status")
    print()
    
    print("📈 SIGNAL STRENGTH BREAKDOWN:")
    print("Base: 30 points")
    print("Trend (good): +0 to +22.5 points")  
    print("Momentum (good): +0 to +18 points")
    print("Session (overlap): +12 points")
    print("Price Action: +0 to +10 points")
    print("TOTAL POSSIBLE: ~72.5 points")
    print("MINIMUM NEEDED: 55 points")
    print()
    
    print("✅ DEBUGGING STEPS:")
    print("1. Apply SevenSYS_BALANCED.pine to TradingView")
    print("2. Check Strategy Tester on 1H timeframe")
    print("3. Look at dashboard values in real-time")
    print("4. Verify small green/red circles appear (signal ready)")
    print("5. Check RSI is between 40-80 for bullish signals")

if __name__ == "__main__":
    analyze_signal_requirements()
