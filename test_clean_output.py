#!/usr/bin/env python3
"""
Test script for clean OANDA output
"""
from oanda_historical_data import OandaHistoricalData
from oanda_config import OANDA_API_KEY, OANDA_ACCOUNT_ID, OANDA_ENVIRONMENT

print("🧪 Testing Clean OANDA Output")
print("=" * 40)

try:
    print("🔗 Initializing OANDA connection...")
    oanda = OandaHistoricalData(OANDA_API_KEY, OANDA_ACCOUNT_ID, OANDA_ENVIRONMENT)
    
    print("📊 Fetching EUR/USD data...")
    data = oanda.get_historical_candles('EUR_USD', count=100)
    
    if data is not None:
        print(f"✅ Success! Retrieved {len(data)} candles")
        print(f"📈 Data columns: {list(data.columns)}")
        print(f"🔍 Spread range: {data['spread_pips'].min():.1f} - {data['spread_pips'].max():.1f} pips")
    else:
        print("❌ Failed to retrieve data")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n✅ Test complete!")
