#!/usr/bin/env python3
"""
Webhook Diagnostic Tool
Checks Flask status and sets up comprehensive logging
"""
import subprocess
import sys
import os
import time
from datetime import datetime

def check_flask_status():
    """Check if Flask is running"""
    print("🔍 FLASK WEBHOOK DIAGNOSTIC")
    print("="*50)
    
    # Check if port 5000 is in use
    try:
        result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, shell=True)
        if ':5000' in result.stdout:
            print("✅ Port 5000 is in use - Flask likely running")
            return True
        else:
            print("❌ Port 5000 NOT in use - Flask NOT running")
            return False
    except Exception as e:
        print(f"⚠️  Could not check port status: {e}")
        return False

def start_flask_with_logging():
    """Start Flask with enhanced logging"""
    print("\n🚀 STARTING FLASK WITH ENHANCED LOGGING...")
    print("="*50)
    
    # Create a startup script that includes logging
    startup_script = """
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔄 Starting Flask Webhook Server...")
print("📡 Webhook URL: http://localhost:5000/webhook")
print("📊 Dashboard URL: http://localhost:5000")
print("💾 Memory logging: ENABLED")
print("🔄 Auto-sync: ENABLED")
print("-" * 50)

# Import and start the Flask app
from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
"""
    
    with open('start_flask.py', 'w') as f:
        f.write(startup_script)
    
    print("✅ Created enhanced Flask starter")
    print("\n💡 TO START FLASK:")
    print("   python start_flask.py")
    print("\n📡 WEBHOOK URL for TradingView:")
    print("   http://localhost:5000/webhook")

def create_test_webhook():
    """Create a test webhook to verify system"""
    print("\n🧪 CREATING TEST WEBHOOK...")
    
    test_script = """
#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def test_webhook():
    url = "http://localhost:5000/webhook"
    
    # Test data simulating TradingView alert
    test_data = {
        "pair": "EURUSD",
        "action": "buy", 
        "entry": 1.0856,
        "stop_loss": 1.0806,
        "take_profit": 1.0956,
        "confidence": 0.85,
        "strategy": "JARVIS_TEST",
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"🧪 Testing webhook: {url}")
    print(f"📤 Sending: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(url, json=test_data, timeout=10)
        print(f"✅ Response Status: {response.status_code}")
        print(f"📥 Response: {response.json()}")
        
        # Check if memory was updated
        print("\\n📊 Checking memory update...")
        from live_trading_memory import live_memory
        live_memory.display_status()
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Flask is not running!")
        print("💡 Start Flask first: python start_flask.py")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_webhook()
"""
    
    with open('test_webhook.py', 'w') as f:
        f.write(test_script)
    
    print("✅ Created webhook test script")
    print("💡 TO TEST: python test_webhook.py (after starting Flask)")

def diagnose_trading_activity():
    """Analyze why trades are happening without webhook alerts"""
    print("\n🕵️ DIAGNOSING MISSING TRADE ACTIVITY...")
    print("="*50)
    
    # Check memory file
    try:
        from live_trading_memory import live_memory
        memory = live_memory.memory
        
        alerts = len(memory.get("webhook_alerts", []))
        attempts = len(memory.get("trade_attempts", []))
        executed = len(memory.get("executed_trades", []))
        cancelled = len(memory.get("cancelled_trades", []))
        
        balance_changes = memory.get("balance_syncs", [])
        
        print(f"📊 MEMORY ANALYSIS:")
        print(f"   🔔 Webhook Alerts: {alerts}")
        print(f"   🎯 Trade Attempts: {attempts}")
        print(f"   ✅ Executed: {executed}")
        print(f"   ❌ Cancelled: {cancelled}")
        print(f"   💰 Balance Changes: {len(balance_changes)}")
        
        if balance_changes:
            print(f"\\n💰 BALANCE HISTORY:")
            for sync in balance_changes:
                change = sync["balance_change"]
                timestamp = sync["timestamp"][:16].replace("T", " ")
                print(f"   {timestamp}: {change:+.2f}")
        
        # Calculate discrepancy
        total_balance_change = sum(sync["balance_change"] for sync in balance_changes)
        print(f"\\n🔍 DISCREPANCY ANALYSIS:")
        print(f"   📊 Total Balance Change: ${total_balance_change:.2f}")
        print(f"   📈 Webhook Alerts Logged: {alerts}")
        print(f"   ⚠️  Missing Alerts: {abs(total_balance_change) // 1} estimated")
        
        if alerts < 2 and abs(total_balance_change) > 2:
            print(f"\\n❌ PROBLEM DETECTED:")
            print(f"   • Balance dropped ${abs(total_balance_change):.2f} but only {alerts} alerts logged")
            print(f"   • Flask webhook is likely NOT receiving TradingView alerts")
            print(f"   • OR trades are happening directly on OANDA platform")
            
    except Exception as e:
        print(f"❌ Could not analyze memory: {e}")

def main():
    """Main diagnostic function"""
    flask_running = check_flask_status()
    
    if not flask_running:
        print(f"\\n🚨 MAIN ISSUE: Flask webhook server is NOT running!")
        print(f"   This is why webhook alerts aren't being logged.")
        
    start_flask_with_logging()
    create_test_webhook()
    diagnose_trading_activity()
    
    print(f"\\n🔧 RECOMMENDED ACTIONS:")
    print(f"1. Start Flask: python start_flask.py")
    print(f"2. Test webhook: python test_webhook.py")
    print(f"3. Check TradingView alert URL: http://localhost:5000/webhook")
    print(f"4. Monitor: python sync_status.py")

if __name__ == "__main__":
    main()
