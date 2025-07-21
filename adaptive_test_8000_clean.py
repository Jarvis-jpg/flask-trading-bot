import logging
import random
import math
from datetime import datetime, timedelta
import time

class TradeSimulator:
    def __init__(self):
        self.performance_history = []
        self.total_trades = 0
        self.total_wins = 0
        self.learning_factor = 5.0  # Start with 5%
        self.base_time = datetime.now()
        
    def generate_market_conditions(self, learning_factor_decimal):
        """Generate simulated market conditions influenced by learning factor."""
        # Adjust probabilities based on learning
        good_setup_chance = 0.6 + (learning_factor_decimal * 0.2)  # Max 80% chance of good setup
        win_rate_good_setup = 0.7 + (learning_factor_decimal * 0.15)  # Max 85% win rate
        
        conditions = {
            'trend': random.choice(['uptrend', 'downtrend', 'sideways']),
            'volatility': random.uniform(0.3 + learning_factor_decimal * 0.2, 0.8),
            'volume': random.uniform(0.5 + learning_factor_decimal * 0.2, 1.0),
            'rsi': random.uniform(20, 80),
            'macd_diff': random.uniform(-0.002, 0.002),
            'is_profitable_setup': random.random() < good_setup_chance,
            'win_rate': win_rate_good_setup
        }
        
        # Adjust RSI based on trend
        if conditions['trend'] == 'uptrend':
            conditions['rsi'] = random.uniform(45 + learning_factor_decimal * 10, 70)
        elif conditions['trend'] == 'downtrend':
            conditions['rsi'] = random.uniform(30, 55 - learning_factor_decimal * 10)
        
        return conditions
        
    def calculate_learning_factor(self):
        """Calculate the learning factor based on performance."""
        trades_processed = len(self.performance_history)
        if trades_processed == 0:
            return 0.05  # Start with 5% learning
        
        # Calculate overall win rate
        wins = sum(1 for trade in self.performance_history if trade.get('profitable', False))
        win_rate = wins / trades_processed
        
        # Initialize early trading phase variables 
        min_trades_for_baseline = 20
        progress = min(1.0, trades_processed / min_trades_for_baseline)
        is_early_phase = trades_processed < min_trades_for_baseline
        
        # Enhanced recent performance (last 5 trades)
        recent_trades = min(5, trades_processed)
        recent_wins = sum(1 for i in range(recent_trades)
                         if i < len(self.performance_history) and
                         self.performance_history[-(i+1)].get('profitable', False))
        recent_win_rate = recent_wins / recent_trades if recent_trades > 0 else 0
        
        # Dynamic win rate contribution
        win_rate_threshold = 0.0 if is_early_phase else 0.25  # No threshold early
        win_rate_factor = max(0, win_rate - win_rate_threshold)
        win_rate_factor *= 2.5 if is_early_phase else 0.5  # Higher impact early
        
        # Enhanced progress contribution
        progress_contribution = progress * (0.25 if is_early_phase else 0.1)
        
        # Add recent performance bonus in early phase
        if is_early_phase:
            progress_contribution += recent_win_rate * 0.2  # Up to 20% extra
        
        # Enhanced early performance boost
        early_stage_bonus = 0.0
        if trades_processed < min_trades_for_baseline:
            # Stronger recent performance impact
            early_stage_bonus = recent_win_rate * 0.3  # Up to 30% boost for perfect recent performance
            
            # Improved consecutive wins bonus
            consecutive_wins = 0
            for i in range(min(3, trades_processed)):
                if i < len(self.performance_history) and self.performance_history[-(i+1)].get('profitable', False):
                    consecutive_wins += 1
                else:
                    break
            # Enhanced exponential bonus for streaks
            early_stage_bonus += (consecutive_wins * consecutive_wins * 0.06)  # 6%, 24%, 54% for 1,2,3 wins
        
        # Combined learning factor with minimum learning
        base_learning = 0.05  # 5% minimum learning
        raw_learning = base_learning + win_rate_factor + progress_contribution + early_stage_bonus
        
        # Minimal smoothing during early phase
        if hasattr(self, 'last_learning_factor'):
            smoothing = max(0.1, 0.3 - (recent_win_rate * 0.2)) if is_early_phase else 0.7
            smoothed_learning = (smoothing * self.last_learning_factor + (1 - smoothing) * raw_learning)
        else:
            smoothed_learning = raw_learning
        
        self.last_learning_factor = smoothed_learning
        return smoothed_learning
        
    def simulate_trades(self, num_trades):
        """Generate trades with improving performance over time."""
        logger = logging.getLogger(__name__)
        logger.info("🔄 Initializing Trade Simulator...")
        
        trades_processed = 0
        learning_factor_decimal = 0.05  # Start with 5% learning
        self.performance_history = []
        
        while trades_processed < num_trades:
            # Generate trade time and conditions
            trade_time = self.base_time + timedelta(minutes=trades_processed)
            conditions = self.generate_market_conditions(learning_factor_decimal)
            
            # Generate trade parameters with learning factor influence
            base_price = 1.1000 + random.uniform(-0.02 * (1 - learning_factor_decimal), 0.02 * (1 - learning_factor_decimal))
            stop_distance = random.uniform(0.0020, 0.0050 * (1 - learning_factor_decimal * 0.3))
            profit_distance = stop_distance * (2 + learning_factor_decimal * 2)  # RR ratio improves with learning
            
            # Create trade data
            trade_data = {
                'timestamp': trade_time.isoformat(),
                'pair': 'EUR_USD',
                'trend': conditions['trend'],
                'volatility': conditions['volatility'],
                'volume': conditions['volume'],
                'rsi': conditions['rsi'],
                'macd_diff': conditions['macd_diff'],
                'price_to_sma20': 1 + random.uniform(-0.005, 0.005) * (1 - learning_factor_decimal),
                'price_to_sma50': 1 + random.uniform(-0.01, 0.01) * (1 - learning_factor_decimal),
                'atr': random.uniform(0.0005, 0.0015),
                'cci': random.uniform(-200 + learning_factor_decimal * 100, 200 - learning_factor_decimal * 100),
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
                trade_data['success_probability'] = 0.6 + learning_factor_decimal * 0.2
            else:
                trade_data['profit'] = -stop_distance
                trade_data['profitable'] = False
                trade_data['success_probability'] = 0.4 - learning_factor_decimal * 0.2
            
            # Update performance tracking
            self.performance_history.append(trade_data)
            trades_processed += 1
            
            if trade_data['profitable']:
                self.total_wins += 1
            
            # Calculate statistics
            self.total_trades = trades_processed
            overall_win_rate = (self.total_wins / self.total_trades * 100)
            
            # Show progress for every trade
            logger.info(
                f"Trade {trades_processed:04d}/{num_trades} | "
                f"Win Rate: {overall_win_rate:.1f}% | "
                f"Result: {'✅ WIN' if trade_data['profitable'] else '❌ LOSS'} | "
                f"P/L: {trade_data['profit']:.5f} | "
                f"Learning: {learning_factor_decimal*100:.2f}%")
            
            # Add significant delay between trades for detailed analysis
            time.sleep(10)  # 10 second delay between trades
            
            # Update learning factor for next trade
            learning_factor_decimal = self.calculate_learning_factor()
        
        return self.performance_history

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )
    
    # Create and run simulator
    simulator = TradeSimulator()
    simulator.simulate_trades(8000)
