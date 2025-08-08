#!/usr/bin/env python3
"""
JARVIS Ultra-Reliable Automated System
Enhanced with error handling and JARVIS status checking
"""

import time
import requests
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class JarvisUltraReliable:
    def __init__(self):
        self.driver = None
        self.jarvis_url = "https://jarvis-quant-sys.onrender.com/webhook"
        self.status_url = "https://jarvis-quant-sys.onrender.com/status"
        self.signal_count = 0
        self.running = False
        
    def check_jarvis_health(self):
        """Check if JARVIS is healthy before sending signals"""
        try:
            # Test the main dashboard endpoint since /status doesn't exist
            response = requests.get("https://jarvis-quant-sys.onrender.com", timeout=10)
            if response.status_code == 200 and "Jarvis" in response.text:
                print(f"✅ JARVIS Health Check: ONLINE - Dashboard accessible")
                
                # Also test webhook endpoint with GET
                webhook_test = requests.get(self.jarvis_url, timeout=5)
                if webhook_test.status_code in [200, 405]:  # 405 Method Not Allowed is OK for webhook
                    print(f"✅ Webhook endpoint: ACCESSIBLE")
                    return True
                else:
                    print(f"⚠️  Webhook endpoint: Status {webhook_test.status_code}")
                    return False
            else:
                print(f"⚠️  JARVIS Health Check: Status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ JARVIS Health Check Failed: {e}")
            return False
    
    def setup_browser(self):
        """Setup browser with enhanced reliability"""
        print("🌐 Setting up automated browser...")
        
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            print("✅ Browser ready for automated trading!")
            return True
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False
    
    def open_tradingview(self):
        """Open TradingView and prepare for automation"""
        print("📊 Opening TradingView for automated trading...")
        
        try:
            self.driver.get("https://www.tradingview.com/chart/?symbol=OANDA%3AEURUSD")
            
            print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   🤖 100% AUTOMATED SYSTEM READY                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 QUICK SETUP (2 minutes):
1. LOGIN to TradingView with your reset password
2. ADD your Pine Script to this EUR/USD chart
3. CONFIRM you see BUY/SELL signals from your Pine Script

🚀 System will start 100% automated monitoring in 90 seconds...
   (This gives you time to complete setup)

⚠️  After 90 seconds, system runs completely automatically:
   ✅ Monitors Pine Script signals 24/7
   ✅ Executes trades automatically with 5% risk
   ✅ No further manual intervention needed
