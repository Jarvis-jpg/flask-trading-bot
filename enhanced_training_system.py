#!/usr/bin/env python3
"""
Enhanced Training System - Integrates 8000 Test Trades with Autonomous Engine
This system uses the proven adaptive test system to rapidly train and improve the trading bot
"""
import logging
import random
import math
import json
import os
from datetime import datetime, timedelta
import time
import pandas as pd
import numpy as np
from typing import Dict, List, Optional

# Import the existing test systems
from adaptive_test_8000_clean import TradeSimulator
from enhanced_trading_strategy import trading_strategy
from autonomous_trading_engine import autonomous_engine
from trade_analyzer import TradeAnalyzer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedTrainingSystem:
    """
    Enhanced training system that uses the proven 8000 trade simulator
    to rapidly train the autonomous trading engine
    """
    
    def __init__(self):
        self.simulator = TradeSimulator()
        self.trade_analyzer = TradeAnalyzer()
        self.training_results = []
        self.performance_metrics = {
            'total_trades': 0,
            'wins': 0,
            'losses': 0,
            'total_profit': 0.0,
            'max_drawdown': 0.0,
            'win_streaks': [],
            'loss_streaks': [],
            'learning_progression': []
        }
        
        # Enhanced training configuration
        self.training_config = {
            'total_trades': 8000,
            'batch_size': 10,  # Smaller batches for better readability
            'learning_rate': 0.05,
            'adaptation_frequency': 50,
            'validation_frequency': 500,
            'early_stopping_patience': 1000,
            'performance_window': 200,
            'min_win_rate_threshold': 0.55,
            'target_win_rate': 0.70,
            'profit_factor_target': 1.5
        }
        
        self.currency_pairs = [
            'EUR_USD', 'GBP_USD', 'USD_JPY', 'USD_CHF',
            'AUD_USD', 'USD_CAD', 'NZD_USD', 'EUR_GBP'
        ]
        
        logger.info("🎯 Enhanced Training System initialized")
        logger.info(f"📊 Target: {self.training_config['total_trades']} trades")
        logger.info(f"🎪 Target Win Rate: {self.training_config['target_win_rate']:.1%}")
    
    def run_accelerated_training(self):
        """Run accelerated training using the 8000 trade system"""
        print("🚀 Starting Enhanced Training Session...")
        print("=" * 60)
        print("⏱️  Each trade will process with a 3-second delay for clarity")
        print("📊 Progress updates every 100 trades")
        print("=" * 60)
        
        start_time = datetime.now()
        best_performance = 0.0
        no_improvement_count = 0
        
        try:
            for batch in range(0, self.training_config['total_trades'], self.training_config['batch_size']):
                batch_start = time.time()
                
                # Run training batch
                batch_results = self._run_training_batch(batch, self.training_config['batch_size'])
                
                # Update performance metrics
                self._update_performance_metrics(batch_results)
                
                # Adapt strategy based on results
                if batch % self.training_config['adaptation_frequency'] == 0:
                    self._adapt_strategy()
                
                # Validate performance
                if batch % self.training_config['validation_frequency'] == 0:
                    current_performance = self._validate_performance()
                    
                    if current_performance > best_performance:
                        best_performance = current_performance
                        no_improvement_count = 0
                        self._save_best_model()
                    else:
                        no_improvement_count += 1
                    
                    # Early stopping check
                    if no_improvement_count >= self.training_config['early_stopping_patience'] / self.training_config['validation_frequency']:
                        print("🛑 Early stopping triggered - no improvement")
                        break
                
                # Progress reporting
                batch_time = time.time() - batch_start
                self._report_batch_progress(batch, batch_results, batch_time)
        
        except KeyboardInterrupt:
            print("⏹️ Training interrupted by user")
        
        # Final results
        training_time = datetime.now() - start_time
        self._generate_training_report(training_time)
        
        return self.performance_metrics
    
    def _run_training_batch(self, batch_start: int, batch_size: int) -> List[Dict]:
        """Run a batch of training trades"""
        batch_results = []
        
        for i in range(batch_size):
            trade_number = batch_start + i + 1
            
            # Select random currency pair
            pair = random.choice(self.currency_pairs)
            
            # Generate market conditions using the proven simulator
            learning_factor = self.simulator.calculate_learning_factor()
            market_conditions = self.simulator.generate_market_conditions(learning_factor)
            
            # Create realistic price data for strategy analysis
            price_data = self._generate_price_data(market_conditions, pair)
            
            # Generate trading signal using enhanced strategy
            signal = trading_strategy.generate_trade_signal(pair, price_data)
            
            # Simulate trade execution and outcome
            trade_result = self._simulate_trade_execution(signal, market_conditions, trade_number)
            
            # Display readable trade information
            self._display_trade_info(trade_result, trade_number, pair, learning_factor)
            
            # Add to simulator's performance history for learning
            self.simulator.performance_history.append({
                'profitable': trade_result['result'] == 'win',
                'profit': trade_result['profit'],
                'confidence': trade_result['confidence'],
                'market_conditions': market_conditions
            })
            
            batch_results.append(trade_result)
            
            # Update analyzer with trade performance (silently)
            try:
                self.trade_analyzer.track_trade_performance({
                    'pair': pair,
                    'profit': trade_result['profit'],
                    'entry_price': trade_result['entry'],
                    'exit_price': trade_result.get('exit_price'),
                    'duration': trade_result.get('duration', 0),
                    'market_conditions': {
                        **market_conditions,
                        'price': trade_result['entry'],
                        'volume_analysis': 'normal',
                        'support_resistance': {
                            'support': market_conditions.get('price', trade_result['entry']) * 0.999,
                            'resistance': market_conditions.get('price', trade_result['entry']) * 1.001
                        },
                        'indicators': {
                            'rsi_14': market_conditions.get('rsi', 50),
                            'macd': 0,
                            'macd_signal': 0,
                            'sma_20': market_conditions.get('price', trade_result['entry']),
                            'sma_50': market_conditions.get('price', trade_result['entry']),
                            'atr': market_conditions.get('volatility', 0.01),
                            'cci': 0
                        }
                    },
                    'trade_setup': signal
                })
            except Exception as e:
                # Silently handle analyzer errors
                pass
            
            # Add 3-second delay between trades for readability
            time.sleep(3)
        
        return batch_results
    
    def _display_trade_info(self, trade_result: Dict, trade_number: int, pair: str, learning_factor: float):
        """Display clean, readable trade information"""
        if trade_result['result'] == 'no_trade':
            logger.info(f"📊 Trade #{trade_number:,} | {pair} | ⏸️  NO SIGNAL | Learning: {learning_factor:.1%}")
        else:
            result_emoji = "🟢" if trade_result['result'] == 'win' else "🔴"
            profit_str = f"${trade_result['profit']:.2f}" if trade_result['profit'] >= 0 else f"-${abs(trade_result['profit']):.2f}"
            confidence_str = f"{trade_result['confidence']:.1%}"
            entry_price = f"{trade_result['entry']:.5f}"
            
            logger.info(f"📈 Trade #{trade_number:,} | {pair} | {result_emoji} {trade_result['result'].upper()} | "
                       f"Profit: {profit_str} | Entry: {entry_price} | Confidence: {confidence_str} | Learning: {learning_factor:.1%}")
    
    def _generate_price_data(self, market_conditions: Dict, pair: str) -> pd.DataFrame:
        """Generate realistic price data based on market conditions"""
        # Base price for the pair
        base_prices = {
            'EUR_USD': 1.0950, 'GBP_USD': 1.2750, 'USD_JPY': 143.50, 'USD_CHF': 0.9150,
            'AUD_USD': 0.6750, 'USD_CAD': 1.3450, 'NZD_USD': 0.6250, 'EUR_GBP': 0.8550
        }
        
        base_price = base_prices.get(pair, 1.0000)
        volatility = market_conditions['volatility']
        
        # Generate 100 periods of price data
        periods = 100
        dates = pd.date_range(end=datetime.now(), periods=periods, freq='1h')
        
        # Create trend-influenced price movement
        trend_direction = 1 if market_conditions['trend'] == 'uptrend' else -1 if market_conditions['trend'] == 'downtrend' else 0
        
        prices = [base_price]
        for i in range(1, periods):
            # Random walk with trend bias
            random_change = np.random.normal(0, volatility * 0.0001)
            trend_change = trend_direction * volatility * 0.00005
            
            new_price = prices[-1] * (1 + random_change + trend_change)
            prices.append(new_price)
        
        # Create OHLC data
        data = []
        for i, price in enumerate(prices):
            high = price * (1 + volatility * 0.0002)
            low = price * (1 - volatility * 0.0002)
            open_price = prices[i-1] if i > 0 else price
            
            data.append({
                'datetime': dates[i],
                'open': open_price,
                'high': high,
                'low': low,
                'close': price,
                'volume': random.randint(int(1000 * market_conditions['volume']), int(5000 * market_conditions['volume']))
            })
        
        df = pd.DataFrame(data)
        df.set_index('datetime', inplace=True)
        
        return df
    
    def _simulate_trade_execution(self, signal: Dict, market_conditions: Dict, trade_number: int) -> Dict:
        """Simulate trade execution with realistic outcomes"""
        if signal['signal'] == 'no_signal':
            return {
                'trade_number': trade_number,
                'result': 'no_trade',
                'profit': 0.0,
                'confidence': 0.0,
                'entry': 0.0,
                'reason': 'no_signal'
            }
        
        # Ensure signal has required fields with defaults
        entry_price = signal.get('entry', signal.get('price', 1.0))
        confidence = signal.get('confidence', 0.5)
        units = signal.get('units', 1000)
        
        # If entry_price is still not available, use a reasonable default
        if entry_price is None or entry_price == 0:
            # Use the close price from market conditions or a default
            entry_price = market_conditions.get('price', 1.0)
        
        # Determine trade outcome based on market conditions and signal quality
        base_win_probability = market_conditions.get('win_rate', 0.5)
        
        # Adjust win probability based on signal confidence and market conditions
        confidence_boost = confidence * 0.2
        
        # Market condition adjustments
        if market_conditions['is_profitable_setup']:
            setup_boost = 0.15
        else:
            setup_boost = -0.1
        
        # RSI condition boost
        rsi = market_conditions['rsi']
        if signal['signal'] == 'buy' and 30 < rsi < 70:
            rsi_boost = 0.1
        elif signal['signal'] == 'sell' and 30 < rsi < 70:
            rsi_boost = 0.1
        else:
            rsi_boost = -0.05
        
        final_win_probability = base_win_probability + confidence_boost + setup_boost + rsi_boost
        final_win_probability = max(0.1, min(0.9, final_win_probability))  # Clamp between 10-90%
        
        # Determine outcome
        is_winner = random.random() < final_win_probability
        
        # Calculate profit/loss
        if is_winner:
            # Winning trade
            profit_multiplier = random.uniform(1.8, 3.5)  # 1.8:1 to 3.5:1 reward
            profit = units * 0.0001 * profit_multiplier
        else:
            # Losing trade
            loss_multiplier = random.uniform(0.8, 1.2)  # Losses slightly smaller than wins
            profit = -units * 0.0001 * loss_multiplier
        
        return {
            'trade_number': trade_number,
            'pair': signal['pair'],
            'action': signal['signal'],
            'entry': entry_price,
            'confidence': confidence,
            'result': 'win' if is_winner else 'loss',
            'profit': round(profit, 2),
            'win_probability': final_win_probability,
            'market_conditions': market_conditions,
            'strategy': signal.get('strategy', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }
    
    def _update_performance_metrics(self, batch_results: List[Dict]):
        """Update performance metrics with batch results"""
        for result in batch_results:
            # Count all trades except 'no_trade' - include both wins and losses
            if result['result'] in ['win', 'loss']:
                self.performance_metrics['total_trades'] += 1
                
                if result['result'] == 'win':
                    self.performance_metrics['wins'] += 1
                elif result['result'] == 'loss':
                    self.performance_metrics['losses'] += 1
                
                self.performance_metrics['total_profit'] += result['profit']
        
        # Calculate running win rate
        if self.performance_metrics['total_trades'] > 0:
            win_rate = self.performance_metrics['wins'] / self.performance_metrics['total_trades']
            self.performance_metrics['learning_progression'].append({
                'trade_count': self.performance_metrics['total_trades'],
                'win_rate': win_rate,
                'total_profit': self.performance_metrics['total_profit'],
                'learning_factor': self.simulator.calculate_learning_factor()
            })
    
    def _adapt_strategy(self):
        """Adapt strategy parameters based on performance"""
        recent_trades = 100
        if len(self.performance_metrics['learning_progression']) < recent_trades:
            return
        
        recent_performance = self.performance_metrics['learning_progression'][-recent_trades:]
        recent_win_rate = sum(p['win_rate'] for p in recent_performance) / len(recent_performance)
        
        # Adapt strategy configuration based on performance
        if recent_win_rate < self.training_config['min_win_rate_threshold']:
            # Increase confidence threshold to be more selective
            trading_strategy.strategy_config['confidence_threshold'] = min(0.85, 
                trading_strategy.strategy_config['confidence_threshold'] + 0.02)
            logger.info(f"📈 Increased confidence threshold to {trading_strategy.strategy_config['confidence_threshold']:.2f}")
        
        elif recent_win_rate > self.training_config['target_win_rate']:
            # Decrease confidence threshold to take more trades
            trading_strategy.strategy_config['confidence_threshold'] = max(0.6, 
                trading_strategy.strategy_config['confidence_threshold'] - 0.01)
            logger.info(f"📉 Decreased confidence threshold to {trading_strategy.strategy_config['confidence_threshold']:.2f}")
    
    def _validate_performance(self) -> float:
        """Validate current performance and return score"""
        if not self.performance_metrics['learning_progression']:
            return 0.0
        
        recent_window = min(self.training_config['performance_window'], 
                           len(self.performance_metrics['learning_progression']))
        
        if recent_window < 50:
            return 0.0
        
        recent_data = self.performance_metrics['learning_progression'][-recent_window:]
        
        # Calculate performance score
        avg_win_rate = sum(p['win_rate'] for p in recent_data) / len(recent_data)
        total_profit = sum(p['total_profit'] for p in recent_data)
        
        # Performance score combines win rate and profitability
        performance_score = (avg_win_rate * 0.7) + (min(total_profit / 1000, 1.0) * 0.3)
        
        logger.info(f"📊 Validation: Win Rate = {avg_win_rate:.1%}, Profit = ${total_profit:.2f}, Score = {performance_score:.3f}")
        
        return performance_score
    
    def _save_best_model(self):
        """Save the best performing model configuration"""
        model_data = {
            'timestamp': datetime.now().isoformat(),
            'performance_metrics': self.performance_metrics.copy(),
            'strategy_config': trading_strategy.strategy_config.copy(),
            'training_config': self.training_config.copy(),
            'learning_factor': self.simulator.calculate_learning_factor()
        }
        
        os.makedirs('models', exist_ok=True)
        with open('models/best_training_model.json', 'w') as f:
            json.dump(model_data, f, indent=2)
        
        logger.info("💾 Best model configuration saved")
    
    def _report_batch_progress(self, batch_start: int, batch_results: List[Dict], batch_time: float):
        """Report progress for current batch"""
        if batch_start % 100 == 0:  # Report every 100 trades (every 10 batches)
            trades_completed = batch_start + len(batch_results)
            total_trades = self.training_config['total_trades']
            progress = trades_completed / total_trades * 100
            
            # Calculate recent performance
            recent_wins = sum(1 for r in batch_results if r['result'] == 'win')
            batch_win_rate = recent_wins / len(batch_results) if batch_results else 0
            
            # Overall statistics
            overall_win_rate = (self.performance_metrics['wins'] / 
                               max(self.performance_metrics['total_trades'], 1))
            
            print("\n" + "="*60)
            print(f"� PROGRESS UPDATE - {progress:.1f}% Complete")
            print("="*60)
            print(f"✅ Trades Completed: {trades_completed:,} / {total_trades:,}")
            print(f"🎯 Current Win Rate: {overall_win_rate:.1%}")
            print(f"💰 Total Profit: ${self.performance_metrics['total_profit']:.2f}")
            print(f"🧠 Learning Factor: {self.simulator.calculate_learning_factor():.1%}")
            print(f"⏱️  Batch Time: {batch_time:.1f}s")
            print("="*60 + "\n")
    
    def _generate_training_report(self, training_time: timedelta):
        """Generate comprehensive training report"""
        logger.info("\n" + "=" * 60)
        logger.info("🏁 ENHANCED TRAINING COMPLETED")
        logger.info("=" * 60)
        
        total_trades = self.performance_metrics['total_trades']
        wins = self.performance_metrics['wins']
        losses = self.performance_metrics['losses']
        total_profit = self.performance_metrics['total_profit']
        
        win_rate = wins / total_trades if total_trades > 0 else 0
        avg_profit_per_trade = total_profit / total_trades if total_trades > 0 else 0
        
        logger.info(f"📊 Training Summary:")
        logger.info(f"   Duration: {training_time}")
        logger.info(f"   Total Trades: {total_trades:,}")
        logger.info(f"   Wins: {wins:,} ({win_rate:.1%})")
        logger.info(f"   Losses: {losses:,}")
        logger.info(f"   Total Profit: ${total_profit:.2f}")
        logger.info(f"   Avg Profit/Trade: ${avg_profit_per_trade:.2f}")
        logger.info(f"   Final Learning Factor: {self.simulator.calculate_learning_factor():.1%}")
        
        # Performance assessment
        if win_rate >= self.training_config['target_win_rate']:
            logger.info("🎉 TARGET WIN RATE ACHIEVED!")
        elif win_rate >= self.training_config['min_win_rate_threshold']:
            logger.info("✅ Acceptable performance achieved")
        else:
            logger.info("⚠️ Performance below target - consider more training")
        
        # Save complete training report
        training_report = {
            'training_completed': datetime.now().isoformat(),
            'training_duration': str(training_time),
            'performance_metrics': self.performance_metrics,
            'final_learning_factor': self.simulator.calculate_learning_factor(),
            'strategy_config': trading_strategy.strategy_config,
            'learning_progression': self.performance_metrics['learning_progression']
        }
        
        os.makedirs('logs', exist_ok=True)
        with open('logs/enhanced_training_report.json', 'w') as f:
            json.dump(training_report, f, indent=2)
        
        logger.info(f"📄 Complete training report saved to: logs/enhanced_training_report.json")
    
    def apply_training_to_autonomous_engine(self):
        """Apply training results to the autonomous trading engine"""
        logger.info("🔄 Applying training results to autonomous engine...")
        
        # Update engine configuration based on training results
        if self.performance_metrics['total_trades'] > 0:
            win_rate = self.performance_metrics['wins'] / self.performance_metrics['total_trades']
            
            # Adjust autonomous engine parameters
            if win_rate >= 0.6:
                # High performance - can be more aggressive
                autonomous_engine.config['max_concurrent_trades'] = 7
                autonomous_engine.config['scan_interval'] = 45
                logger.info("🚀 High performance detected - increased aggression")
            
            elif win_rate >= 0.5:
                # Good performance - standard settings
                autonomous_engine.config['max_concurrent_trades'] = 5
                autonomous_engine.config['scan_interval'] = 60
                logger.info("✅ Good performance - standard settings")
            
            else:
                # Lower performance - more conservative
                autonomous_engine.config['max_concurrent_trades'] = 3
                autonomous_engine.config['scan_interval'] = 90
                trading_strategy.strategy_config['confidence_threshold'] = 0.8
                logger.info("⚠️ Conservative settings applied")
        
        logger.info("✅ Training results applied to autonomous engine")

def main():
    """Run the enhanced training system"""
    print("🎯 Enhanced Training System - 8000 Trade Accelerated Learning")
    print("=" * 60)
    
    training_system = EnhancedTrainingSystem()
    
    try:
        # Run accelerated training
        results = training_system.run_accelerated_training()
        
        # Apply results to autonomous engine
        training_system.apply_training_to_autonomous_engine()
        
        print("\n🎉 Enhanced training completed successfully!")
        print(f"✅ System learned from {results['total_trades']:,} simulated trades")
        print(f"📈 Final win rate: {results['wins'] / max(results['total_trades'], 1):.1%}")
        print(f"💰 Total simulated profit: ${results['total_profit']:.2f}")
        print("\n🤖 Your autonomous trading engine is now enhanced and ready!")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
