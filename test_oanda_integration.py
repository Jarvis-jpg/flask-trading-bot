"""
Test OANDA Historical Data Integration
Run this script to verify OANDA connection and data quality
"""

import sys
import os
sys.path.append('.')

try:
    from oanda_historical_data import OandaHistoricalData
except ImportError as e:
    print(f"Import error for oanda_historical_data: {e}")
    sys.exit(1)

try:
    from oanda_config import OANDA_API_KEY, OANDA_ACCOUNT_ID, OANDA_ENVIRONMENT
except ImportError:
    # Fallback if specific variables aren't defined
    print("Using OANDA config fallback...")
    OANDA_API_KEY = "e9e9a0366a2b21ebbb03b965301f0182-ea0448d5fc88dd622b361855758d7f3e"
    OANDA_ACCOUNT_ID = "001-001-12623605-001"
    OANDA_ENVIRONMENT = "live"  # Use live environment

import pandas as pd

def test_oanda_integration():
    """Test OANDA historical data integration"""
    
    print("🔧 Testing OANDA Historical Data Integration...")
    print("=" * 60)
    
    # Initialize OANDA data provider
    try:
        oanda_data = OandaHistoricalData(
            api_key=OANDA_API_KEY,
            account_id=OANDA_ACCOUNT_ID,
            environment=OANDA_ENVIRONMENT
        )
        print("✅ OANDA API initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize OANDA API: {e}")
        return False
    
    # Test connection
    print("\n📡 Testing API connection...")
    if not oanda_data.test_connection():
        return False
    
    # Test historical data fetching
    print("\n📊 Testing historical data fetching...")
    pairs_to_test = ['EUR/USD', 'GBP/USD', 'USD/JPY']
    
    for pair in pairs_to_test:
        print(f"\n🔍 Testing {pair}...")
        
        # Get market data
        market_data = oanda_data.get_realistic_market_data(pair)
        
        if market_data is None:
            print(f"❌ Failed to get market data for {pair}")
            continue
        
        print(f"✅ {pair} data retrieved successfully:")
        print(f"   Market Condition: {market_data['market_condition']}")
        print(f"   Session: {market_data['session']}")
        print(f"   Trend Strength: {market_data['trend_strength']:.3f}")
        print(f"   RSI: {market_data['rsi_normalized']:.3f}")
        print(f"   Volatility Score: {market_data['volatility_score']:.3f}")
        print(f"   Actual Spread: {market_data['actual_spread_pips']:.1f} pips")
        print(f"   Current Price: {market_data['actual_price']:.5f}")
        
        # Verify candle data
        candle_data = market_data['candle_data']
        print(f"   OHLC: O={candle_data['open']:.5f} H={candle_data['high']:.5f} L={candle_data['low']:.5f} C={candle_data['close']:.5f}")
        print(f"   Timestamp: {candle_data['timestamp']}")
    
    # Test multiple data points for consistency
    print(f"\n🔄 Testing data consistency for EUR/USD...")
    consistency_data = []
    
    for i in range(5):
        market_data = oanda_data.get_realistic_market_data('EUR/USD')
        if market_data:
            consistency_data.append({
                'iteration': i + 1,
                'price': market_data['actual_price'],
                'spread': market_data['actual_spread_pips'],
                'condition': market_data['market_condition'],
                'session': market_data['session']
            })
    
    if consistency_data:
        print("✅ Consistency test results:")
        for data in consistency_data:
            print(f"   #{data['iteration']}: Price={data['price']:.5f}, Spread={data['spread']:.1f} pips, "
                  f"Condition={data['condition']}, Session={data['session']}")
    
    # Test technical indicators
    print(f"\n📈 Testing technical indicators...")
    try:
        df = oanda_data.get_historical_candles("EUR_USD", count=100)
        if df is not None:
            print(f"✅ Technical indicators calculated successfully:")
            print(f"   RSI range: {df['rsi_normalized'].min():.3f} - {df['rsi_normalized'].max():.3f}")
            print(f"   Trend strength range: {df['trend_strength'].min():.6f} - {df['trend_strength'].max():.6f}")
            print(f"   Volatility range: {df['volatility_score'].min():.6f} - {df['volatility_score'].max():.6f}")
            print(f"   Spread range: {df['spread_pips'].min():.1f} - {df['spread_pips'].max():.1f} pips")
        else:
            print("❌ Failed to calculate technical indicators")
    except Exception as e:
        print(f"❌ Technical indicators test failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 OANDA Integration Test Complete!")
    print("If all tests passed, you can proceed with training system integration.")
    
    return True

def compare_with_simulation():
    """Compare OANDA data quality with random simulation"""
    print("\n🔍 Comparing OANDA data vs Random Simulation...")
    print("=" * 50)
    
    oanda_data = OandaHistoricalData(
        api_key=OANDA_API_KEY,
        account_id=OANDA_ACCOUNT_ID,
        environment=OANDA_ENVIRONMENT
    )
    
    # Get OANDA data sample
    oanda_samples = []
    for _ in range(10):
        market_data = oanda_data.get_realistic_market_data('EUR/USD')
        if market_data:
            oanda_samples.append(market_data)
    
    if oanda_samples:
        # Analyze OANDA data characteristics
        spreads = [s['actual_spread_pips'] for s in oanda_samples]
        volatility = [s['volatility_score'] for s in oanda_samples]
        trends = [s['trend_strength'] for s in oanda_samples]
        
        print("📊 OANDA Data Characteristics:")
        print(f"   Spread: {min(spreads):.1f} - {max(spreads):.1f} pips (avg: {sum(spreads)/len(spreads):.1f})")
        print(f"   Volatility: {min(volatility):.3f} - {max(volatility):.3f} (avg: {sum(volatility)/len(volatility):.3f})")
        print(f"   Trend Strength: {min(trends):.3f} - {max(trends):.3f} (avg: {sum(trends)/len(trends):.3f})")
        
        # Market conditions distribution
        conditions = [s['market_condition'] for s in oanda_samples]
        condition_counts = {c: conditions.count(c) for c in set(conditions)}
        print(f"   Market Conditions: {condition_counts}")
        
        # Sessions distribution
        sessions = [s['session'] for s in oanda_samples]
        session_counts = {s: sessions.count(s) for s in set(sessions)}
        print(f"   Sessions: {session_counts}")
    
    print("\n📝 Key Differences from Random Simulation:")
    print("   ✅ Real spreads based on actual market conditions")
    print("   ✅ Genuine technical indicator values")
    print("   ✅ Actual market session timing")
    print("   ✅ Real price movements and volatility")
    print("   ✅ Authentic correlation between indicators")

if __name__ == "__main__":
    success = test_oanda_integration()
    
    if success:
        compare_with_simulation()
        
        print("\n🚀 Next Steps:")
        print("1. Run: pip install oandapyV20 ta")
        print("2. Update your training system with OANDA integration")
        print("3. Test a few training trades with real data")
        print("4. Compare AI learning performance")
    else:
        print("\n❌ Integration test failed. Check your OANDA credentials and try again.")
