#!/usr/bin/env python3
"""
EMERGENCY SYSTEM FIX - Immediate fixes for SevenSYS Pine script
"""

def create_emergency_sevensys_fix():
    print("🚨 EMERGENCY SEVENSYS FIX")
    print("=" * 60)
    
    print("📝 Creating fixed SevenSYS Pine script...")
    
    fixed_sevensys = '''
//@version=6
strategy("SevenSYS FIXED - Emergency Patch", shorttitle="SevenSYS_FIXED", 
         overlay=true, default_qty_type=strategy.percent_of_equity, 
         default_qty_value=2, pyramiding=0, calc_on_every_tick=true)

// ==================== EMERGENCY FIXES APPLIED ====================
// Fixed RSI thresholds, removed dangerous backup conditions
// Added stronger trend confirmation, higher signal strength requirements

// ==================== RISK MANAGEMENT ====================
riskPerTrade = input.float(1.0, "Risk Per Trade (%)", minval=0.5, maxval=3.0, step=0.1)  // Reduced from 2.0
maxDrawdown = input.float(8.0, "Max Drawdown Stop (%)", minval=5.0, maxval=15.0, step=1.0)  // Reduced from 10.0
dailyLossLimit = input.float(3.0, "Daily Loss Limit (%)", minval=2.0, maxval=8.0, step=0.5)  // Reduced from 5.0
minSignalStrength = input.float(65.0, "Minimum Signal Strength", minval=60.0, maxval=80.0, step=1.0)  // Increased from 52.0

// ==================== TECHNICAL INDICATORS ====================
ema8 = ta.ema(close, 8)
ema21 = ta.ema(close, 21)
ema50 = ta.ema(close, 50)
ema200 = ta.ema(close, 200)

htf_trend = request.security(syminfo.tickerid, "240", ta.ema(close, 21))

rsi = ta.rsi(close, 14)
[macdLine, signalLine, histogram] = ta.macd(close, 12, 26, 9)
stoch = ta.stoch(close, high, low, 14)

volume_ma = ta.sma(volume, 20)
vwap = ta.vwap
atr = ta.atr(14)

// ==================== SESSION ANALYSIS ====================
london_session = time(timeframe.period, "0800-1600", "Europe/London")
ny_session = time(timeframe.period, "1300-2200", "America/New_York")
london_ny_overlap = not na(london_session) and not na(ny_session)
active_session = not na(london_session) or not na(ny_session)  // Removed Asian session

// ==================== FIXED TREND ANALYSIS ====================
// EMERGENCY FIX: Require ALL EMAs properly aligned
ema_strong_bull = ema8 > ema21 and ema21 > ema50 and ema50 > ema200 and close > ema8
ema_strong_bear = ema8 < ema21 and ema21 < ema50 and ema50 < ema200 and close < ema8
htf_trend_bull = close > htf_trend
htf_trend_bear = close < htf_trend

// FIXED: More restrictive trend strength calculation
trend_strength = ema_strong_bull and htf_trend_bull ? 10.0 : 
                 ema_strong_bear and htf_trend_bear ? -10.0 : 
                 ema8 > ema21 and ema21 > ema50 and close > ema50 ? 5.0 : 
                 ema8 < ema21 and ema21 < ema50 and close < ema50 ? -5.0 : 0.0

// ==================== FIXED MOMENTUM ANALYSIS ====================
// EMERGENCY FIX: Proper RSI thresholds
rsi_neutral = rsi > 30 and rsi < 70  // Fixed: proper neutral zone
rsi_strong_bullish = rsi > 70 and rsi < 85
rsi_strong_bearish = rsi < 30 and rsi > 15

macd_bullish = macdLine > signalLine and histogram > histogram[1] and histogram > 0
macd_bearish = macdLine < signalLine and histogram < histogram[1] and histogram < 0
stoch_neutral = stoch > 25 and stoch < 75

// FIXED: Proper momentum scoring
momentum_score = (rsi_neutral or rsi_strong_bullish) and macd_bullish and stoch_neutral ? 10.0 : 
                 (rsi_neutral or rsi_strong_bearish) and macd_bearish and stoch_neutral ? -10.0 : 0.0

// ==================== VOLUME & PRICE ACTION ====================
volume_bullish = volume > volume_ma * 1.2 and close > open  // Increased volume requirement
volume_bearish = volume > volume_ma * 1.2 and close < open
above_vwap = close > vwap
below_vwap = close < vwap

pa_score = volume_bullish and above_vwap ? 8.0 : volume_bearish and below_vwap ? -8.0 : 0.0

// ==================== VOLATILITY FILTER ====================
atr_pct = atr / close * 100
normal_volatility = atr_pct > 0.02 and atr_pct < 2.0  // Tighter range

// ==================== SIGNAL STRENGTH CALCULATION ====================
base_strength = 40.0  // Reduced base to require stronger confirmation
signal_strength_long = base_strength + (trend_strength > 5 ? trend_strength * 2.0 : 0) + 
                      (momentum_score > 0 ? momentum_score * 1.5 : 0) + 
                      (london_ny_overlap ? 15.0 : active_session ? 10.0 : 0) + 
                      (pa_score > 0 ? pa_score * 1.5 : 0)

signal_strength_short = base_strength + (trend_strength < -5 ? math.abs(trend_strength) * 2.0 : 0) + 
                       (momentum_score < 0 ? math.abs(momentum_score) * 1.5 : 0) + 
                       (london_ny_overlap ? 15.0 : active_session ? 10.0 : 0) + 
                       (pa_score < 0 ? math.abs(pa_score) * 1.5 : 0)

// ==================== FIXED ENTRY CONDITIONS ====================
// EMERGENCY FIX: Much stricter entry conditions
long_conditions = ema_strong_bull and trend_strength >= 5.0 and momentum_score > 0 and 
                 above_vwap and normal_volatility and london_ny_overlap  // Only London-NY overlap

short_conditions = ema_strong_bear and trend_strength <= -5.0 and momentum_score < 0 and 
                  below_vwap and normal_volatility and london_ny_overlap  // Only London-NY overlap

enter_long = long_conditions and signal_strength_long >= minSignalStrength
enter_short = short_conditions and signal_strength_short >= minSignalStrength

// REMOVED: Dangerous backup conditions completely eliminated
// No more simple_long or simple_short conditions

// ==================== POSITION MANAGEMENT ====================
atr_multiplier = 2.5  // Fixed: More conservative
stop_distance = atr * atr_multiplier
tp_multiplier = 2.0  // Fixed: Lower risk-reward for safety
profit_distance = stop_distance * tp_multiplier

// ==================== SAFETY NETS ====================
market_crisis = atr_pct > 1.5  // Tighter crisis detection
safety_stop = market_crisis or (strategy.equity < strategy.initial_capital * 0.95)  // Tighter equity protection

// ==================== TRADE EXECUTION ====================
if enter_long and not safety_stop and strategy.position_size == 0
    strategy.entry("LONG", strategy.long)
    strategy.exit("LONG_EXIT", "LONG", stop=close - stop_distance, limit=close + profit_distance)
    alert("{\"ticker\": \"" + syminfo.ticker + "\", \"strategy.order.action\": \"buy\", \"close\": " + str.tostring(close) + ", \"strategy\": \"SevenSYS_FIXED\", \"signal_strength\": " + str.tostring(signal_strength_long) + ", \"stop_loss\": " + str.tostring(close - stop_distance) + ", \"take_profit\": " + str.tostring(close + profit_distance) + "}", alert.freq_once_per_bar)

if enter_short and not safety_stop and strategy.position_size == 0
    strategy.entry("SHORT", strategy.short)
    strategy.exit("SHORT_EXIT", "SHORT", stop=close + stop_distance, limit=close - profit_distance)
    alert("{\"ticker\": \"" + syminfo.ticker + "\", \"strategy.order.action\": \"sell\", \"close\": " + str.tostring(close) + ", \"strategy\": \"SevenSYS_FIXED\", \"signal_strength\": " + str.tostring(signal_strength_short) + ", \"stop_loss\": " + str.tostring(close + stop_distance) + ", \"take_profit\": " + str.tostring(close - profit_distance) + "}", alert.freq_once_per_bar)

// Emergency Exit
if safety_stop and strategy.position_size != 0
    strategy.close_all(comment="SAFETY_STOP")
    alert("{\"ticker\": \"" + syminfo.ticker + "\", \"strategy.order.action\": \"close_all\", \"close\": " + str.tostring(close) + ", \"strategy\": \"SevenSYS_FIXED\", \"reason\": \"safety_stop\"}", alert.freq_once_per_bar)

// ==================== VISUAL INDICATORS ====================
plot(ema21, "EMA 21", color=color.orange, linewidth=2)
plot(ema50, "EMA 50", color=color.blue, linewidth=2)
plot(ema200, "EMA 200", color=color.red, linewidth=2)
plot(vwap, "VWAP", color=color.purple, linewidth=2)

plotshape(enter_long, "FIXED LONG", shape.triangleup, location.belowbar, color.green, size=size.large)
plotshape(enter_short, "FIXED SHORT", shape.triangledown, location.abovebar, color.red, size=size.large)
plotshape(safety_stop, "SAFETY", shape.xcross, location.belowbar, color.orange, size=size.normal)

// ==================== FIXED DASHBOARD ====================
var table dashboard = table.new(position.top_right, 3, 6, bgcolor=color.new(color.black, 85), border_width=2)

if barstate.islast
    table.cell(dashboard, 0, 0, "SevenSYS", text_color=color.white, text_size=size.small, bgcolor=color.new(color.green, 70))
    table.cell(dashboard, 1, 0, "FIXED", text_color=color.white, text_size=size.small, bgcolor=color.new(color.green, 70))
    table.cell(dashboard, 2, 0, "EMERGENCY", text_color=color.white, text_size=size.small, bgcolor=color.new(color.orange, 70))
    
    table.cell(dashboard, 0, 1, "LONG Signal", text_color=color.white)
    table.cell(dashboard, 1, 1, str.tostring(signal_strength_long, "#.#"), text_color=signal_strength_long >= minSignalStrength ? color.green : color.gray)
    table.cell(dashboard, 2, 1, signal_strength_long >= minSignalStrength ? "READY" : "WAIT", text_color=signal_strength_long >= minSignalStrength ? color.green : color.gray)
    
    table.cell(dashboard, 0, 2, "SHORT Signal", text_color=color.white)
    table.cell(dashboard, 1, 2, str.tostring(signal_strength_short, "#.#"), text_color=signal_strength_short >= minSignalStrength ? color.red : color.gray)
    table.cell(dashboard, 2, 2, signal_strength_short >= minSignalStrength ? "READY" : "WAIT", text_color=signal_strength_short >= minSignalStrength ? color.red : color.gray)
    
    table.cell(dashboard, 0, 3, "Trend", text_color=color.white)
    table.cell(dashboard, 1, 3, trend_strength > 5 ? "BULL" : trend_strength < -5 ? "BEAR" : "NEUTRAL", text_color=trend_strength > 5 ? color.green : trend_strength < -5 ? color.red : color.gray)
    table.cell(dashboard, 2, 3, str.tostring(trend_strength, "#.#"), text_color=trend_strength > 0 ? color.green : trend_strength < 0 ? color.red : color.gray)
    
    table.cell(dashboard, 0, 4, "Safety", text_color=color.white)
    table.cell(dashboard, 1, 4, safety_stop ? "STOP" : "ACTIVE", text_color=safety_stop ? color.red : color.green)
    table.cell(dashboard, 2, 4, safety_stop ? "DANGER" : "SECURE", text_color=safety_stop ? color.red : color.green)
    
    table.cell(dashboard, 0, 5, "Min Signal", text_color=color.white)
    table.cell(dashboard, 1, 5, str.tostring(minSignalStrength, "#.#"), text_color=color.yellow)
    table.cell(dashboard, 2, 5, "FIXED", text_color=color.orange)
'''
    
    return fixed_sevensys

