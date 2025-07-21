import logging
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import deque

logger = logging.getLogger(__name__)

class PerformanceAnalyzer:
    def __init__(self, risk_manager, position_manager):
        self.risk_manager = risk_manager
        self.position_manager = position_manager
        self.metrics = {}
        self.report_interval = 300  # 5 minutes
        
        # Performance tracking
        self.trades_history = deque(maxlen=1000)
        self.daily_results = []
        self.hourly_metrics = {}
        
        # Analysis windows
        self.short_window = 20   # Last 20 trades
        self.medium_window = 50  # Last 50 trades
        self.long_window = 100   # Last 100 trades
        
    async def analyze_performance(self):
        """Real-time performance analysis"""
        while True:
            try:
                # Calculate core metrics
                self.metrics['sharpe_ratio'] = self.calculate_sharpe_ratio()
                self.metrics['sortino_ratio'] = self.calculate_sortino_ratio()
                self.metrics['max_drawdown'] = self.calculate_max_drawdown()
                self.metrics['win_rate'] = self.calculate_win_rate()
                self.metrics['profit_factor'] = self.calculate_profit_factor()
                self.metrics['average_trade'] = self.calculate_average_trade()
                self.metrics['risk_reward_ratio'] = self.calculate_risk_reward_ratio()
                
                # Calculate window-based metrics
                self.calculate_window_metrics()
                
                # Check for performance degradation
                if self.detect_performance_degradation():
                    await self.alert_administrators()
                    
                # Log performance summary
                self.log_performance_summary()
                
            except Exception as e:
                logger.error(f"Performance analysis error: {str(e)}")
                
            await asyncio.sleep(self.report_interval)
            
    def calculate_sharpe_ratio(self, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe Ratio"""
        if not self.trades_history:
            return 0.0
            
        returns = [trade['profit_pct'] for trade in self.trades_history]
        if not returns:
            return 0.0
            
        excess_returns = np.array(returns) - (risk_free_rate / 252)  # Daily adjustment
        if len(excess_returns) < 2:
            return 0.0
            
        return np.mean(excess_returns) / np.std(excess_returns, ddof=1) * np.sqrt(252)
        
    def calculate_sortino_ratio(self, risk_free_rate: float = 0.02) -> float:
        """Calculate Sortino Ratio"""
        if not self.trades_history:
            return 0.0
            
        returns = [trade['profit_pct'] for trade in self.trades_history]
        if not returns:
            return 0.0
            
        excess_returns = np.array(returns) - (risk_free_rate / 252)
        negative_returns = excess_returns[excess_returns < 0]
        
        if len(negative_returns) < 1:
            return np.inf
            
        downside_std = np.std(negative_returns, ddof=1)
        if downside_std == 0:
            return 0.0
            
        return np.mean(excess_returns) / downside_std * np.sqrt(252)
        
    def calculate_max_drawdown(self) -> float:
        """Calculate Maximum Drawdown"""
        if not self.trades_history:
            return 0.0
            
        cumulative = np.array([trade['cumulative_balance'] for trade in self.trades_history])
        peak = np.maximum.accumulate(cumulative)
        drawdown = (peak - cumulative) / peak
        return np.max(drawdown)
        
    def calculate_win_rate(self, window: int = None) -> float:
        """Calculate Win Rate"""
        if not self.trades_history:
            return 0.0
            
        trades = list(self.trades_history)
        if window:
            trades = trades[-window:]
            
        if not trades:
            return 0.0
            
        wins = sum(1 for trade in trades if trade['profit'] > 0)
        return wins / len(trades)
        
    def calculate_profit_factor(self, window: int = None) -> float:
        """Calculate Profit Factor"""
        if not self.trades_history:
            return 0.0
            
        trades = list(self.trades_history)
        if window:
            trades = trades[-window:]
            
        if not trades:
            return 0.0
            
        gross_profit = sum(trade['profit'] for trade in trades if trade['profit'] > 0)
        gross_loss = abs(sum(trade['profit'] for trade in trades if trade['profit'] < 0))
        
        return gross_profit / gross_loss if gross_loss != 0 else float('inf')
        
    def calculate_average_trade(self, window: int = None) -> float:
        """Calculate Average Trade Profit"""
        if not self.trades_history:
            return 0.0
            
        trades = list(self.trades_history)
        if window:
            trades = trades[-window:]
            
        if not trades:
            return 0.0
            
        return np.mean([trade['profit'] for trade in trades])
        
    def calculate_risk_reward_ratio(self, window: int = None) -> float:
        """Calculate Risk/Reward Ratio"""
        if not self.trades_history:
            return 0.0
            
        trades = list(self.trades_history)
        if window:
            trades = trades[-window:]
            
        if not trades:
            return 0.0
            
        avg_win = np.mean([trade['profit'] for trade in trades if trade['profit'] > 0])
        avg_loss = abs(np.mean([trade['profit'] for trade in trades if trade['profit'] < 0]))
        
        return avg_win / avg_loss if avg_loss != 0 else float('inf')
        
    def calculate_window_metrics(self):
        """Calculate metrics over different time windows"""
        self.metrics['short_term'] = {
            'win_rate': self.calculate_win_rate(self.short_window),
            'profit_factor': self.calculate_profit_factor(self.short_window),
            'average_trade': self.calculate_average_trade(self.short_window)
        }
        
        self.metrics['medium_term'] = {
            'win_rate': self.calculate_win_rate(self.medium_window),
            'profit_factor': self.calculate_profit_factor(self.medium_window),
            'average_trade': self.calculate_average_trade(self.medium_window)
        }
        
        self.metrics['long_term'] = {
            'win_rate': self.calculate_win_rate(self.long_window),
            'profit_factor': self.calculate_profit_factor(self.long_window),
            'average_trade': self.calculate_average_trade(self.long_window)
        }
        
    def detect_performance_degradation(self) -> bool:
        """Detect significant performance degradation"""
        if not self.metrics.get('short_term') or not self.metrics.get('long_term'):
            return False
            
        # Check for significant deterioration in key metrics
        win_rate_drop = self.metrics['long_term']['win_rate'] - self.metrics['short_term']['win_rate']
        profit_factor_drop = self.metrics['long_term']['profit_factor'] - self.metrics['short_term']['profit_factor']
        
        return (win_rate_drop > 0.1 or  # 10% drop in win rate
                profit_factor_drop > 0.2)  # 0.2 drop in profit factor
                
    def log_performance_summary(self):
        """Log performance summary"""
        logger.info("\n=== Performance Summary ===")
        logger.info(f"Sharpe Ratio: {self.metrics.get('sharpe_ratio', 0):.2f}")
        logger.info(f"Sortino Ratio: {self.metrics.get('sortino_ratio', 0):.2f}")
        logger.info(f"Max Drawdown: {self.metrics.get('max_drawdown', 0):.2%}")
        logger.info(f"Overall Win Rate: {self.metrics.get('win_rate', 0):.2%}")
        logger.info(f"Profit Factor: {self.metrics.get('profit_factor', 0):.2f}")
        logger.info(f"Risk/Reward Ratio: {self.metrics.get('risk_reward_ratio', 0):.2f}")
        
        if self.metrics.get('short_term'):
            logger.info("\nShort-term Metrics (Last 20 trades):")
            logger.info(f"Win Rate: {self.metrics['short_term']['win_rate']:.2%}")
            logger.info(f"Profit Factor: {self.metrics['short_term']['profit_factor']:.2f}")
            
    async def alert_administrators(self):
        """Send performance degradation alerts"""
        message = (
            "⚠️ Performance Degradation Alert:\n"
            f"Short-term Win Rate: {self.metrics['short_term']['win_rate']:.2%}\n"
            f"Long-term Win Rate: {self.metrics['long_term']['win_rate']:.2%}\n"
            f"Short-term Profit Factor: {self.metrics['short_term']['profit_factor']:.2f}\n"
            f"Long-term Profit Factor: {self.metrics['long_term']['profit_factor']:.2f}"
        )
        
        logger.warning(message)
        # Add your notification mechanism here (email, Slack, etc.)
