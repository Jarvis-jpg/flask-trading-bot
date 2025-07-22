"""
OANDA Historical Data Integration for Trading AI
Replaces random market simulation with real OANDA OHLC data
"""

import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random
import logging

# Try to import technical analysis libraries
try:
    import ta
    TA_AVAILABLE = True
except ImportError:
    TA_AVAILABLE = False
    print("⚠️ Warning: 'ta' library not installed. Run: pip install ta")

logger = logging.getLogger(__name__)

class OandaHistoricalData:
    """
    OANDA Historical Data Provider for AI Training
    Fetches real market OHLC data and technical indicators
    """
    
    def __init__(self, api_key, account_id, environment="practice"):
        """
        Initialize OANDA API connection
        
        Args:
            api_key: OANDA API key
            account_id: OANDA account ID
            environment: "practice" or "live"
        """
        self.api_key = api_key
        self.account_id = account_id
        
        if environment == "practice":
            self.api = oandapyV20.API(access_token=api_key, environment="practice")
        else:
            self.api = oandapyV20.API(access_token=api_key, environment="live")
        
        # Data cache to avoid repeated API calls
        self.data_cache = {}
        self.last_request_time = 0
        self.min_request_interval = 0.5  # 500ms between requests
        
        print(f"🔗 OANDA Historical Data initialized ({environment} environment)")
    
    def _rate_limit(self):
        """Implement rate limiting for API requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def get_historical_candles(self, instrument, count=5000, granularity="M1"):
        """
        Fetch historical OHLC data from OANDA
        
        Args:
            instrument: Currency pair in OANDA format (e.g., "EUR_USD")
            count: Number of candles (max 5000)
            granularity: M1, M5, M15, M30, H1, H4, D
            
        Returns:
            pandas.DataFrame with OHLC data and technical indicators
        """
        cache_key = f"{instrument}_{granularity}_{count}"
        
        # Return cached data if available
        if cache_key in self.data_cache:
            return self.data_cache[cache_key]
        
        try:
            # Rate limiting
            self._rate_limit()
            
            params = {
                "count": count,
                "granularity": granularity,
                "price": "MBA"  # Mid, Bid, Ask prices
            }
            
            request = instruments.InstrumentsCandles(instrument=instrument, params=params)
            response = self.api.request(request)
            
            # Convert to DataFrame
            candles = []
            for candle in response['candles']:
                if candle['complete']:
                    candle_data = {
                        'time': candle['time'],
                        'open': float(candle['mid']['o']),
                        'high': float(candle['mid']['h']),
                        'low': float(candle['mid']['l']),
                        'close': float(candle['mid']['c']),
                        'volume': int(candle['volume']),
                        'bid_open': float(candle['bid']['o']),
                        'bid_close': float(candle['bid']['c']),
                        'ask_open': float(candle['ask']['o']),
                        'ask_close': float(candle['ask']['c'])
                    }
                    candles.append(candle_data)
            
            if not candles:
                print(f"⚠️ No candle data received for {instrument}")
                return None
            
            df = pd.DataFrame(candles)
            df['time'] = pd.to_datetime(df['time'])
            df.set_index('time', inplace=True)
            
            # Calculate real spreads
            df['spread'] = df['ask_close'] - df['bid_close']
            df['spread_pips'] = df['spread'] * 10000  # Convert to pips for major pairs
            
            # Add technical indicators
            df = self.add_technical_indicators(df)
            
            # Cache the data
            self.data_cache[cache_key] = df
            
            print(f"✅ Fetched {len(df)} candles for {instrument}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching OANDA data for {instrument}: {e}")
            print(f"❌ Failed to fetch OANDA data for {instrument}: {e}")
            return None
    
    def add_technical_indicators(self, df):
        """Add technical indicators to OHLC data"""
        try:
            if not TA_AVAILABLE:
                # Fallback to simple calculations if ta library not available
                return self.add_simple_indicators(df)
            
            # RSI
            df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
            df['rsi_normalized'] = df['rsi'] / 100.0
            
            # MACD
            macd = ta.trend.MACD(df['close'])
            df['macd'] = macd.macd()
            df['macd_signal'] = macd.macd_signal()
            df['macd_diff'] = macd.macd_diff()
            
            # Moving Averages
            df['sma_20'] = ta.trend.SMAIndicator(df['close'], window=20).sma_indicator()
            df['ema_12'] = ta.trend.EMAIndicator(df['close'], window=12).ema_indicator()
            df['ema_26'] = ta.trend.EMAIndicator(df['close'], window=26).ema_indicator()
            
            # Bollinger Bands
            bb = ta.volatility.BollingerBands(df['close'])
            df['bb_upper'] = bb.bollinger_hband()
            df['bb_lower'] = bb.bollinger_lband()
            df['bb_middle'] = bb.bollinger_mavg()
            
            # ATR (Average True Range)
            df['atr'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()
            
            # Volume indicators
            if 'volume' in df.columns:
                df['volume_sma'] = df['volume'].rolling(window=20).mean()
            else:
                df['volume_sma'] = 1000  # Default volume
            
            # Price-based calculations
            df['price_change'] = df['close'].pct_change()
            df['high_low_ratio'] = (df['high'] - df['low']) / df['close']
            
            # Trend strength calculation
            df['trend_strength'] = abs(df['ema_12'] - df['ema_26']) / df['close']
            
            # Support/Resistance levels (simplified)
            df['support_level'] = df['low'].rolling(window=20).min()
            df['resistance_level'] = df['high'].rolling(window=20).max()
            df['support_resistance_clarity'] = (df['resistance_level'] - df['support_level']) / df['close']
            
            # Market structure score
            df['market_structure_score'] = (df['close'] - df['sma_20']) / df['sma_20']
            
            # Volatility score
            df['volatility_score'] = df['atr'] / df['close']
            
            # Fill NaN values
            df = df.fillna(method='bfill').fillna(method='ffill')
            
            # Normalize values that might be extreme
            df['trend_strength'] = df['trend_strength'].clip(0, 0.01)  # Cap at 1%
            df['volatility_score'] = df['volatility_score'].clip(0, 0.01)  # Cap at 1%
            df['support_resistance_clarity'] = df['support_resistance_clarity'].clip(0, 0.1)  # Cap at 10%
            df['market_structure_score'] = df['market_structure_score'].clip(-0.1, 0.1)  # Cap at ±10%
            
            return df
            
        except Exception as e:
            logger.error(f"Error adding technical indicators: {e}")
            print(f"⚠️ Error calculating technical indicators: {e}")
            return self.add_simple_indicators(df)
    
    def add_simple_indicators(self, df):
        """Add simple indicators when ta library is not available"""
        try:
            # Simple Moving Average
            df['sma_20'] = df['close'].rolling(window=20).mean()
            df['ema_12'] = df['close'].ewm(span=12).mean()
            df['ema_26'] = df['close'].ewm(span=26).mean()
            
            # Simple RSI calculation
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['rsi'] = 100 - (100 / (1 + rs))
            df['rsi_normalized'] = df['rsi'] / 100.0
            
            # Simple MACD
            df['macd'] = df['ema_12'] - df['ema_26']
            df['macd_signal'] = df['macd'].ewm(span=9).mean()
            df['macd_diff'] = df['macd'] - df['macd_signal']
            
            # Price-based calculations
            df['price_change'] = df['close'].pct_change()
            df['high_low_ratio'] = (df['high'] - df['low']) / df['close']
            
            # True Range and ATR
            df['tr1'] = df['high'] - df['low']
            df['tr2'] = (df['high'] - df['close'].shift()).abs()
            df['tr3'] = (df['low'] - df['close'].shift()).abs()
            df['true_range'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
            df['atr'] = df['true_range'].rolling(window=14).mean()
            
            # Trend strength
            df['trend_strength'] = abs(df['ema_12'] - df['ema_26']) / df['close']
            
            # Support/Resistance
            df['support_level'] = df['low'].rolling(window=20).min()
            df['resistance_level'] = df['high'].rolling(window=20).max()
            df['support_resistance_clarity'] = (df['resistance_level'] - df['support_level']) / df['close']
            
            # Market structure
            df['market_structure_score'] = (df['close'] - df['sma_20']) / df['sma_20']
            
            # Volatility
            df['volatility_score'] = df['atr'] / df['close']
            
            # Volume (if not available, use price movement as proxy)
            if 'volume' not in df.columns:
                df['volume'] = abs(df['price_change']) * 1000000  # Synthetic volume
            df['volume_sma'] = df['volume'].rolling(window=20).mean()
            
            # Fill NaN values
            df = df.fillna(method='bfill').fillna(method='ffill')
            
            # Normalize extreme values
            df['trend_strength'] = df['trend_strength'].clip(0, 0.01)
            df['volatility_score'] = df['volatility_score'].clip(0, 0.01)
            df['support_resistance_clarity'] = df['support_resistance_clarity'].clip(0, 0.1)
            df['market_structure_score'] = df['market_structure_score'].clip(-0.1, 0.1)
            
            return df
            
        except Exception as e:
            logger.error(f"Error in simple indicators calculation: {e}")
            # Return DataFrame with minimal calculations
            df['rsi_normalized'] = 0.5
            df['trend_strength'] = 0.005
            df['volatility_score'] = 0.002
            df['support_resistance_clarity'] = 0.01
            df['market_structure_score'] = 0.0
            return df
    
    def get_realistic_market_data(self, instrument, index=None):
        """
        Get realistic market data for a specific candle from OANDA
        
        Args:
            instrument: Currency pair (e.g., "EUR/USD")
            index: Specific candle index, or None for random
            
        Returns:
            dict: Market data for AI feature generation
        """
        # Convert pair format (EUR/USD -> EUR_USD)
        oanda_instrument = instrument.replace('/', '_')
        
        # Get historical data
        df = self.get_historical_candles(oanda_instrument)
        
        if df is None or len(df) == 0:
            print(f"⚠️ No OANDA data available for {instrument}")
            return None
        
        # Select candle (avoid first 50 for indicators to be stable)
        if index is None:
            index = random.randint(50, len(df) - 1)
        else:
            index = max(50, min(index, len(df) - 1))
        
        candle = df.iloc[index]
        
        # Determine market session based on timestamp
        hour = candle.name.hour
        if 0 <= hour < 8:
            session = 'tokyo'
        elif 8 <= hour < 16:
            session = 'london'
        elif 16 <= hour < 24:
            session = 'newyork'
        else:
            session = 'overlap'
        
        # Determine market condition based on real indicators
        macd_strength = abs(candle.get('macd_diff', 0))
        atr_value = candle.get('atr', 0.0001)
        trend_strength = candle.get('trend_strength', 0.001)
        
        if macd_strength > atr_value * 0.5:
            if trend_strength > 0.002:
                market_condition = 'trending'
            else:
                market_condition = 'volatile'
        else:
            if candle.get('volatility_score', 0.002) < 0.001:
                market_condition = 'quiet'
            else:
                market_condition = 'ranging'
        
        # Calculate volume surge factor
        volume_current = candle.get('volume', 1000)
        volume_avg = candle.get('volume_sma', 1000)
        volume_surge = volume_current / max(volume_avg, 1)
        
        # Prepare market data dictionary
        market_data = {
            'pair': instrument,
            'market_condition': market_condition,
            'session': session,
            'trend_strength': min(1.0, max(0.0, trend_strength * 500)),  # Scale to 0-1
            'rsi_normalized': candle.get('rsi_normalized', 0.5),
            'macd_signal_strength': min(1.0, macd_strength / (atr_value + 0.0001)),
            'volume_surge_factor': min(3.0, max(0.5, volume_surge)),
            'support_resistance_clarity': min(1.0, max(0.0, candle.get('support_resistance_clarity', 0.01) * 10)),
            'market_structure_score': min(1.0, max(0.0, abs(candle.get('market_structure_score', 0.0)) * 10)),
            'session_quality_score': self.get_session_quality(hour),
            'volatility_score': min(1.0, candle.get('volatility_score', 0.002) * 500),
            'time_quality_score': self.get_time_quality(hour),
            'actual_spread_pips': candle.get('spread_pips', 1.5),
            'actual_price': candle['close'],
            'candle_data': {
                'open': candle['open'],
                'high': candle['high'],
                'low': candle['low'],
                'close': candle['close'],
                'volume': volume_current,
                'high_low_ratio': candle.get('high_low_ratio', 0.001),
                'price_change': candle.get('price_change', 0.0),
                'atr': atr_value,
                'timestamp': candle.name
            }
        }
        
        return market_data
    
    def get_session_quality(self, hour):
        """Calculate session quality based on actual trading hour"""
        # London/NY overlap (13-16 UTC) = highest quality
        if 13 <= hour <= 16:
            return random.uniform(0.8, 1.0)
        # London session (8-17 UTC)
        elif 8 <= hour <= 17:
            return random.uniform(0.7, 0.9)
        # NY session (13-22 UTC)  
        elif 13 <= hour <= 22:
            return random.uniform(0.6, 0.8)
        # Tokyo session (0-9 UTC)
        elif 0 <= hour <= 9:
            return random.uniform(0.5, 0.7)
        else:
            return random.uniform(0.3, 0.6)
    
    def get_time_quality(self, hour):
        """Calculate time quality based on optimal trading hours"""
        # Best times: London open, NY open, overlaps
        prime_hours = [8, 9, 13, 14, 15, 16]
        if hour in prime_hours:
            return random.uniform(0.8, 1.0)
        elif 7 <= hour <= 18:
            return random.uniform(0.6, 0.8)
        else:
            return random.uniform(0.4, 0.7)
    
    def test_connection(self):
        """Test OANDA API connection"""
        try:
            # Try to fetch a small amount of EUR_USD data
            df = self.get_historical_candles("EUR_USD", count=100)
            if df is not None and len(df) > 0:
                print(f"✅ OANDA connection successful! Fetched {len(df)} candles")
                return True
            else:
                print("❌ OANDA connection failed - no data received")
                return False
        except Exception as e:
            print(f"❌ OANDA connection test failed: {e}")
            return False
