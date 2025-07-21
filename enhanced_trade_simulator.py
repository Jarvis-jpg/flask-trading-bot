import logging
import random
import math
from datetime import datetime, timedelta
import time
import numpy as np
from market_conditions import MarketConditions
from risk_manager import RiskManager
from market_execution import MarketExecution
from market_validator import MarketDataValidator
from system_monitor import SystemMonitor
from trading_failsafe import TradingFailsafe
from position_manager import PositionManager
from performance_analyzer import PerformanceAnalyzer
import asyncio

class TradeSimulator:
    def __init__(self, initial_balance: float = 200.0):
        self.performance_history = []
        self.total_trades = 0
        self.total_wins = 0
        self.learning_factor = 5.0  # Start with 5%
        self.base_time = datetime.now()
        
        # Initialize core components
        self.market_conditions = MarketConditions()
        self.risk_manager = RiskManager(initial_balance=initial_balance)
        self.market_execution = MarketExecution()
        self.current_balance = initial_balance
        
        # Initialize enhanced safety components
        self.market_validator = MarketDataValidator()
        self.position_manager = PositionManager(self.risk_manager)
        self.system_monitor = SystemMonitor()
        self.performance_analyzer = PerformanceAnalyzer(self.risk_manager, self.position_manager)
        self.failsafe = TradingFailsafe(self.risk_manager, self.position_manager, self.system_monitor)
        
        # Trading restrictions
        self.min_time_between_trades = 60  # Minimum 60 seconds between trades
        self.max_daily_trades = 20  # Maximum trades per day
        self.daily_trades = 0
        self.last_trade_time = None
        self.daily_reset_time = None
        
        # Start monitoring tasks
        self.monitoring_tasks = []
        self._start_monitoring()
        
    def generate_market_conditions(self, learning_factor_decimal):
        """Generate realistic market conditions matching live trading environment."""
        current_time = datetime.now()
        current_hour = current_time.hour
        current_minute = current_time.minute
        
        # Check if market is open (Forex market hours)
        # For testing purposes, we'll consider the market always open
        # Real implementation would check weekends and specific session times
        is_weekend = False  # Disable weekend check for testing
        if is_weekend:
            return None  # Market closed on weekends
            
        # Major forex session times (EST)
        asian_session = 19 <= current_hour or current_hour < 4
        london_session = 3 <= current_hour < 12
        ny_session = 8 <= current_hour < 17
        
        # Get session-specific conditions
        base_spread = 0.5  # Base spread in pips
        base_liquidity = 0.7  # Base liquidity factor
        base_volatility = 0.5  # Base volatility factor
        
        # Session adjustments
        if asian_session:
            spread = base_spread + random.uniform(0.2, 0.5)  # Moderate spreads
            liquidity = base_liquidity + random.uniform(-0.1, 0.1)  # Normal liquidity
            volatility = base_volatility + random.uniform(-0.1, 0.1)
        elif london_session and ny_session:  # Overlap
            spread = base_spread + random.uniform(-0.2, 0.2)  # Tightest spreads
            liquidity = base_liquidity + random.uniform(0.1, 0.3)  # Highest liquidity
            volatility = base_volatility + random.uniform(0.0, 0.2)
        elif london_session:
            spread = base_spread + random.uniform(0.0, 0.3)  # Good spreads
            liquidity = base_liquidity + random.uniform(0.0, 0.2)  # Good liquidity
            volatility = base_volatility + random.uniform(-0.1, 0.1)
        elif ny_session:
            spread = base_spread + random.uniform(0.1, 0.4)  # Normal spreads
            liquidity = base_liquidity + random.uniform(0.0, 0.2)  # Good liquidity
            volatility = base_volatility + random.uniform(-0.1, 0.1)
        else:
            spread = base_spread + random.uniform(0.3, 0.7)  # Higher spreads
            liquidity = base_liquidity + random.uniform(-0.2, 0.0)  # Lower liquidity
            volatility = base_volatility + random.uniform(-0.2, 0.0)
        
        # Calculate recent performance metrics
        recent_trades = self.performance_history[-5:]
        recent_win_rate = (
            sum(1 for t in recent_trades if t.get('profitable', False)) / len(recent_trades)
            if recent_trades else 0.5
        )
        
        # Adjust probabilities based on learning, market conditions, and performance
        good_setup_chance = 0.6 + (learning_factor_decimal * 0.2)  # Base chance
        win_rate_good_setup = 0.7 + (learning_factor_decimal * 0.15)  # Base win rate
        
        # Enhance probabilities during good performance
        if recent_win_rate > 0.6:
            good_setup_chance += 0.1
            win_rate_good_setup += 0.05
        
        # Account for market conditions in setup quality
        if spread > 2.0:
            good_setup_chance *= 0.8  # Reduce setup quality in high spread
        if liquidity < 0.6:
            good_setup_chance *= 0.9  # Reduce setup quality in low liquidity
        if volatility > 0.7:
            win_rate_good_setup *= 0.9  # Reduce win rate in high volatility
        
        conditions = {
            'timestamp': datetime.now().isoformat(),
            'pair': 'EUR_USD',
            'trend': random.choice(['uptrend', 'downtrend', 'sideways']),
            'volatility': volatility,
            'volume': liquidity,
            'spread': spread,
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
        
    def simulate_trades(self, num_trades):
        """Generate trades with improving performance over time."""
        logger = logging.getLogger(__name__)
        logger.info("🔄 Initializing Enhanced Trade Simulator...")
        logger.info(f"Initial Balance: ${self.current_balance:.2f}")
        
        trades_processed = 0
        learning_factor_decimal = 0.05  # Start with 5% learning
        self.performance_history = []
        
        while trades_processed < num_trades:
            # Generate trade time and conditions
            trade_time = self.base_time + timedelta(minutes=trades_processed)
            conditions = self.generate_market_conditions(learning_factor_decimal)
            
            # Skip if market is closed
            if conditions is None:
                logger.info("Market is closed (weekend). Skipping trade...")
                time.sleep(10)  # Wait 10 seconds before next attempt
                continue
                
            # Generate trade parameters with learning factor influence
            base_price = 1.1000 + random.uniform(-0.02 * (1 - learning_factor_decimal), 
                                               0.02 * (1 - learning_factor_decimal))
            stop_distance = random.uniform(0.0020, 0.0050 * (1 - learning_factor_decimal * 0.3))
            profit_distance = stop_distance * (2 + learning_factor_decimal * 2)
            
            # Calculate position size based on risk management
            position_size = self.risk_manager.calculate_position_size({
                'entry': base_price,
                'stop_loss': base_price - stop_distance,
                'pair': 'EUR_USD'
            })
            
            # Create trade data
            trade_data = {
                'timestamp': trade_time.isoformat(),
                'pair': 'EUR_USD',
                'trend': conditions['trend'],
                'volatility': conditions['volatility'],
                'volume': conditions['volume'],
                'spread': conditions['spread'],
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
                'units': position_size,
                'balance': self.current_balance
            }
            
            # Validate trade with risk manager
            # Basic validation first
            if conditions['spread'] > 3.0:  # Skip if spread is too high
                logger.info(f"Trade {trades_processed + 1:04d}/{num_trades} | Skipped: High spread {conditions['spread']:.1f}")
                time.sleep(5)
                continue
                
            if conditions['volume'] < 0.3:  # Skip if volume is too low
                logger.info(f"Trade {trades_processed + 1:04d}/{num_trades} | Skipped: Low volume {conditions['volume']:.1f}")
                time.sleep(5)
                continue
                
            if position_size < 0.01:  # Skip if position size is too small
                logger.info(f"Trade {trades_processed + 1:04d}/{num_trades} | Skipped: Position size too small")
                time.sleep(5)
                continue
                
            # Risk management validation
            max_position_size = self.current_balance * 0.02  # Max 2% risk per trade
            if position_size > max_position_size:
                position_size = max_position_size  # Adjust position size if needed
                
            # Market condition checks
            spread_factor = max(0, min(1, 1.5 - conditions['spread'] / 2.0))  # Normalize spread impact
            volume_factor = conditions['volume']  # Already normalized
            volatility_factor = max(0, min(1, 1.0 - abs(conditions['volatility'] - 0.5)))  # Center around 0.5
            
            market_quality = (
                spread_factor * 0.4 +     # 40% weight on spread
                volume_factor * 0.4 +     # 40% weight on volume
                volatility_factor * 0.2    # 20% weight on volatility
            )
            
            if market_quality < 0.3:  # Lower threshold for market quality
                logger.info(f"Trade {trades_processed + 1:04d}/{num_trades} | Skipped: Poor market quality {market_quality:.2f}")
                time.sleep(5)
                continue
                
            logger.debug(f"Market quality: {market_quality:.2f} (Spread: {spread_factor:.2f}, Volume: {volume_factor:.2f}, Vol: {volatility_factor:.2f})")
                
            # Calculate risk-reward ratio
            trade_data['risk_reward_ratio'] = profit_distance / stop_distance
            
            # Enhanced profitability determination with losing streak protection
            trade_success_chance = random.random()
            
            # Check recent performance
            recent_trades = self.performance_history[-3:]
            consecutive_losses = 0
            for t in reversed(recent_trades):
                if not t.get('profitable', False):
                    consecutive_losses += 1
                else:
                    break
            
            # Base probability factors
            market_quality = (1.0 - conditions['spread'] / 2.0) * conditions['volume']
            trend_strength = abs(conditions['rsi'] - 50) / 50.0
            
            # Calculate win probability with multiple factors
            win_probability = (
                conditions['win_rate'] * 0.4 +    # Base win rate
                market_quality * 0.3 +            # Market conditions
                trend_strength * 0.3              # Trend strength
            )
            
            # Adjust probability based on recent performance
            if consecutive_losses > 0:
                # Increase required market quality after losses
                required_market_quality = 0.6 + (consecutive_losses * 0.1)
                if market_quality < required_market_quality:
                    win_probability *= 0.8  # Reduce win probability if market isn't ideal
                    
                # Require stronger trends after losses
                required_trend_strength = 0.3 + (consecutive_losses * 0.1)
                if trend_strength < required_trend_strength:
                    win_probability *= 0.8
            
            # Final probability adjustment
            win_probability = win_probability * (1 + learning_factor_decimal * 0.2)
            
            # Stricter entry conditions after losses
            if consecutive_losses >= 2:
                # Require better spreads after losses
                if conditions['spread'] > 1.0:
                    win_probability *= 0.7
                    
                # Require higher volume after losses
                if conditions['volume'] < 0.7:
                    win_probability *= 0.7
            
            if (conditions['is_profitable_setup'] and 
                trade_success_chance < win_probability and 
                conditions['spread'] < 2.0):
                
                # Calculate profit with market impact
                market_impact = 1 + (conditions['volatility'] * 0.2)
                trade_data['profit'] = profit_distance * position_size * market_impact
                trade_data['profitable'] = True
                trade_data['success_probability'] = win_probability
            else:
                # Loss calculation with spread impact
                spread_impact = 1 + (conditions['spread'] * 0.1)
                trade_data['profit'] = -stop_distance * position_size * spread_impact
                trade_data['profitable'] = False
                trade_data['success_probability'] = 1 - win_probability
            
            # Update account balance and risk metrics
            self.current_balance += trade_data['profit']
            self.risk_manager.update_trade_history(trade_data)
            
            # Update performance tracking
            self.performance_history.append(trade_data)
            trades_processed += 1
            
            if trade_data['profitable']:
                self.total_wins += 1
            
            # Calculate statistics
            self.total_trades = trades_processed
            overall_win_rate = (self.total_wins / self.total_trades * 100)
            
            # Enhanced logging with market conditions and risk metrics
            logger.info(
                f"Trade {trades_processed:04d}/{num_trades} | "
                f"Balance: ${self.current_balance:.2f} | "
                f"Win Rate: {overall_win_rate:.1f}% | "
                f"Result: {'✅ WIN' if trade_data['profitable'] else '❌ LOSS'} | "
                f"P/L: ${trade_data['profit']:.2f} | "
                f"Spread: {conditions['spread']:.1f} | "
                f"Learning: {learning_factor_decimal*100:.2f}%")
            
            # Add delay between trades
            time.sleep(10)  # 10 second delay between trades
            
            # Update learning factor for next trade
            learning_factor_decimal = self._calculate_learning_factor()
        
        return self.performance_history
        
    def _calculate_learning_factor(self):
        """Calculate the learning factor based on performance and market conditions."""
        # Implementation remains similar but with additional market condition factors
        trades_processed = len(self.performance_history)
        if trades_processed == 0:
            return 0.05
            
        # Calculate overall win rate
        wins = sum(1 for trade in self.performance_history if trade.get('profitable', False))
        win_rate = wins / trades_processed
        
        # Consider market conditions in learning
        recent_trades = self.performance_history[-5:]
        avg_spread = np.mean([t.get('spread', 2.0) for t in recent_trades])
        avg_volatility = np.mean([t.get('volatility', 0.5) for t in recent_trades])
        
        # Adjust learning based on market conditions
        market_adjustment = 1.0
        if avg_spread > 2.0:
            market_adjustment *= 0.8
        if avg_volatility > 0.7:
            market_adjustment *= 0.9
            
        # Calculate base learning factor (cap at 30%)
        base_learning = max(0.05, min(0.3, win_rate * 0.5))
        
        # Apply market adjustment
        adjusted_learning = base_learning * market_adjustment
        
        # Smooth the learning factor (more gradual changes)
        if hasattr(self, 'last_learning_factor'):
            smoothing = 0.9  # Increased smoothing for more gradual changes
            smoothed_learning = (smoothing * self.last_learning_factor + 
                               (1 - smoothing) * adjusted_learning)
        else:
            smoothed_learning = adjusted_learning
            
        self.last_learning_factor = smoothed_learning
        return smoothed_learning
        
    def _start_monitoring(self):
        """Start all monitoring tasks"""
        loop = asyncio.get_event_loop()
        self.monitoring_tasks = [
            loop.create_task(self.system_monitor.monitor_system_health()),
            loop.create_task(self.failsafe.monitor_trading_conditions()),
            loop.create_task(self.performance_analyzer.analyze_performance())
        ]
        
    def stop_monitoring(self):
        """Stop all monitoring tasks"""
        for task in self.monitoring_tasks:
            task.cancel()
        
    async def _validate_market_conditions(self, symbol: str, price: float, spread: float, volume: float) -> bool:
        """Validate market conditions before trading"""
        # Basic market validation
        is_valid, reason = self.market_validator.validate_price(symbol, price, spread, volume)
        if not is_valid:
            logger.warning(f"Market validation failed: {reason}")
            return False
            
        # Check system health
        if not self.system_monitor.is_healthy:
            logger.warning("System health check failed")
            return False
            
        # Check failsafe status
        if self.failsafe.is_shutdown:
            logger.warning("Trading is currently in failsafe shutdown")
            return False
            
        return True

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )
    
    # Create and run enhanced simulator
    simulator = TradeSimulator(initial_balance=200.0)
    simulator.simulate_trades(8000)
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )
    
    # Create and run enhanced simulator with micro-account balance
    simulator = TradeSimulator(initial_balance=200.0)
    simulator.simulate_trades(8000)
