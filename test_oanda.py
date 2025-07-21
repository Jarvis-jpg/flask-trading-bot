#!/usr/bin/env python3
"""Test OANDA connection"""
try:
    from dotenv import load_dotenv
    load_dotenv()
    
    from oanda_client import OandaClient
    
    print("🌐 Testing OANDA Connection...")
    client = OandaClient()
    
    # Test price fetch
    price_data = client.get_current_price('EUR_USD')
    print(f"✓ Price data received: {price_data}")
    
    print("✅ OANDA connection test passed!")
    
except Exception as e:
    print(f"❌ OANDA connection test failed: {e}")
    import traceback
    traceback.print_exc()
