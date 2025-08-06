#!/usr/bin/env python3
"""
TradingView Free Plan Signal Reader
Automatically reads signals from TradingView free charts and sends to JARVIS
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
import schedule

# Configuration
JARVIS_WEBHOOK_URL = "https://jarvis-quant-sys.onrender.com/webhook"
TRADINGVIEW_CHART_URL = "https://www.tradingview.com/chart/"  # Add your specific chart URL
CHECK_INTERVAL_SECONDS = 30
CONFIDENCE_THRESHOLD = 0.70

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TradingViewReader:
    def __init__(self):
        self.driver = None
        self.last_signal = None
        self.setup_driver()
        
    def setup_driver(self):
        """Set up Chrome driver with stealth options"""
        logger.info("🚀 Setting up Chrome WebDriver...")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        # Remove headless mode so you can see what's happening
        # chrome_options.add_argument("--headless")
        
        # Install and set up ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        logger.info("✅ Chrome WebDriver initialized successfully")
    
    def login_to_tradingview(self, username=None, password=None):
        """Login to TradingView (optional for free charts)"""
        try:
            if not username or not password:
                logger.info("ℹ️ No login credentials provided - using anonymous access")
                return True
                
            logger.info("🔐 Logging into TradingView...")
            self.driver.get("https://www.tradingview.com/accounts/signin/")
            
            # Wait for login form
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = self.driver.find_element(By.NAME, "password")
            
            username_field.send_keys(username)
            password_field.send_keys(password)
            
            # Submit login
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            time.sleep(5)  # Wait for login to complete
            logger.info("✅ Successfully logged into TradingView")
            return True
            
        except Exception as e:
            logger.error(f"❌ Login failed: {e}")
            return False
    
    def load_chart(self, chart_url=None):
        """Load TradingView chart"""
        try:
            url = chart_url or TRADINGVIEW_CHART_URL
            logger.info(f"📊 Loading TradingView chart: {url}")
            
            self.driver.get(url)
            time.sleep(10)  # Wait for chart to load
            
            logger.info("✅ Chart loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load chart: {e}")
            return False
    
    def read_indicators(self):
        """Read indicator values from the chart"""
        try:
            # Wait for chart to be fully loaded
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "chart-container"))
            )
            
            # Get current price
            price_element = self.driver.find_element(By.CSS_SELECTOR, "[data-name='legend-source-item']")
            current_price = float(price_element.text.split()[1]) if price_element else 0
            
            # Read indicator values (you'll need to customize these selectors based on your chart)
            indicators = {
                'price': current_price,
                'timestamp': datetime.now().isoformat(),
                'pair': 'EUR_USD'  # Default pair, customize as needed
            }
            
            # Try to read EMA values (customize selector based on your indicators)
            try:
                ema_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-name='legend-source-item']")
                for i, elem in enumerate(ema_elements[:3]):  # Get first 3 indicators
                    indicators[f'indicator_{i}'] = elem.text
            except:
                pass
            
            logger.info(f"📈 Current indicators: {indicators}")
            return indicators
            
        except Exception as e:
            logger.error(f"❌ Failed to read indicators: {e}")
            return None
    
    def analyze_signals(self, indicators):
        """Analyze indicators and generate trading signals"""
        if not indicators or not indicators.get('price'):
            return None
        
        # Simple signal logic (customize based on your strategy)
        price = indicators['price']
        timestamp = indicators['timestamp']
        
        # Example signal generation (replace with your actual logic)
        # This is a placeholder - you'll customize based on your indicators
        import random
        
        # Generate signal based on price movement or your indicators
        signal_type = None
        confidence = 0
        
        # Example: Simple price-based signal (replace with your indicator logic)
        if random.random() > 0.7:  # Simulate signal condition
            signal_type = "buy" if random.random() > 0.5 else "sell"
            confidence = random.uniform(0.7, 0.95)
        
        if signal_type and confidence >= CONFIDENCE_THRESHOLD:
            signal = {
                "action": signal_type,
                "symbol": indicators.get('pair', 'EUR_USD'),
                "confidence": confidence,
                "price": price,
                "timestamp": timestamp,
                "source": "tradingview_free",
                "risk_percentage": 5.0,
                "stop_loss_pips": 20,
                "take_profit_pips": 40
            }
            
            logger.info(f"📡 Generated signal: {signal}")
            return signal
        
        return None
    
    def send_signal_to_jarvis(self, signal):
        """Send trading signal to JARVIS webhook"""
        try:
            if signal == self.last_signal:
                logger.info("🔄 Signal unchanged, skipping duplicate")
                return False
            
            logger.info(f"📤 Sending signal to JARVIS: {signal}")
            
            response = requests.post(
                JARVIS_WEBHOOK_URL,
                json=signal,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("✅ Signal sent successfully to JARVIS")
                self.last_signal = signal
                return True
            else:
                logger.error(f"❌ Failed to send signal: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error sending signal: {e}")
            return False
    
    def monitor_chart(self):
        """Main monitoring loop"""
        logger.info("🔍 Starting chart monitoring...")
        
        try:
            # Read current indicators
            indicators = self.read_indicators()
            if not indicators:
                return
            
            # Analyze for signals
            signal = self.analyze_signals(indicators)
            if signal:
                self.send_signal_to_jarvis(signal)
            else:
                logger.info("📊 No trading signals detected")
                
        except Exception as e:
            logger.error(f"❌ Error in monitoring: {e}")
    
    def start_monitoring(self):
        """Start continuous monitoring"""
        logger.info("🚀 Starting TradingView Free Signal Reader")
        logger.info(f"📊 Monitoring interval: {CHECK_INTERVAL_SECONDS} seconds")
        logger.info(f"🎯 Confidence threshold: {CONFIDENCE_THRESHOLD}")
        logger.info(f"📡 JARVIS webhook: {JARVIS_WEBHOOK_URL}")
        
        # Schedule monitoring
        schedule.every(CHECK_INTERVAL_SECONDS).seconds.do(self.monitor_chart)
        
        # Initial monitoring
        self.monitor_chart()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
            logger.info("🧹 WebDriver cleanup completed")

def main():
    reader = None
    try:
        reader = TradingViewReader()
        
        # Optional: Login to TradingView (leave None for anonymous)
        # reader.login_to_tradingview("your_username", "your_password")
        
        # Load your chart
        chart_success = reader.load_chart()
        if not chart_success:
            logger.error("❌ Failed to load chart - exiting")
            return
        
        # Start monitoring
        reader.start_monitoring()
        
    except KeyboardInterrupt:
        logger.info("⏹️ Monitoring stopped by user")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
    finally:
        if reader:
            reader.cleanup()

if __name__ == "__main__":
    main()
