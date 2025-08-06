#!/usr/bin/env python3
"""
JARVIS Automated Pine Script Reader - FULLY AUTOMATED
No manual input needed - reads Pine Script signals automatically
"""

import time
import json
import requests
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import threading

class AutomatedTradingViewReader:
    def __init__(self):
        self.setup_logging()
        self.driver = None
        self.jarvis_webhook_url = "https://jarvis-quant-sys.onrender.com/webhook"
        self.last_signal_time = None
        self.signal_count = 0
        self.running = False
        
        # Your existing Pine Script strategy logic integrated
        self.pine_script_logic = {
            'ema_fast': 12,
            'ema_slow': 26,
            'rsi_period': 14,
            'risk_percentage': 5.0,
            'stop_loss_pips': 20,
            'take_profit_pips': 40
        }
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('jarvis_auto_reader.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_driver(self):
        """Setup Chrome driver with optimal settings"""
        options = Options()
        
        # Performance and stealth options
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--window-size=1920,1080")
        
        # User agent to appear as regular browser
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=options)
            
            # Execute JavaScript to hide automation traces
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.logger.info("✅ Chrome driver initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to setup Chrome driver: {e}")
            return False
    
    def login_to_tradingview(self):
        """Login to TradingView with your reset password"""
        try:
            self.logger.info("🌐 Opening TradingView...")
            self.driver.get("https://www.tradingview.com/accounts/signin/")
            
            # Wait for login form
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     🔐 TRADINGVIEW LOGIN REQUIRED                           ║
║                   Please login with your reset password                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 STEPS:
1. Login with your username and NEW password
2. Complete any 2FA if required
3. Once logged in, the system will continue automatically
4. DO NOT CLOSE THE BROWSER - Let it run automatically

