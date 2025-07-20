import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import random
from market_data import MarketData
from model_trainer import ModelTrainer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradeDataGenerator:
    def __init__(self):
        self.market_data = MarketData()
        self.model_trainer = ModelTrainer()
        self.pairs = ['EUR_USD', 'GBP_USD', 'USD_JPY', 'AUD_USD', 'USD_CAD']
        
        # Define the columns we'll generate
        self.columns = [
            'timestamp', 'pair', 'trend', 'volatility', 'volume',
            'rsi', 'macd_diff', 'price_to_sma20', 'price_to_sma50',
            'atr', 'cci', 'risk_reward_ratio', 'hour_of_day',
            'profit', 'profitable', 'success_probability'
        ]
        
    def generate_market_conditions(self):
        """Generate realistic market conditions"""
        return {
            'trend': random.choice(['uptrend', 'downtrend', 'sideways']),
            'volatility': random.uniform(0.1, 0.9),
            'volume_analysis': random.uniform(0.2, 1.0),
            'indicators': {
                'rsi_14': random.uniform(20, 80),
                'macd': random.uniform(-0.002, 0.002),
                'macd_signal': random.uniform(-0.002, 0.002),
                'sma_20': random.uniform(1.0500, 1.1500),
                'sma_50': random.uniform(1.0400, 1.1600),
                'atr': random.uniform(0.0005, 0.0020),
                'cci': random.uniform(-200, 200)
            }
        }
    
    def generate_trade_setup(self, pair, entry_price):
        """Generate a trade setup with realistic parameters"""
        action = random.choice(['buy', 'sell'])
        pip_value = 0.0001 if 'JPY' not in pair else 0.01
        
        # More conservative risk management
        stop_loss_pips = random.uniform(10, 30) * pip_value
        take_profit_pips = stop_loss_pips * random.uniform(1.5, 2.5)  # Maintain good risk:reward
        
        return {
            'pair': pair,
            'action': action,
            'entry': entry_price,
            'stop_loss': entry_price - stop_loss_pips if action == 'buy' else entry_price + stop_loss_pips,
            'take_profit': entry_price + take_profit_pips if action == 'buy' else entry_price - take_profit_pips,
            'units': random.choice([1000, 2000, 5000, 10000]),
            'confidence': random.uniform(0.6, 0.95)
        }
    
    def simulate_trade_outcome(self, trade_setup, market_conditions):
        """Simulate trade outcome based on setup and conditions"""
        # Weight factors for success probability
        weights = {
            'trend_alignment': 0.3,
            'volatility_fit': 0.2,
            'indicator_signals': 0.3,
            'volume_quality': 0.2
        }
        
        # Calculate success probability components
        trend_alignment = 0.7 if (
            (trade_setup['action'] == 'buy' and market_conditions['trend'] == 'uptrend') or
            (trade_setup['action'] == 'sell' and market_conditions['trend'] == 'downtrend')
        ) else 0.3
        
        volatility_fit = 0.6 if 0.3 <= market_conditions['volatility'] <= 0.7 else 0.4
        
        rsi = market_conditions['indicators']['rsi_14']
        indicator_signals = 0.8 if (
            (trade_setup['action'] == 'buy' and rsi < 40) or
            (trade_setup['action'] == 'sell' and rsi > 60)
        ) else 0.3
        
        volume_quality = market_conditions['volume_analysis']
        
        # Calculate overall success probability
        success_prob = (
            weights['trend_alignment'] * trend_alignment +
            weights['volatility_fit'] * volatility_fit +
            weights['indicator_signals'] * indicator_signals +
            weights['volume_quality'] * volume_quality
        )
        
        # Determine outcome
        is_successful = random.random() < success_prob
        
        # Calculate profit/loss
        if is_successful:
            profit = abs(trade_setup['take_profit'] - trade_setup['entry'])
        else:
            profit = -abs(trade_setup['stop_loss'] - trade_setup['entry'])
        
        return {
            'profitable': is_successful,
            'profit': profit,
            'success_probability': success_prob
        }
    
    def generate_historical_trades(self, num_trades=8000):
        """Generate historical trade data for model training"""
        logger.info(f"Generating {num_trades} historical trades...")
        trades = []
        start_date = datetime.now() - timedelta(days=365)
        
        for i in range(num_trades):
            if i % 100 == 0:
                logger.info(f"Generated {i} trades...")
            
            # Generate trade data
            pair = random.choice(self.pairs)
            trade_date = start_date + timedelta(
                minutes=random.randint(0, 525600)  # Minutes in a year
            )
            
            # Generate market conditions
            market_conditions = self.generate_market_conditions()
            base_price = random.uniform(1.0500, 1.1500)
            
            # Generate trade setup
            trade_setup = self.generate_trade_setup(pair, base_price)
            
            # Simulate outcome
            outcome = self.simulate_trade_outcome(trade_setup, market_conditions)
            
            # Convert all data to a DataFrame row
            trade_data = {
                'timestamp': trade_date.isoformat(),
                'pair': pair,
                'trend': market_conditions['trend'],
                'volatility': float(market_conditions['volatility']),
                'volume': float(market_conditions['volume_analysis']),
                'rsi': float(market_conditions['indicators']['rsi_14']),
                'macd_diff': float(market_conditions['indicators']['macd'] - 
                                 market_conditions['indicators']['macd_signal']),
                'price_to_sma20': float(base_price / market_conditions['indicators']['sma_20']),
                'price_to_sma50': float(base_price / market_conditions['indicators']['sma_50']),
                'atr': float(market_conditions['indicators']['atr']),
                'cci': float(market_conditions['indicators']['cci']),
                'risk_reward_ratio': float(abs(trade_setup['take_profit'] - trade_setup['entry']) /
                                        abs(trade_setup['stop_loss'] - trade_setup['entry'])),
                'hour_of_day': int(trade_date.hour),
                'profit': float(outcome['profit']),
                'profitable': bool(outcome['profitable']),
                'success_probability': float(outcome['success_probability'])
            }
            # Convert to pandas Series with consistent types
            trade_series = pd.Series({
                'timestamp': pd.to_datetime(trade_data['timestamp']),
                'pair': str(trade_data['pair']),
                'trend': str(trade_data['trend']),
                'volatility': float(trade_data['volatility']),
                'volume': float(trade_data['volume']),
                'rsi': float(trade_data['rsi']),
                'macd_diff': float(trade_data['macd_diff']),
                'price_to_sma20': float(trade_data['price_to_sma20']),
                'price_to_sma50': float(trade_data['price_to_sma50']),
                'atr': float(trade_data['atr']),
                'cci': float(trade_data['cci']),
                'risk_reward_ratio': float(trade_data['risk_reward_ratio']),
                'hour_of_day': int(trade_data['hour_of_day']),
                'profit': float(trade_data['profit']),
                'profitable': bool(trade_data['profitable']),
                'success_probability': float(trade_data['success_probability'])
            })
            trades.append(trade_series)
        
        # Convert to DataFrame and save
        df = pd.DataFrame(trades)
        os.makedirs('data', exist_ok=True)
        df.to_csv('data/historical_trades.csv', index=False)
        logger.info(f"Generated {num_trades} trades and saved to data/historical_trades.csv")
        
        # Train initial model
        self.model_trainer.train_model(df)
        logger.info("Initial model trained successfully")
        
        return df

if __name__ == '__main__':
    generator = TradeDataGenerator()
    historical_data = generator.generate_historical_trades(8000)
    
    # Print some statistics
    print("\n📊 Training Data Statistics:")
    print(f"Total Trades: {len(historical_data)}")
    print(f"Profitable Trades: {historical_data['profitable'].sum()}")
    print(f"Win Rate: {(historical_data['profitable'].mean() * 100):.2f}%")
    print(f"Average Profit: {historical_data['profit'].mean():.5f}")
    print(f"Profit Factor: {abs(historical_data[historical_data['profit'] > 0]['profit'].sum() / historical_data[historical_data['profit'] < 0]['profit'].sum()):.2f}")
