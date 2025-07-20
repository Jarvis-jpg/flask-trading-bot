import pandas as pd
import numpy as np
from datetime import datetime
import joblib
import logging
from market_data import MarketData
from typing import Dict, List, Tuple
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradeAnalyzer:
    def __init__(self):
        self.market_data = MarketData()
        self.model = None
        self.scaler = None
        self.load_models()
        
    def load_models(self):
        """Load trained models and scalers"""
        try:
            model_path = os.path.join('models', 'model.pkl')
            scaler_path = os.path.join('models', 'scaler.pkl')
            
            if os.path.exists(model_path) and os.path.exists(scaler_path):
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                logger.info("Models loaded successfully")
            else:
                logger.warning("No trained models found")
                
        except Exception as e:
            logger.error(f"Error loading models: {e}")
    
    def extract_features(self, market_conditions: Dict, trade_setup: Dict) -> pd.DataFrame:
        """Extract features for trade analysis"""
        try:
            features = {}
            
            # Market condition features
            indicators = market_conditions['indicators']
            features.update({
                'trend': self._encode_trend(market_conditions['trend']),
                'volatility': self._encode_volatility(market_conditions['volatility']),
                'volume': self._encode_volume(market_conditions['volume_analysis']),
                'rsi': indicators['rsi_14'],
                'macd_diff': indicators['macd'] - indicators['macd_signal'],
                'price_to_sma20': market_conditions['price'] / indicators['sma_20'],
                'price_to_sma50': market_conditions['price'] / indicators['sma_50'],
                'atr': indicators['atr'],
                'cci': indicators['cci']
            })
            
            # Trade setup features
            if trade_setup:
                risk_reward = abs(float(trade_setup['take_profit']) - float(trade_setup['entry'])) / \
                             abs(float(trade_setup['stop_loss']) - float(trade_setup['entry']))
                features.update({
                    'risk_reward_ratio': risk_reward,
                    'confidence': float(trade_setup['confidence']),
                    'hour_of_day': datetime.now().hour,
                    'distance_to_support': abs(market_conditions['price'] - 
                                            market_conditions['support_resistance']['support']),
                    'distance_to_resistance': abs(market_conditions['price'] - 
                                               market_conditions['support_resistance']['resistance'])
                })
            
            return pd.DataFrame([features])
            
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            return None
    
    def analyze_trade(self, pair: str, trade_setup: Dict) -> Dict:
        """Analyze potential trade setup"""
        try:
            # Get market conditions
            market_conditions = self.market_data.analyze_market_conditions(pair)
            if not market_conditions:
                return {'error': 'Could not analyze market conditions'}
            
            # Extract features
            features = self.extract_features(market_conditions, trade_setup)
            if features is None:
                return {'error': 'Could not extract features'}
            
            # Make prediction if model exists
            prediction = {}
            if self.model and self.scaler:
                features_scaled = self.scaler.transform(features)
                win_probability = self.model.predict_proba(features_scaled)[0][1]
                prediction = {
                    'win_probability': round(win_probability, 4),
                    'recommended': win_probability > 0.6
                }
            
            # Prepare analysis result
            analysis = {
                'pair': pair,
                'timestamp': datetime.now().isoformat(),
                'market_conditions': {
                    'trend': market_conditions['trend'],
                    'volatility': market_conditions['volatility'],
                    'volume': market_conditions['volume_analysis']
                },
                'technical_analysis': {
                    'rsi': market_conditions['indicators']['rsi_14'],
                    'macd': market_conditions['indicators']['macd'],
                    'support': market_conditions['support_resistance']['support'],
                    'resistance': market_conditions['support_resistance']['resistance']
                },
                'trade_quality': self._analyze_trade_quality(trade_setup, market_conditions),
                'prediction': prediction
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing trade: {e}")
            return {'error': str(e)}
    
    def _analyze_trade_quality(self, trade_setup: Dict, 
                             market_conditions: Dict) -> Dict:
        """Analyze the quality of a trade setup"""
        try:
            price = market_conditions['price']
            indicators = market_conditions['indicators']
            
            # Calculate various quality metrics
            quality = {
                'risk_reward_ratio': abs(float(trade_setup['take_profit']) - float(trade_setup['entry'])) / \
                                   abs(float(trade_setup['stop_loss']) - float(trade_setup['entry'])),
                'trend_alignment': self._check_trend_alignment(
                    trade_setup['action'], 
                    market_conditions['trend']
                ),
                'support_resistance_quality': self._check_support_resistance(
                    trade_setup,
                    market_conditions['support_resistance']
                ),
                'indicator_alignment': self._check_indicator_alignment(
                    trade_setup['action'],
                    indicators
                )
            }
            
            # Calculate overall score
            weights = {
                'risk_reward_ratio': 0.3,
                'trend_alignment': 0.3,
                'support_resistance_quality': 0.2,
                'indicator_alignment': 0.2
            }
            
            quality['overall_score'] = sum(
                quality[metric] * weights[metric] 
                for metric in weights
            )
            
            return quality
            
        except Exception as e:
            logger.error(f"Error analyzing trade quality: {e}")
            return {}
    
    def _encode_trend(self, trend: str) -> float:
        """Encode trend as numeric value"""
        trend_values = {
            'strong_uptrend': 1.0,
            'weak_uptrend': 0.5,
            'sideways': 0.0,
            'weak_downtrend': -0.5,
            'strong_downtrend': -1.0,
            'unknown': 0.0
        }
        return trend_values.get(trend, 0.0)
    
    def _encode_volatility(self, volatility: str) -> float:
        """Encode volatility as numeric value"""
        vol_values = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.9,
            'unknown': 0.5
        }
        return vol_values.get(volatility, 0.5)
    
    def _encode_volume(self, volume: str) -> float:
        """Encode volume as numeric value"""
        vol_values = {
            'low': 0.3,
            'normal': 0.6,
            'high': 0.9,
            'unknown': 0.5
        }
        return vol_values.get(volume, 0.5)
    
    def _check_trend_alignment(self, action: str, trend: str) -> float:
        """Check if trade aligns with trend"""
        if action == 'buy':
            if trend in ['strong_uptrend', 'weak_uptrend']:
                return 1.0
            elif trend == 'sideways':
                return 0.5
            else:
                return 0.0
        else:  # sell
            if trend in ['strong_downtrend', 'weak_downtrend']:
                return 1.0
            elif trend == 'sideways':
                return 0.5
            else:
                return 0.0
    
    def _check_support_resistance(self, trade_setup: Dict, 
                                levels: Dict) -> float:
        """Check trade alignment with support/resistance levels"""
        try:
            entry = float(trade_setup['entry'])
            support = levels['support']
            resistance = levels['resistance']
            
            if trade_setup['action'] == 'buy':
                if entry - support < (resistance - support) * 0.3:
                    return 1.0  # Good buy near support
                elif entry > resistance:
                    return 0.0  # Bad buy above resistance
                else:
                    return 0.5
            else:  # sell
                if resistance - entry < (resistance - support) * 0.3:
                    return 1.0  # Good sell near resistance
                elif entry < support:
                    return 0.0  # Bad sell below support
                else:
                    return 0.5
                    
        except Exception as e:
            logger.error(f"Error checking support/resistance: {e}")
            return 0.5
    
    def _check_indicator_alignment(self, action: str, indicators: Dict) -> float:
        """Check if indicators align with trade direction"""
        try:
            score = 0.0
            total_indicators = 0
            
            # RSI
            if 'rsi_14' in indicators:
                total_indicators += 1
                rsi = indicators['rsi_14']
                if action == 'buy' and rsi < 30:
                    score += 1
                elif action == 'sell' and rsi > 70:
                    score += 1
                elif 40 <= rsi <= 60:
                    score += 0.5
            
            # MACD
            if 'macd' in indicators and 'macd_signal' in indicators:
                total_indicators += 1
                if action == 'buy' and indicators['macd'] > indicators['macd_signal']:
                    score += 1
                elif action == 'sell' and indicators['macd'] < indicators['macd_signal']:
                    score += 1
            
            # Moving Averages
            if 'sma_20' in indicators and 'sma_50' in indicators:
                total_indicators += 1
                if action == 'buy' and indicators['sma_20'] > indicators['sma_50']:
                    score += 1
                elif action == 'sell' and indicators['sma_20'] < indicators['sma_50']:
                    score += 1
            
            return score / total_indicators if total_indicators > 0 else 0.5
            
        except Exception as e:
            logger.error(f"Error checking indicator alignment: {e}")
            return 0.5