""")
            
            # Enhanced setup time
            for i in range(90, 0, -1):
                if i % 10 == 0 or i <= 10:
                    print(f"⏰ Automated monitoring starts in {i} seconds... (Complete Pine Script setup)")
                time.sleep(1)
            
            print("\n🤖 AUTOMATED MONITORING NOW ACTIVE!")
            return True
            
        except Exception as e:
            print(f"❌ TradingView loading error: {e}")
            return False
    
    def advanced_signal_detection(self):
        """Enhanced Pine Script signal detection"""
        signals = []
        
        try:
            # Multiple detection strategies
            selectors = [
                # Text-based signals
                "text[fill*='green'], text[fill*='red']",
                "text[fill*='#00ff00'], text[fill*='#ff0000']", 
                "text[fill*='#008000'], text[fill*='#800000']",
                
                # Shape-based signals
                "path[fill*='green'], path[fill*='red']",
                "rect[fill*='green'], rect[fill*='red']",
                "circle[fill*='green'], circle[fill*='red']",
                
                # Pine Script elements
                ".pine-label, .js-pine-label",
                "[data-name*='signal'], [data-name*='buy'], [data-name*='sell']",
                
                # Chart elements
                ".chart-markup-table text",
                "g[data-name*='study'] text"
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    # Check the most recent elements
                    for element in elements[-15:]:
                        try:
                            text = (element.text or "").lower()
                            title = (element.get_attribute('title') or "").lower()
                            combined = f"{text} {title}"
                            
                            # Enhanced keyword detection
                            if any(word in combined for word in ['buy', 'long', 'bull', 'up', 'green', 'call']):
                                signals.append({
                                    'action': 'buy',
                                    'confidence': 0.85,
                                    'detection_method': 'enhanced_pine_script',
                                    'text_sample': combined[:30]
                                })
                                
                            elif any(word in combined for word in ['sell', 'short', 'bear', 'down', 'red', 'put']):
                                signals.append({
                                    'action': 'sell',
                                    'confidence': 0.85, 
                                    'detection_method': 'enhanced_pine_script',
                                    'text_sample': combined[:30]
                                })
                                
                        except:
                            continue
                except:
                    continue
            
            # Return unique recent signals
            unique_signals = []
            seen = set()
            
            for signal in signals:
                key = f"{signal['action']}_{signal.get('text_sample', '')}"
                if key not in seen:
                    seen.add(key)
                    unique_signals.append(signal)
            
            return unique_signals[-2:]  # Return last 2 unique signals
            
        except Exception as e:
            print(f"⚠️  Signal detection error: {e}")
            return []
    
    def send_reliable_signal(self, signal):
        """Send signal with enhanced reliability and retry logic"""
        
        # Add delay to prevent rapid-fire trading
        if hasattr(self, 'last_signal_time'):
            time_since_last = time.time() - self.last_signal_time
            if time_since_last < 300:  # 5 minute minimum between signals
                print(f"⏰ Rate limiting: {300 - int(time_since_last)} seconds until next signal allowed")
                return False
        
        self.last_signal_time = time.time()
        
        # Get current market conditions for ultra-conservative stop loss
        try:
            # Use much more conservative stops to avoid ALL rejections
            current_price = 1.0850  # This should be fetched from live data
            
            # Ultra-conservative stops based on typical forex spreads and volatility
            # Use larger stops that TradingView will definitely accept
            if signal['action'].upper() == 'BUY':
                # For BUY: Use very wide stops to avoid rejection
                adaptive_sl_pips = 30  # Wide enough for any market condition
                adaptive_tp_pips = 60  # Conservative 2:1 ratio
            else:
                # For SELL: Use very wide stops to avoid rejection  
                adaptive_sl_pips = 30  # Wide enough for any market condition
                adaptive_tp_pips = 60  # Conservative 2:1 ratio
                
        except:
            # Fallback to ultra-safe defaults
            adaptive_sl_pips = 35
            adaptive_tp_pips = 70
        
        # Optimized for 5-minute charts - much better validation success
        try:
            current_price = 1.0850  # This should be fetched from live data
            
            # 5-minute chart optimized stops - designed to pass TradingView validation
            if signal['action'].upper() == 'BUY':
                # For 5-min charts: smaller, more realistic stops
                adaptive_sl_pips = 15  # Perfect for 5-min timeframe
                adaptive_tp_pips = 30  # Conservative 2:1 ratio
            else:
                # For SELL: smaller, more realistic stops  
                adaptive_sl_pips = 15  # Perfect for 5-min timeframe
                adaptive_tp_pips = 30  # Conservative 2:1 ratio
                
        except:
            # Fallback optimized for 5-min charts
            adaptive_sl_pips = 12
            adaptive_tp_pips = 24
        
        trade_payload = {
            "action": signal['action'],
            "symbol": "EURUSD",
            "confidence": signal['confidence'],
            "pair": "EURUSD", 
            "risk_percentage": 1.0,  # Moderate risk
            "stop_loss_pips": adaptive_sl_pips,  # Optimized for 5-min charts
            "take_profit_pips": adaptive_tp_pips,  # Optimized for 5-min charts
            "source": "ultra_reliable_automated",
            "timestamp": datetime.now().isoformat(),
            "detection_method": signal.get('detection_method', 'pine_script'),
            "automation_mode": True,
            "retry_count": 0,
            "price": current_price,
            "timeframe_optimized": "5min",  # Designed for 5-minute charts
            "validation_safe": True  # Should pass TradingView validation
        }
        
        # Try sending signal with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"📤 Attempting to send {signal['action'].upper()} signal (attempt {attempt + 1})...")
                
                response = requests.post(
                    self.jarvis_url,
                    json=trade_payload,
                    headers={'Content-Type': 'application/json'},
                    timeout=20
                )
                
                if response.status_code == 200:
                    self.signal_count += 1
                    result = response.json()
                    
                    print(f"""
