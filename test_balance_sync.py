#!/usr/bin/env python3
"""
Quick Balance Sync Test
Tests syncing with OANDA account balance
"""
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_oanda_balance_sync():
    """Test OANDA balance sync functionality"""
    print("🔄 Testing OANDA Balance Sync...")
    print("="*50)
    
    try:
        # Import and test sync
        from oanda_sync import oanda_sync
        
        print("✅ Modules imported successfully")
        
        # Test sync
        success = oanda_sync.sync_balance_with_oanda()
        
        if success:
            print("✅ Balance sync successful!")
        else:
            print("⚠️  Balance sync returned False")
            
        # Display current status
        print("\n📊 Current Memory Status:")
        from live_trading_memory import live_memory
        live_memory.display_status()
        
    except Exception as e:
        print(f"❌ Error testing sync: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_oanda_balance_sync()
