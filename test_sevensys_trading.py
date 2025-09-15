#!/usr/bin/env python3
"""
SEVENSYS TRADING SYSTEM TEST
Comprehensive validation of Pine Script trading logic
Tests signal generation, entry conditions, and trade execution
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class SevenSYSTradingTest:
    def __init__(self):
        self.test_results = {}
        self.trade_count = 0
        self.signal_strength_threshold = 35.0
        
    def simulate_market_data(self, bars=1000):
        """Generate realistic market data for testing"""
        np.random.seed(42)  # For reproducible results
        
        # Generate EUR/USD-like price data
        base_price = 1.0800
        price_changes = np.random.normal(0, 0.0002, bars)  # Small price movements
        prices = [base_price]
        
        for change in price_changes:
            new_price = prices[-1] + change
            prices.append(max(1.0400, min(1.1200, new_price)))  # Keep in realistic range
        
        # Create OHLC data
        data = []
        for i in range(len(prices) - 1):
            open_price = prices[i]
            close_price = prices[i + 1]
            
            # Generate high/low based on volatility
            volatility = abs(close_price - open_price) * 2
            high = max(open_price, close_price) + volatility
            low = min(open_price, close_price) - volatility
            
            # Generate volume (EUR/USD typical range)
            volume = np.random.uniform(50000, 200000)
            
            data.append({
                'timestamp': datetime.now() - timedelta(minutes=15 * (bars - i)),
                'open': round(open_price, 5),
                'high': round(high, 5),
                'low': round(low, 5),
                'close': round(close_price, 5),
                'volume': int(volume)
            })
        
        return pd.DataFrame(data)
    
    def calculate_emas(self, df):
        """Calculate EMA indicators"""
        df['ema8'] = df['close'].ewm(span=8).mean()
        df['ema21'] = df['close'].ewm(span=21).mean()
        df['ema50'] = df['close'].ewm(span=50).mean()
        df['ema200'] = df['close'].ewm(span=200).mean()
        return df
    
    def calculate_rsi(self, df, period=14):
        """Calculate RSI indicator"""
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        df['rsi'] = rsi
        return df
    
    def calculate_macd(self, df):
        """Calculate MACD indicator"""
        ema12 = df['close'].ewm(span=12).mean()
        ema26 = df['close'].ewm(span=26).mean()
        df['macd_line'] = ema12 - ema26
        df['macd_signal'] = df['macd_line'].ewm(span=9).mean()
        df['macd_histogram'] = df['macd_line'] - df['macd_signal']
        return df
    
    def calculate_atr(self, df, period=14):
        """Calculate ATR for stop loss calculation"""
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        df['atr'] = true_range.rolling(window=period).mean()
        return df
    
    def check_trend_conditions(self, row):
        """Check trend alignment conditions"""
        # EMA alignment checks
        ema_bull_weak = row['ema8'] > row['ema21'] and row['close'] > row['ema21']
        ema_bear_weak = row['ema8'] < row['ema21'] and row['close'] < row['ema21']
        
        # Base trend strength (simplified)
        if ema_bull_weak:
            base_trend_strength = 5.0
        elif ema_bear_weak:
            base_trend_strength = -5.0
        else:
            base_trend_strength = 0.0
        
        return {
            'trend_strength': base_trend_strength,
            'ema_bull_weak': ema_bull_weak,
            'ema_bear_weak': ema_bear_weak
        }
    
    def check_momentum_conditions(self, row):
        """Check momentum conditions"""
        # RSI conditions (FIXED logic)
        rsi_bullish_confirmed = 45 < row['rsi'] < 75
        rsi_bearish_confirmed = 25 < row['rsi'] < 55
        
        # MACD conditions
        macd_bullish_basic = row['macd_line'] > row['macd_signal']
        macd_bearish_basic = row['macd_line'] < row['macd_signal']
        
        # Momentum score (simplified)
        momentum_score = 0.0
        if rsi_bullish_confirmed and macd_bullish_basic:
            momentum_score = 8.0
        elif rsi_bearish_confirmed and macd_bearish_basic:
            momentum_score = -8.0
        
        return {
            'momentum_score': momentum_score,
            'rsi_bullish_confirmed': rsi_bullish_confirmed,
            'rsi_bearish_confirmed': rsi_bearish_confirmed,
            'macd_bullish_basic': macd_bullish_basic,
            'macd_bearish_basic': macd_bearish_basic
        }
    
    def calculate_signal_strength(self, trend_data, momentum_data):
        """Calculate signal strength"""
        base_strength = 25.0
        session_quality = 2.0  # Assume active session
        
        # Long signal strength
        signal_strength_long = base_strength + (session_quality * 4.0)
        if trend_data['trend_strength'] > 0:
            signal_strength_long += trend_data['trend_strength'] * 1.6
        if momentum_data['momentum_score'] > 0:
            signal_strength_long += momentum_data['momentum_score'] * 1.4
        
        # Short signal strength  
        signal_strength_short = base_strength + (session_quality * 4.0)
        if trend_data['trend_strength'] < 0:
            signal_strength_short += abs(trend_data['trend_strength']) * 1.6
        if momentum_data['momentum_score'] < 0:
            signal_strength_short += abs(momentum_data['momentum_score']) * 1.4
        
        return signal_strength_long, signal_strength_short
    
    def check_entry_conditions(self, row):
        """Check if entry conditions are met"""
        trend_data = self.check_trend_conditions(row)
        momentum_data = self.check_momentum_conditions(row)
        
        signal_strength_long, signal_strength_short = self.calculate_signal_strength(
            trend_data, momentum_data
        )
        
        # Relaxed entry conditions from our Pine script
        long_trend_ok = (trend_data['trend_strength'] > 0.5 and 
                        trend_data['ema_bull_weak'])
        
        long_momentum_ok = (momentum_data['momentum_score'] > -5.0 and 
                           momentum_data['rsi_bullish_confirmed'] and 
                           momentum_data['macd_bullish_basic'])
        
        short_trend_ok = (trend_data['trend_strength'] < -0.5 and 
                         trend_data['ema_bear_weak'])
        
        short_momentum_ok = (momentum_data['momentum_score'] < 5.0 and 
                            momentum_data['rsi_bearish_confirmed'] and 
                            momentum_data['macd_bearish_basic'])
        
        # Final entry signals
        enter_long = (long_trend_ok and long_momentum_ok and 
                     signal_strength_long >= self.signal_strength_threshold)
        
        enter_short = (short_trend_ok and short_momentum_ok and 
                      signal_strength_short >= self.signal_strength_threshold)
        
        return {
            'enter_long': enter_long,
            'enter_short': enter_short,
            'signal_strength_long': signal_strength_long,
            'signal_strength_short': signal_strength_short,
            'long_trend_ok': long_trend_ok,
            'long_momentum_ok': long_momentum_ok,
            'short_trend_ok': short_trend_ok,
            'short_momentum_ok': short_momentum_ok
        }
    
    def simulate_trading(self, df):
        """Simulate trading with the SevenSYS logic"""
        trades = []
        position = None
        
        print("🔄 Running SevenSYS Trading Simulation...")
        print("=" * 60)
        
        for i, row in df.iterrows():
            if i < 200:  # Skip first 200 bars for indicator warmup
                continue
                
            entry_conditions = self.check_entry_conditions(row)
            
            # Close existing position if opposite signal
            if position:
                if ((position['type'] == 'LONG' and entry_conditions['enter_short']) or
                    (position['type'] == 'SHORT' and entry_conditions['enter_long'])):
                    
                    # Calculate P&L
                    if position['type'] == 'LONG':
                        pnl = row['close'] - position['entry_price']
                    else:
                        pnl = position['entry_price'] - row['close']
                    
                    position['exit_price'] = row['close']
                    position['exit_time'] = row['timestamp']
                    position['pnl'] = pnl
                    position['pnl_pips'] = pnl * 10000
                    
                    trades.append(position.copy())
                    position = None
                    
                    print(f"📊 Trade #{len(trades)} CLOSED:")
                    print(f"   Type: {trades[-1]['type']}")
                    print(f"   P&L: {trades[-1]['pnl_pips']:.1f} pips")
                    print()
            
            # Enter new position
            if not position:
                if entry_conditions['enter_long']:
                    # Calculate stop loss and take profit
                    atr_stop = row['atr'] * 2.5
                    stop_loss = row['close'] - atr_stop
                    take_profit = row['close'] + (atr_stop * 2.5)
                    
                    position = {
                        'type': 'LONG',
                        'entry_price': row['close'],
                        'entry_time': row['timestamp'],
                        'stop_loss': stop_loss,
                        'take_profit': take_profit,
                        'signal_strength': entry_conditions['signal_strength_long']
                    }
                    
                    print(f"🟢 LONG ENTRY:")
                    print(f"   Price: {row['close']:.5f}")
                    print(f"   Signal Strength: {entry_conditions['signal_strength_long']:.1f}")
                    print(f"   Stop Loss: {stop_loss:.5f}")
                    print(f"   Take Profit: {take_profit:.5f}")
                    print()
                
                elif entry_conditions['enter_short']:
                    # Calculate stop loss and take profit
                    atr_stop = row['atr'] * 2.5
                    stop_loss = row['close'] + atr_stop
                    take_profit = row['close'] - (atr_stop * 2.5)
                    
                    position = {
                        'type': 'SHORT',
                        'entry_price': row['close'],
                        'entry_time': row['timestamp'],
                        'stop_loss': stop_loss,
                        'take_profit': take_profit,
                        'signal_strength': entry_conditions['signal_strength_short']
                    }
                    
                    print(f"🔴 SHORT ENTRY:")
                    print(f"   Price: {row['close']:.5f}")
                    print(f"   Signal Strength: {entry_conditions['signal_strength_short']:.1f}")
                    print(f"   Stop Loss: {stop_loss:.5f}")
                    print(f"   Take Profit: {take_profit:.5f}")
                    print()
        
        return trades
    
    def analyze_results(self, trades):
        """Analyze trading results"""
        if not trades:
            print("❌ NO TRADES GENERATED!")
            print("This indicates the entry conditions are too restrictive.")
            return
        
        print("📈 TRADING RESULTS ANALYSIS")
        print("=" * 60)
        
        total_trades = len(trades)
        winning_trades = len([t for t in trades if t['pnl'] > 0])
        losing_trades = total_trades - winning_trades
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        total_pnl = sum(t['pnl'] for t in trades)
        total_pips = sum(t['pnl_pips'] for t in trades)
        
        avg_win = np.mean([t['pnl_pips'] for t in trades if t['pnl'] > 0]) if winning_trades > 0 else 0
        avg_loss = np.mean([t['pnl_pips'] for t in trades if t['pnl'] < 0]) if losing_trades > 0 else 0
        
        print(f"Total Trades: {total_trades}")
        print(f"Winning Trades: {winning_trades}")
        print(f"Losing Trades: {losing_trades}")
        print(f"Win Rate: {win_rate:.1f}%")
        print(f"Total P&L: {total_pips:.1f} pips")
        print(f"Average Win: {avg_win:.1f} pips")
        print(f"Average Loss: {avg_loss:.1f} pips")
        
        if avg_loss != 0:
            risk_reward = abs(avg_win / avg_loss)
            print(f"Risk/Reward Ratio: 1:{risk_reward:.2f}")
        
        # Trade distribution
        long_trades = [t for t in trades if t['type'] == 'LONG']
        short_trades = [t for t in trades if t['type'] == 'SHORT']
        
        print(f"\nTrade Distribution:")
        print(f"Long Trades: {len(long_trades)}")
        print(f"Short Trades: {len(short_trades)}")
        
        print("\n✅ SYSTEM VALIDATION:")
        if total_trades >= 5:
            print("✅ Trading frequency: GOOD (multiple trades generated)")
        else:
            print("⚠️  Trading frequency: LOW (may need further adjustment)")
        
        if win_rate >= 40:
            print("✅ Win rate: ACCEPTABLE")
        else:
            print("⚠️  Win rate: NEEDS IMPROVEMENT")
        
        if total_pips > 0:
            print("✅ Overall profitability: POSITIVE")
        else:
            print("⚠️  Overall profitability: NEGATIVE")
    
    def run_comprehensive_test(self):
        """Run comprehensive trading system test"""
        print("🤖 SEVENSYS COMPREHENSIVE TRADING TEST")
        print("=" * 60)
        print("Testing optimized Pine Script logic...")
        print("Signal Strength Threshold: 35.0")
        print("Timeframe: 15 minutes")
        print("Instrument: EUR/USD")
        print()
        
        # Generate test data
        df = self.simulate_market_data(1000)
        
        # Calculate indicators
        df = self.calculate_emas(df)
        df = self.calculate_rsi(df)
        df = self.calculate_macd(df)
        df = self.calculate_atr(df)
        
        # Run trading simulation
        trades = self.simulate_trading(df)
        
        # Analyze results
        self.analyze_results(trades)
        
        return trades

def main():
    """Run the SevenSYS trading system test"""
    tester = SevenSYSTradingTest()
    trades = tester.run_comprehensive_test()
    
    # Save results
    if trades:
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_trades': len(trades),
            'trade_details': trades
        }
        
        with open('sevensys_test_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Results saved to: sevensys_test_results.json")
    
    print("\n🎯 NEXT STEPS:")
    print("1. If trades are generated: System is working correctly")
    print("2. If no trades: Further relaxation of conditions needed")
    print("3. Test in TradingView Strategy Tester for real market data")

if __name__ == "__main__":
    main()
