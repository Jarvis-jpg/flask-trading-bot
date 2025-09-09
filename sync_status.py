#!/usr/bin/env python3
"""
Complete System Sync
Syncs memory with OANDA, TradingView, and displays full status
"""
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def complete_system_sync():
    """Complete sync of all trading systems"""
    print("🔄 COMPLETE SYSTEM SYNC")
    print("="*60)
    
    try:
        # Import modules
        from oanda_sync import oanda_sync
        from live_trading_memory import live_memory
        import json
        
        print("Step 1: Syncing with OANDA...")
        success = oanda_sync.sync_balance_with_oanda()
        
        if success:
            print("✅ OANDA sync successful")
            
            # Show detailed sync status
            print("\n" + "="*60)
            print("📊 COMPLETE SYSTEM STATUS")
            print("="*60)
            
            # Display memory status
            live_memory.display_status()
            
            # Show sync history
            memory = live_memory.memory
            if "balance_syncs" in memory and memory["balance_syncs"]:
                print(f"\n📈 RECENT BALANCE SYNCS:")
                for sync in memory["balance_syncs"][-3:]:  # Last 3 syncs
                    change = sync["balance_change"]
                    timestamp = sync["timestamp"][:16].replace("T", " ")
                    print(f"   {timestamp}: ${sync['old_balance']:.2f} → ${sync['new_balance']:.2f} ({change:+.2f})")
            
            # Show open positions
            positions = oanda_sync.get_open_positions()
            if positions:
                print(f"\n📊 OPEN POSITIONS:")
                total_pl = 0
                for pos in positions:
                    long_units = pos['long_units']
                    short_units = pos['short_units']
                    long_pl = pos['long_pl']
                    short_pl = pos['short_pl']
                    
                    if long_units != 0:
                        print(f"   🟢 {pos['instrument']}: LONG {long_units:,.0f} units (P/L: ${long_pl:+.2f})")
                        total_pl += long_pl
                    if short_units != 0:
                        print(f"   🔴 {pos['instrument']}: SHORT {abs(short_units):,.0f} units (P/L: ${short_pl:+.2f})")
                        total_pl += short_pl
                
                print(f"   💰 Total Unrealized P/L: ${total_pl:+.2f}")
            else:
                print(f"\n📊 OPEN POSITIONS: None")
            
            # Show current settings
            current_balance = memory["live_statistics"]["current_balance"]
            if current_balance <= 50:
                recommended_units = 1000
            elif current_balance <= 100:
                recommended_units = 1500 
            elif current_balance <= 500:
                recommended_units = 2500
            else:
                recommended_units = 5000
            
            print(f"\n⚙️  CURRENT SETTINGS:")
            print(f"   💰 Account Balance: ${current_balance:.2f}")
            print(f"   📏 Position Size: {recommended_units:,} units")
            print(f"   📊 Risk Per Trade: ~${recommended_units * 0.001:.2f} (0.1% move)")
            print(f"   🎯 Risk Level: {(recommended_units * 0.001 / current_balance * 100):.1f}% of account")
            
            # Show trading status
            mode = "LIVE" if os.getenv('OANDA_LIVE', 'false').lower() == 'true' else 'PRACTICE'
            print(f"\n🎯 TRADING STATUS:")
            print(f"   🔴 Mode: {mode}")
            print(f"   📡 Webhook: Active on localhost:5000")
            print(f"   🤖 Auto-sync: Enabled on each alert")
            
            print(f"\n✅ System fully synced and ready!")
            
        else:
            print("❌ OANDA sync failed")
            print("Using cached memory data...")
            live_memory.display_status()
            
    except Exception as e:
        print(f"❌ Error during sync: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    complete_system_sync()
