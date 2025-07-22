"""
Simple OANDA Test - Quick Connection Check
"""

# Test OANDA API connection
try:
    import oandapyV20
    import oandapyV20.endpoints.instruments as instruments
    
    # Your credentials
    api_key = "e9e9a0366a2b21ebbb03b965301f0182-ea0448d5fc88dd622b361855758d7f3e"
    account_id = "001-001-12623605-001"
    
    # Initialize API
    api = oandapyV20.API(access_token=api_key, environment="practice")
    
    # Test connection with a simple request
    params = {
        "count": 10,
        "granularity": "M1",
        "price": "M"
    }
    
    request = instruments.InstrumentsCandles(instrument="EUR_USD", params=params)
    response = api.request(request)
    
    print("✅ OANDA Connection Successful!")
    print(f"✅ Received {len(response['candles'])} EUR/USD candles")
    
    # Show sample data
    if response['candles']:
        latest_candle = response['candles'][-1]
        print(f"✅ Latest EUR/USD Price: {latest_candle['mid']['c']}")
        print(f"✅ Candle Time: {latest_candle['time']}")
        print(f"✅ Volume: {latest_candle['volume']}")
    
    print("\n🎉 Your OANDA credentials are working!")
    print("📊 Ready to integrate real historical data")
    
except ImportError as e:
    print(f"❌ Missing packages: {e}")
    print("Run: pip install oandapyV20")
    
except Exception as e:
    print(f"❌ OANDA connection failed: {e}")
    print("Check your API credentials and internet connection")
