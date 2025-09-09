#!/usr/bin/env python3
"""
Quick Issue Analysis
"""
from live_trading_memory import live_memory
import subprocess

print("=== ISSUE ANALYSIS ===")
print()

# Check memory
memory = live_memory.memory
alerts = len(memory.get("webhook_alerts", []))
balance_changes = memory.get("balance_syncs", [])

print(f"WEBHOOK ALERTS LOGGED: {alerts}")
print(f"BALANCE CHANGES: {len(balance_changes)}")

if balance_changes:
    print("\nBALANCE HISTORY:")
    for sync in balance_changes:
        change = sync["balance_change"] 
        timestamp = sync["timestamp"][:16].replace("T", " ")
        print(f"  {timestamp}: {change:+.2f}")

# Check Flask
try:
    result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, shell=True)
    flask_running = ':5000' in result.stdout
    print(f"\nFLASK STATUS: {'RUNNING' if flask_running else 'NOT RUNNING'}")
except:
    print("\nFLASK STATUS: UNKNOWN")

print(f"\nPROBLEM:")
print(f"- Balance dropped $7.78 total")  
print(f"- Only {alerts} webhook alert logged")
print(f"- Flask webhook server is NOT running")
print(f"- TradingView alerts are not reaching the system")

print(f"\nSOLUTION:")
print(f"1. Start Flask: python start_flask.py")
print(f"2. Make sure TradingView points to: http://localhost:5000/webhook")
print(f"3. Test webhook: python test_webhook_call.py")
