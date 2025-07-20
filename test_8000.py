import os
import pandas as pd
from datetime import datetime, timedelta
import random
from trade_analyzer import TradeAnalyzer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_test_trades():
    """Generate 8000 test trades with realistic market conditions"""
    trades = []
    analyzer = TradeAnalyzer()
    base_time = datetime.now()
    
    # Market conditions that lead to profitable trades
    profitable_conditions = {
        'trend': ['uptrend', 'downtrend'],  # Strong trends are better than sideways
        'volatility': (0.4, 0.8),  # Medium to high volatility
        'volume': (0.6, 1.0),  # Higher volume is better
        'rsi': [(20, 30), (70, 80)],  # Extreme RSI values for reversals
    }
    
    logger.info("Generating 8000 test trades...")
    
    for i in range(8000):
        if i % 100 == 0:
            logger.info(f"Generated {i} trades...")
            
        # Simulate time passing
        trade_time = base_time + timedelta(minutes=random.randint(1, 60*24*30))
        
        # Randomly select market conditions but bias towards profitable setups
        is_profitable_setup = random.random() < 0.6  # 60% chance of good setup
        
        if is_profitable_setup:
            trend = random.choice(profitable_conditions['trend'])
            volatility = random.uniform(*profitable_conditions['volatility'])
            volume = random.uniform(*profitable_conditions['volume'])
            rsi_range = random.choice(profitable_conditions['rsi'])
            rsi = random.uniform(*rsi_range)
        else:
            trend = random.choice(['uptrend', 'downtrend', 'sideways'])
            volatility = random.uniform(0.1, 1.0)
            volume = random.uniform(0.1, 1.0)
            rsi = random.uniform(30, 70)
        
        # Generate trade data
        base_price = random.uniform(1.0500, 1.1500)  # EUR/USD typical range
        trade_data = {
            'timestamp': trade_time.isoformat(),
            'pair': 'EUR_USD',
            'trend': trend,
            'volatility': volatility,
            'volume': volume,
            'rsi': rsi,
            'macd_diff': random.uniform(-0.002, 0.002),
            'price_to_sma20': random.uniform(0.995, 1.005),
            'price_to_sma50': random.uniform(0.99, 1.01),
            'atr': random.uniform(0.0005, 0.0015),
            'cci': random.uniform(-200, 200),
            'hour_of_day': trade_time.hour,
            'entry': base_price,
            'stop_loss': base_price - random.uniform(0.0020, 0.0050),
            'take_profit': base_price + random.uniform(0.0040, 0.0100),
            'units': 100000
        }
        
        # Calculate risk-reward ratio
        trade_data['risk_reward_ratio'] = (
            abs(trade_data['take_profit'] - trade_data['entry']) /
            abs(trade_data['stop_loss'] - trade_data['entry'])
        )
        
        # Determine if trade would be profitable based on conditions
        if is_profitable_setup and random.random() < 0.7:  # 70% win rate for good setups
            profit = random.uniform(0.0040, 0.0100)  # Take profit hit
            profitable = True
        else:
            profit = -random.uniform(0.0020, 0.0050)  # Stop loss hit
            profitable = False
        
        trade_data['profit'] = profit
        trade_data['profitable'] = profitable
        trade_data['success_probability'] = 0.7 if profitable else 0.3
        
        trades.append(trade_data)
    
    # Convert to DataFrame
    df = pd.DataFrame(trades)
    
    # Save to CSV
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/test_trades_8000.csv', index=False)
    
    # Calculate and log statistics
    win_rate = (df['profitable'].astype(bool).mean() * 100)
    avg_profit = df['profit'].mean()
    profit_factor = abs(df[df['profit'] > 0]['profit'].sum()) / abs(df[df['profit'] < 0]['profit'].sum())
    
    logger.info("\n📊 Test Trade Statistics:")
    logger.info(f"Total Trades: {len(df)}")
    logger.info(f"Win Rate: {win_rate:.2f}%")
    logger.info(f"Average Profit: {avg_profit:.5f}")
    logger.info(f"Profit Factor: {profit_factor:.2f}")
    
    return df

if __name__ == '__main__':
    # Generate test trades
    trades_df = generate_test_trades()
    
    # Test the analyzer with the generated trades
    analyzer = TradeAnalyzer()
    
    logger.info("\n🔄 Testing Trade Analysis...")
    successful_analyses = 0
    
    for i, trade in trades_df.iterrows():
        try:
            # Test immediate analysis
            analysis = analyzer.analyze_trade(trade['pair'], {
                'action': 'buy' if trade['profit'] > 0 else 'sell',
                'entry': trade['entry'],
                'stop_loss': trade['stop_loss'],
                'take_profit': trade['take_profit'],
                'units': trade['units']
            })
            
            if analysis.get('status') != 'error':
                successful_analyses += 1
                
        except Exception as e:
            logger.error(f"Error analyzing trade {i}: {str(e)}")
    
    logger.info(f"\n✅ Analysis Success Rate: {(successful_analyses/len(trades_df))*100:.2f}%")
