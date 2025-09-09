#!/usr/bin/env python3
"""
OANDA Balance Sync System
Syncs live trading memory with actual OANDA account balance and positions
"""
import json
import os
from datetime import datetime
try:
    from live_trading_memory import live_memory
except ImportError:
    live_memory = None
try:
    from oanda_client import OandaClient
except ImportError:
    OandaClient = None
from dotenv import load_dotenv

class OandaBalanceSync:
    """Syncs memory system with real OANDA account data"""
    
    def __init__(self):
        load_dotenv()
        if not OandaClient:
            print("⚠️  OandaClient not available")
            self.oanda_client = None
            return
        if not live_memory:
            print("⚠️  live_memory not available")
            self.oanda_client = None
            return
        try:
            self.oanda_client = OandaClient()
            print(f"✅ OANDA client initialized - {'LIVE' if os.getenv('OANDA_LIVE', 'false').lower() == 'true' else 'PRACTICE'} mode")
        except Exception as e:
            print(f"❌ OANDA client error: {e}")
            self.oanda_client = None
    
    def get_real_account_data(self):
        """Get actual account data from OANDA"""
        if not self.oanda_client:
            return None
            
        try:
            # Try different method names that might exist in your client
            methods_to_try = [
                'get_account_details',
                'get_account_info', 
                'get_account_summary',
                'account_details'
            ]
            
            account_data = None
            for method_name in methods_to_try:
                if hasattr(self.oanda_client, method_name):
                    method = getattr(self.oanda_client, method_name)
                    try:
                        account_data = method()
                        print(f"✅ Successfully got account data using {method_name}")
                        break
                    except Exception as e:
                        print(f"⚠️  Method {method_name} failed: {e}")
                        continue
            
            if not account_data:
                # Try direct API approach
                import oandapyV20.endpoints.accounts as accounts
                r = accounts.AccountDetails(accountID=self.oanda_client.account_id)
                response = self.oanda_client.client.request(r)
                account_data = response.get('account', {})
                print(f"✅ Got account data via direct API call")
            
            return account_data
            
        except Exception as e:
            print(f"❌ Error getting account data: {e}")
            return None
    
    def sync_balance_with_oanda(self):
        """Sync memory system balance with real OANDA balance"""
        print("🔄 SYNCING WITH OANDA ACCOUNT...")
        print("="*50)
        
        # Get real account data
        account_data = self.get_real_account_data()
        
        if not account_data:
            print("❌ Could not retrieve OANDA account data")
            return False
        
        # Extract balance information
        try:
            real_balance = float(account_data.get('balance', 50.0))
            currency = account_data.get('currency', 'USD')
            margin_used = float(account_data.get('marginUsed', 0))
            margin_available = float(account_data.get('marginAvailable', real_balance))
            unrealized_pl = float(account_data.get('unrealizedPL', 0))
            open_positions = len(account_data.get('positions', []))
            open_trades = len(account_data.get('trades', []))
            
            print(f"📊 REAL OANDA ACCOUNT DATA:")
            print(f"   💰 Balance: {currency} {real_balance:.2f}")
            print(f"   📈 Unrealized P/L: {currency} {unrealized_pl:.2f}")
            print(f"   🔒 Margin Used: {currency} {margin_used:.2f}")
            print(f"   💵 Margin Available: {currency} {margin_available:.2f}")
            print(f"   📊 Open Positions: {open_positions}")
            print(f"   🎯 Open Trades: {open_trades}")
            
            # Update memory system with real data
            current_memory = live_memory.memory
            old_balance = current_memory["live_statistics"]["current_balance"]
            
            # Calculate the difference (profit/loss since last sync)
            balance_change = real_balance - old_balance
            
            # Update memory with real OANDA data
            current_memory["live_statistics"]["current_balance"] = real_balance
            current_memory["live_statistics"]["account_currency"] = currency
            current_memory["live_statistics"]["margin_used"] = margin_used
            current_memory["live_statistics"]["margin_available"] = margin_available
            current_memory["live_statistics"]["unrealized_pl"] = unrealized_pl
            current_memory["live_statistics"]["open_positions"] = open_positions
            current_memory["live_statistics"]["open_trades"] = open_trades
            
            # If there's a balance change, log it
            if abs(balance_change) > 0.01:  # More than 1 cent change
                current_memory["live_statistics"]["total_profit_loss"] += balance_change
                
                sync_record = {
                    "timestamp": datetime.now().isoformat(),
                    "sync_type": "oanda_balance_sync",
                    "old_balance": old_balance,
                    "new_balance": real_balance,
                    "balance_change": balance_change,
                    "unrealized_pl": unrealized_pl,
                    "sync_reason": "manual_sync"
                }
                
                # Add to system decisions log
                if "balance_syncs" not in current_memory:
                    current_memory["balance_syncs"] = []
                current_memory["balance_syncs"].append(sync_record)
                
                print(f"📈 BALANCE CHANGE DETECTED:")
                print(f"   Old: {currency} {old_balance:.2f}")
                print(f"   New: {currency} {real_balance:.2f}")
                print(f"   Change: {currency} {balance_change:+.2f}")
            
            # Save updated memory
            live_memory.save_memory()
            
            print(f"✅ Memory system synced with OANDA!")
            return True
            
        except Exception as e:
            print(f"❌ Error processing account data: {e}")
            print(f"Raw account data: {account_data}")
            return False
    
    def get_open_positions(self):
        """Get current open positions from OANDA"""
        account_data = self.get_real_account_data()
        if not account_data:
            return []
        
        positions = account_data.get('positions', [])
        open_positions = []
        
        for pos in positions:
            if float(pos.get('long', {}).get('units', 0)) != 0 or float(pos.get('short', {}).get('units', 0)) != 0:
                position_info = {
                    'instrument': pos.get('instrument', 'Unknown'),
                    'long_units': float(pos.get('long', {}).get('units', 0)),
                    'short_units': float(pos.get('short', {}).get('units', 0)),
                    'long_pl': float(pos.get('long', {}).get('unrealizedPL', 0)),
                    'short_pl': float(pos.get('short', {}).get('unrealizedPL', 0))
                }
                open_positions.append(position_info)
        
        return open_positions
    
    def display_sync_status(self):
        """Display current sync status"""
        print("\n" + "="*60)
        print("🔄 OANDA SYNC STATUS")
        print("="*60)
        
        if self.sync_balance_with_oanda():
            # Show updated memory status
            live_memory.display_status()
            
            # Show open positions
            positions = self.get_open_positions()
            if positions:
                print(f"\n📊 OPEN POSITIONS:")
                for pos in positions:
                    long_units = pos['long_units']
                    short_units = pos['short_units']
                    long_pl = pos['long_pl']
                    short_pl = pos['short_pl']
                    
                    if long_units != 0:
                        print(f"   🟢 {pos['instrument']}: LONG {long_units:,.0f} units (P/L: ${long_pl:+.2f})")
                    if short_units != 0:
                        print(f"   🔴 {pos['instrument']}: SHORT {abs(short_units):,.0f} units (P/L: ${short_pl:+.2f})")
            else:
                print(f"\n📊 OPEN POSITIONS: None")
        
        else:
            print("❌ Sync failed - using cached memory data")
            live_memory.display_status()

# Create global sync instance
oanda_sync = OandaBalanceSync()

if __name__ == "__main__":
    # Run sync and display status
    oanda_sync.display_sync_status()
    
    print(f"\n💡 TO KEEP SYNCED:")
    print(f"   • Run this script regularly: python oanda_sync.py")
    print(f"   • Balance will auto-sync on each webhook call")
    print(f"   • Check sync status anytime: python live_trading_memory.py")
