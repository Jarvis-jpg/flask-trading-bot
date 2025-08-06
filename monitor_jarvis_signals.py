#!/usr/bin/env python3
"""
Real-time JARVIS Signal Monitor
Shows live signals being received by JARVIS system
"""

import requests
import time
import json
from datetime import datetime, timedelta

class JARVISSignalMonitor:
    def __init__(self):
        self.jarvis_url = "https://jarvis-quant-sys.onrender.com"
        self.last_check = datetime.now() - timedelta(minutes=5)
        
    def monitor_signals(self):
        """Monitor signals in real-time"""
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                📡 JARVIS LIVE SIGNAL MONITOR                                ║
║                    Real-time Signal Detection                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

🔍 Monitoring for signals...
📊 Dashboard: https://jarvis-quant-sys.onrender.com
⏰ Press Ctrl+C to stop monitoring

""")
        
        signal_count = 0
        
        try:
            while True:
                # Check for new signals
                signals = self.check_recent_signals()
                
                if signals:
                    for signal in signals:
                        signal_count += 1
                        self.display_signal(signal, signal_count)
                
                # Show status every 30 seconds
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"🔄 {current_time} - Monitoring... (Signals detected: {signal_count})")
                
                time.sleep(30)
                
        except KeyboardInterrupt:
            print(f"\n👋 Monitoring stopped. Total signals detected: {signal_count}")
    
    def check_recent_signals(self):
        """Check for recent signals from JARVIS"""
        try:
            # Get recent trades/signals from JARVIS
            response = requests.get(f"{self.jarvis_url}/recent-signals", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('signals', [])
            else:
                return []
                
        except Exception as e:
            print(f"⚠️  Error checking signals: {e}")
            return []
    
    def display_signal(self, signal, count):
        """Display detected signal"""
        timestamp = signal.get('timestamp', datetime.now().isoformat())
        action = signal.get('action', 'Unknown').upper()
        symbol = signal.get('symbol', 'Unknown')
        confidence = signal.get('confidence', 0) * 100
        source = signal.get('source', 'Unknown')
        
        print(f"""
🚨 SIGNAL #{count} DETECTED!
   ⏰ Time: {timestamp}
   📈 Action: {action}
   💱 Symbol: {symbol}
   💪 Confidence: {confidence:.1f}%
   📡 Source: {source}
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
    
    def test_signal_flow(self):
        """Test the complete signal flow"""
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   🧪 TESTING COMPLETE SIGNAL FLOW                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
        
        # Send test signal
        test_signal = {
            "action": "buy",
            "symbol": "EUR_USD",
            "confidence": 0.80,
            "risk_percentage": 5.0,
            "source": "flow_test",
            "timestamp": datetime.now().isoformat(),
            "test_mode": True
        }
        
        print("📤 Sending test signal...")
        
        try:
            response = requests.post(
                f"{self.jarvis_url}/webhook",
                json=test_signal,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ TEST SIGNAL SUCCESSFUL!")
                print(f"   Response: {result}")
                
                # Wait and check if signal appears in system
                print("⏳ Checking if signal appears in system...")
                time.sleep(3)
                
                signals = self.check_recent_signals()
                if signals:
                    print("✅ Signal flow working correctly!")
                    return True
                else:
                    print("⚠️  Signal sent but not visible in system")
                    return False
                    
            else:
                print(f"❌ Test signal failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Test signal error: {e}")
            return False

def main():
    """Main function"""
    monitor = JARVISSignalMonitor()
    
    print("Choose monitoring option:")
    print("1. Real-time signal monitoring")
    print("2. Test signal flow")
    print("3. Both")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        monitor.monitor_signals()
    elif choice == "2":
        monitor.test_signal_flow()
    elif choice == "3":
        print("Testing signal flow first...")
        monitor.test_signal_flow()
        print("\nStarting real-time monitoring...")
        time.sleep(2)
        monitor.monitor_signals()
    else:
        print("Invalid choice. Starting real-time monitoring...")
        monitor.monitor_signals()

if __name__ == "__main__":
    main()
