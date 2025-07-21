import logging
import random
import math

class TradeSimulator:
    def __init__(self):
        self.performance_history = []
        self.total_trades = 0
        self.total_wins = 0
        self.learning_factor = 5.0  # Start with 5%
        self.last_learning_factor = 0.05  # Initialize last_learning_factor
        
    def generate_market_conditions(self, learning_factor_decimal):
        """Generate simulated market conditions influenced by learning factor."""
        conditions = {
            'trend': random.choice(['uptrend', 'downtrend', 'sideways']),
            'volatility': random.uniform(0, 1),
            'volume': random.uniform(0, 1),
        }
        
        # Adjust technical indicators based on learning
        if conditions['trend'] == 'uptrend':
            conditions['rsi'] = random.uniform(45 + learning_factor_decimal * 10, 70)
        elif conditions['trend'] == 'downtrend':
            conditions['rsi'] = random.uniform(30, 55 - learning_factor_decimal * 10)
        else:
            conditions['rsi'] = random.uniform(40, 60)
            
        return conditions
        
    def calculate_learning_factor(self):
        """Calculate the learning factor based on performance."""
        trades_processed = len(self.performance_history)
        if trades_processed == 0:
            return 0.05  # Start with 5% learning
        
        # Calculate win rate
        wins = sum(1 for trade in self.performance_history if trade.get('profitable', False))
        win_rate = wins / trades_processed
        
        # Initialize early trading phase variables
        min_trades_for_baseline = 20
        progress = min(1.0, trades_processed / min_trades_for_baseline)
        is_early_phase = trades_processed < min_trades_for_baseline
        
        # Calculate recent performance (last 5 trades)
        recent_trades = min(5, trades_processed)
        recent_wins = sum(1 for i in range(recent_trades) 
                         if i < len(self.performance_history) and 
                         self.performance_history[-(i+1)].get('profitable', False))
        recent_win_rate = recent_wins / recent_trades if recent_trades > 0 else 0
        
        # Dynamic win rate contribution
        win_rate_threshold = 0.0 if is_early_phase else 0.25  # No threshold early
        win_rate_factor = max(0, win_rate - win_rate_threshold)
        win_rate_factor *= 2.0 if is_early_phase else 0.5  # Doubled impact early
        
        # Enhanced progress contribution
        progress_contribution = progress * (0.2 if is_early_phase else 0.1)
        
        # Add recent performance bonus in early phase
        if is_early_phase:
            progress_contribution += recent_win_rate * 0.15  # Up to 15% extra
        
        # Aggressive early performance boost
        early_stage_bonus = 0.0
        if trades_processed < min_trades_for_baseline:
            # Larger early bonus for good performance
            early_stage_bonus = recent_win_rate * 0.25  # Up to 25% boost for perfect recent performance
            
            # Enhanced consecutive wins bonus
            consecutive_wins = 0
            for i in range(min(3, trades_processed)):
                if i < len(self.performance_history) and self.performance_history[-(i+1)].get('profitable', False):
                    consecutive_wins += 1
                else:
                    break
            # Exponential bonus for streaks
            early_stage_bonus += (consecutive_wins * consecutive_wins * 0.05)  # 5%, 20%, 45% for 1,2,3 wins
        
        # Combined learning factor with minimum learning and early stage bonus
        base_learning = 0.05  # 5% minimum learning
        raw_learning = base_learning + win_rate_factor + progress_contribution + early_stage_bonus
        
        # Minimal smoothing during early phase
        if trades_processed < min_trades_for_baseline:
            smoothing = max(0.1, 0.3 - (recent_win_rate * 0.2))  # Can go as low as 0.1
        else:
            smoothing = 0.7
            
        smoothed_learning = (smoothing * self.last_learning_factor + (1 - smoothing) * raw_learning)
        self.last_learning_factor = smoothed_learning
        return smoothed_learning
        
    def simulate_trades(self, num_trades):
        """Generate trades with improving performance over time."""
        logger = logging.getLogger(__name__)
        
        logger.info("🔄 Initializing Trade Simulator...")
        trades_processed = 0
        learning_factor_decimal = 0.05  # Start with 5% learning
        
        while trades_processed < num_trades:
            # Generate market conditions with current learning factor
            conditions = self.generate_market_conditions(learning_factor_decimal)
            
            # Simulate trade result with increasing win chance based on learning
            base_win_rate = 0.4  # 40% base win rate
            current_win_rate = base_win_rate + learning_factor_decimal
            is_profitable = random.random() < current_win_rate
            
            # Calculate profit/loss with improved values for winners
            profit_loss = random.uniform(0.005, 0.01) if is_profitable else -random.uniform(0.002, 0.005)
            
            trade_data = {
                'profitable': is_profitable,
                'profit_loss': profit_loss,
                'conditions': conditions
            }
            
            # Update performance history
            self.performance_history.append(trade_data)
            if is_profitable:
                self.total_wins += 1
            self.total_trades += 1
            
            # Calculate and update learning factor
            trades_processed += 1
            learning_factor_decimal = self.calculate_learning_factor()
            
            # Log progress with detailed stats
            win_rate = (self.total_wins / self.total_trades) * 100
            logger.info(f"Trade {trades_processed:04d}/{num_trades} | "
                      f"Win Rate: {win_rate:.1f}% | "
                      f"Result: {'✅ WIN' if is_profitable else '❌ LOSS'} | "
                      f"P/L: {profit_loss:.5f} | "
                      f"Learning: {learning_factor_decimal*100:.2f}%")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )
    
    # Create and run simulator
    simulator = TradeSimulator()
    simulator.simulate_trades(8000)
