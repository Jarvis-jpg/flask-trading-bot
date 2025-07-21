from typing import Dict, List, Optional
import numpy as np
from datetime import datetime, timedelta

class RiskManager:
    def __init__(self, initial_balance: float = 200.0):
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.max_drawdown = 0.15  # 15% maximum drawdown - adjusted for small account
        self.max_risk_per_trade = 0.05  # 5% risk per trade as requested
        self.max_daily_risk = 0.15  # 15% maximum daily risk - adjusted for aggressive trading
        self.correlation_threshold = 0.85  # More lenient correlation threshold (was 0.7)
        self.min_trades_for_correlation = 3  # Minimum trades before checking correlation
        self.trade_history: List[Dict] = []
        self.daily_trades: List[Dict] = []
        
    def validate_trade(self, trade: Dict, market_conditions: Dict) -> tuple[bool, str]:
        """
        Validate if a trade meets all risk management criteria.
        Returns: (is_valid, reason)
        """
        # Check drawdown
        if self._check_drawdown():
            return False, "Maximum drawdown reached"
            
        # Check daily risk
        if self._check_daily_risk(trade):
            return False, "Maximum daily risk reached"
            
        # Check market conditions
        if not self._validate_market_conditions(market_conditions):
            return False, "Unfavorable market conditions"
            
        # Check position sizing
        if not self._validate_position_size(trade):
            return False, "Invalid position size"
            
        # Check correlation risk
        if self._check_correlation_risk(trade):
            return False, "High correlation with existing trades"
            
        return True, "Trade validated"
        
    def calculate_position_size(self, trade: Dict) -> float:
        """Calculate safe position size based on risk parameters and Oanda requirements."""
        entry = trade['entry']
        stop_loss = trade['stop_loss']
        
        # Calculate pip size for the currency pair
        if trade['pair'].endswith('JPY'):
            pip_size = 0.01
        else:
            pip_size = 0.0001
            
        # Calculate stop loss in pips
        stop_loss_pips = abs(entry - stop_loss) / pip_size
        
        # Calculate risk amount in account currency (5% of balance)
        risk_amount = self.current_balance * self.max_risk_per_trade
        
        # Calculate pip value for minimum position size (1 unit)
        if trade['pair'].endswith('JPY'):
            pip_value_per_unit = 0.01 / entry  # Convert to USD
        else:
            pip_value_per_unit = 0.0001  # USD pairs
            
        # Calculate position size
        if stop_loss_pips > 0:
            # Calculate required position size to achieve desired risk
            position_size = int(risk_amount / (stop_loss_pips * pip_value_per_unit))
            # Ensure minimum viable position size
            position_size = max(1, position_size)
            # Cap maximum position size at 50% of account value converted to units
            max_units = int((self.current_balance * 0.5) / entry)
            position_size = min(position_size, max_units)
        else:
            position_size = 0
            
        return position_size
        
    def update_trade_history(self, trade: Dict):
        """Update trade history and recalculate metrics."""
        self.trade_history.append(trade)
        self.daily_trades.append(trade)
        
        # Update current balance
        self.current_balance += trade['profit']
        
        # Clean up old daily trades
        self._cleanup_daily_trades()
        
    def _check_drawdown(self) -> bool:
        """Check if maximum drawdown has been reached."""
        if not self.trade_history:
            return False
            
        peak_balance = max(self.initial_balance, max(t['balance'] for t in self.trade_history))
        current_drawdown = (peak_balance - self.current_balance) / peak_balance
        
        return current_drawdown > self.max_drawdown
        
    def _check_daily_risk(self, new_trade: Dict) -> bool:
        """Check if adding this trade would exceed daily risk limit."""
        daily_risk = sum(abs(t['profit']) for t in self.daily_trades)
        new_risk = abs(new_trade['entry'] - new_trade['stop_loss'])
        
        return (daily_risk + new_risk) > (self.current_balance * self.max_daily_risk)
        
    def _validate_market_conditions(self, conditions: Dict) -> bool:
        """Validate if market conditions are suitable for trading."""
        # Calculate recent performance
        recent_trades = self.trade_history[-5:] if self.trade_history else []
        recent_win_rate = sum(1 for t in recent_trades if t.get('profitable', False)) / len(recent_trades) if recent_trades else 0
        
        # Adjust thresholds based on recent performance
        spread_threshold = 2.5 if recent_win_rate > 0.5 else 2.0
        liquidity_threshold = 0.25 if recent_win_rate > 0.5 else 0.3
        volatility_threshold = 1.0 if recent_win_rate > 0.5 else 0.9
        
        # Dynamic market condition validation
        if conditions.get('spread', 0) > spread_threshold:
            return False
            
        if conditions.get('liquidity', 1.0) < liquidity_threshold:
            return False
            
        if conditions.get('volatility', 0) > volatility_threshold:
            return False
            
        # Allow trading if conditions are very good
        if (conditions.get('spread', 0) < 1.0 and 
            conditions.get('liquidity', 1.0) > 0.7 and
            0.3 < conditions.get('volatility', 0) < 0.7):
            return True
            
        return True
        
    def _validate_position_size(self, trade: Dict) -> bool:
        """Validate if position size is within acceptable limits."""
        position_size = trade.get('units', 0)
        
        # Check minimum position size - Oanda allows minimum 1 unit
        if position_size < 1:
            return False
            
        # Ensure position size is a whole number (Oanda requirement)
        if not float(position_size).is_integer():
            return False
            
        # Check maximum position size - allow up to 50% of account for small accounts
        max_position = self.current_balance * 0.5
        if position_size > max_position:
            return False
            
        return True
        
    def _check_correlation_risk(self, trade: Dict) -> bool:
        """Smart pattern detection that focuses only on risky trade repetition."""
        # Don't check until we have some history
        if len(self.trade_history) < 2:
            return False
            
        # Get last 3 trades
        recent_trades = self.trade_history[-3:]
        
        # Only care about correlation in these cases:
        # 1. After consecutive losses
        # 2. When market conditions are poor
        # 3. When trying same direction repeatedly
        
        # Count recent losses
        recent_losses = sum(1 for t in recent_trades if not t.get('profitable', False))
        
        # If we don't have losses, don't worry about correlation
        if recent_losses == 0:
            return False
            
        # Get current trade direction
        is_buy = trade['take_profit'] > trade['entry']
        
        # Check last trade
        last_trade = recent_trades[-1]
        last_trade_was_buy = last_trade['take_profit'] > last_trade['entry']
        
        # Only block trades if ALL these are true:
        # 1. Same direction as last trade
        # 2. We had a recent loss
        # 3. Market conditions aren't great
        if (is_buy == last_trade_was_buy and  # Same direction
            not last_trade.get('profitable', False) and  # Last trade was a loss
            (
                trade.get('spread', 0) > 1.2 or  # Poor spread
                trade.get('volatility', 0.5) > 0.8 or  # High volatility
                trade.get('volume', 1.0) < 0.5  # Low volume
            )):
            return True
            
        # If market conditions are very good, always allow trade
        if (trade.get('spread', 0) < 0.8 and  # Tight spread
            trade.get('volume', 1.0) > 0.8 and  # Good volume
            0.3 < trade.get('volatility', 0.5) < 0.7):  # Good volatility
            return False
            
        # Allow trade by default
        return False
            
        # If we're in a winning streak or neutral, be more lenient
        winning_streak = sum(1 for t in recent_trades[-2:] if t.get('profitable', False)) == 2
        if winning_streak:
            return False  # Allow similar trades during winning streaks
            
        # Default to allowing the trade
        return False
        
    def _calculate_pip_value(self, pair: str) -> float:
        """Calculate pip value for given currency pair based on Oanda standards."""
        # Standard pip values for $1000 position size
        base_pip_values = {
            "EUR_USD": 0.0001,  # $0.10 per pip per 1000 units
            "GBP_USD": 0.0001,  # $0.10 per pip per 1000 units
            "USD_JPY": 0.01,    # ¥1.00 per pip per 1000 units ≈ $0.09
            "USD_CHF": 0.0001,  # CHF0.10 per pip per 1000 units
            "AUD_USD": 0.0001,  # $0.10 per pip per 1000 units
            "NZD_USD": 0.0001   # $0.10 per pip per 1000 units
        }
        
        # Get base pip value and adjust for actual position size
        pip_size = base_pip_values.get(pair, 0.0001)
        
        # For USD pairs, 1 pip = $0.0001 per unit
        if pair.endswith('USD'):
            return pip_size * 0.0001
        # For JPY pairs, 1 pip = ¥0.01 per unit ≈ $0.00009
        elif pair.endswith('JPY'):
            return pip_size * 0.00009
        # Default for other pairs
        else:
            return pip_size * 0.0001
        
    def _round_position_size(self, size: float) -> float:
        """Round position size to nearest standard lot size."""
        # Round down to nearest 0.01 lot (1000 units)
        return float(int(size / 1000) * 1000)
        
    def _cleanup_daily_trades(self):
        """Remove trades older than 24 hours from daily trades list."""
        current_time = datetime.now()
        self.daily_trades = [
            trade for trade in self.daily_trades
            if datetime.fromisoformat(trade['timestamp']) > current_time - timedelta(days=1)
        ]
        
    def _calculate_trade_correlation(self, trade: Dict) -> float:
        """Calculate correlation of new trade with existing trades."""
        recent_trades = self.trade_history[-5:]  # Last 5 trades
        if not recent_trades:
            return 0.0
            
        # Convert trend to numeric value
        def trend_to_numeric(trend):
            if isinstance(trend, str):
                return {'uptrend': 1, 'downtrend': -1, 'sideways': 0}.get(trend, 0)
            return float(trend)
            
        # Extract features for correlation calculation
        trade_features = np.array([
            trend_to_numeric(trade.get('trend', 0)),
            float(trade.get('volatility', 0)),
            float(trade.get('rsi', 50)),
            float(trade.get('macd_diff', 0))
        ])
        
        correlations = []
        for past_trade in recent_trades:
            past_features = np.array([
                trend_to_numeric(past_trade.get('trend', 0)),
                float(past_trade.get('volatility', 0)),
                float(past_trade.get('rsi', 50)),
                float(past_trade.get('macd_diff', 0))
            ])
            
            # Reshape arrays for correlation calculation
            trade_features_reshaped = trade_features.reshape(1, -1)
            past_features_reshaped = past_features.reshape(1, -1)
            
            try:
                # Calculate correlation while handling potential numerical issues
                correlation = np.corrcoef(trade_features_reshaped[0], past_features_reshaped[0])[0, 1]
                if np.isnan(correlation):
                    correlation = 0.0
            except:
                correlation = 0.0
                
            correlations.append(abs(correlation))
            
        return max(correlations) if correlations else 0.0
