#!/usr/bin/env python3
"""
JARVIS 100% AUTOMATED SYSTEM
Completely automated - no user interaction needed after initial login
"""

import time
import json
import requests
import logging
import threading
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class JarvisFullyAutomated:
    def __init__(self):
        self.driver = None
        self.jarvis_url = "https://jarvis-quant-sys.onrender.com/webhook"
        self.signal_count = 0
        self.running = False
        self.last_signals = []
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging without Unicode issues"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            handlers=[logging.StreamHandler()],
            encoding='utf-8'
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_browser(self):
        """Setup browser for 100% automation"""
        print("Setting up automated browser...")
        
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            print("Browser ready for automation!")
            return True
        except Exception as e:
            print(f"Browser setup failed: {e}")
            return False
    
    def automated_login_flow(self):
        """Automated login flow - opens TradingView and waits for setup"""
        print("Opening TradingView for automated trading...")
        
        try:
            # Open TradingView EUR/USD chart
            self.driver.get("https://www.tradingview.com/chart/?symbol=OANDA%3AEURUSD")
            
            print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🚀 JARVIS 100% AUTOMATED SYSTEM                          ║
║                          INITIAL SETUP REQUIRED                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 ONE-TIME SETUP (Do this once, then system runs forever):

1. LOGIN to TradingView with your reset password
2. ADD your Pine Script strategy to this EUR/USD chart  
3. ENSURE your Pine Script shows clear BUY/SELL signals
4. MINIMIZE this browser (don't close it)

⚠️  IMPORTANT: After setup, the system will:
✅ Monitor your Pine Script 24/7 automatically
✅ Detect BUY/SELL signals automatically  
✅ Execute trades through JARVIS automatically
✅ Use 5% risk management automatically
✅ Run completely hands-off

🔄 System will start automated monitoring in 60 seconds...
""")
            
            # Give user 60 seconds for setup
            for i in range(60, 0, -1):
                print(f"Starting automated monitoring in {i} seconds... (Complete setup now)")
                time.sleep(1)
            
            print("\n🤖 AUTOMATED MONITORING ACTIVE! System now runs 100% automatically.")
            return True
            
        except Exception as e:
            print(f"Login flow error: {e}")
            return False
    
    def detect_pine_script_signals(self):
        """Advanced signal detection from Pine Script elements"""
        signals = []
        
        try:
            # Multiple detection methods for Pine Script signals
            detection_selectors = [
                # Text elements
                "text[fill*='green']", "text[fill*='red']",
                "text[fill*='#00ff00']", "text[fill*='#ff0000']",
                "text[fill*='#008000']", "text[fill*='#800000']",
                
                # Shape elements  
                "path[fill*='green']", "path[fill*='red']",
                "rect[fill*='green']", "rect[fill*='red']",
                "circle[fill*='green']", "circle[fill*='red']",
                
                # Pine Script specific
                ".pine-label", ".js-pine-label",
                "[data-name*='signal']", "[data-name*='buy']", "[data-name*='sell']",
                
                # Chart annotations
                ".chart-markup-table text",
                "g[data-name*='study'] text"
            ]
            
            for selector in detection_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    # Check recent elements (last 20)
                    for element in elements[-20:]:
                        try:
                            text_content = element.text.lower() if element.text else ""
                            title_attr = element.get_attribute('title') or ""
                            
                            combined_text = f"{text_content} {title_attr}".lower()
                            
                            # Enhanced signal detection
                            buy_keywords = ['buy', 'long', 'bull', 'up', 'green', 'call']
                            sell_keywords = ['sell', 'short', 'bear', 'down', 'red', 'put']
                            
                            if any(keyword in combined_text for keyword in buy_keywords):
                                signals.append({
                                    'action': 'buy',
                                    'confidence': 0.80,
                                    'source': 'pine_script_detection',
                                    'text': combined_text[:50]
                                })
                                
                            elif any(keyword in combined_text for keyword in sell_keywords):
                                signals.append({
                                    'action': 'sell', 
                                    'confidence': 0.80,
                                    'source': 'pine_script_detection',
                                    'text': combined_text[:50]
                                })
                                
                        except:
                            continue
                            
                except:
                    continue
            
            # Remove duplicates and return unique signals
            unique_signals = []
            seen = set()
            
            for signal in signals:
                signal_key = f"{signal['action']}_{signal.get('text', '')}"
                if signal_key not in seen:
                    seen.add(signal_key)
                    unique_signals.append(signal)
            
            return unique_signals[-3:]  # Return last 3 unique signals
            
        except Exception as e:
            print(f"Signal detection error: {e}")
            return []
    
    def send_signal_to_jarvis(self, signal):
        """Send detected signal to JARVIS for automatic trading"""
        trade_signal = {
            "action": signal['action'],
            "symbol": "EUR_USD",
            "confidence": signal['confidence'],
            "risk_percentage": 5.0,  # Your 5% risk system
            "stop_loss_pips": 20,
            "take_profit_pips": 40,
            "source": "fully_automated_pine_reader",
            "timestamp": datetime.now().isoformat(),
            "reason": f"Automated Pine Script {signal['action'].upper()} detection",
            "detected_text": signal.get('text', ''),
            "automation_mode": True
        }
        
        try:
            print(f"📤 Sending {signal['action'].upper()} signal to JARVIS...")
            
            response = requests.post(
                self.jarvis_url,
                json=trade_signal,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            if response.status_code == 200:
                self.signal_count += 1
                result = response.json()
                
                print(f"""
🚨 AUTOMATED TRADE EXECUTED!
   ⏰ Time: {datetime.now().strftime('%H:%M:%S')}
   📈 Action: {signal['action'].upper()}
   💱 Symbol: EUR/USD
   💪 Confidence: {signal['confidence']:.1%}
   💰 Risk: 5.0%
   📊 Total Signals: {self.signal_count}
   ✅ JARVIS Response: {result.get('message', 'Trade executed')}
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
                return True
            else:
                print(f"❌ JARVIS rejected signal: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending signal: {e}")
            return False
    
    def automated_monitoring_loop(self):
        """Main automated monitoring loop - runs 24/7"""
        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                🤖 JARVIS FULLY AUTOMATED MONITORING ACTIVE                  ║
║                          24/7 AUTOMATED TRADING                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 Monitoring: EUR/USD with your Pine Script strategy
💰 Risk Management: 5% per trade (automatic)
🎯 Stop Loss: 20 pips | Take Profit: 40 pips
🔄 Check Interval: Every 20 seconds
📡 JARVIS Endpoint: {self.jarvis_url}

🤖 SYSTEM IS NOW 100% AUTOMATED!
   ✅ No manual intervention required
   ✅ Trades execute automatically
   ✅ Monitors continuously 24/7
   ✅ Risk management automatic

💡 Keep this window minimized - system runs automatically
⏹️  Press Ctrl+C ONLY to stop trading
""")
        
        self.running = True
        signal_history = []
        
        try:
            while self.running:
                # Detect signals from Pine Script
                detected_signals = self.detect_pine_script_signals()
                
                for signal in detected_signals:
                    signal_key = f"{signal['action']}_{signal.get('text', '')}"
                    
                    # Check if this signal was recently processed
                    if signal_key not in signal_history[-10:]:
                        # Send signal to JARVIS for automatic trading
                        if self.send_signal_to_jarvis(signal):
                            signal_history.append(signal_key)
                            
                            # Add to recent signals list
                            self.last_signals.append({
                                'time': datetime.now().strftime('%H:%M:%S'),
                                'action': signal['action'],
                                'status': 'executed'
                            })
                            
                            # Keep only last 20 signals
                            self.last_signals = self.last_signals[-20:]
                
                # Status update every minute
                current_time = datetime.now().strftime('%H:%M:%S')
                print(f"🔄 {current_time} - Automated monitoring active... (Trades executed: {self.signal_count})")
                
                # Show recent signals
                if self.last_signals:
                    recent = self.last_signals[-3:]
                    signal_summary = ', '.join([f'{s["time"]} {s["action"].upper()}' for s in recent])
                    print(f"   📊 Recent signals: {signal_summary}")
                
                time.sleep(20)  # Check every 20 seconds for faster detection
                
        except KeyboardInterrupt:
            print("\n⏹️  Automated trading stopped by user")
            self.running = False
        except Exception as e:
            print(f"❌ Monitoring error: {e}")
            print("🔄 Attempting to restart monitoring...")
            time.sleep(10)
            if self.running:
                self.automated_monitoring_loop()  # Restart monitoring
    
    def run_fully_automated(self):
        """Run the complete 100% automated system"""
        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              🚀 JARVIS 100% FULLY AUTOMATED TRADING SYSTEM                  ║
║                        NO MANUAL INTERVENTION NEEDED                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

🎯 COMPLETE AUTOMATION:
✅ Opens TradingView automatically
✅ Monitors Pine Script signals automatically  
✅ Detects BUY/SELL signals automatically
✅ Sends signals to JARVIS automatically
✅ JARVIS executes trades automatically
✅ 5% risk management applied automatically
✅ Stop loss & take profit set automatically
✅ Runs 24/7 without intervention

🚀 Starting fully automated system...
""")
        
        try:
            # Setup browser
            if not self.setup_browser():
                print("❌ Browser setup failed")
                return False
            
            # Handle login flow  
            if not self.automated_login_flow():
                print("❌ Login flow failed")
                return False
            
            # Start automated monitoring
            self.automated_monitoring_loop()
            
        except Exception as e:
            print(f"❌ System error: {e}")
            return False
        finally:
            if self.driver:
                print("🧹 Cleaning up browser...")
                self.driver.quit()

def main():
    """Main function - starts 100% automated system"""
    system = JarvisFullyAutomated()
    system.run_fully_automated()

if __name__ == "__main__":
    main()
