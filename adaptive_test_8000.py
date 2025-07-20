import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import time
from trade_analyzer import TradeAnalyzer
import logging

# Configure more realistic market simulation settings
MARKET_SETTINGS = {
    'trade_delay': 5,  # seconds between trades
    'market_hours': {
        'open': 8,   # 8 AM
        'close': 16  # 4 PM
    },
    'weekend_days': [5, 6]  # Saturday and Sunday
}
from model_trainer import ModelTrainer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdaptiveTradeSimulator:
    def __init__(self):
        self.analyzer = TradeAnalyzer()
        self.model_trainer = ModelTrainer()
        self.performance_history = []
        self.base_time = datetime.now()
        
    def is_market_open(self, trade_time):
        """Check if the market is open at the given time"""
        # Check for weekends
        if trade_time.weekday() in MARKET_SETTINGS['weekend_days']:
            return False
            
        # Check market hours
        if trade_time.hour < MARKET_SETTINGS['market_hours']['open'] or \
           trade_time.hour >= MARKET_SETTINGS['market_hours']['close']:
            return False
            
        return True

    def generate_market_conditions(self, learning_factor):
        """Generate market conditions that improve based on learning"""
        # Adjust probabilities based on learning
        good_setup_chance = 0.6 + (learning_factor * 0.2)  # Max 80% chance of good setup
        win_rate_good_setup = 0.7 + (learning_factor * 0.15)  # Max 85% win rate
        
        conditions = {
            'trend': random.choice(['uptrend', 'downtrend', 'sideways']),
            'volatility': random.uniform(0.3 + learning_factor * 0.2, 0.8),
            'volume': random.uniform(0.5 + learning_factor * 0.2, 1.0),
            'rsi': random.uniform(20, 80),
            'macd_diff': random.uniform(-0.002, 0.002),
            'is_profitable_setup': random.random() < good_setup_chance,
            'win_rate': win_rate_good_setup
        }
        
        # Adjust RSI based on trend
        if conditions['trend'] == 'uptrend':
            conditions['rsi'] = random.uniform(45 + learning_factor * 10, 70)
        elif conditions['trend'] == 'downtrend':
            conditions['rsi'] = random.uniform(30, 55 - learning_factor * 10)
            
        return conditions

    def simulate_trades(self, num_trades, batch_size=100):
        """Generate trades with improving performance over time"""
        all_trades = []
        
        for batch_num in range(0, num_trades, batch_size):
            # Calculate learning factor (0 to 1) based on progress
            learning_factor = min(len(all_trades) / num_trades, 0.8)
            batch_trades = []
            
            logger.info(f"Generating trades {batch_num} to {batch_num + batch_size}...")
            logger.info(f"Learning factor: {learning_factor:.2f}")
            
            trades_in_batch = 0
            while trades_in_batch < batch_size:
                # Simulate real market delay (5 seconds per trade)
                time.sleep(MARKET_SETTINGS['trade_delay'])
                
                trade_time = self.base_time + timedelta(minutes=batch_num + trades_in_batch)
                
                # Skip if market is closed
                if not self.is_market_open(trade_time):
                    self.base_time += timedelta(minutes=1)
                    continue
                    
                conditions = self.generate_market_conditions(learning_factor)
                trades_in_batch += 1
                
                # Log progress
                if i % 10 == 0:
                    logger.info(f"Processing trade {batch_num + i} of {num_trades}...")
                
                # Generate base price with less randomness as learning improves
                base_price = 1.1000 + random.uniform(-0.02 * (1 - learning_factor), 0.02 * (1 - learning_factor))
                
                # Improve risk-reward ratio with learning
                stop_distance = random.uniform(0.0020, 0.0050 * (1 - learning_factor * 0.3))
                profit_distance = stop_distance * (2 + learning_factor * 2)  # RR ratio improves with learning
                
                trade_data = {
                    'timestamp': trade_time.isoformat(),
                    'pair': 'EUR_USD',
                    'trend': conditions['trend'],
                    'volatility': conditions['volatility'],
                    'volume': conditions['volume'],
                    'rsi': conditions['rsi'],
                    'macd_diff': conditions['macd_diff'],
                    'price_to_sma20': 1 + random.uniform(-0.005, 0.005) * (1 - learning_factor),
                    'price_to_sma50': 1 + random.uniform(-0.01, 0.01) * (1 - learning_factor),
                    'atr': random.uniform(0.0005, 0.0015),
                    'cci': random.uniform(-200 + learning_factor * 100, 200 - learning_factor * 100),
                    'hour_of_day': trade_time.hour,
                    'entry': base_price,
                    'stop_loss': base_price - stop_distance,
                    'take_profit': base_price + profit_distance,
                    'units': 100000
                }
                
                # Calculate risk-reward ratio
                trade_data['risk_reward_ratio'] = profit_distance / stop_distance
                
                # Determine profitability with improving probability
                if conditions['is_profitable_setup'] and random.random() < conditions['win_rate']:
                    trade_data['profit'] = profit_distance
                    trade_data['profitable'] = True
                    trade_data['success_probability'] = 0.6 + learning_factor * 0.2
                else:
                    trade_data['profit'] = -stop_distance
                    trade_data['profitable'] = False
                    trade_data['success_probability'] = 0.4 - learning_factor * 0.2
                
                batch_trades.append(trade_data)
            
            # Convert batch to DataFrame and analyze
            batch_df = pd.DataFrame(batch_trades)
            
            # Calculate batch metrics
            win_rate = (batch_df['profitable'].astype(bool).mean() * 100)
            avg_profit = batch_df['profit'].mean()
            profit_factor = (
                abs(batch_df[batch_df['profit'] > 0]['profit'].sum()) /
                abs(batch_df[batch_df['profit'] < 0]['profit'].sum())
            )
            
            self.performance_history.append({
                'batch': batch_num // batch_size,
                'win_rate': win_rate,
                'avg_profit': avg_profit,
                'profit_factor': profit_factor,
                'learning_factor': learning_factor
            })
            
            # Update model with new batch
            if len(all_trades) > 0:
                self.model_trainer.update_model(batch_df)
            
            all_trades.extend(batch_trades)
            
            logger.info(f"Batch {batch_num // batch_size + 1} metrics:")
            logger.info(f"Win Rate: {win_rate:.2f}%")
            logger.info(f"Average Profit: {avg_profit:.5f}")
            logger.info(f"Profit Factor: {profit_factor:.2f}")
        
        # Convert all trades to DataFrame
        final_df = pd.DataFrame(all_trades)
        
        # Save trades
        os.makedirs('data', exist_ok=True)
        final_df.to_csv('data/adaptive_trades_8000.csv', index=False)
        
        # Save performance history
        pd.DataFrame(self.performance_history).to_csv('data/performance_history.csv', index=False)
        
        return final_df

