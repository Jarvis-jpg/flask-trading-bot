import logging
import numpy as np
from datetime import datetime, timedelta
from collections import deque
from typing import Tuple, Dict, Optional

logger = logging.getLogger(__name__)

class MarketDataValidator:
    def __init__(self):
        self.price_history = {}
        self.spread_history = {}
        self.volatility_window = 20
        self.max_spread_multiple = 2.0
        self.min_tick_size = 0.00001
        self.max_price_change = 0.02  # 2% max instant change
        self.max_spread = 0.0003  # 3 pips for EUR/USD
        self.min_volume = 0.3
        
    def validate_price(self, symbol: str, price: float, spread: float, volume: float) -> Tuple[bool, str]:
        """Validate incoming price data"""
        # Initialize history for new symbols
        if symbol not in self.price_history:
            self.price_history[symbol] = deque(maxlen=self.volatility_window)
            self.spread_history[symbol] = deque(maxlen=self.volatility_window)
            return True, "Initial price accepted"
            
        # Check for price gaps
        if self.price_history[symbol]:
            last_price = self.price_history[symbol][-1]
            price_change = abs(price - last_price) / last_price
            if price_change > self.max_price_change:
                return False, f"Price gap detected: {price_change:.2%}"
                
        # Check spread
        avg_spread = np.mean(list(self.spread_history[symbol])) if self.spread_history[symbol] else spread
        if spread > avg_spread * self.max_spread_multiple:
            return False, f"Abnormal spread: {spread} > {avg_spread * self.max_spread_multiple}"
            
        # Check absolute spread
        if spread > self.max_spread:
            return False, f"Spread too high: {spread}"
            
        # Check volume
        if volume < self.min_volume:
            return False, f"Volume too low: {volume}"
            
        # Validate tick size
        if not self._validate_tick_size(price):
            return False, "Invalid tick size"
            
        # Update history
        self.price_history[symbol].append(price)
        self.spread_history[symbol].append(spread)
        
        return True, "Price validated"
        
    def calculate_volatility(self, symbol: str) -> Optional[float]:
        """Calculate current volatility for a symbol"""
        if symbol not in self.price_history or len(self.price_history[symbol]) < 2:
            return None
            
        prices = np.array(list(self.price_history[symbol]))
        returns = np.diff(np.log(prices))
        return np.std(returns)
        
    def _validate_tick_size(self, price: float) -> bool:
        """Check if price matches valid tick size"""
        return abs(round(price / self.min_tick_size) * self.min_tick_size - price) < 1e-10
        
    def get_market_quality(self, symbol: str, current_price: float, spread: float, volume: float) -> float:
        """Calculate overall market quality score"""
        # Spread quality (40% weight)
        spread_quality = max(0, 1 - spread / self.max_spread)
        
        # Volume quality (40% weight)
        volume_quality = min(1, volume / self.min_volume)
        
        # Volatility quality (20% weight)
        volatility = self.calculate_volatility(symbol)
        volatility_quality = 0.5  # Default if not enough data
        if volatility is not None:
            # Prefer moderate volatility (not too high, not too low)
            volatility_quality = 1 - abs(volatility - 0.0001) / 0.0002  # Adjust these values based on your needs
            volatility_quality = max(0, min(1, volatility_quality))
            
        # Calculate weighted score
        market_quality = (
            spread_quality * 0.4 +
            volume_quality * 0.4 +
            volatility_quality * 0.2
        )
        
        return market_quality
