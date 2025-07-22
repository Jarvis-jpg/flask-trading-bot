# OANDA Historical Data Integration Guide

## 🎯 OBJECTIVE
Replace random market simulation with actual OANDA historical OHLC data to train AI on real market patterns.

## 📋 PREREQUISITES

### 1. OANDA Account Setup
- [ ] Create OANDA practice account (free)
- [ ] Generate API key from OANDA developer portal
- [ ] Note your Account ID
- [ ] Save API credentials securely

### 2. Required Python Packages
```bash
pip install oandapyV20
pip install pandas
pip install numpy
pip install ta-lib  # For technical indicators
```

## 🔧 STEP-BY-STEP IMPLEMENTATION

### STEP 1: Create OANDA Configuration File

Create `oanda_historical_data.py`:

```python
import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import ta  # Technical analysis library
import time
import random

class OandaHistoricalData:
    def __init__(self, api_key, account_id, environment="practice"):
        """
        Initialize OANDA API connection
        environment: "practice" or "live"
        """
        self.api_key = api_key
        self.account_id = account_id
        
        if environment == "practice":
            self.api = oandapyV20.API(access_token=api_key, environment="practice")
        else:
            self.api = oandapyV20.API(access_token=api_key, environment="live")
        
        # Cache for historical data
        self.data_cache = {}
        
    def get_historical_candles(self, instrument, count=5000, granularity="M1"):
        """
        Fetch historical OHLC data from OANDA
        
        Args:
            instrument: Currency pair (e.g., "EUR_USD")
            count: Number of candles (max 5000)
            granularity: M1, M5, M15, M30, H1, H4, D
        """
        cache_key = f"{instrument}_{granularity}_{count}"
        
        if cache_key in self.data_cache:
            return self.data_cache[cache_key]
        
        try:
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
                    candles.append({
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
                    })
            
            df = pd.DataFrame(candles)
            df['time'] = pd.to_datetime(df['time'])
            df.set_index('time', inplace=True)
            
            # Calculate real spreads
            df['spread'] = df['ask_close'] - df['bid_close']
            df['spread_pips'] = df['spread'] * 10000  # Convert to pips
            
            # Add technical indicators
            df = self.add_technical_indicators(df)
            
            # Cache the data
            self.data_cache[cache_key] = df
            
            return df
            
        except Exception as e:
            print(f"Error fetching OANDA data: {e}")
            return None
    
    def add_technical_indicators(self, df):
        """Add technical indicators to OHLC data"""
        try:
            # RSI
            df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
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
            df['volume_sma'] = ta.volume.VolumeSMAIndicator(df['close'], df['volume']).volume_sma()
            
            # Price change and returns
            df['price_change'] = df['close'].pct_change()
            df['high_low_ratio'] = (df['high'] - df['low']) / df['close']
            
            # Trend strength calculation
            df['trend_strength'] = abs(df['ema_12'] - df['ema_26']) / df['close']
            df['trend_strength'] = df['trend_strength'].fillna(0.5)
            
            # Support/Resistance levels (simplified)
            df['support_level'] = df['low'].rolling(window=20).min()
            df['resistance_level'] = df['high'].rolling(window=20).max()
            df['support_resistance_clarity'] = (df['resistance_level'] - df['support_level']) / df['close']
            
            # Market structure score
            df['market_structure_score'] = (df['close'] - df['sma_20']) / df['sma_20']
            df['market_structure_score'] = df['market_structure_score'].fillna(0.5)
            
            # Volatility score
            df['volatility_score'] = df['atr'] / df['close']
            df['volatility_score'] = df['volatility_score'].fillna(0.5)
            
            # Normalize indicators
            df = df.fillna(method='bfill').fillna(method='ffill')
            
            return df
            
        except Exception as e:
            print(f"Error adding technical indicators: {e}")
            return df
    
    def get_realistic_market_data(self, instrument, index=None):
        """
        Get realistic market data for a specific candle
        """
        # Convert pair format (EUR/USD -> EUR_USD)
        oanda_instrument = instrument.replace('/', '_')
        
        # Get historical data
        df = self.get_historical_candles(oanda_instrument)
        
        if df is None or len(df) == 0:
            return None
        
        # Select random candle or specific index
        if index is None:
            index = random.randint(50, len(df) - 1)  # Avoid first 50 for indicators
        
        candle = df.iloc[index]
        
        # Determine market session based on time
        hour = candle.name.hour
        if 0 <= hour < 8:
            session = 'tokyo'
        elif 8 <= hour < 16:
            session = 'london'
        elif 16 <= hour < 24:
            session = 'newyork'
        else:
            session = 'overlap'
        
        # Determine market condition
        if abs(candle['macd_diff']) > candle['atr'] * 0.5:
            if candle['trend_strength'] > 0.002:
                market_condition = 'trending'
            else:
                market_condition = 'volatile'
        else:
            if candle['volatility_score'] < 0.001:
                market_condition = 'quiet'
            else:
                market_condition = 'ranging'
        
        # Calculate volume surge factor
        volume_surge = candle['volume'] / candle['volume_sma'] if candle['volume_sma'] > 0 else 1.0
        
        return {
            'pair': instrument,
            'market_condition': market_condition,
            'session': session,
            'trend_strength': min(1.0, max(0.0, candle['trend_strength'] * 100)),
            'rsi_normalized': candle['rsi_normalized'],
            'macd_signal_strength': min(1.0, abs(candle['macd_diff']) / (candle['atr'] + 0.0001)),
            'volume_surge_factor': min(3.0, max(0.5, volume_surge)),
            'support_resistance_clarity': min(1.0, max(0.0, candle['support_resistance_clarity'])),
            'market_structure_score': min(1.0, max(0.0, abs(candle['market_structure_score']))),
            'session_quality_score': self.get_session_quality(hour),
            'volatility_score': min(1.0, candle['volatility_score'] * 1000),
            'time_quality_score': self.get_time_quality(hour),
            'actual_spread_pips': candle['spread_pips'],
            'actual_price': candle['close'],
            'candle_data': candle.to_dict()
        }
    
    def get_session_quality(self, hour):
        """Calculate session quality based on hour"""
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
        """Calculate time quality based on hour"""
        # Best times: London open, NY open, overlaps
        prime_hours = [8, 9, 13, 14, 15, 16]
        if hour in prime_hours:
            return random.uniform(0.8, 1.0)
        elif 7 <= hour <= 18:
            return random.uniform(0.6, 0.8)
        else:
            return random.uniform(0.4, 0.7)
```

