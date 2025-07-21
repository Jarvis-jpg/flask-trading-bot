import random
from datetime import datetime, time
import numpy as np
from typing import Dict, Optional

class MarketConditions:
    def __init__(self):
        self.MAX_DRAWDOWN = 0.05  # 5% maximum drawdown
        self.MAX_CORRELATION = 0.7  # 70% maximum correlation between trades
        self.trade_history = []
        
    def market_hours_spread(self, current_time: Optional[datetime] = None) -> float:
        """Calculate spread based on market session."""
        if current_time is None:
            current_time = datetime.now()
            
        current_hour = current_time.hour
        
        # Define market sessions and their typical spreads (adjusted for better conditions)
        if self._is_asian_session(current_hour):
            return random.uniform(0.8, 1.5)  # Moderate spreads in Asian session
        elif self._is_london_session(current_hour):
            return random.uniform(0.5, 1.0)  # Very tight spreads in London
        elif self._is_new_york_session(current_hour):
            return random.uniform(0.6, 1.2)  # Tight spreads in NY
        else:
            return random.uniform(1.0, 2.0)  # Moderate spreads in off-hours
            
    def calculate_market_depth(self, pair: str = "EUR_USD") -> float:
        """Simulate market depth/liquidity."""
        base_liquidity = {
            "EUR_USD": 1.0,
            "GBP_USD": 0.8,
            "USD_JPY": 0.9,
            "USD_CHF": 0.6
        }
        
        liquidity = base_liquidity.get(pair, 0.5)
        current_hour = datetime.now().hour
        
        # Adjust liquidity based on market session
        if self._is_asian_session(current_hour):
            liquidity *= 0.7
        elif self._is_london_session(current_hour):
            liquidity *= 1.2
        elif self._is_new_york_session(current_hour):
            liquidity *= 1.0
        else:
            liquidity *= 0.4
            
        return liquidity
        
    def get_real_market_volatility(self, timeframe: str = "H1") -> float:
        """Calculate market volatility based on recent price action."""
        # In real implementation, this would use actual market data
        base_volatility = random.uniform(0.3, 0.8)
        
        # Adjust for market conditions
        if self._is_high_impact_news():
            base_volatility *= 1.5
        
        return base_volatility
        
    def _is_asian_session(self, hour: int) -> bool:
        return 0 <= hour < 8
        
    def _is_london_session(self, hour: int) -> bool:
        return 8 <= hour < 16
        
    def _is_new_york_session(self, hour: int) -> bool:
        return 13 <= hour < 21
        
    def _is_high_impact_news(self) -> bool:
        """Simulate high impact news events."""
        return random.random() < 0.1  # 10% chance of high impact news
        
    def calculate_correlation_risk(self, new_trade: Dict) -> float:
        """Calculate correlation risk with existing trades."""
        if not self.trade_history:
            return 0.0
            
        # Extract relevant features for correlation
        trade_features = [
            new_trade.get('trend', 0),
            new_trade.get('volatility', 0),
            new_trade.get('rsi', 50),
            new_trade.get('macd_diff', 0)
        ]
        
        # Calculate correlation with recent trades
        correlations = []
        for past_trade in self.trade_history[-5:]:  # Look at last 5 trades
            past_features = [
                past_trade.get('trend', 0),
                past_trade.get('volatility', 0),
                past_trade.get('rsi', 50),
                past_trade.get('macd_diff', 0)
            ]
            correlation = np.corrcoef(trade_features, past_features)[0, 1]
            correlations.append(abs(correlation))
            
        return max(correlations) if correlations else 0.0