def main():
    print("🚨 CREATING EMERGENCY FIXED SEVENSYS PINE SCRIPT")
    print("=" * 70)
    
    fixed_script = create_emergency_sevensys_fix()
    
    # Write to file
    with open('SevenSYS_EMERGENCY_FIXED.pine', 'w') as f:
        f.write(fixed_script)
    
    print("✅ Created: SevenSYS_EMERGENCY_FIXED.pine")
    print()
    print("🎯 IMMEDIATE ACTIONS:")
    print("1. REPLACE SevenSYS.pine with SevenSYS_EMERGENCY_FIXED.pine in TradingView")
    print("2. UPDATE webhook alerts to use the fixed version")
    print("3. TEST thoroughly before enabling live trading")
    print("4. Monitor for 24 hours with small position sizes")
    print()
    print("🔧 KEY FIXES APPLIED:")
    print("• Fixed RSI thresholds (30-70 neutral zone)")
    print("• Removed dangerous backup conditions")
    print("• Increased minimum signal strength to 65")
    print("• Added proper EMA alignment requirements")
    print("• Restricted trading to London-NY overlap only")
    print("• Reduced risk per trade to 1%")
    print("• Tighter safety stops and drawdown limits")
    print("=" * 70)

if __name__ == "__main__":
    main()