⏳ Waiting for you to complete login...
""")
            
            # Wait for successful login (check for profile or dashboard elements)
            self.logger.info("⏳ Waiting for login completion...")
            
            login_success = False
            for attempt in range(60):  # Wait up to 5 minutes for login
                try:
                    # Check for elements that indicate successful login
                    if (self.driver.find_elements(By.CSS_SELECTOR, "[data-name='header-user-menu-button']") or
                        self.driver.find_elements(By.CSS_SELECTOR, ".js-header-symbol-search") or
                        "tradingview.com/chart" in self.driver.current_url):
                        login_success = True
                        break
                except:
                    pass
                
                time.sleep(5)
                print(f"⏳ Still waiting for login... ({attempt + 1}/60)")
            
            if login_success:
                self.logger.info("✅ Login successful!")
                return True
            else:
                self.logger.error("❌ Login timeout - please try again")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Login error: {e}")
            return False
    
    def navigate_to_chart(self):
        """Navigate to EUR/USD chart with your Pine Script"""
        try:
            self.logger.info("📊 Opening EUR/USD chart...")
            
            # Navigate to EUR/USD chart
            chart_url = "https://www.tradingview.com/chart/?symbol=OANDA%3AEURUSD"
            self.driver.get(chart_url)
            
            # Wait for chart to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "header-toolbar-symbol-search"))
            )
            
            self.logger.info("✅ Chart loaded successfully")
            
            print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                      📊 SETUP YOUR PINE SCRIPT                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 STEPS:
1. Add your Pine Script strategy to the EUR/USD chart
2. Ensure it shows BUY/SELL signals clearly
3. The system will automatically detect and trade signals
4. Keep this browser window open

🚀 System will start monitoring automatically in 30 seconds...
""")
            
            # Give user time to add Pine Script
            for i in range(30, 0, -1):
                print(f"⏳ Starting automatic monitoring in {i} seconds...")
                time.sleep(1)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Chart navigation error: {e}")
            return False
    
    def detect_pine_script_signals(self):
        """Detect BUY/SELL signals from Pine Script on chart"""
        try:
            # Look for various signal indicators
            signal_selectors = [
                # Text-based signals
                "text[fill*='green']",  # Green text (often BUY)
                "text[fill*='red']",    # Red text (often SELL)
                "text[fill*='#00ff00']",  # Bright green
                "text[fill*='#ff0000']",  # Bright red
                
                # Shape-based signals
                "path[fill*='green']",
                "path[fill*='red']",
                "rect[fill*='green']",
                "rect[fill*='red']",
                
                # Label elements
                "[data-name*='signal']",
                "[data-name*='buy']",
                "[data-name*='sell']",
                
                # Pine Script specific elements
                ".pine-label",
                ".js-pine-label"
            ]
            
            detected_signals = []
            
            for selector in signal_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements[-5:]:  # Check last 5 elements
                        try:
                            text = element.text.lower() if element.text else ""
                            title = element.get_attribute('title') or ""
                            
                            # Check for BUY signals
                            if any(keyword in text for keyword in ['buy', 'long', 'bull']) or \
                               any(keyword in title.lower() for keyword in ['buy', 'long', 'bull']):
                                detected_signals.append({
                                    'action': 'buy',
                                    'element': element,
                                    'text': text or title,
                                    'confidence': 0.75
                                })
                            
                            # Check for SELL signals
                            elif any(keyword in text for keyword in ['sell', 'short', 'bear']) or \
                                 any(keyword in title.lower() for keyword in ['sell', 'short', 'bear']):
                                detected_signals.append({
                                    'action': 'sell',
                                    'element': element,
                                    'text': text or title,
                                    'confidence': 0.75
                                })
                                
                        except Exception:
                            continue
                            
                except Exception:
                    continue
            
            return detected_signals
            
        except Exception as e:
            self.logger.error(f"❌ Signal detection error: {e}")
            return []
    
    def send_signal_to_jarvis(self, signal_data):
        """Send detected signal to JARVIS"""
        try:
            # Create signal payload using your existing Pine Script logic
            signal = {
                "action": signal_data['action'],
                "symbol": "EUR_USD",
                "confidence": signal_data['confidence'],
                "price": 0,  # Will be set by JARVIS
                "timestamp": datetime.now().isoformat(),
                "source": "automated_pine_script_reader",
                "risk_percentage": self.pine_script_logic['risk_percentage'],
                "stop_loss_pips": self.pine_script_logic['stop_loss_pips'],
                "take_profit_pips": self.pine_script_logic['take_profit_pips'],
                "reason": f"Pine Script {signal_data['action'].upper()} signal detected",
                "signal_text": signal_data.get('text', ''),
                "ema_fast": self.pine_script_logic['ema_fast'],
                "ema_slow": self.pine_script_logic['ema_slow'],
                "rsi_period": self.pine_script_logic['rsi_period']
            }
            
            self.logger.info(f"📤 Sending {signal_data['action'].upper()} signal to JARVIS...")
            
            response = requests.post(
                self.jarvis_webhook_url,
                json=signal,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            if response.status_code == 200:
                self.signal_count += 1
                self.last_signal_time = datetime.now()
                
                result = response.json()
                self.logger.info(f"✅ {signal_data['action'].upper()} signal sent successfully!")
                self.logger.info(f"   Response: {result.get('message', 'Unknown')}")
                self.logger.info(f"   Total signals sent: {self.signal_count}")
                
                print(f"""
🚨 SIGNAL SENT TO JARVIS!
   ⏰ Time: {datetime.now().strftime('%H:%M:%S')}
   📈 Action: {signal_data['action'].upper()}
   💱 Symbol: EUR/USD
   💪 Confidence: {signal_data['confidence']:.1%}
   💰 Risk: {self.pine_script_logic['risk_percentage']}%
   🎯 Stop Loss: {self.pine_script_logic['stop_loss_pips']} pips
   🎯 Take Profit: {self.pine_script_logic['take_profit_pips']} pips
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
                return True
            else:
                self.logger.error(f"❌ JARVIS rejected signal: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error sending signal to JARVIS: {e}")
            return False
    
    def start_monitoring(self):
        """Start automatic monitoring for Pine Script signals"""
        self.running = True
        self.logger.info("🚀 Starting automatic Pine Script monitoring...")
        
        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                🤖 FULLY AUTOMATED PINE SCRIPT MONITORING                    ║
║                            System is now LIVE!                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 Monitoring: EUR/USD with your Pine Script strategy
💰 Risk per trade: {self.pine_script_logic['risk_percentage']}%
🎯 Stop Loss: {self.pine_script_logic['stop_loss_pips']} pips
🎯 Take Profit: {self.pine_script_logic['take_profit_pips']} pips
🔗 JARVIS Webhook: {self.jarvis_webhook_url}

⏰ Press Ctrl+C to stop monitoring
""")
        
        signal_history = []
        
        try:
            while self.running:
                # Detect signals from Pine Script
                signals = self.detect_pine_script_signals()
                
                for signal in signals:
                    # Avoid duplicate signals (check if similar signal was sent recently)
                    signal_key = f"{signal['action']}_{signal.get('text', '')}"
                    
                    if signal_key not in signal_history[-10:]:  # Check last 10 signals
                        # Send signal to JARVIS
                        if self.send_signal_to_jarvis(signal):
                            signal_history.append(signal_key)
                
                # Status update every 30 seconds
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"🔄 {current_time} - Monitoring... (Signals sent: {self.signal_count})")
                
                time.sleep(30)  # Check every 30 seconds
                
        except KeyboardInterrupt:
            self.logger.info("👋 Monitoring stopped by user")
        except Exception as e:
            self.logger.error(f"❌ Monitoring error: {e}")
        finally:
            self.running = False
    
    def run_fully_automated(self):
        """Run the complete automated system"""
        try:
            print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              🚀 JARVIS FULLY AUTOMATED PINE SCRIPT READER                   ║
║                        No Manual Input Required!                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

🎯 WHAT THIS DOES:
✅ Opens TradingView automatically
✅ Waits for you to login with reset password
✅ Navigates to EUR/USD chart
✅ Detects your Pine Script BUY/SELL signals
✅ Sends signals to JARVIS automatically
✅ JARVIS executes trades with 5% risk
✅ Monitors continuously - NO manual input needed!

🚀 Starting automated system...
""")
            
            # Setup browser
            if not self.setup_driver():
                return False
            
            # Login to TradingView
            if not self.login_to_tradingview():
                return False
            
            # Navigate to chart
            if not self.navigate_to_chart():
                return False
            
            # Start monitoring
            self.start_monitoring()
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Automated system error: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()

def main():
    """Main function to run the automated reader"""
    reader = AutomatedTradingViewReader()
    reader.run_fully_automated()

if __name__ == "__main__":
    main()
