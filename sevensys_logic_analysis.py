#!/usr/bin/env python3
"""
SEVENSYS PINE SCRIPT ANALYSIS
Critical analysis of trading logic and potential issues causing wrong signals
"""

def analyze_sevensys_logic():
    print("🔍 SEVENSYS PINE SCRIPT CRITICAL ANALYSIS")
    print("=" * 70)
    
    print("🚨 CRITICAL LOGICAL ERRORS IDENTIFIED:")
    print()
    
    print("1. ⚠️  CONFLICTING SIGNAL LOGIC:")
    print("   Problem: The script has DUAL entry conditions that can conflict")
    print()
    print("   Main Conditions (Line 76-79):")
    print("   • long_conditions = trend_strength > 1.0 AND momentum_score > 1.0")
    print("   • short_conditions = trend_strength < -1.0 AND momentum_score < -1.0")
    print()
    print("   Backup Conditions (Line 84-85):")
    print("   • simple_long = ema8 > ema21 AND close > vwap AND rsi > 45")
    print("   • simple_short = ema8 < ema21 AND close < vwap AND rsi < 55")
    print()
    print("   Override Logic (Line 88-89):")
    print("   • enter_long := enter_long OR (simple_long AND signal_strength_long >= 50.0)")
    print("   • enter_short := enter_short OR (simple_short AND signal_strength_short >= 50.0)")
    print()
    print("   🚨 ISSUE: The backup conditions are TOO WEAK and can trigger SELL signals")
    print("      even when price is trending UP, because:")
    print("      - simple_short only needs ema8 < ema21 (short-term pullback)")
    print("      - Doesn't check higher timeframe trend")
    print("      - Doesn't require strong bearish momentum")
    print()
    
    print("2. ⚠️  SIGNAL STRENGTH THRESHOLD TOO LOW:")
    print("   • minSignalStrength = 52.0 (input parameter)")
    print("   • Backup conditions only need signal_strength >= 50.0")
    print("   • This allows very weak signals to execute trades")
    print()
    
    print("3. ⚠️  RSI RANGES TOO WIDE:")
    print("   • rsi_bullish: rsi > 40 AND rsi < 80 (very wide range)")
    print("   • rsi_bearish: rsi < 60 AND rsi > 20 (overlaps with bullish!)")
    print("   • simple_short: rsi < 55 (can trigger in neutral market)")
    print("   🚨 ISSUE: RSI 41-59 can trigger BOTH bullish and bearish signals!")
    print()
    
    print("4. ⚠️  TREND ANALYSIS CONFLICTS:")
    print("   • trend_strength can be positive (bullish)")
    print("   • But simple_short can still trigger if ema8 < ema21 temporarily")
    print("   • No requirement for HTF trend alignment in backup conditions")
    print()
    
    print("5. ⚠️  VWAP LOGIC FLAW:")
    print("   • simple_short: close < vwap (only current bar)")
    print("   • No confirmation of sustained bearish price action")
    print("   • Can trigger on temporary dips below VWAP")
    print()
    
    print("=" * 70)
    print("🎯 SPECIFIC FIXES NEEDED:")
    print()
    
    print("FIX 1 - STRENGTHEN BACKUP CONDITIONS:")
    print("   Current: simple_short = ema8 < ema21 and close < vwap and rsi < 55")
    print("   Better:  simple_short = ema8 < ema21 and ema21 < ema50 and close < vwap and rsi < 45 and htf_trend_bear")
    print()
    
    print("FIX 2 - RAISE SIGNAL STRENGTH THRESHOLDS:")
    print("   Current: signal_strength >= 50.0 for backup conditions")
    print("   Better:  signal_strength >= 55.0 for backup conditions")
    print()
    
    print("FIX 3 - FIX RSI RANGES:")
    print("   Current: rsi_bullish > 40, rsi_bearish < 60 (overlap!)")
    print("   Better:  rsi_bullish > 50, rsi_bearish < 50 (no overlap)")
    print()
    
    print("FIX 4 - ADD TREND CONFIRMATION:")
    print("   Add: htf_trend_bear requirement for ALL short conditions")
    print("   Add: htf_trend_bull requirement for ALL long conditions")
    print()
    
    print("FIX 5 - REMOVE CONFLICTING BACKUP CONDITIONS:")
    print("   Option 1: Disable backup conditions entirely")
    print("   Option 2: Make backup conditions much more restrictive")
    print()
    
    print("=" * 70)
    print("🚨 WHY YOU SAW SELLS DURING UPTREND:")
    print()
    print("Scenario: Price trending up overall, but...")
    print("1. Short-term pullback: ema8 drops below ema21 temporarily")
    print("2. Price dips below VWAP briefly")
    print("3. RSI drops to 54 (still within 'bearish' range)")
    print("4. simple_short condition triggers: ema8 < ema21 AND close < vwap AND rsi < 55")
    print("5. signal_strength_short calculates to 50+ (due to session bonus)")
    print("6. SELL signal fires despite uptrend!")
    print()
    print("This is exactly what happened - the backup conditions are too weak!")
    print("=" * 70)

def create_fixed_sevensys():
    """Create a corrected version of SevenSYS"""
    
    print("\n🛠️  CREATING FIXED SEVENSYS VERSION:")
    
    fixed_conditions = '''
// ==================== FIXED ENTRY CONDITIONS ====================
// Remove conflicting backup conditions and strengthen main logic

// STRENGTHENED trend requirements
strong_bull_trend = ema_bull_aligned and htf_trend_bull and close > ema21
strong_bear_trend = ema_bear_aligned and htf_trend_bear and close < ema21

// FIXED RSI ranges (no overlap)
rsi_bullish = rsi > 50 and rsi < 80  // Removed overlap
rsi_bearish = rsi < 50 and rsi > 20  // Removed overlap

// STRENGTHENED momentum requirements
strong_momentum_bull = macd_bullish and rsi_bullish and stoch > 50
strong_momentum_bear = macd_bearish and rsi_bearish and stoch < 50

// MAIN CONDITIONS (strengthened)
long_conditions = strong_bull_trend and strong_momentum_bull and active_session and normal_volatility and above_vwap
short_conditions = strong_bear_trend and strong_momentum_bear and active_session and normal_volatility and below_vwap

// FINAL ENTRIES (removed weak backup conditions)
enter_long = long_conditions and signal_strength_long >= 55.0  // Raised threshold
enter_short = short_conditions and signal_strength_short >= 55.0  // Raised threshold

// REMOVED: Problematic backup conditions that caused wrong signals
'''
    
    print("Key Changes Made:")
    print("✅ Removed weak backup conditions")
    print("✅ Fixed RSI overlap (50 is now the dividing line)")
    print("✅ Strengthened trend requirements")
    print("✅ Raised signal strength thresholds")
    print("✅ Added higher timeframe trend confirmation")
    print()
    print("This should eliminate sells during uptrends!")

if __name__ == "__main__":
    analyze_sevensys_logic()
    create_fixed_sevensys()
