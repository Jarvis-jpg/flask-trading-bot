#!/usr/bin/env python3
"""
Market Microstructure Enhancement
Adds order book analysis, liquidity detection, and smart execution
"""

import numpy as np
import random
from datetime import datetime

class MarketMicrostructure:
    """
    Analyzes market depth, liquidity, and execution quality
    to improve trade timing and reduce slippage
    """
    
    def __init__(self):
        self.liquidity_threshold = 0.7
        self.depth_analysis_window = 100
        
    def analyze_market_depth(self, pair, market_condition):
        """Analyze order book depth and liquidity"""
        # Simulate realistic market depth based on pair and conditions
        base_liquidity = {
            'EUR/USD': 0.95, 'GBP/USD': 0.88, 'USD/JPY': 0.92,
            'USD/CHF': 0.82, 'AUD/USD': 0.78, 'USD/CAD': 0.80,
            'NZD/USD': 0.72, 'EUR/GBP': 0.75
        }
        
        liquidity = base_liquidity.get(pair, 0.70)
        
        # Adjust for market conditions
        if market_condition == 'volatile':
            liquidity *= random.uniform(0.6, 0.8)  # Reduced liquidity
        elif market_condition == 'quiet':
            liquidity *= random.uniform(1.1, 1.3)  # Better liquidity
        elif market_condition == 'ranging':
            liquidity *= random.uniform(0.9, 1.1)  # Normal
        
        # Add time-of-day effects
        current_hour = datetime.now().hour
        if current_hour in [2, 3, 4, 22, 23]:  # Low activity hours
            liquidity *= random.uniform(0.7, 0.9)
        elif current_hour in [8, 9, 13, 14, 15]:  # High activity
            liquidity *= random.uniform(1.1, 1.4)
        
        return min(1.0, max(0.3, liquidity))
    
    def get_optimal_execution_size(self, intended_size, liquidity_score):
        """Determine optimal position size based on market depth"""
        if liquidity_score > 0.9:
            return intended_size * 1.0  # Full size
        elif liquidity_score > 0.8:
            return intended_size * 0.9  # Slight reduction
        elif liquidity_score > 0.7:
            return intended_size * 0.8  # Moderate reduction
        elif liquidity_score > 0.6:
            return intended_size * 0.6  # Significant reduction
        else:
            return intended_size * 0.4  # Heavy reduction
    
    def calculate_smart_slippage(self, pair, size, liquidity_score, volatility):
        """Calculate realistic slippage based on market conditions"""
        # Base slippage by pair
        base_slippage = {
            'EUR/USD': 0.0003, 'GBP/USD': 0.0005, 'USD/JPY': 0.0004,
            'USD/CHF': 0.0006, 'AUD/USD': 0.0007, 'USD/CAD': 0.0006,
            'NZD/USD': 0.0008, 'EUR/GBP': 0.0007
        }
        
        slippage = base_slippage.get(pair, 0.0008)
        
        # Size impact
        if size > 100000:  # Large position
            slippage *= 1.5
        elif size > 50000:  # Medium position
            slippage *= 1.2
        
        # Liquidity impact
        slippage *= (2.0 - liquidity_score)  # Lower liquidity = higher slippage
        
        # Volatility impact
        slippage *= (1 + volatility)
        
        return min(0.002, slippage)  # Cap at 20 pips equivalent
    
    def should_execute_trade(self, pair, market_condition, intended_size):
        """Determine if trade should execute based on microstructure"""
        liquidity = self.analyze_market_depth(pair, market_condition)
        
        if liquidity < self.liquidity_threshold:
            return False, f"Low liquidity: {liquidity:.2f}"
        
        # Check for market stress indicators
        if market_condition == 'volatile' and liquidity < 0.8:
            return False, "High volatility + low liquidity"
        
        return True, f"Good execution environment: {liquidity:.2f}"
