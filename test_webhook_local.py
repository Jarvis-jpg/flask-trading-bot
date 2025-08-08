#!/usr/bin/env python3
"""
Quick test of our webhook fix locally
"""

import requests
import json

# Test data with 'symbol' field (like TradingView sends)
test_data_symbol = {
    "symbol": "EURUSD",
    "action": "BUY",
    "price": 1.0850,
    "timestamp": "2024-01-01T12:00:00Z"
}

# Test data with 'pair' field (like our old format)
test_data_pair = {
    "pair": "GBPUSD", 
    "action": "SELL",
    "price": 1.2650,
    "timestamp": "2024-01-01T12:05:00Z"
}

# Test data with neither field (should fallback to EURUSD)
test_data_neither = {
    "action": "BUY",
    "price": 1.0860,
    "timestamp": "2024-01-01T12:10:00Z"
}

print("🔧 Testing webhook fix locally...")

# Start Flask app locally first
print("Please start the Flask app locally first (python app.py)")
print("Then press Enter to test...")
input()

url = "http://localhost:5000/webhook"

print("\n📊 Test 1: 'symbol' field (TradingView format)")
try:
    response = requests.post(url, json=test_data_symbol, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("\n📊 Test 2: 'pair' field (old format)")
try:
    response = requests.post(url, json=test_data_pair, timeout=10)  
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("\n📊 Test 3: Neither field (fallback test)")
try:
    response = requests.post(url, json=test_data_neither, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("\n✅ Webhook fix testing complete!")
