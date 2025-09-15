#!/usr/bin/env python3
"""
Direct OANDA API Test - Diagnose connection and trading issues
"""

import os
from dotenv import load_dotenv
from oanda_client import OandaClient
import logging

# Load environment variables
load_dotenv()

# Enable verbose logging
logging.basicConfig(level=logging.DEBUG)

def test_oanda_connection():
    """Test OANDA connection and account access"""
    print("🔧 Testing OANDA Connection...")
    
    try:
        # Initialize client
        oanda = OandaClient()
        print("✅ OANDA client initialized successfully")
        
        # Test account access
        print("\n📊 Testing account access...")
        account_details = oanda.get_account_details()
        
        print(f"✅ Account Details:")
        print(f"   Balance: ${account_details['balance']:.2f}")
        print(f"   Currency: {account_details['currency']}")
        print(f"   Margin Used: ${account_details['margin_used']:.2f}")
        print(f"   Margin Available: ${account_details['margin_available']:.2f}")
        print(f"   Open Positions: {account_details['open_positions']}")
        print(f"   Open Trades: {account_details['open_trades']}")
        print(f"   Unrealized P/L: ${account_details['unrealized_pl']:.2f}")
        
        # Test price retrieval
        print("\n💰 Testing price retrieval...")
        price_data = oanda.get_current_price("EUR_USD")
        print(f"✅ EUR_USD Price:")
        print(f"   Bid: {price_data['bid']}")
        print(f"   Ask: {price_data['ask']}")
        print(f"   Time: {price_data['timestamp']}")
        
        return True
        
    except Exception as e:
        print(f"❌ OANDA connection failed: {e}")
        return False

def test_small_trade():
    """Test placing a very small trade"""
    print("\n🚀 Testing small trade placement...")
    
    try:
        oanda = OandaClient()
        
        # Get current price first
        price_data = oanda.get_current_price("EUR_USD")
        current_price = price_data['ask']  # Use ask for buy order
        
        print(f"Current EUR_USD ask price: {current_price}")
        
        # Calculate minimal TP/SL (5 pips each)
        pip_value = 0.0001  # For EUR_USD
        stop_loss = current_price - (5 * pip_value)  # 5 pips below
        take_profit = current_price + (5 * pip_value)  # 5 pips above
        
        # Minimal trade data
        trade_data = {
            'symbol': 'EUR_USD',
            'units': 1,  # Smallest possible position
            'close_price': current_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit
        }
        
        print(f"Trade Data:")
        print(f"   Symbol: {trade_data['symbol']}")
        print(f"   Units: {trade_data['units']}")
        print(f"   Entry: {current_price}")
        print(f"   Stop Loss: {stop_loss}")
        print(f"   Take Profit: {take_profit}")
        
        # Place the trade
        result = oanda.place_trade(trade_data)
        print(f"✅ Trade placed successfully:")
        print(f"   Order ID: {result.get('order_id', 'N/A')}")
        print(f"   Fill Price: {result.get('filled_price', 'N/A')}")
        print(f"   Status: {result.get('status', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Trade placement failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run comprehensive OANDA testing"""
    print("🔍 OANDA API Diagnostic Test")
    print("=" * 50)
    
    # Test connection first
    if not test_oanda_connection():
        print("\n❌ Cannot proceed without API connection")
        return
    
    # Test trade placement
    if not test_small_trade():
        print("\n❌ Trade placement test failed")
        return
    
    print("\n✅ All OANDA tests passed!")
    print("\nThe issue is likely in the webhook processing, not OANDA connection.")

if __name__ == "__main__":
    main()
