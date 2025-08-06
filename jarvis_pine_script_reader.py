#!/usr/bin/env python3
"""
JARVIS Pine Script Integration
Uses your existing Pine Script strategy with TradingView FREE plan
No custom strategies needed - uses your already-developed Pine Script logic
"""

import time
import json
import requests
import logging
import re
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import schedule

# Configuration - uses your existing JARVIS settings
JARVIS_WEBHOOK_URL = "https://jarvis-quant-sys.onrender.com/webhook"
TRADINGVIEW_CHART_URL = "https://www.tradingview.com/chart/"  # You can customize this
CHECK_INTERVAL_SECONDS = 30
CONFIDENCE_THRESHOLD = 0.70  # Same as your Pine Script
DEFAULT_RISK_PERCENTAGE = 5.0  # Same as your JARVIS system
DEFAULT_STOP_LOSS_PIPS = 20
DEFAULT_TAKE_PROFIT_PIPS = 40

class JarvisPineScriptReader:
    def __init__(self):
        self.driver = None
        self.signal_history = []
        self.last_signal_time = None
        self.setup_logging()
        self.setup_driver()
        
    def setup_logging(self):
        """Set up logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('jarvis_pine_reader.log')
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_driver(self):
        """Set up Chrome driver with advanced stealth mode"""
        self.logger.info("🚀 Setting up JARVIS Automated Pine Script Reader...")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        
        # Advanced stealth mode to completely avoid TradingView detection
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Use a clean browser profile since password was reset
        # Don't use existing profile to avoid cached login issues
        # chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        # chrome_options.add_argument("--profile-directory=Default")
        
        # Enhanced user agent and device properties
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)
            self.driver.set_page_load_timeout(30)
            
            # Execute stealth scripts to hide automation
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
            
            self.logger.info("✅ JARVIS Pine Script Reader initialized (Stealth Mode Active)")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to setup WebDriver: {e}")
            return False
    
    def load_chart(self):
        """Load TradingView chart with your Pine Script indicators"""
        try:
            self.logger.info(f"📊 Loading TradingView chart with JARVIS Pine Script indicators...")
            
            # Load TradingView chart
            self.driver.get(TRADINGVIEW_CHART_URL)
            
            # Wait for chart to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".chart-container"))
            )
            
            time.sleep(10)  # Wait for indicators to load
            self.logger.info("✅ Chart loaded - JARVIS Pine Script indicators should be visible")
            
            # Instructions for user
            self.logger.info("🎯 SETUP INSTRUCTIONS:")
            self.logger.info("   1. Add your JARVIS Pine Script to this chart")
            self.logger.info("   2. Ensure EMA (12,26), RSI (14), MACD, and Bollinger Bands are visible")
            self.logger.info("   3. System will read these indicators and generate signals")
            self.logger.info("   4. Signals will be sent to your JARVIS system automatically")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load chart: {e}")
            return False
    
    def read_pine_script_indicators(self):
        """Read the exact indicators your Pine Script uses"""
        try:
            indicators = {}
            
            # Read current price
            current_price = self.read_current_price()
            if not current_price:
                return None
                
            indicators['price'] = current_price
            
            # Read your Pine Script indicators
            indicators.update(self.read_ema_values())
            indicators['rsi'] = self.read_rsi_value()
            indicators.update(self.read_macd_values())
            indicators.update(self.read_bollinger_bands())
            indicators['session'] = self.get_trading_session()
            
            # Validate indicators
            if not self.validate_indicators(indicators):
                return None
                
            return indicators
            
        except Exception as e:
            self.logger.error(f"❌ Error reading Pine Script indicators: {e}")
            return None
    
    def read_current_price(self):
        """Read current price from chart"""
        price_selectors = [
            ".tv-symbol-price-quote__value",
            ".js-symbol-last", 
            "[data-field='last_price']"
        ]
        
        for selector in price_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    text = element.text.strip()
                    price_match = re.search(r'([\d,]+\.?\d*)', text.replace(',', ''))
                    if price_match:
                        return float(price_match.group(1))
            except:
                continue
                
        return None
    
    def read_ema_values(self):
        """Read EMA 12 and EMA 26 (matching your Pine Script)"""
        emas = {}
        
        try:
            legend_items = self.driver.find_elements(By.CSS_SELECTOR, ".legend-source-item")
            
            for item in legend_items:
                text = item.text.lower()
                
                if 'ema' in text and '12' in text:
                    value_match = re.search(r'([\d,]+\.?\d*)', text.replace(',', ''))
                    if value_match:
                        emas['ema_12'] = float(value_match.group(1))
                
                elif 'ema' in text and '26' in text:
                    value_match = re.search(r'([\d,]+\.?\d*)', text.replace(',', ''))
                    if value_match:
                        emas['ema_26'] = float(value_match.group(1))
                        
        except Exception as e:
            self.logger.debug(f"Could not read EMA values: {e}")
            
        return emas
    
    def read_rsi_value(self):
        """Read RSI 14 (matching your Pine Script)"""
        try:
            legend_items = self.driver.find_elements(By.CSS_SELECTOR, ".legend-source-item")
            
            for item in legend_items:
                text = item.text.lower()
                
                if 'rsi' in text:
                    value_match = re.search(r'(\d{1,2}\.?\d*)', text)
                    if value_match:
                        rsi_value = float(value_match.group(1))
                        if 0 <= rsi_value <= 100:
                            return rsi_value
                            
        except Exception as e:
            self.logger.debug(f"Could not read RSI: {e}")
            
        return 50  # Default neutral
    
    def read_macd_values(self):
        """Read MACD values (matching your Pine Script)"""
        macd = {}
        
        try:
            legend_items = self.driver.find_elements(By.CSS_SELECTOR, ".legend-source-item")
            
            for item in legend_items:
                text = item.text.lower()
                
                if 'macd' in text:
                    numbers = re.findall(r'([-]?[\d,]+\.?\d*)', text.replace(',', ''))
                    
                    if len(numbers) >= 2:
                        macd['macd'] = float(numbers[0])
                        macd['macd_signal'] = float(numbers[1])
                        
        except Exception as e:
            self.logger.debug(f"Could not read MACD: {e}")
            
        return macd
    
    def read_bollinger_bands(self):
        """Read Bollinger Bands (matching your Pine Script)"""
        bb = {}
        
        try:
            legend_items = self.driver.find_elements(By.CSS_SELECTOR, ".legend-source-item")
            
            for item in legend_items:
                text = item.text.lower()
                
                if 'bollinger' in text or 'bb' in text:
                    numbers = re.findall(r'([\d,]+\.?\d*)', text.replace(',', ''))
                    
                    if len(numbers) >= 3:
                        bb['bb_upper'] = float(numbers[0])
                        bb['bb_middle'] = float(numbers[1])
                        bb['bb_lower'] = float(numbers[2])
                        
        except Exception as e:
            self.logger.debug(f"Could not read Bollinger Bands: {e}")
            
        return bb
    
    def get_trading_session(self):
        """Get trading session (matching your Pine Script filters)"""
        current_time = datetime.utcnow()
        hour = current_time.hour
        
        if 8 <= hour < 17:
            return "london"
        elif 13 <= hour < 22:
            return "newyork"
        elif hour >= 23 or hour < 8:
            return "tokyo"
        else:
            return "inactive"
    
    def validate_indicators(self, indicators):
        """Ensure minimum required indicators"""
        current_price = indicators.get('price')
        if not current_price:
            return False
            
        # Set defaults for missing indicators
        if 'ema_12' not in indicators:
            indicators['ema_12'] = current_price
        if 'ema_26' not in indicators:
            indicators['ema_26'] = current_price
        if 'rsi' not in indicators:
            indicators['rsi'] = 50
        if 'macd' not in indicators:
            indicators['macd'] = 0
        if 'macd_signal' not in indicators:
            indicators['macd_signal'] = 0
        if 'bb_upper' not in indicators:
            indicators['bb_upper'] = current_price * 1.02
        if 'bb_lower' not in indicators:
            indicators['bb_lower'] = current_price * 0.98
            
        return True
    
    def apply_jarvis_pine_script_logic(self, indicators):
        """Apply your existing Pine Script trading logic"""
        try:
            current_price = indicators['price']
            ema_12 = indicators['ema_12']
            ema_26 = indicators['ema_26'] 
            rsi = indicators['rsi']
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            bb_upper = indicators['bb_upper']
            bb_lower = indicators['bb_lower']
            session = indicators['session']
            
            # JARVIS Pine Script Buy Conditions (same logic as your Pine Script)
            buy_condition = (
                current_price > ema_12 and           # Price above fast EMA
                ema_12 > ema_26 and                 # Bullish EMA alignment
                rsi < 70 and rsi > 30 and           # RSI in range
                macd > macd_signal and              # MACD bullish
                current_price < bb_upper * 0.98 and # Not overbought
                session in ["london", "newyork"]    # Active trading session
            )
            
            # JARVIS Pine Script Sell Conditions
            sell_condition = (
                current_price < ema_12 and          # Price below fast EMA
                ema_12 < ema_26 and                # Bearish EMA alignment
                rsi > 30 and rsi < 70 and          # RSI in range  
                macd < macd_signal and             # MACD bearish
                current_price > bb_lower * 1.02 and # Not oversold
                session in ["london", "newyork"]    # Active trading session
            )
            
            if buy_condition:
                # Calculate confidence (matching your Pine Script logic)
                ema_strength = min(abs(ema_12 - ema_26) / ema_26 * 10, 0.15)
                rsi_strength = min(abs(50 - rsi) / 50 * 0.5, 0.1)
                
                confidence = min(0.95, 0.75 + ema_strength + rsi_strength)
                
                return {
                    "action": "buy",
                    "confidence": confidence,
                    "reason": f"JARVIS Pine Script BUY: EMA12({ema_12:.4f})>EMA26({ema_26:.4f}), RSI({rsi:.1f}), MACD+, {session.upper()}"
                }
                
            elif sell_condition:
                ema_strength = min(abs(ema_26 - ema_12) / ema_12 * 10, 0.15)
                rsi_strength = min(abs(50 - rsi) / 50 * 0.5, 0.1)
                
                confidence = min(0.95, 0.75 + ema_strength + rsi_strength)
                
                return {
                    "action": "sell",
                    "confidence": confidence,
                    "reason": f"JARVIS Pine Script SELL: EMA12({ema_12:.4f})<EMA26({ema_26:.4f}), RSI({rsi:.1f}), MACD-, {session.upper()}"
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error in Pine Script logic: {e}")
            return None
    
    def send_to_jarvis(self, signal, symbol="EUR_USD"):
        """Send signal to JARVIS system"""
        try:
            # Avoid duplicate signals
            if self.last_signal_time:
                time_diff = datetime.now() - self.last_signal_time
                if time_diff.total_seconds() < 60:
                    return False
            
            complete_signal = {
                "action": signal['action'],
                "symbol": symbol,
                "confidence": signal['confidence'],
                "price": 0,  # Will be set by JARVIS
                "timestamp": datetime.now().isoformat(),
                "source": "jarvis_pine_script_reader",
                "risk_percentage": DEFAULT_RISK_PERCENTAGE,
                "stop_loss_pips": DEFAULT_STOP_LOSS_PIPS,
                "take_profit_pips": DEFAULT_TAKE_PROFIT_PIPS,
                "reason": signal['reason']
            }
            
            self.logger.info(f"📤 Sending to JARVIS: {complete_signal}")
            
            response = requests.post(
                JARVIS_WEBHOOK_URL,
                json=complete_signal,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            if response.status_code == 200:
                self.logger.info("✅ Signal sent successfully to JARVIS")
                self.signal_history.append(complete_signal)
                self.last_signal_time = datetime.now()
                return True
            else:
                self.logger.error(f"❌ JARVIS error: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error sending to JARVIS: {e}")
            return False
    
    def monitor_and_trade(self):
        """Main monitoring loop using your Pine Script logic"""
        try:
            self.logger.info("🔍 Reading Pine Script indicators...")
            
            # Read indicators from chart
            indicators = self.read_pine_script_indicators()
            if not indicators:
                self.logger.warning("⚠️ No indicators available")
                return
            
            # Apply your Pine Script logic
            signal = self.apply_jarvis_pine_script_logic(indicators)
            
            if signal and signal.get('confidence', 0) >= CONFIDENCE_THRESHOLD:
                # Send to JARVIS
                symbol = self.extract_symbol() or "EUR_USD"
                success = self.send_to_jarvis(signal, symbol)
                
                if success:
                    self.logger.info(f"🎯 JARVIS Pine Script Signal: {signal['action'].upper()} {symbol} ({signal['confidence']:.1%})")
                else:
                    self.logger.error("❌ Failed to send signal to JARVIS")
            else:
                self.logger.info("📊 No JARVIS Pine Script signals found")
                
        except Exception as e:
            self.logger.error(f"❌ Error in monitoring: {e}")
    
    def extract_symbol(self):
        """Extract symbol from chart"""
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, ".tv-symbol-header__short-title")
            if elements:
                symbol = elements[0].text.strip()
                if len(symbol) >= 6:
                    return f"{symbol[:3]}_{symbol[3:6]}"
        except:
            pass
        return "EUR_USD"
    
    def start_monitoring(self):
        """Start the JARVIS Pine Script monitoring system"""
        self.logger.info("🚀 Starting JARVIS Pine Script Reader")
        self.logger.info("📊 Uses your existing Pine Script strategy")
        self.logger.info("💡 No custom programming needed - reads your indicators directly")
        self.logger.info(f"🔗 Connected to JARVIS: {JARVIS_WEBHOOK_URL}")
        
        # Load chart
        if not self.load_chart():
            self.logger.error("❌ Failed to load chart")
            return
        
        # Schedule monitoring  
        schedule.every(CHECK_INTERVAL_SECONDS).seconds.do(self.monitor_and_trade)
        
        # Initial check
        self.monitor_and_trade()
        
        # Keep running
        self.logger.info("🔄 JARVIS Pine Script monitoring started...")
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except KeyboardInterrupt:
                self.logger.info("⏹️ Stopped by user")
                break
            except Exception as e:
                self.logger.error(f"❌ Error: {e}")
                time.sleep(5)
    
    def cleanup(self):
        """Clean up"""
        if self.driver:
            self.driver.quit()
            self.logger.info("🧹 Cleanup completed")

def main():
    """Main function"""
    reader = None
    try:
        reader = JarvisPineScriptReader()
        reader.start_monitoring()
    except Exception as e:
        logging.error(f"❌ Fatal error: {e}")
    finally:
        if reader:
            reader.cleanup()

if __name__ == "__main__":
    main()
