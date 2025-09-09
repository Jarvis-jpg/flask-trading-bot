#!/usr/bin/env python3
"""
TP/SL Diagnostic Tool
Analyzes why Take Profit and Stop Loss orders are being cancelled
"""
import json
from datetime import datetime

def analyze_tp_sl_issue():
    """Analyze the TP/SL cancellation issue from the logs"""
    
    print("🔍 TAKE PROFIT / STOP LOSS ANALYSIS")
    print("="*50)
    
    # Data from your Render logs
    entry_price = 1.17095
    stop_loss = 1.17353  # From logs: 1.1722152226 rounded to 1.17353
    take_profit = 1.16603  # From logs: 1.1686895548 rounded to 1.16603
    action = "sell"
    units = -500
    
    print(f"📊 TRADE DETAILS FROM LOGS:")
    print(f"   Action: {action.upper()}")
    print(f"   Entry Price: {entry_price}")
    print(f"   Stop Loss: {stop_loss}")
    print(f"   Take Profit: {take_profit}")
    print(f"   Units: {units}")
    
    # Calculate distances
    sl_distance = abs(stop_loss - entry_price)
    tp_distance = abs(entry_price - take_profit)
    
    print(f"\n📏 DISTANCE ANALYSIS:")
    print(f"   SL Distance: {sl_distance:.5f} ({sl_distance*10000:.1f} pips)")
    print(f"   TP Distance: {tp_distance:.5f} ({tp_distance*10000:.1f} pips)")
    
    # Check direction logic for SELL order
    print(f"\n🎯 DIRECTION LOGIC CHECK:")
    print(f"   For SELL orders:")
    print(f"   - Stop Loss should be ABOVE entry (losses cut when price rises)")
    print(f"   - Take Profit should be BELOW entry (profits taken when price falls)")
    
    sl_direction_correct = stop_loss > entry_price  # SL above entry for sell
    tp_direction_correct = take_profit < entry_price  # TP below entry for sell
    
    print(f"\n✅ DIRECTION VALIDATION:")
    print(f"   Stop Loss Direction: {'✅ CORRECT' if sl_direction_correct else '❌ WRONG'}")
    print(f"   Take Profit Direction: {'✅ CORRECT' if tp_direction_correct else '❌ WRONG'}")
    
    # Check minimum distance requirements
    min_distance = 0.00010  # Typical minimum distance for EUR/USD
    sl_distance_ok = sl_distance >= min_distance
    tp_distance_ok = tp_distance >= min_distance
    
    print(f"\n📐 DISTANCE VALIDATION:")
    print(f"   SL Distance OK: {'✅ YES' if sl_distance_ok else '❌ TOO SMALL'}")
    print(f"   TP Distance OK: {'✅ YES' if tp_distance_ok else '❌ TOO SMALL'}")
    
    # Check for precision issues
    print(f"\n🔧 PRECISION ANALYSIS:")
    print(f"   Original SL: 1.1722152226")
    print(f"   OANDA SL: {stop_loss}")
    print(f"   Precision Loss: {abs(1.1722152226 - stop_loss):.10f}")
    
    print(f"   Original TP: 1.1686895548") 
    print(f"   OANDA TP: {take_profit}")
    print(f"   Precision Loss: {abs(1.1686895548 - take_profit):.10f}")
    
    # Identify likely issues
    print(f"\n🚨 LIKELY ISSUES:")
    
    issues_found = []
    
    if not sl_direction_correct:
        issues_found.append("Stop Loss direction is wrong")
    if not tp_direction_correct:
        issues_found.append("Take Profit direction is wrong")
    if not sl_distance_ok:
        issues_found.append("Stop Loss too close to entry price")
    if not tp_distance_ok:
        issues_found.append("Take Profit too close to entry price")
    
    # Check precision rounding
    if abs(1.1722152226 - stop_loss) > 0.00001:
        issues_found.append("Stop Loss precision rounding issue")
    if abs(1.1686895548 - take_profit) > 0.00001:
        issues_found.append("Take Profit precision rounding issue")
    
    if not issues_found:
        print("   ✅ No obvious issues detected")
        print("   💡 Likely broker/platform specific requirements")
    else:
        for i, issue in enumerate(issues_found, 1):
            print(f"   {i}. ❌ {issue}")
    
    # Suggest fixes
    print(f"\n🔧 SUGGESTED FIXES:")
    print(f"1. 📊 Use higher precision (5 decimal places): {stop_loss:.5f}")
    print(f"2. 📐 Increase minimum distance to 1.5 pips minimum")
    print(f"3. 🕐 Add small delay between market order and TP/SL orders")
    print(f"4. 📋 Use bracket orders instead of separate TP/SL orders")
    print(f"5. ⚡ Check OANDA's minimum distance requirements for EUR/USD")

def check_oanda_requirements():
    """Check OANDA specific requirements"""
    print(f"\n📋 OANDA SPECIFIC REQUIREMENTS:")
    print(f"   • Minimum distance: Usually 0.5-2 pips for major pairs")
    print(f"   • Precision: 5 decimal places for EUR/USD")
    print(f"   • Order timing: TP/SL can be placed with market order")
    print(f"   • Bracket orders: Preferred method for guaranteed execution")

if __name__ == "__main__":
    analyze_tp_sl_issue()
    check_oanda_requirements()
    
    print(f"\n💡 NEXT STEPS:")
    print(f"1. Check if the market order + TP/SL are being sent as one request")
    print(f"2. Verify OANDA account settings allow TP/SL orders")
    print(f"3. Test with wider TP/SL distances (3+ pips)")
    print(f"4. Consider using bracket orders instead")
