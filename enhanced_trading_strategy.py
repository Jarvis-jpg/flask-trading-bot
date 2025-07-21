#!/usr/bin/env python3
"""
Enhanced Trading Strategy Implementation with AI-Driven Decisions
This module implements advanced trading strategies with machine learning
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import ta  # Technical analysis library
import logging
from typing import Dict, List, Tuple, Optional
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedTradingStrategy:
    """
    Advanced trading strategy with multiple proven indicators and AI decision making
    """
    
    def __init__(self):
        self.strategy_config = {
            'risk_reward_min': 2.0,  # Minimum 2:1 risk reward ratio
            'max_risk_per_trade': 0.02,  # 2% max risk per trade
            'confidence_threshold': 0.7,  # 70% minimum confidence
            'stop_loss_atr_multiplier': 2.0,  # Dynamic stop loss
            'take_profit_atr_multiplier': 4.0,  # Dynamic take profit
        }
        
        self.currency_pairs = [
            'EUR_USD', 'GBP_USD', 'USD_JPY', 'USD_CHF',
            'AUD_USD', 'USD_CAD', 'NZD_USD', 'EUR_GBP'
        ]
        
        self.session_times = {
            'london': {'start': 8, 'end': 16},
            'new_york': {'start': 13, 'end': 21},
            'asian': {'start': 22, 'end': 6}
        }
        
    def calculate_technical_indicators(self, price_data: pd.DataFrame) -> Dict:
        """Calculate comprehensive technical indicators"""
        try:
            if len(price_data) < 50:
                logger.warning("Insufficient data for technical analysis")
                return {}
                
            # Trend indicators
            sma_20 = ta.trend.sma_indicator(price_data['close'], window=20)
            sma_50 = ta.trend.sma_indicator(price_data['close'], window=50)
            ema_12 = ta.trend.ema_indicator(price_data['close'], window=12)
            ema_26 = ta.trend.ema_indicator(price_data['close'], window=26)
            
            # Momentum indicators
            rsi = ta.momentum.rsi(price_data['close'], window=14)
            macd = ta.trend.macd_diff(price_data['close'])
            stoch = ta.momentum.stoch(price_data['high'], price_data['low'], price_data['close'])
            
            # Volatility indicators
            bb_high, bb_low = ta.volatility.bollinger_hband(price_data['close']), ta.volatility.bollinger_lband(price_data['close'])
            atr = ta.volatility.average_true_range(price_data['high'], price_data['low'], price_data['close'])
            
            # Volume indicators (if available)
            if 'volume' in price_data.columns:
                # Calculate simple moving average of volume
                volume_sma = price_data['volume'].rolling(window=20).mean()
            else:
                volume_sma = pd.Series([1] * len(price_data))
            
            current_price = price_data['close'].iloc[-1]
            
            indicators = {
                'sma_20': sma_20.iloc[-1],
                'sma_50': sma_50.iloc[-1],
                'ema_12': ema_12.iloc[-1],
                'ema_26': ema_26.iloc[-1],
                'rsi': rsi.iloc[-1],
                'macd': macd.iloc[-1],
                'stoch': stoch.iloc[-1],
                'bb_high': bb_high.iloc[-1],
                'bb_low': bb_low.iloc[-1],
                'atr': atr.iloc[-1],
                'current_price': current_price,
                'volume_sma': volume_sma.iloc[-1],
                
                # Derived indicators
                'price_above_sma20': current_price > sma_20.iloc[-1],
                'price_above_sma50': current_price > sma_50.iloc[-1],
                'sma20_above_sma50': sma_20.iloc[-1] > sma_50.iloc[-1],
                'ema_bullish': ema_12.iloc[-1] > ema_26.iloc[-1],
                'rsi_oversold': rsi.iloc[-1] < 30,
                'rsi_overbought': rsi.iloc[-1] > 70,
                'macd_bullish': macd.iloc[-1] > 0,
                'stoch_oversold': stoch.iloc[-1] < 20,
                'stoch_overbought': stoch.iloc[-1] > 80,
                'near_bb_lower': current_price <= bb_low.iloc[-1] * 1.01,
                'near_bb_upper': current_price >= bb_high.iloc[-1] * 0.99,
            }
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating technical indicators: {e}")
            return {}
    
    def detect_market_session(self) -> str:
        """Detect current market session"""
        current_hour = datetime.now().hour
        
        for session, times in self.session_times.items():
            if times['start'] <= times['end']:
                if times['start'] <= current_hour <= times['end']:
                    return session
            else:  # Handle overnight sessions (like Asian)
                if current_hour >= times['start'] or current_hour <= times['end']:
                    return session
        
        return 'off_session'
    
    def calculate_volatility_regime(self, price_data: pd.DataFrame) -> str:
        """Determine current volatility regime"""
        if len(price_data) < 20:
            return 'unknown'
            
        returns = price_data['close'].pct_change().dropna()
        current_vol = returns.rolling(20).std().iloc[-1]
        long_term_vol = returns.rolling(100).std().iloc[-1] if len(returns) >= 100 else current_vol
        
        if current_vol > long_term_vol * 1.5:
            return 'high'
        elif current_vol < long_term_vol * 0.7:
            return 'low'
        else:
            return 'normal'
    
    def generate_trade_signal(self, pair: str, price_data: pd.DataFrame) -> Dict:
        """Generate comprehensive trade signal using multiple strategies"""
        try:
            indicators = self.calculate_technical_indicators(price_data)
            if not indicators:
                return {
                    'signal': 'no_signal', 
                    'confidence': 0, 
                    'reason': 'insufficient_data',
                    'pair': pair,
                    'entry': price_data['close'].iloc[-1] if len(price_data) > 0 else 1.0
                }
            
            session = self.detect_market_session()
            volatility = self.calculate_volatility_regime(price_data)
            
            # Strategy 1: Trend Following with RSI Filter
            trend_signal = self._trend_following_strategy(indicators)
            
            # Strategy 2: Mean Reversion at Support/Resistance
            mean_reversion_signal = self._mean_reversion_strategy(indicators)
            
            # Strategy 3: Breakout Strategy
            breakout_signal = self._breakout_strategy(indicators, price_data)
            
            # Strategy 4: Session-based Momentum
            momentum_signal = self._momentum_strategy(indicators, session)
            
            # Combine signals with weights
            signals = [trend_signal, mean_reversion_signal, breakout_signal, momentum_signal]
            combined_signal = self._combine_signals(signals, session, volatility)
            
            # Ensure entry price is always included
            current_price = indicators.get('current_price', price_data['close'].iloc[-1] if len(price_data) > 0 else 1.0)
            
            # Add risk management parameters
            if combined_signal['signal'] != 'no_signal':
                combined_signal.update(self._calculate_risk_parameters(indicators, combined_signal))
            else:
                # Even for no_signal, include basic entry price
                combined_signal['entry'] = current_price
            
            combined_signal['pair'] = pair
            combined_signal['timestamp'] = datetime.now().isoformat()
            combined_signal['session'] = session
            combined_signal['volatility_regime'] = volatility
            
            return combined_signal
            
        except Exception as e:
            logger.error(f"Error generating trade signal for {pair}: {e}")
            return {
                'signal': 'no_signal', 
                'confidence': 0, 
                'reason': f'error: {str(e)}',
                'pair': pair,
                'entry': price_data['close'].iloc[-1] if len(price_data) > 0 else 1.0
            }
    
    def _trend_following_strategy(self, indicators: Dict) -> Dict:
        """Trend following strategy with multiple confirmations"""
        score = 0
        max_score = 6
        
        # Check trend alignment
        if indicators.get('price_above_sma20') and indicators.get('sma20_above_sma50'):
            score += 2  # Strong uptrend
        elif not indicators.get('price_above_sma20') and not indicators.get('sma20_above_sma50'):
            score -= 2  # Strong downtrend
            
        # EMA confirmation
        if indicators.get('ema_bullish'):
            score += 1
        else:
            score -= 1
            
        # MACD confirmation
        if indicators.get('macd_bullish'):
            score += 1
        else:
            score -= 1
            
        # RSI filter (avoid overbought/oversold)
        rsi = indicators.get('rsi', 50)
        if 30 < rsi < 70:
            score += 2  # Neutral RSI is good for trend following
        elif rsi > 80 or rsi < 20:
            score -= 2  # Extreme RSI
            
        confidence = abs(score) / max_score
        
        if score >= 4:
            return {'signal': 'buy', 'confidence': confidence, 'strategy': 'trend_following'}
        elif score <= -4:
            return {'signal': 'sell', 'confidence': confidence, 'strategy': 'trend_following'}
        else:
            return {'signal': 'no_signal', 'confidence': confidence, 'strategy': 'trend_following'}
    
    def _mean_reversion_strategy(self, indicators: Dict) -> Dict:
        """Mean reversion strategy using Bollinger Bands and RSI"""
        score = 0
        max_score = 4
        
        # Bollinger Bands mean reversion
        if indicators.get('near_bb_lower') and indicators.get('rsi_oversold'):
            score += 2  # Buy signal
        elif indicators.get('near_bb_upper') and indicators.get('rsi_overbought'):
            score -= 2  # Sell signal
            
        # Stochastic confirmation
        if indicators.get('stoch_oversold'):
            score += 1
        elif indicators.get('stoch_overbought'):
            score -= 1
            
        # Trend filter - avoid counter-trend trades in strong trends
        if indicators.get('sma20_above_sma50'):
            if score < 0:  # Don't sell in uptrend
                score = 0
        else:
            if score > 0:  # Don't buy in downtrend
                score = 0
                
        confidence = abs(score) / max_score
        
        if score >= 3:
            return {'signal': 'buy', 'confidence': confidence, 'strategy': 'mean_reversion'}
        elif score <= -3:
            return {'signal': 'sell', 'confidence': confidence, 'strategy': 'mean_reversion'}
        else:
            return {'signal': 'no_signal', 'confidence': confidence, 'strategy': 'mean_reversion'}
    
    def _breakout_strategy(self, indicators: Dict, price_data: pd.DataFrame) -> Dict:
        """Breakout strategy using volatility and momentum"""
        if len(price_data) < 20:
            return {'signal': 'no_signal', 'confidence': 0, 'strategy': 'breakout'}
            
        current_price = indicators.get('current_price')
        bb_high = indicators.get('bb_high')
        bb_low = indicators.get('bb_low')
        
        # Recent high/low analysis
        recent_high = price_data['high'].rolling(20).max().iloc[-1]
        recent_low = price_data['low'].rolling(20).min().iloc[-1]
        
        score = 0
        max_score = 4
        
        # Breakout detection
        if current_price > bb_high and current_price > recent_high * 0.999:
            score += 2  # Upward breakout
        elif current_price < bb_low and current_price < recent_low * 1.001:
            score -= 2  # Downward breakout
            
        # Volume confirmation (if available)
        if indicators.get('volume_sma', 1) > 1.2:
            score += 1 if score > 0 else -1
            
        # Momentum confirmation
        if indicators.get('rsi', 50) > 60 and score > 0:
            score += 1
        elif indicators.get('rsi', 50) < 40 and score < 0:
            score -= 1
            
        confidence = abs(score) / max_score
        
        if score >= 3:
            return {'signal': 'buy', 'confidence': confidence, 'strategy': 'breakout'}
        elif score <= -3:
            return {'signal': 'sell', 'confidence': confidence, 'strategy': 'breakout'}
        else:
            return {'signal': 'no_signal', 'confidence': confidence, 'strategy': 'breakout'}
    
    def _momentum_strategy(self, indicators: Dict, session: str) -> Dict:
        """Session-based momentum strategy"""
        score = 0
        max_score = 4
        
        # Session-specific logic
        if session == 'london':
            # London session - look for continuation moves
            if indicators.get('ema_bullish') and indicators.get('macd_bullish'):
                score += 2
            elif not indicators.get('ema_bullish') and not indicators.get('macd_bullish'):
                score -= 2
        elif session == 'new_york':
            # NY session - momentum continuation
            if indicators.get('rsi', 50) > 55 and indicators.get('price_above_sma20'):
                score += 2
            elif indicators.get('rsi', 50) < 45 and not indicators.get('price_above_sma20'):
                score -= 2
        else:
            # Other sessions - reduce activity
            score = 0
            
        # MACD momentum
        if indicators.get('macd', 0) > 0.0001:
            score += 1
        elif indicators.get('macd', 0) < -0.0001:
            score -= 1
            
        confidence = abs(score) / max_score
        
        if score >= 3:
            return {'signal': 'buy', 'confidence': confidence, 'strategy': 'momentum'}
        elif score <= -3:
            return {'signal': 'sell', 'confidence': confidence, 'strategy': 'momentum'}
        else:
            return {'signal': 'no_signal', 'confidence': confidence, 'strategy': 'momentum'}
    
    def _combine_signals(self, signals: List[Dict], session: str, volatility: str) -> Dict:
        """Intelligently combine multiple strategy signals"""
        buy_votes = sum(1 for s in signals if s['signal'] == 'buy')
        sell_votes = sum(1 for s in signals if s['signal'] == 'sell')
        
        # Calculate weighted confidence
        total_confidence = sum(s['confidence'] for s in signals if s['signal'] != 'no_signal')
        active_signals = sum(1 for s in signals if s['signal'] != 'no_signal')
        
        if active_signals == 0:
            return {'signal': 'no_signal', 'confidence': 0, 'reason': 'no_active_signals'}
        
        avg_confidence = total_confidence / active_signals
        
        # Session and volatility adjustments
        if session == 'off_session':
            avg_confidence *= 0.7  # Reduce confidence during off hours
        if volatility == 'high':
            avg_confidence *= 0.8  # Reduce confidence in high volatility
        elif volatility == 'low':
            avg_confidence *= 1.1  # Increase confidence in stable markets
            
        # Determine final signal
        if buy_votes >= 2 and buy_votes > sell_votes and avg_confidence >= self.strategy_config['confidence_threshold']:
            return {
                'signal': 'buy',
                'confidence': min(avg_confidence, 0.95),
                'strategy': 'combined',
                'votes': {'buy': buy_votes, 'sell': sell_votes}
            }
        elif sell_votes >= 2 and sell_votes > buy_votes and avg_confidence >= self.strategy_config['confidence_threshold']:
            return {
                'signal': 'sell',
                'confidence': min(avg_confidence, 0.95),
                'strategy': 'combined',
                'votes': {'buy': buy_votes, 'sell': sell_votes}
            }
        else:
            return {
                'signal': 'no_signal',
                'confidence': avg_confidence,
                'reason': 'insufficient_consensus',
                'votes': {'buy': buy_votes, 'sell': sell_votes}
            }
    
    def _calculate_risk_parameters(self, indicators: Dict, signal: Dict) -> Dict:
        """Calculate dynamic risk management parameters"""
        current_price = indicators.get('current_price')
        atr = indicators.get('atr', current_price * 0.01)  # Default 1% if ATR unavailable
        
        # Dynamic stop loss based on ATR
        stop_distance = atr * self.strategy_config['stop_loss_atr_multiplier']
        
        # Dynamic take profit based on risk-reward ratio
        profit_distance = stop_distance * self.strategy_config['risk_reward_min']
        
        if signal['signal'] == 'buy':
            stop_loss = current_price - stop_distance
            take_profit = current_price + profit_distance
        elif signal['signal'] == 'sell':
            stop_loss = current_price + stop_distance
            take_profit = current_price - profit_distance
        else:
            return {}
        
        # Calculate position size based on risk
        account_risk = 10000 * self.strategy_config['max_risk_per_trade']  # Assume $10k account
        risk_per_unit = abs(current_price - stop_loss)
        position_size = min(int(account_risk / risk_per_unit), 100000)  # Max 100k units
        
        return {
            'entry': current_price,
            'stop_loss': round(stop_loss, 5),
            'take_profit': round(take_profit, 5),
            'units': position_size,
            'risk_reward_ratio': round(abs(take_profit - current_price) / abs(current_price - stop_loss), 2),
            'atr': round(atr, 5)
        }

# Global instance for easy access
trading_strategy = EnhancedTradingStrategy()
