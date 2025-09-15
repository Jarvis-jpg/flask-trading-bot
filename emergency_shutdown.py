#!/usr/bin/env python3
"""
EMERGENCY SYSTEM SHUTDOWN
Immediate shutdown and status check
"""

def emergency_shutdown():
    print("🚨 EMERGENCY SYSTEM SHUTDOWN INITIATED")
    print("=" * 60)
    
    # Create emergency stop file
    with open('EMERGENCY_STOP.txt', 'w') as f:
        f.write("EMERGENCY STOP ACTIVATED\n")
        f.write("Reason: Critical Pine script errors causing inappropriate trades\n")
        f.write("Time: 2024-12-20\n")
        f.write("Status: SYSTEM DISABLED\n")
        f.write("Action Required: Apply SevenSYS_EMERGENCY_FIXED.pine\n")
    
    print("✅ Emergency stop file created: EMERGENCY_STOP.txt")
    
    # Quick OANDA check with better error handling
    try:
        import oandapyV20
        import oandapyV20.endpoints.accounts as accounts
        from datetime import datetime
        
        account_id = "001-001-12623605-001"
        access_token = "46ba4cde17b7a48ff25d9a2d6c52b7ca-a5e7c4ffea7b5be5a4e3b1a9ecec4c97"
        
        client = oandapyV20.API(access_token=access_token, environment="live")
        
        r = accounts.AccountSummary(account_id)
        response = client.request(r)
        summary = r.response['account']
        
        print(f"\n💰 ACCOUNT STATUS:")
        print(f"Balance: ${float(summary['balance']):,.2f}")
        print(f"Open Trades: {summary['openTradeCount']}")
        print(f"Margin Used: ${float(summary.get('marginUsed', 0)):,.2f}")
        print(f"Unrealized P&L: ${float(summary.get('unrealizedPL', 0)):,.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ OANDA Connection Error: {e}")
        print("⚠️  Cannot verify account status - manual check required")
        return False

if __name__ == "__main__":
    success = emergency_shutdown()
    print("\n🎯 IMMEDIATE ACTIONS REQUIRED:")
    print("1. STOP all TradingView alerts immediately")
    print("2. Replace SevenSYS.pine with SevenSYS_EMERGENCY_FIXED.pine")
    print("3. Verify no open positions")
    print("4. Check account balance manually")
    print("=" * 60)