### STEP 2: Create OANDA Credentials Configuration

Create `oanda_config.py`:

```python
# OANDA API Configuration
# REPLACE WITH YOUR ACTUAL CREDENTIALS

OANDA_CONFIG = {
    "api_key": "YOUR_OANDA_API_KEY_HERE",
    "account_id": "YOUR_ACCOUNT_ID_HERE",
    "environment": "practice",  # or "live" for real account
    "max_requests_per_second": 2  # Rate limiting
}

# Currency pairs mapping
CURRENCY_PAIRS = {
    'EUR/USD': 'EUR_USD',
    'GBP/USD': 'GBP_USD', 
    'USD/JPY': 'USD_JPY',
    'USD/CHF': 'USD_CHF',
    'AUD/USD': 'AUD_USD',
    'USD/CAD': 'USD_CAD',
    'NZD/USD': 'NZD_USD',
    'EUR/GBP': 'EUR_GBP'
}
```

### STEP 3: Modify Your Training System

Update `train_and_trade_100_sessions.py`:

1. **Add imports at the top:**
```python
from oanda_historical_data import OandaHistoricalData
from oanda_config import OANDA_CONFIG
```

2. **Initialize OANDA in `__init__` method:**
```python
# Initialize OANDA historical data (add after other initializations)
self.oanda_data = OandaHistoricalData(
    api_key=OANDA_CONFIG["api_key"],
    account_id=OANDA_CONFIG["account_id"],
    environment=OANDA_CONFIG["environment"]
)
```

3. **Replace `generate_realistic_trade` method:**
```python
def generate_realistic_trade(self):
    """Generate trade using REAL OANDA historical data"""
    pairs = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'USD/CHF', 'AUD/USD', 'USD/CAD', 'NZD/USD', 'EUR/GBP']
    pair = random.choice(pairs)
    
    # Get REAL market data from OANDA
    market_data = self.oanda_data.get_realistic_market_data(pair)
    
    if market_data is None:
        print(f"⚠️ Failed to get OANDA data for {pair}, skipping...")
        return None
    
    # Enhanced Market Hours Check using REAL time data
    session = market_data['session']
    if self.enhanced_config['market_hours_filter']:
        # Use actual market hours from OANDA timestamp
        if session == 'tokyo' and random.random() < 0.15:  # 15% rejection for tokyo
            return None
        elif session in ['london', 'newyork', 'overlap'] and random.random() < 0.05:  # 5% rejection for prime times
            return None
    
    # Rest of the method stays the same, but use market_data from OANDA
    # ... (keep existing filtering logic)
    
    # Use REAL spreads from OANDA
    real_spread_pips = market_data['actual_spread_pips']
    spread_cost = base_risk_amount * (real_spread_pips / 10000)  # Convert pips to decimal
    
    # ... rest of method
```

