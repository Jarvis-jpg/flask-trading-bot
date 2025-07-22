#!/usr/bin/env python3
"""
Advanced Risk Management System
Implements portfolio heat, correlation monitoring, and dynamic position sizing
"""

import numpy as np
from datetime import datetime, timedelta
import random

class AdvancedRiskManager:
    """
    Sophisticated risk management with portfolio heat monitoring,
    correlation analysis, and dynamic position sizing
    """
    
    def __init__(self):
        self.max_portfolio_heat = 0.06  # 6% max total risk
        self.max_correlation_exposure = 0.03  # 3% max correlated risk
        self.correlation_matrix = self.build_correlation_matrix()
        self.active_positions = {}
        self.portfolio_var = 0.0
        
    def build_correlation_matrix(self):
        """Build realistic currency correlation matrix"""
        return {
            ('EUR/USD', 'GBP/USD'): 0.75,
            ('EUR/USD', 'AUD/USD'): 0.65,
            ('EUR/USD', 'NZD/USD'): 0.60,
            ('EUR/USD', 'USD/CHF'): -0.85,
            ('GBP/USD', 'AUD/USD'): 0.70,
            ('GBP/USD', 'EUR/GBP'): -0.80,
            ('USD/JPY', 'USD/CHF'): 0.60,
            ('AUD/USD', 'NZD/USD'): 0.85,
            # Add more correlations as needed
        }
    
    def get_correlation(self, pair1, pair2):
        """Get correlation between two pairs"""
        key = (pair1, pair2) if pair1 < pair2 else (pair2, pair1)
        return self.correlation_matrix.get(key, 0.0)
    
    def calculate_portfolio_heat(self, new_pair, new_size, new_risk):
        """Calculate total portfolio heat including correlations"""
        total_heat = new_risk
        
        # Add existing position risks
        for pair, position in self.active_positions.items():
            correlation = self.get_correlation(new_pair, pair)
            
            if abs(correlation) > 0.5:  # Significant correlation
                # Add correlated risk
                correlated_risk = position['risk'] * abs(correlation)
                total_heat += correlated_risk
            else:
                # Add uncorrelated risk (diversification benefit)
                total_heat += position['risk'] * 0.5
        
        return total_heat
    
    def calculate_var_95(self, pair, size, confidence_score):
        """Calculate Value at Risk (95% confidence)"""
        # Estimate daily volatility by pair
        daily_volatility = {
            'EUR/USD': 0.008, 'GBP/USD': 0.012, 'USD/JPY': 0.009,
            'USD/CHF': 0.007, 'AUD/USD': 0.011, 'USD/CAD': 0.009,
            'NZD/USD': 0.013, 'EUR/GBP': 0.010
        }
        
        vol = daily_volatility.get(pair, 0.010)
        
        # Adjust volatility based on market conditions
        if confidence_score < 0.5:
            vol *= 1.3  # Higher uncertainty = higher VaR
        elif confidence_score > 0.8:
            vol *= 0.8  # High confidence = lower VaR
        
        # 95% VaR calculation (1.645 * volatility * position size)
        var_95 = 1.645 * vol * size
        return var_95
    
    def optimize_position_size(self, pair, intended_size, confidence_score, market_condition):
        """Optimize position size based on risk constraints"""
        base_risk = intended_size * 0.02  # 2% risk assumption
        
        # Calculate portfolio heat
        total_heat = self.calculate_portfolio_heat(pair, intended_size, base_risk)
        
        # Check portfolio heat limit
        if total_heat > self.max_portfolio_heat:
            reduction_factor = self.max_portfolio_heat / total_heat
            intended_size *= reduction_factor
            base_risk *= reduction_factor
        
        # Check correlation limits
        correlated_risk = 0
        for existing_pair, position in self.active_positions.items():
            correlation = abs(self.get_correlation(pair, existing_pair))
            if correlation > 0.7:  # High correlation
                correlated_risk += position['risk'] * correlation
        
        if correlated_risk > self.max_correlation_exposure:
            correlation_reduction = self.max_correlation_exposure / (correlated_risk + base_risk)
            intended_size *= correlation_reduction
            base_risk *= correlation_reduction
        
        # VaR-based sizing
        var_95 = self.calculate_var_95(pair, intended_size, confidence_score)
        if var_95 > intended_size * 0.03:  # VaR > 3% of position
            var_reduction = (intended_size * 0.03) / var_95
            intended_size *= var_reduction
        
        # Confidence-based adjustment
        if confidence_score > 0.85:
            intended_size *= 1.2  # Increase size for high confidence
        elif confidence_score < 0.4:
            intended_size *= 0.6  # Reduce size for low confidence
        
        return intended_size
    
    def should_take_position(self, pair, size, confidence_score, market_condition):
        """Final risk check before taking position"""
        # Check maximum positions limit
        if len(self.active_positions) >= 5:
            return False, "Maximum positions reached"
        
        # Check if pair already has position
        if pair in self.active_positions:
            return False, f"Already have position in {pair}"
        
        # Check market condition risks
        if market_condition == 'volatile' and confidence_score < 0.7:
            return False, "High volatility requires higher confidence"
        
        # Check portfolio heat
        risk = size * 0.02
        total_heat = self.calculate_portfolio_heat(pair, size, risk)
        if total_heat > self.max_portfolio_heat:
            return False, f"Portfolio heat too high: {total_heat:.3f}"
        
        return True, "Position approved"
    
    def add_position(self, pair, size, entry_price, confidence_score):
        """Add position to portfolio tracking"""
        risk = size * 0.02
        self.active_positions[pair] = {
            'size': size,
            'entry_price': entry_price,
            'risk': risk,
            'confidence': confidence_score,
            'entry_time': datetime.now()
        }
        
        # Update portfolio VaR
        self.portfolio_var = self.calculate_portfolio_var()
    
    def remove_position(self, pair):
        """Remove position from portfolio tracking"""
        if pair in self.active_positions:
            del self.active_positions[pair]
            self.portfolio_var = self.calculate_portfolio_var()
    
    def calculate_portfolio_var(self):
        """Calculate total portfolio VaR"""
        if not self.active_positions:
            return 0.0
        
        total_var = 0
        for pair, position in self.active_positions.items():
            var_95 = self.calculate_var_95(pair, position['size'], position['confidence'])
            total_var += var_95 ** 2  # Square for portfolio calculation
        
        return np.sqrt(total_var)  # Portfolio VaR with correlation effects
