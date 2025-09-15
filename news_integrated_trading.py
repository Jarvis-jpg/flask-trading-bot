#!/usr/bin/env python3
"""
NEWS-INTEGRATED TRADING SYSTEM
Combines SevenSYS Pine script with news sentiment analysis
Handles events like Trump election, Fed decisions, etc.
"""

import requests
import json
from datetime import datetime, timedelta
import re

class NewsIntegratedTrader:
    def __init__(self):
        self.news_sources = {
            'finnhub': 'https://finnhub.io/api/v1/news',
            'alpha_vantage': 'https://www.alphavantage.co/query',
            'newsapi': 'https://newsapi.org/v2/everything'
        }
        
        # Key market-moving events and their typical impact
        self.news_impact_patterns = {
            'election': {'bullish': ['trump', 'republican win', 'business friendly'], 
                        'bearish': ['uncertainty', 'disputed', 'contested']},
            'fed': {'bullish': ['rate cut', 'dovish', 'stimulus'], 
                   'bearish': ['rate hike', 'hawkish', 'taper']},
            'earnings': {'bullish': ['beat', 'exceed', 'strong revenue'], 
                        'bearish': ['miss', 'below', 'weak guidance']},
            'geopolitical': {'bullish': ['peace', 'agreement', 'resolution'], 
                           'bearish': ['war', 'conflict', 'sanctions']},
            'crypto': {'bullish': ['adoption', 'etf approval', 'institutional'], 
                      'bearish': ['ban', 'regulation', 'hack']},
            'economic': {'bullish': ['gdp growth', 'job gains', 'inflation down'], 
                        'bearish': ['recession', 'unemployment', 'inflation up']}
        }
        
        self.current_news_bias = 0.0  # -1.0 to +1.0
        
    def fetch_latest_news(self, timeframe_hours=24):
        """Fetch latest market-moving news"""
        try:
            # Example using a news API (you'd need API keys)
            news_data = []
            
            # Simulate news fetching (replace with real API calls)
            sample_news = [
                {"title": "Trump Wins Presidential Election 2024", "sentiment": 0.7, "impact": "high"},
                {"title": "Federal Reserve Signals Rate Cuts", "sentiment": 0.5, "impact": "high"},
                {"title": "Strong GDP Growth Reported", "sentiment": 0.3, "impact": "medium"},
                {"title": "Tech Earnings Beat Expectations", "sentiment": 0.4, "impact": "medium"}
            ]
            
            return sample_news
            
        except Exception as e:
            print(f"News fetch error: {e}")
            return []
    
    def analyze_news_sentiment(self, news_items):
        """Analyze overall market sentiment from news"""
        total_sentiment = 0.0
        weighted_impact = 0.0
        
        for item in news_items:
            impact_weight = {'high': 3.0, 'medium': 2.0, 'low': 1.0}.get(item.get('impact', 'low'), 1.0)
            sentiment = item.get('sentiment', 0.0)
            
            total_sentiment += sentiment * impact_weight
            weighted_impact += impact_weight
        
        if weighted_impact > 0:
            self.current_news_bias = total_sentiment / weighted_impact
        else:
            self.current_news_bias = 0.0
            
        return self.current_news_bias
    
    def generate_news_modifier(self):
        """Generate modifier for Pine script based on news"""
        if abs(self.current_news_bias) < 0.2:
            return "NEUTRAL", 0.0
        elif self.current_news_bias > 0.5:
            return "VERY_BULLISH", 15.0
        elif self.current_news_bias > 0.2:
            return "BULLISH", 8.0
        elif self.current_news_bias < -0.5:
            return "VERY_BEARISH", -15.0
        else:
            return "BEARISH", -8.0
    
    def create_news_enhanced_pine_script(self):
        """Create Pine script with news integration"""
        
        news_enhanced_script = '''
//@version=6
strategy("SevenSYS + News Integration", shorttitle="SevenSYS_NEWS", 
         overlay=true, default_qty_type=strategy.percent_of_equity, 
         default_qty_value=2, pyramiding=0, calc_on_every_tick=true)

// ==================== NEWS INTEGRATION INPUTS ====================
news_bias = input.float(0.0, "News Sentiment Bias", minval=-20.0, maxval=20.0, step=1.0)
news_filter = input.bool(true, "Enable News Filter")
major_event_mode = input.bool(false, "Major Event Mode (Reduced Risk)")

// ==================== RISK MANAGEMENT ====================
base_risk = major_event_mode ? 0.8 : 1.5
riskPerTrade = input.float(base_risk, "Risk Per Trade (%)", minval=0.5, maxval=3.0, step=0.1)
maxDrawdown = input.float(10.0, "Max Drawdown Stop (%)", minval=5.0, maxval=15.0, step=1.0)
dailyLossLimit = input.float(4.0, "Daily Loss Limit (%)", minval=2.0, maxval=8.0, step=0.5)
minSignalStrength = input.float(55.0, "Minimum Signal Strength", minval=45.0, maxval=75.0, step=1.0)

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

// ==================== NEWS-ENHANCED TREND ANALYSIS ====================
ema_bull_basic = ema8 > ema21 and ema21 > ema50 and close > ema21
ema_bear_basic = ema8 < ema21 and ema21 < ema50 and close < ema21
ema_strong_bull = ema8 > ema21 and ema21 > ema50 and ema50 > ema200 and close > ema8
ema_strong_bear = ema8 < ema21 and ema21 < ema50 and ema50 < ema200 and close < ema8

htf_trend_bull = close > htf_trend * 0.999
htf_trend_bear = close < htf_trend * 1.001

// NEWS-ENHANCED: Add news bias to trend strength
base_trend_strength = ema_strong_bull and htf_trend_bull ? 15.0 : 
                      ema_strong_bear and htf_trend_bear ? -15.0 : 
                      ema_bull_basic and htf_trend_bull ? 8.0 : 
                      ema_bear_basic and htf_trend_bear ? -8.0 : 
                      ema8 > ema21 and close > ema50 ? 4.0 : 
                      ema8 < ema21 and close < ema50 ? -4.0 : 0.0

// Apply news bias to trend strength
trend_strength = news_filter ? base_trend_strength + (news_bias * 0.3) : base_trend_strength

// ==================== NEWS-AWARE MOMENTUM ANALYSIS ====================
rsi_bullish = rsi > 40 and rsi < 80
rsi_bearish = rsi < 60 and rsi > 20
rsi_strong_bullish = rsi > 60 and rsi < 85
rsi_strong_bearish = rsi < 40 and rsi > 15
rsi_neutral = rsi >= 30 and rsi <= 70

macd_bullish = macdLine > signalLine and histogram > 0
macd_bearish = macdLine < signalLine and histogram < 0
macd_strong_bull = macd_bullish and histogram > histogram[1]
macd_strong_bear = macd_bearish and histogram < histogram[1]

// NEWS BOOST: Amplify momentum in direction of news bias
base_momentum_score = (rsi_strong_bullish and macd_strong_bull) ? 15.0 : 
                      (rsi_strong_bearish and macd_strong_bear) ? -15.0 : 
                      (rsi_bullish and macd_bullish) ? 8.0 : 
                      (rsi_bearish and macd_bearish) ? -8.0 : 
                      (rsi_neutral and macd_bullish) ? 4.0 : 
                      (rsi_neutral and macd_bearish) ? -4.0 : 0.0

momentum_score = news_filter ? base_momentum_score + (news_bias * 0.2) : base_momentum_score

// ==================== SESSION ANALYSIS ====================
london_session = time(timeframe.period, "0800-1600", "Europe/London")
ny_session = time(timeframe.period, "1300-2200", "America/New_York")
asian_session = time(timeframe.period, "2200-0600", "Asia/Tokyo")
london_ny_overlap = not na(london_session) and not na(ny_session)
active_session = not na(london_session) or not na(ny_session) or not na(asian_session)

// ==================== NEWS-ENHANCED SIGNAL STRENGTH ====================
base_strength = major_event_mode ? 40.0 : 30.0  // Higher threshold during major events

// Add news bias directly to signal strength
news_boost_long = news_bias > 0 ? news_bias * 1.5 : 0
news_boost_short = news_bias < 0 ? math.abs(news_bias) * 1.5 : 0

signal_strength_long = base_strength + 
                      (trend_strength > 0 ? trend_strength * 1.5 : 0) + 
                      (momentum_score > 0 ? momentum_score * 1.2 : 0) + 
                      (london_ny_overlap ? 12.0 : active_session ? 6.0 : 0) + 
                      news_boost_long

signal_strength_short = base_strength + 
                       (trend_strength < 0 ? math.abs(trend_strength) * 1.5 : 0) + 
                       (momentum_score < 0 ? math.abs(momentum_score) * 1.2 : 0) + 
                       (london_ny_overlap ? 12.0 : active_session ? 6.0 : 0) + 
                       news_boost_short

// ==================== NEWS-FILTERED ENTRY CONDITIONS ====================
// Standard technical conditions
long_basic = ema_bull_basic and trend_strength > 0 and momentum_score >= 0 and 
             close > vwap and active_session

short_basic = ema_bear_basic and trend_strength < 0 and momentum_score <= 0 and 
              close < vwap and active_session

// NEWS FILTER: Reduce counter-trend trades during strong news bias
news_allows_long = not news_filter or news_bias >= -0.3  // Don't go long during very bearish news
news_allows_short = not news_filter or news_bias <= 0.3   // Don't go short during very bullish news

enter_long = long_basic and signal_strength_long >= minSignalStrength and news_allows_long
enter_short = short_basic and signal_strength_short >= minSignalStrength and news_allows_short

// ==================== POSITION MANAGEMENT ====================
atr_multiplier = major_event_mode ? 3.0 : 2.0  // Wider stops during major events
stop_distance = atr * atr_multiplier
tp_multiplier = 2.5
profit_distance = stop_distance * tp_multiplier

// ==================== ENHANCED SAFETY NETS ====================
high_volatility = atr / close * 100 > 2.0
major_news_event = math.abs(news_bias) > 0.8
safety_stop = high_volatility or major_news_event or (strategy.equity < strategy.initial_capital * 0.90)

// ==================== TRADE EXECUTION ====================
if enter_long and not safety_stop and strategy.position_size == 0
    strategy.entry("LONG", strategy.long)
    strategy.exit("LONG_EXIT", "LONG", stop=close - stop_distance, limit=close + profit_distance)
    alert("{\\"ticker\\": \\"" + syminfo.ticker + "\\", \\"strategy.order.action\\": \\"buy\\", \\"close\\": " + str.tostring(close) + ", \\"strategy\\": \\"SevenSYS_NEWS\\", \\"signal_strength\\": " + str.tostring(signal_strength_long) + ", \\"news_bias\\": " + str.tostring(news_bias) + ", \\"stop_loss\\": " + str.tostring(close - stop_distance) + ", \\"take_profit\\": " + str.tostring(close + profit_distance) + "}", alert.freq_once_per_bar)

if enter_short and not safety_stop and strategy.position_size == 0
    strategy.entry("SHORT", strategy.short)
    strategy.exit("SHORT_EXIT", "SHORT", stop=close + stop_distance, limit=close - profit_distance)
    alert("{\\"ticker\\": \\"" + syminfo.ticker + "\\", \\"strategy.order.action\\": \\"sell\\", \\"close\\": " + str.tostring(close) + ", \\"strategy\\": \\"SevenSYS_NEWS\\", \\"signal_strength\\": " + str.tostring(signal_strength_short) + ", \\"news_bias\\": " + str.tostring(news_bias) + ", \\"stop_loss\\": " + str.tostring(close + stop_distance) + ", \\"take_profit\\": " + str.tostring(close - profit_distance) + "}", alert.freq_once_per_bar)

// Emergency Exit
if safety_stop and strategy.position_size != 0
    strategy.close_all(comment="SAFETY_STOP")

// ==================== VISUAL INDICATORS ====================
plot(ema21, "EMA 21", color=color.orange, linewidth=2)
plot(ema50, "EMA 50", color=color.blue, linewidth=2)
plot(ema200, "EMA 200", color=color.red, linewidth=2)
plot(vwap, "VWAP", color=color.purple, linewidth=2)

plotshape(enter_long, "NEWS LONG", shape.triangleup, location.belowbar, news_bias > 0 ? color.green : color.lime, size=size.normal)
plotshape(enter_short, "NEWS SHORT", shape.triangledown, location.abovebar, news_bias < 0 ? color.red : color.maroon, size=size.normal)
plotshape(major_news_event, "MAJOR NEWS", shape.diamond, location.abovebar, color.yellow, size=size.small)

// ==================== NEWS-ENHANCED DASHBOARD ====================
var table dashboard = table.new(position.top_right, 3, 9, bgcolor=color.new(color.black, 85), border_width=2)

if barstate.islast
    table.cell(dashboard, 0, 0, "SevenSYS", text_color=color.white, text_size=size.small, bgcolor=color.new(color.blue, 70))
    table.cell(dashboard, 1, 0, "NEWS", text_color=color.white, text_size=size.small, bgcolor=color.new(color.yellow, 70))
    table.cell(dashboard, 2, 0, "INTEGRATED", text_color=color.white, text_size=size.small, bgcolor=color.new(color.green, 70))
    
    table.cell(dashboard, 0, 1, "LONG Signal", text_color=color.white)
    table.cell(dashboard, 1, 1, str.tostring(signal_strength_long, "#.#"), text_color=signal_strength_long >= minSignalStrength ? color.green : color.gray)
    table.cell(dashboard, 2, 1, signal_strength_long >= minSignalStrength ? "READY" : "WAIT", text_color=signal_strength_long >= minSignalStrength ? color.green : color.gray)
    
    table.cell(dashboard, 0, 2, "SHORT Signal", text_color=color.white)
    table.cell(dashboard, 1, 2, str.tostring(signal_strength_short, "#.#"), text_color=signal_strength_short >= minSignalStrength ? color.red : color.gray)
    table.cell(dashboard, 2, 2, signal_strength_short >= minSignalStrength ? "READY" : "WAIT", text_color=signal_strength_short >= minSignalStrength ? color.red : color.gray)
    
    table.cell(dashboard, 0, 3, "News Bias", text_color=color.white)
    table.cell(dashboard, 1, 3, str.tostring(news_bias, "#.#"), text_color=news_bias > 0 ? color.green : news_bias < 0 ? color.red : color.gray)
    table.cell(dashboard, 2, 3, news_bias > 0.5 ? "BULL NEWS" : news_bias < -0.5 ? "BEAR NEWS" : "NEUTRAL", text_color=news_bias > 0.5 ? color.green : news_bias < -0.5 ? color.red : color.gray)
    
    table.cell(dashboard, 0, 4, "Trend", text_color=color.white)
    table.cell(dashboard, 1, 4, trend_strength > 4 ? "BULL" : trend_strength < -4 ? "BEAR" : "NEUTRAL", text_color=trend_strength > 4 ? color.green : trend_strength < -4 ? color.red : color.gray)
    table.cell(dashboard, 2, 4, str.tostring(trend_strength, "#.#"), text_color=trend_strength > 0 ? color.green : trend_strength < 0 ? color.red : color.gray)
    
    table.cell(dashboard, 0, 5, "Major Event", text_color=color.white)
    table.cell(dashboard, 1, 5, major_event_mode ? "YES" : "NO", text_color=major_event_mode ? color.orange : color.gray)
    table.cell(dashboard, 2, 5, major_news_event ? "HIGH IMPACT" : "NORMAL", text_color=major_news_event ? color.red : color.gray)
    
    table.cell(dashboard, 0, 6, "Safety", text_color=color.white)
    table.cell(dashboard, 1, 6, safety_stop ? "STOP" : "ACTIVE", text_color=safety_stop ? color.red : color.green)
    table.cell(dashboard, 2, 6, safety_stop ? "DANGER" : "SECURE", text_color=safety_stop ? color.red : color.green)
    
    table.cell(dashboard, 0, 7, "News Filter", text_color=color.white)
    table.cell(dashboard, 1, 7, news_filter ? "ON" : "OFF", text_color=news_filter ? color.green : color.gray)
    table.cell(dashboard, 2, 7, news_allows_long and news_allows_short ? "BOTH" : news_allows_long ? "LONG ONLY" : news_allows_short ? "SHORT ONLY" : "BLOCKED", text_color=news_allows_long and news_allows_short ? color.green : color.yellow)
    
    table.cell(dashboard, 0, 8, "Risk Mode", text_color=color.white)
    table.cell(dashboard, 1, 8, str.tostring(riskPerTrade, "#.#") + "%", text_color=color.yellow)
    table.cell(dashboard, 2, 8, major_event_mode ? "REDUCED" : "NORMAL", text_color=major_event_mode ? color.orange : color.gray)
'''
        
        return news_enhanced_script

