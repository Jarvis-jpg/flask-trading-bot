#!/usr/bin/env python3
"""
JARVIS Simple Automated Reader - Fresh Start
Clean implementation after password reset
"""

import time
import json
import requests
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class SimpleJarvisReader:
    def __init__(self):
        self.driver = None
        self.jarvis_url = "https://jarvis-quant-sys.onrender.com/webhook"
        self.signal_count = 0
        self.setup_logging()
        
    def setup_logging(self):
        """Simple logging setup"""
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
    def start_browser(self):
        """Start fresh Chrome browser"""
        print("🌐 Starting fresh Chrome browser...")
        
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            print("✅ Chrome browser ready!")
            return True
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False
    
    def open_tradingview(self):
        """Open TradingView and wait for user login"""
        print("🔐 Opening TradingView - Please login with your reset password...")
        
        try:
            self.driver.get("https://www.tradingview.com/chart/?symbol=OANDA%3AEURUSD")
            
            print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          🔐 LOGIN REQUIRED                                  ║
║                                                                              ║
║  1. Login with your RESET password                                          ║
║  2. Navigate to EUR/USD chart (should already be loaded)                    ║
║  3. Add your Pine Script strategy to the chart                              ║
║  4. Press ENTER in this terminal when ready for automation                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
            
            input("Press ENTER when you've logged in and added your Pine Script...")
            print("🚀 Starting automated monitoring...")
            return True
            
        except Exception as e:
            print(f"❌ TradingView loading error: {e}")
            return False
    
    def detect_signals(self):
        """Simple signal detection from Pine Script"""
        try:
            # Look for common Pine Script signal elements
            elements = self.driver.find_elements(By.CSS_SELECTOR, 
                "text, .pine-label, [data-name*='signal'], [data-name*='buy'], [data-name*='sell']")
            
            signals = []
            for element in elements[-10:]:  # Check last 10 elements
                try:
                    text = element.text.lower() if element.text else ""
                    
                    if any(word in text for word in ['buy', 'long', 'bull']):
                        signals.append({'action': 'buy', 'confidence': 0.75})
                    elif any(word in text for word in ['sell', 'short', 'bear']):
                        signals.append({'action': 'sell', 'confidence': 0.75})
                        
                except:
                    continue
            
            return signals
            
        except Exception as e:
            self.logger.error(f"Signal detection error: {e}")
            return []
    
    def send_signal(self, signal):
        """Send signal to JARVIS"""
        payload = {
            "action": signal['action'],
            "symbol": "EUR_USD",
            "confidence": signal['confidence'],
            "risk_percentage": 5.0,
            "stop_loss_pips": 20,
            "take_profit_pips": 40,
            "source": "simple_automated_reader",
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            response = requests.post(self.jarvis_url, json=payload, timeout=10)
            if response.status_code == 200:
                self.signal_count += 1
                print(f"✅ {signal['action'].upper()} signal #{self.signal_count} sent to JARVIS!")
                return True
            else:
                print(f"❌ Signal rejected: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Signal sending error: {e}")
            return False
    
    def monitor_continuously(self):
        """Monitor for signals continuously"""
        print(f"""
🤖 AUTOMATED MONITORING ACTIVE!

📊 Monitoring: EUR/USD with your Pine Script
💰 Risk per trade: 5%
🎯 Stop Loss: 20 pips | Take Profit: 40 pips
📡 JARVIS Webhook: {self.jarvis_url}

⏰ Press Ctrl+C to stop
""")
        
        last_signals = []
        
        try:
            while True:
                signals = self.detect_signals()
                
                for signal in signals:
                    signal_key = f"{signal['action']}"
                    
                    # Avoid duplicate signals
                    if signal_key not in last_signals[-5:]:
                        if self.send_signal(signal):
                            last_signals.append(signal_key)
                
                # Status update
                print(f"🔄 {datetime.now().strftime('%H:%M:%S')} - Monitoring... (Signals: {self.signal_count})")
                time.sleep(30)  # Check every 30 seconds
                
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped by user")
        except Exception as e:
            print(f"❌ Monitoring error: {e}")
    
    def run(self):
        """Main execution function"""
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                🚀 JARVIS SIMPLE AUTOMATED READER                            ║
║                        Fresh Start - No Issues                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
        
        try:
            if not self.start_browser():
                return
            
            if not self.open_tradingview():
                return
            
            self.monitor_continuously()
            
        except Exception as e:
            print(f"❌ System error: {e}")
        finally:
            if self.driver:
                self.driver.quit()

def main():
    reader = SimpleJarvisReader()
    reader.run()

if __name__ == "__main__":
    main()
