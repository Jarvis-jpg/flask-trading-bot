import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

print("=== VERIFICATION TEST ===")
print()

# Test 1: Environment Variables
print("1. Testing Environment Variables:")
api_key = os.getenv('OANDA_API_KEY')
account_id = os.getenv('OANDA_ACCOUNT_ID')
is_live = os.getenv('OANDA_LIVE')

print(f"   OANDA_API_KEY: {'✓ Set' if api_key else '✗ Missing'}")
print(f"   OANDA_ACCOUNT_ID: {'✓ Set' if account_id else '✗ Missing'}")
print(f"   OANDA_LIVE: {is_live}")
print()

# Test 2: OANDA Client
print("2. Testing OANDA Client:")
try:
    from oanda_client import OandaClient
    oanda = OandaClient()
    print(f"   ✓ OandaClient initialized successfully")
    print(f"   Environment: {oanda.environment}")
    print(f"   API URL: {oanda.api_url}")
    print(f"   Account ID: {oanda.account_id}")
except Exception as e:
    print(f"   ✗ OandaClient failed: {e}")
print()

# Test 3: Flask App
print("3. Testing Flask App:")
try:
    from app import app, calculate_position_size
    print("   ✓ Flask app imported successfully")
    
    # Test position size calculation
    pos_size = calculate_position_size(1.0900, 1.0850, 25000, 4.0)
    print(f"   ✓ Position size calculation: {pos_size} units")
    
    # Test routes
    routes = [rule.rule for rule in app.url_map.iter_rules()]
    print(f"   ✓ Available routes: {routes}")
except Exception as e:
    print(f"   ✗ Flask app failed: {e}")
print()

print("=== VERIFICATION COMPLETE ===")
