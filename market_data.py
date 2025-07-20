from datetime import datetime
import requests
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import talib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketData:
    def __init__(self):
        self.api_key = None  # Add your broker/data provider API key here
        self.price_cache = {}
        self.timeframes = ['1m', '5m', '15m', '1h', '4h', '1d']
        
    def get_live_price(self, pair: str) -> Dict:
        """Get real-time price data for a currency pair"""
        try:
            # Replace this with your actual broker/data provider API call
            # This is a placeholder that would need to be implemented with your broker's API
            current_price = self.price_cache.get(pair, {}).get('price', 0)
            
            if not current_price:
                logger.warning(f"No live price available for {pair}, using simulation")
                # Simulate price data for testing
                base_prices = {
                    "EURUSD": 1.0950,
                    "GBPUSD": 1.2750,
                    "USDJPY": 143.50,
                    "AUDUSD": 0.6750,
                    "USDCAD": 1.3450,
                    "NZDUSD": 0.6250,
                    "EURGBP": 0.8550,
                    "EURJPY": 157.50
                }
                current_price = base_prices.get(pair, 1.0000)
                
            return {
                'pair': pair,
                'price': current_price,
                'timestamp': datetime.now().isoformat(),
                'bid': current_price - 0.0001,
                'ask': current_price + 0.0001,
                'volume': 1000000  # Simulated volume
            }
            
        except Exception as e:
            logger.error(f"Error getting live price for {pair}: {e}")
            return None
    
    def get_historical_data(self, pair: str, timeframe: str = '1h', 
                          bars: int = 100) -> pd.DataFrame:
        """Get historical price data for analysis"""
        try:
            # Replace this with your actual broker/data provider API call
            # This is a placeholder that would need to be implemented with your broker's API
            
            # Simulate historical data for testing
            timestamps = pd.date_range(end=datetime.now(), periods=bars, freq=timeframe)
            base_price = float(self.get_live_price(pair)['price'])
            
            data = pd.DataFrame({
                'timestamp': timestamps,
                'open': [base_price + np.random.normal(0, 0.0010) for _ in range(bars)],
                'high': [base_price + np.random.normal(0, 0.0015) for _ in range(bars)],
                'low': [base_price + np.random.normal(0, 0.0015) for _ in range(bars)],
                'close': [base_price + np.random.normal(0, 0.0010) for _ in range(bars)],
                'volume': [np.random.randint(100000, 1000000) for _ in range(bars)]
            })
            
            # Ensure high is highest and low is lowest
            data['high'] = data[['open', 'high', 'close']].max(axis=1)
            data['low'] = data[['open', 'low', 'close']].min(axis=1)
            
            return data
            
        except Exception as e:
            logger.error(f"Error getting historical data for {pair}: {e}")
            return None
    
    def calculate_indicators(self, data: pd.DataFrame) -> Dict:
        """Calculate technical indicators for analysis"""
        try:
            if len(data) < 50:
                raise ValueError("Not enough data for indicator calculation")
                
            indicators = {}
            
            # Basic indicators
            indicators['sma_20'] = talib.SMA(data['close'], timeperiod=20)[-1]
            indicators['sma_50'] = talib.SMA(data['close'], timeperiod=50)[-1]
            indicators['rsi_14'] = talib.RSI(data['close'], timeperiod=14)[-1]
            
            # Trend indicators
            indicators['macd'], indicators['macd_signal'], _ = talib.MACD(
                data['close'], fastperiod=12, slowperiod=26, signalperiod=9
            )
            indicators['macd'] = indicators['macd'][-1]
            indicators['macd_signal'] = indicators['macd_signal'][-1]
            
            # Volatility indicators
            indicators['atr'] = talib.ATR(
                data['high'], data['low'], data['close'], timeperiod=14
            )[-1]
            
            # Momentum indicators
            indicators['cci'] = talib.CCI(
                data['high'], data['low'], data['close'], timeperiod=14
            )[-1]
            
            # Volume indicators
            indicators['obv'] = talib.OBV(data['close'], data['volume'])[-1]
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return None
    
    def analyze_market_conditions(self, pair: str) -> Dict:
        """Analyze current market conditions"""
        try:
            # Get historical data for analysis
            data = self.get_historical_data(pair)
            if data is None:
                return None
                
            # Get current price
            current_price = self.get_live_price(pair)
            if current_price is None:
                return None
                
            # Calculate indicators
            indicators = self.calculate_indicators(data)
            if indicators is None:
                return None
                
            # Determine market conditions
            conditions = {
                'pair': pair,
                'price': current_price['price'],
                'timestamp': datetime.now().isoformat(),
                'indicators': indicators,
                'trend': self._determine_trend(data, indicators),
                'volatility': self._calculate_volatility(data),
                'volume_analysis': self._analyze_volume(data),
                'support_resistance': self._find_support_resistance(data)
            }
            
            return conditions
            
        except Exception as e:
            logger.error(f"Error analyzing market conditions: {e}")
            return None
    
    def _determine_trend(self, data: pd.DataFrame, indicators: Dict) -> str:
        """Determine the current market trend"""
        try:
            # Simple trend determination using moving averages
            current_price = data['close'].iloc[-1]
            
            if (current_price > indicators['sma_20'] > indicators['sma_50']):
                return 'strong_uptrend'
            elif (current_price > indicators['sma_20'] and indicators['sma_20'] < indicators['sma_50']):
                return 'weak_uptrend'
            elif (current_price < indicators['sma_20'] < indicators['sma_50']):
                return 'strong_downtrend'
            elif (current_price < indicators['sma_20'] and indicators['sma_20'] > indicators['sma_50']):
                return 'weak_downtrend'
            else:
                return 'sideways'
                
        except Exception as e:
            logger.error(f"Error determining trend: {e}")
            return 'unknown'
    
    def _calculate_volatility(self, data: pd.DataFrame) -> str:
        """Calculate market volatility"""
        try:
            # Calculate price changes
            returns = data['close'].pct_change()
            volatility = returns.std() * np.sqrt(252)  # Annualized volatility
            
            if volatility < 0.10:
                return 'low'
            elif volatility < 0.25:
                return 'medium'
            else:
                return 'high'
                
        except Exception as e:
            logger.error(f"Error calculating volatility: {e}")
            return 'unknown'
    
    def _analyze_volume(self, data: pd.DataFrame) -> str:
        """Analyze trading volume"""
        try:
            current_volume = data['volume'].iloc[-1]
            avg_volume = data['volume'].mean()
            
            if current_volume > avg_volume * 1.5:
                return 'high'
            elif current_volume < avg_volume * 0.5:
                return 'low'
            else:
                return 'normal'
                
        except Exception as e:
            logger.error(f"Error analyzing volume: {e}")
            return 'unknown'
    
    def _find_support_resistance(self, data: pd.DataFrame) -> Dict[str, float]:
        """Find support and resistance levels"""
        try:
            # Simple support/resistance using recent highs and lows
            recent_data = data.tail(20)
            
            resistance = recent_data['high'].max()
            support = recent_data['low'].min()
            
            return {
                'support': support,
                'resistance': resistance
            }
            
        except Exception as e:
            logger.error(f"Error finding support/resistance: {e}")
            return {'support': 0, 'resistance': 0}
