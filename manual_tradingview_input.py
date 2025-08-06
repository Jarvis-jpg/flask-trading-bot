#!/usr/bin/env python3
"""
JARVIS Pine Script Reader - Manual Mode
For when automated browser login is blocked by TradingView
"""

import time
import json
import requests
import logging
from datetime import datetime

# Configuration
JARVIS_WEBHOOK_URL = "https://jarvis-quant-sys.onrender.com/webhook"
CHECK_INTERVAL_SECONDS = 30
DEFAULT_RISK_PERCENTAGE = 5.0

class ManualTradingViewReader:
    def __init__(self):
        self.setup_logging()
        self.signal_history = []
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
    def manual_signal_input(self):
        """Manual signal input when TradingView blocks automated login"""
        
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    📊 MANUAL TRADINGVIEW SIGNAL INPUT                       ║
║                 Use this when automated login is blocked                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

🎯 INSTRUCTIONS:
1. Open TradingView in your regular browser
2. Login to your account normally  
3. Set up your Pine Script on EUR/USD chart
4. Watch for BUY/SELL signals
5. When you see a signal, input it below

📋 SIGNAL FORMAT:
- BUY: Enter 'buy' when your Pine Script shows bullish signal
- SELL: Enter 'sell' when your Pine Script shows bearish signal  
- QUIT: Enter 'quit' to exit

🚀 Ready to monitor your Pine Script signals manually...
""")
        
        while True:
            try:
                # Get user input
                signal_input = input("\n🔍 Enter signal (buy/sell/quit): ").strip().lower()
                
                if signal_input == 'quit':
                    print("👋 Goodbye! Manual monitoring stopped.")
                    break
                    
                elif signal_input in ['buy', 'sell']:
                    # Get additional details
                    confidence = input("💪 Enter confidence (70-95): ").strip()
                    try:
                        confidence_val = float(confidence) / 100
                        if confidence_val < 0.7 or confidence_val > 0.95:
                            print("❌ Confidence must be between 70-95")
                            continue
                    except:
                        confidence_val = 0.75  # Default
                        print(f"📊 Using default confidence: 75%")
                    
                    # Create signal
                    signal = {
                        "action": signal_input,
                        "symbol": "EUR_USD",
                        "confidence": confidence_val,
                        "price": 0,  # Will be set by JARVIS
                        "timestamp": datetime.now().isoformat(),
                        "source": "manual_tradingview_input",
                        "risk_percentage": DEFAULT_RISK_PERCENTAGE,
                        "stop_loss_pips": 20,
                        "take_profit_pips": 40,
                        "reason": f"Manual Pine Script {signal_input.upper()} signal"
                    }
                    
                    # Send to JARVIS
                    success = self.send_to_jarvis(signal)
                    
                    if success:
                        print(f"✅ {signal_input.upper()} signal sent to JARVIS successfully!")
                        print(f"📊 Confidence: {confidence_val:.1%}")
                        print(f"💰 Risk: {DEFAULT_RISK_PERCENTAGE}%")
                    else:
                        print("❌ Failed to send signal to JARVIS")
                        
                else:
                    print("❌ Invalid input. Please enter 'buy', 'sell', or 'quit'")
                    
            except KeyboardInterrupt:
                print("\n👋 Manual monitoring stopped by user")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                
    def send_to_jarvis(self, signal):
        """Send signal to JARVIS system"""
        try:
            self.logger.info(f"📤 Sending manual signal to JARVIS: {signal}")
            
            response = requests.post(
                JARVIS_WEBHOOK_URL,
                json=signal,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            if response.status_code == 200:
                self.logger.info("✅ Manual signal sent successfully to JARVIS")
                self.signal_history.append(signal)
                return True
            else:
                self.logger.error(f"❌ JARVIS error: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error sending manual signal: {e}")
            return False

def main():
    """Main function for manual TradingView input"""
    reader = ManualTradingViewReader()
    reader.manual_signal_input()

if __name__ == "__main__":
    main()
