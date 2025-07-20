import os
import pandas as pd
import logging
from datetime import datetime
from model_trainer import ModelTrainer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_strategies():
    """Test trading strategies with different parameters"""
    try:
        # Load historical data
        historical_data = pd.read_csv('data/historical_trades.csv')
        
        # Initialize model trainer
        model_trainer = ModelTrainer()
        
        # Test different parameter combinations
        strategies = [
            {
                'name': 'Conservative',
                'confidence_threshold': 0.7,
                'risk_reward_min': 2.0,
                'max_risk_per_trade': 0.01
            },
            {
                'name': 'Moderate',
                'confidence_threshold': 0.6,
                'risk_reward_min': 1.5,
                'max_risk_per_trade': 0.02
            },
            {
                'name': 'Aggressive',
                'confidence_threshold': 0.5,
                'risk_reward_min': 1.2,
                'max_risk_per_trade': 0.03
            }
        ]
        
        results = []
        for strategy in strategies:
            logger.info(f"\nTesting {strategy['name']} strategy...")
            
            # Filter trades based on strategy parameters
            strategy_trades = historical_data[
                (historical_data['risk_reward_ratio'] >= strategy['risk_reward_min'])
            ].copy()
            
            # Train model on filtered data
            model_result = model_trainer.train_model(strategy_trades)
            
            # Calculate strategy performance
            win_rate = (strategy_trades['profitable'].astype(bool).mean() * 100)
            profit_factor = (
                abs(strategy_trades[strategy_trades['profit'] > 0]['profit'].sum()) /
                abs(strategy_trades[strategy_trades['profit'] < 0]['profit'].sum())
            )
            
            results.append({
                'strategy': strategy['name'],
                'trades': len(strategy_trades),
                'win_rate': win_rate,
                'profit_factor': profit_factor,
                'test_accuracy': model_result['test_accuracy'],
                'parameters': strategy
            })
            
            logger.info(f"Win Rate: {win_rate:.2f}%")
            logger.info(f"Profit Factor: {profit_factor:.2f}")
            logger.info(f"Test Accuracy: {model_result['test_accuracy']:.2f}")
        
        # Save results
        results_df = pd.DataFrame(results)
        os.makedirs('data/strategy_tests', exist_ok=True)
        results_df.to_csv(f'data/strategy_tests/results_{datetime.now().strftime("%Y%m%d")}.csv', index=False)
        
        logger.info("\nStrategy testing completed successfully")
        return results
        
    except Exception as e:
        logger.error(f"Strategy testing failed: {str(e)}")
        return None

if __name__ == '__main__':
    test_strategies()