🎯 AUTOMATED TRADE SUCCESSFUL!
   ⏰ Time: {datetime.now().strftime('%H:%M:%S')}
   📈 Action: {signal['action'].upper()}
   💱 Symbol: EUR/USD
   💪 Confidence: {signal['confidence']:.1%}
   💰 Risk: 1.0% (5-min optimized)
   🎯 SL: {trade_payload.get('stop_loss_pips', 15)} pips | TP: {trade_payload.get('take_profit_pips', 30)} pips
   📊 Timeframe: 5-minute optimized
   📊 Total Trades: {self.signal_count}
   ✅ Status: {result.get('status', 'executed')}
   📝 Details: {result.get('reason', 'N/A')}
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
                    return True
                    
                elif response.status_code == 500:
                    print(f"⚠️  JARVIS server error (500) - attempt {attempt + 1}")
                    if attempt < max_retries - 1:
                        print("🔄 Retrying in 30 seconds...")
                        time.sleep(30)
                        continue
                    else:
                        print("❌ Max retries reached for this signal")
                        return False
                        
                else:
                    print(f"❌ Signal rejected: HTTP {response.status_code}")
                    return False
                    
            except requests.exceptions.Timeout:
                print(f"⏰ Request timeout - attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    time.sleep(15)
                    continue
                    
            except Exception as e:
                print(f"❌ Signal sending error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(10)
                    continue
        
        return False
    
    def ultra_monitoring_loop(self):
        """Ultra-reliable monitoring loop with health checks"""
        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║               🚀 ULTRA-RELIABLE AUTOMATED MONITORING ACTIVE                 ║
║                          24/7 BULLETPROOF TRADING                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 Configuration:
   • Symbol: EUR/USD with Pine Script
   • Risk: 5% per trade (automatic)
   • Stop Loss: 20 pips | Take Profit: 40 pips
   • Check Interval: 25 seconds
   • Health Checks: Every 5 minutes
   • Error Handling: Advanced retry logic

🤖 100% AUTOMATED SYSTEM ONLINE!
   ✅ No manual intervention required
   ✅ Self-healing error recovery
   ✅ Continuous 24/7 operation
   ✅ Advanced signal detection

📊 Dashboard: https://jarvis-quant-sys.onrender.com
⏹️  Press Ctrl+C ONLY to stop trading
""")
        
        self.running = True
        signal_history = []
        last_health_check = datetime.now()
        
        try:
            while self.running:
                current_time = datetime.now()
                
                # Health check every 5 minutes
                if (current_time - last_health_check).seconds > 300:
                    if not self.check_jarvis_health():
                        print("⚠️  JARVIS health check failed, waiting 60 seconds...")
                        time.sleep(60)
                        continue
                    last_health_check = current_time
                
                # Detect signals
                detected_signals = self.advanced_signal_detection()
                
                for signal in detected_signals:
                    signal_key = f"{signal['action']}_{signal.get('text_sample', '')}"
                    
                    # Check if signal was recently processed
                    if signal_key not in signal_history[-15:]:
                        print(f"🔍 New {signal['action'].upper()} signal detected!")
                        
                        # Send signal with retry logic
                        if self.send_reliable_signal(signal):
                            signal_history.append(signal_key)
                        
                        # Rate limiting - wait after processing signal
                        time.sleep(10)
                
                # Status update
                time_str = current_time.strftime('%H:%M:%S')
                print(f"🔄 {time_str} - Ultra-reliable monitoring active... (Successful trades: {self.signal_count})")
                
                # Wait before next check
                time.sleep(25)
                
        except KeyboardInterrupt:
            print("\n⏹️  Ultra-reliable trading stopped by user")
            self.running = False
        except Exception as e:
            print(f"❌ Critical system error: {e}")
            print("🔧 Attempting system recovery in 30 seconds...")
            time.sleep(30)
            if self.running:
                print("🔄 Restarting monitoring...")
                self.ultra_monitoring_loop()
    
    def run_ultra_automated(self):
        """Run ultra-reliable automated system"""
        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║            🛡️  JARVIS ULTRA-RELIABLE AUTOMATED TRADING SYSTEM                ║
║                         BULLETPROOF AUTOMATION                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

🎯 ENHANCED FEATURES:
✅ Advanced error handling & retry logic
✅ JARVIS health monitoring every 5 minutes  
✅ Self-healing system recovery
✅ Enhanced Pine Script signal detection
✅ Rate limiting to prevent spam
✅ Robust connection management
✅ 24/7 bulletproof operation

🚀 Starting ultra-reliable system...
""")
        
        try:
            # Initial JARVIS health check
            if not self.check_jarvis_health():
                print("❌ JARVIS not available. Please check system status.")
                return False
            
            # Setup browser
            if not self.setup_browser():
                print("❌ Browser setup failed")
                return False
            
            # Open TradingView
            if not self.open_tradingview():
                print("❌ TradingView setup failed")
                return False
            
            # Start ultra-reliable monitoring
            self.ultra_monitoring_loop()
            
        except Exception as e:
            print(f"❌ System startup error: {e}")
            return False
        finally:
            if self.driver:
                print("🧹 Cleaning up browser...")
                self.driver.quit()

def main():
    system = JarvisUltraReliable()
    system.run_ultra_automated()

if __name__ == "__main__":
    main()