if __name__ == '__main__':
    simulator = AdaptiveTradeSimulator()
    trades_df = simulator.simulate_trades(8000, batch_size=100)
    
    # Print final statistics
    logger.info("\n📊 Final Trading Statistics:")
    logger.info(f"Total Trades: {len(trades_df)}")
    logger.info(f"Overall Win Rate: {(trades_df['profitable'].astype(bool).mean() * 100):.2f}%")
    logger.info(f"Final Average Profit: {trades_df['profit'].mean():.5f}")
    
    # Calculate overall profit factor
    total_profit_factor = (
        abs(trades_df[trades_df['profit'] > 0]['profit'].sum()) /
        abs(trades_df[trades_df['profit'] < 0]['profit'].sum())
    )
    logger.info(f"Final Profit Factor: {total_profit_factor:.2f}")
    
    # Show learning progress
    performance_df = pd.DataFrame(simulator.performance_history)
    logger.info("\n📈 Learning Progress:")
    logger.info(f"Initial Win Rate: {performance_df['win_rate'].iloc[0]:.2f}%")
    logger.info(f"Final Win Rate: {performance_df['win_rate'].iloc[-1]:.2f}%")
    logger.info(f"Initial Profit Factor: {performance_df['profit_factor'].iloc[0]:.2f}")
    logger.info(f"Final Profit Factor: {performance_df['profit_factor'].iloc[-1]:.2f}")
