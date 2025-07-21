import random
from datetime import datetime, timedelta
from typing import Dict, Optional

class MarketExecution:
    def __init__(self):
        self.last_execution_time = None
        self.min_execution_delay = 0.2  # 200ms minimum execution delay
        self.max_execution_delay = 2.0  # 2 second maximum delay
        
    def calculate_slippage(self, trade: Dict, market_conditions: Dict) -> float:
        """Calculate realistic slippage based on market conditions."""
        # Base slippage factors
        base_slippage_pips = random.uniform(0.1, 0.5)
        
        # Increase slippage in poor conditions
        if market_conditions.get('liquidity', 1.0) < 0.7:
            base_slippage_pips *= 1.5
        if market_conditions.get('volatility', 0.5) > 0.7:
            base_slippage_pips *= 1.3
            
        # More slippage during news events
        if market_conditions.get('is_news_time', False):
            base_slippage_pips *= 2.0
            
        # Convert pips to price
        if trade['pair'].endswith('JPY'):
            slippage = base_slippage_pips * 0.01
        else:
            slippage = base_slippage_pips * 0.0001
            
        return slippage
        
    def simulate_execution(self, trade: Dict, market_conditions: Dict) -> Dict:
        """Simulate realistic trade execution with delays and slippage."""
        # Calculate execution delay
        current_time = datetime.now()
        
        # Enforce minimum time between executions
        if self.last_execution_time:
            time_since_last = (current_time - self.last_execution_time).total_seconds()
            if time_since_last < self.min_execution_delay:
                return None  # Too soon to execute another trade
                
        # Calculate execution delay based on conditions
        base_delay = random.uniform(self.min_execution_delay, self.max_execution_delay)
        
        # Increase delay in poor conditions
        if market_conditions.get('liquidity', 1.0) < 0.7:
            base_delay *= 1.5
        if market_conditions.get('volatility', 0.5) > 0.7:
            base_delay *= 1.3
            
        # Calculate slippage
        slippage = self.calculate_slippage(trade, market_conditions)
        
        # Apply slippage to entry price
        original_entry = trade['entry']
        if trade['take_profit'] > trade['entry']:  # Long trade
            trade['entry'] = original_entry + slippage
        else:  # Short trade
            trade['entry'] = original_entry - slippage
            
        # Update stop loss and take profit with slippage
        sl_distance = abs(original_entry - trade['stop_loss'])
        tp_distance = abs(trade['take_profit'] - original_entry)
        
        if trade['take_profit'] > trade['entry']:  # Long trade
            trade['stop_loss'] = trade['entry'] - sl_distance
            trade['take_profit'] = trade['entry'] + tp_distance
        else:  # Short trade
            trade['stop_loss'] = trade['entry'] + sl_distance
            trade['take_profit'] = trade['entry'] - tp_distance
            
        # Record execution time
        self.last_execution_time = current_time
        
        # Add execution metrics to trade
        trade['execution_delay'] = base_delay
        trade['slippage'] = slippage
        
        return trade
        
    def check_broker_restrictions(self, trade: Dict) -> bool:
        """Check if trade meets broker's restrictions."""
        # Minimum and maximum position sizes
        if trade.get('units', 0) < 1:  # Minimum 1 unit
            return False
        if trade.get('units', 0) > 10000000:  # Maximum 10M units
            return False
            
        # Minimum distance between entry and SL/TP
        min_distance = 0.0010  # 10 pips minimum distance
        if trade['pair'].endswith('JPY'):
            min_distance = 0.01
            
        if abs(trade['entry'] - trade['stop_loss']) < min_distance:
            return False
        if abs(trade['entry'] - trade['take_profit']) < min_distance:
            return False
            
        return True