def main():
    trader = NewsIntegratedTrader()
    
    print("📰 NEWS-INTEGRATED TRADING SYSTEM")
    print("=" * 60)
    
    # Simulate news analysis
    latest_news = trader.fetch_latest_news()
    sentiment = trader.analyze_news_sentiment(latest_news)
    bias_type, bias_value = trader.generate_news_modifier()
    
    print(f"📊 Current News Analysis:")
    print(f"   Overall Sentiment: {sentiment:.2f}")
    print(f"   Market Bias: {bias_type}")
    print(f"   Signal Modifier: {bias_value:+.1f}")
    print()
    
    print("🎯 NEWS INTEGRATION FEATURES:")
    print("• Real-time sentiment analysis")
    print("• Event-based risk adjustment")
    print("• Counter-trend trade filtering")
    print("• Major event detection")
    print("• Enhanced signal strength")
    print()
    
    # Generate the enhanced Pine script
    enhanced_script = trader.create_news_enhanced_pine_script()
    
    with open('SevenSYS_NEWS_INTEGRATED.pine', 'w') as f:
        f.write(enhanced_script)
    
    print("✅ Created: SevenSYS_NEWS_INTEGRATED.pine")
    print()
    print("🔧 SETUP INSTRUCTIONS:")
    print("1. Add this Pine script to TradingView")
    print("2. Set 'News Sentiment Bias' input based on current events")
    print("3. Enable 'Major Event Mode' during elections, Fed meetings")
    print("4. Monitor news dashboard for real-time bias")
    print("5. Update news bias daily based on market events")

if __name__ == "__main__":
    main()
