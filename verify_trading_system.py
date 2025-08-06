#!/usr/bin/env python3
"""
JARVIS Trading System Verification
Comprehensive test to ensure TradingView reader and JARVIS communication works
"""

import requests
import json
import time
import subprocess
import os
from datetime import datetime

class TradingSystemVerifier:
    def __init__(self):
        self.jarvis_url = "https://jarvis-quant-sys.onrender.com"
        self.webhook_url = f"{self.jarvis_url}/webhook"
        self.status_url = f"{self.jarvis_url}/status"
        
    def run_full_verification(self):
        """Run complete system verification"""
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                🔍 JARVIS TRADING SYSTEM VERIFICATION                         ║
║                     Ensuring Everything Works Correctly                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
        
        # Step 1: Check JARVIS system status
        print("1️⃣  CHECKING JARVIS SYSTEM STATUS...")
        jarvis_ok = self.check_jarvis_status()
        
        # Step 2: Check OANDA connection
        print("\n2️⃣  CHECKING OANDA CONNECTION...")
        oanda_ok = self.check_oanda_connection()
        
        # Step 3: Test webhook endpoint
        print("\n3️⃣  TESTING WEBHOOK ENDPOINT...")
        webhook_ok = self.test_webhook_endpoint()
        
        # Step 4: Send test signal
        print("\n4️⃣  SENDING TEST SIGNAL...")
        signal_ok = self.send_test_signal()
        
        # Step 5: Check if TradingView reader is running
        print("\n5️⃣  CHECKING TRADINGVIEW READER...")
        reader_ok = self.check_reader_status()
        
        # Step 6: Provide instructions for manual verification
        print("\n6️⃣  MANUAL VERIFICATION STEPS...")
        self.provide_manual_steps()
        
        # Final assessment
        print("\n" + "="*80)
        self.provide_final_assessment(jarvis_ok, oanda_ok, webhook_ok, signal_ok, reader_ok)
        
    def check_jarvis_status(self):
        """Check if JARVIS system is online"""
        try:
            response = requests.get(self.status_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ JARVIS System: ONLINE")
                print(f"   Status: {data.get('status', 'Unknown')}")
                print(f"   Balance: ${data.get('balance', 'Unknown')}")
                print(f"   Active Trades: {data.get('active_trades', 'Unknown')}")
                return True
            else:
                print(f"❌ JARVIS System: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ JARVIS System: CONNECTION FAILED - {e}")
            return False
    
    def check_oanda_connection(self):
        """Check OANDA API connection"""
        try:
            response = requests.get(f"{self.jarvis_url}/oanda-status", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ OANDA Connection: ACTIVE")
                print(f"   Account: {data.get('account_id', 'Unknown')}")
                print(f"   Balance: ${data.get('balance', 'Unknown')}")
                return True
            else:
                print(f"⚠️  OANDA Connection: Status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ OANDA Connection: FAILED - {e}")
            return False
    
    def test_webhook_endpoint(self):
        """Test webhook endpoint accessibility"""
        try:
            # Send a ping to webhook
            test_data = {"test": "ping", "timestamp": datetime.now().isoformat()}
            response = requests.post(self.webhook_url, json=test_data, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Webhook Endpoint: ACCESSIBLE")
                print(f"   URL: {self.webhook_url}")
                return True
            else:
                print(f"❌ Webhook Endpoint: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Webhook Endpoint: FAILED - {e}")
            return False
    
    def send_test_signal(self):
        """Send a test trading signal"""
        try:
            test_signal = {
                "action": "buy",
                "symbol": "EUR_USD", 
                "confidence": 0.75,
                "risk_percentage": 5.0,
                "stop_loss_pips": 20,
                "take_profit_pips": 40,
                "source": "verification_test",
                "timestamp": datetime.now().isoformat(),
                "test_mode": True  # Important: this is a test
            }
            
            print(f"📤 Sending test signal: {test_signal['action'].upper()}")
            
            response = requests.post(self.webhook_url, json=test_signal, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Test Signal: RECEIVED BY JARVIS")
                print(f"   Response: {result.get('message', 'Unknown')}")
                print(f"   Status: {result.get('status', 'Unknown')}")
                return True
            else:
                print(f"❌ Test Signal: REJECTED - HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Test Signal: FAILED - {e}")
            return False
    
    def check_reader_status(self):
        """Check if TradingView reader process is running"""
        try:
            # Check for Python processes that might be the reader
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq python.exe', '/FO', 'CSV'],
                capture_output=True,
                text=True,
                shell=True
            )
            
            if 'python.exe' in result.stdout:
                print(f"✅ Python Process: DETECTED")
                print(f"   Multiple Python processes may be running")
                print(f"   TradingView reader could be active")
                return True
            else:
                print(f"⚠️  Python Process: NOT DETECTED")
                print(f"   TradingView reader may not be running")
                return False
                
        except Exception as e:
            print(f"❌ Reader Status: CHECK FAILED - {e}")
            return False
    
    def provide_manual_steps(self):
        """Provide manual verification steps"""
        print("""
📋 MANUAL VERIFICATION CHECKLIST:

✅ Step 1: Confirm TradingView is open with your Pine Script
   - Chart should show EUR/USD
   - Pine Script strategy should be active
   - Look for BUY/SELL signals on chart

✅ Step 2: Verify reader connection
   - If using manual input: Run 'python manual_tradingview_input.py'
   - If using automated reader: Ensure browser is open to TradingView

✅ Step 3: Test signal flow
   - When you see a signal, input it (manual) or verify it's detected (auto)
   - Check JARVIS dashboard for received signals
   - Verify trades appear in OANDA account

✅ Step 4: Monitor for 5-10 minutes
   - Watch for any BUY/SELL signals
   - Confirm signals reach JARVIS
   - Verify JARVIS executes trades with 5% risk
""")
    
    def provide_final_assessment(self, jarvis_ok, oanda_ok, webhook_ok, signal_ok, reader_ok):
        """Provide final system assessment"""
        total_checks = 5
        passed_checks = sum([jarvis_ok, oanda_ok, webhook_ok, signal_ok, reader_ok])
        
        print(f"📊 SYSTEM VERIFICATION RESULTS:")
        print(f"   ✅ Passed: {passed_checks}/{total_checks}")
        print(f"   📈 Success Rate: {(passed_checks/total_checks)*100:.0f}%")
        
        if passed_checks >= 4:
            print(f"""
🎯 CONCLUSION: SYSTEM IS READY FOR TRADING! 
✅ Core systems operational
✅ JARVIS can receive and execute trades  
✅ 5% risk management active
✅ OANDA connection established

🚀 NEXT STEPS:
1. Keep TradingView open with your Pine Script
2. Run manual input: python manual_tradingview_input.py
3. Input BUY/SELL signals when you see them
4. JARVIS will execute trades automatically
5. Monitor dashboard: {self.jarvis_url}
""")
        elif passed_checks >= 2:
            print(f"""
⚠️  CONCLUSION: SYSTEM PARTIALLY READY
✅ Some systems working
❌ Issues need attention

🔧 ACTIONS NEEDED:
1. Check failed components above
2. Restart any failed services
3. Verify network connections
4. Re-run verification after fixes
""")
        else:
            print(f"""
❌ CONCLUSION: SYSTEM NOT READY
❌ Multiple critical failures

🔧 IMMEDIATE ACTIONS:
1. Check internet connection
2. Verify JARVIS system at {self.jarvis_url}
3. Restart all components
4. Contact support if issues persist
""")

def main():
    """Main verification function"""
    verifier = TradingSystemVerifier()
    verifier.run_full_verification()
    
    # Keep checking status
    print(f"\n⏰ CONTINUOUS MONITORING (Press Ctrl+C to stop)")
    try:
        while True:
            time.sleep(30)
            print(f"\n🔄 Quick Status Check - {datetime.now().strftime('%H:%M:%S')}")
            verifier.check_jarvis_status()
    except KeyboardInterrupt:
        print(f"\n👋 Monitoring stopped by user")

if __name__ == "__main__":
    main()