### STEP 4: Update Feature Generation

Modify `generate_ai_features` to use real market data:

```python
def generate_ai_features(self, market_data, trade_signal):
    """Generate enhanced features using REAL OANDA market data"""
    
    # Get REAL candle data
    candle_data = market_data.get('candle_data', {})
    
    # Enhanced feature set with REAL data
    features = [
        # REAL technical features from OANDA
        market_data.get('trend_strength', 0.5),
        market_data.get('rsi_normalized', 0.5),
        market_data.get('macd_signal_strength', 0.5),
        market_data.get('volume_surge_factor', 1.0),
        market_data.get('support_resistance_clarity', 0.5),
        market_data.get('market_structure_score', 0.5),
        market_data.get('session_quality_score', 0.5),
        market_data.get('volatility_score', 0.5),
        trade_signal.get('risk_reward_ratio', 2.0) / 5.0,
        trade_signal.get('base_confidence', 0.5),
        
        # REAL market condition features
        1.0 if market_data.get('market_condition') == 'trending' else 0.0,
        1.0 if market_data.get('session') == 'overlap' else 0.0,
        market_data.get('time_quality_score', 0.5),
        
        # Pair-specific learning (existing)
        self.get_pair_learning_factor(trade_signal.get('pair', 'EUR/USD')),
        
        # Additional REAL features from OANDA candle
        candle_data.get('high_low_ratio', 0.01) * 100,  # Candle range
        min(1.0, candle_data.get('price_change', 0.0) * 1000),  # Price momentum
        min(1.0, candle_data.get('atr', 0.001) * 10000),  # Volatility
        
        # ... rest of features
    ]
    
    return np.array(features).reshape(1, -1)
```

## 🚀 IMPLEMENTATION STEPS

### Phase 1: Setup (Day 1)
1. [ ] Create OANDA practice account
2. [ ] Get API credentials
3. [ ] Install required packages
4. [ ] Create configuration files
5. [ ] Test API connection

### Phase 2: Integration (Days 2-3)
1. [ ] Create `oanda_historical_data.py`
2. [ ] Create `oanda_config.py` with your credentials
3. [ ] Test historical data fetching
4. [ ] Verify technical indicators

### Phase 3: Training System Update (Days 4-5)
1. [ ] Modify `train_and_trade_100_sessions.py`
2. [ ] Replace random simulation with OANDA data
3. [ ] Update feature generation
4. [ ] Test with small sample

### Phase 4: Testing (Days 6-7)
1. [ ] Run training session with real data
2. [ ] Compare AI learning with real vs simulated
3. [ ] Verify performance metrics
4. [ ] Fine-tune parameters

## ⚠️ IMPORTANT CONSIDERATIONS

### Rate Limiting
- OANDA allows ~1000 requests per hour
- Cache historical data to avoid repeated API calls
- Use rate limiting in your requests

### Data Quality
- Ensure sufficient historical data (5000+ candles)
- Handle missing data gracefully
- Validate technical indicators

### Performance Impact
- Real data fetching will be slower than simulation
- Consider pre-loading and caching data
- Monitor API usage limits

### Cost Considerations
- Practice accounts are free
- Live accounts may have costs
- Monitor API usage

## 🎯 EXPECTED OUTCOMES

### Positive Changes
- AI learns from real market patterns
- More realistic spread and execution costs
- Better preparation for live trading
- Improved model accuracy on real data

### Challenges
- Slower execution due to API calls
- More complex error handling
- Rate limiting considerations
- Need for proper caching

## 📊 VERIFICATION STEPS

1. **Data Quality Check:**
   - Verify OHLC data looks realistic
   - Check technical indicators are calculating correctly
   - Ensure spreads match real market conditions

2. **Performance Comparison:**
   - Compare AI accuracy: simulated vs real data
   - Monitor win rate changes
   - Track learning curve differences

3. **System Stability:**
   - Test error handling
   - Verify caching works properly
   - Monitor API rate limits

This integration will significantly improve your system's realism and prepare it for eventual live trading!
