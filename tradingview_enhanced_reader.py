#!/usr/bin/env python3
"""
Enhanced TradingView Free Signal Reader
Advanced version with custom strategy logic and better error handling
"""

import time
import json
import requests
import logging
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import schedule
from tradingview_config import *

class EnhancedTradingViewReader:
    def __init__(self):
        self.driver = None
        self.signal_history = []
        self.last_signal_time = None
        self.error_count = 0
        self.setup_logging()
        self.setup_driver()
        
    def setup_logging(self):
        """Set up logging configuration"""
        log_level = getattr(logging, LOGGING_SETTINGS['level'])
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(LOGGING_SETTINGS['log_file']) if LOGGING_SETTINGS['log_to_file'] else logging.NullHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_driver(self):
        """Set up Chrome driver with enhanced options"""
        self.logger.info("🚀 Setting up Enhanced Chrome WebDriver...")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"--window-size={BROWSER_SETTINGS['window_width']},{BROWSER_SETTINGS['window_height']}")
        
        if BROWSER_SETTINGS['headless']:
            chrome_options.add_argument("--headless")
        
        # Additional stability options
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(BROWSER_SETTINGS['implicit_wait'])
            self.driver.set_page_load_timeout(BROWSER_SETTINGS['page_load_timeout'])
            
            # Execute script to remove automation indicators
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.logger.info("✅ Enhanced Chrome WebDriver initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to setup WebDriver: {e}")
            return False
    
    def load_chart(self, retries=0):
        """Load TradingView chart with retry logic"""
        try:
            url = CHART_URL or "https://www.tradingview.com/chart/"
            self.logger.info(f"📊 Loading TradingView chart: {url}")
            
            self.driver.get(url)
            
            # Wait for chart to fully load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, SELECTORS['chart_container']))
            )
            
            # Wait for loading to complete
            try:
                WebDriverWait(self.driver, 5).until_not(
                    EC.presence_of_element_located((By.CSS_SELECTOR, SELECTORS['loading_indicator']))
                )
            except:
                pass  # Loading indicator might not be present
            
            time.sleep(5)  # Additional wait for stability
            self.logger.info("✅ Chart loaded successfully")
            self.error_count = 0
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load chart: {e}")
            
            if retries < ERROR_SETTINGS['max_retries']:
                self.logger.info(f"🔄 Retrying... ({retries + 1}/{ERROR_SETTINGS['max_retries']})")
                time.sleep(ERROR_SETTINGS['retry_delay'])
                return self.load_chart(retries + 1)
            
            return False
    
    def extract_price_data(self):
        """Extract current price and Pine Script indicators"""
        try:
            # Import the indicator reader
            from tradingview_indicator_reader import TradingViewIndicatorReader
            
            # Create indicator reader
            indicator_reader = TradingViewIndicatorReader(self.driver)
            
            # Read all Pine Script indicators
            indicators = indicator_reader.read_pine_script_indicators()
            
            if not indicators:
                self.logger.warning("⚠️ Could not read Pine Script indicators")
                return None
            
            # Validate we have minimum required data
            if not indicator_reader.validate_indicators(indicators):
                self.logger.warning("⚠️ Invalid indicator data")
                return None
            
            # Get symbol/pair information
            symbol = self.extract_symbol() or "EUR_USD"
            
            # Complete market data with Pine Script indicators
            market_data = {
                'price': indicators['price'],
                'symbol': symbol,
                'timestamp': datetime.now().isoformat(),
                'source': 'tradingview_pine_script',
                
                # Pine Script indicators (exactly matching your strategy)
                'ema_12': indicators.get('ema_12'),
                'ema_26': indicators.get('ema_26'),
                'rsi': indicators.get('rsi', 50),
                'macd': indicators.get('macd', 0),
                'macd_signal': indicators.get('macd_signal', 0),
                'macd_histogram': indicators.get('macd_histogram', 0),
                'bb_upper': indicators.get('bb_upper'),
                'bb_lower': indicators.get('bb_lower'),
                'bb_middle': indicators.get('bb_middle'),
                'session': indicators.get('session', 'unknown')
            }
            
            self.logger.info(f"📈 Pine Script indicators extracted: Price={market_data['price']}, EMA12={market_data['ema_12']}, EMA26={market_data['ema_26']}, RSI={market_data['rsi']}")
            return market_data
            
        except Exception as e:
            self.logger.error(f"❌ Error extracting Pine Script indicators: {e}")
            return None
    
    def extract_symbol(self):
        """Extract current trading symbol/pair"""
        try:
            symbol_selectors = [
                ".tv-symbol-header__short-title",
                ".js-symbol-short",
                "[data-name='legend-source-title']"
            ]
            
            for selector in symbol_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        symbol_text = elements[0].text.strip()
                        # Convert to OANDA format (e.g., EURUSD -> EUR_USD)
                        if len(symbol_text) >= 6 and symbol_text.isalpha():
                            return f"{symbol_text[:3]}_{symbol_text[3:6]}"
                except:
                    continue
            
            return "EUR_USD"  # Default fallback
            
        except Exception as e:
            self.logger.error(f"❌ Error extracting symbol: {e}")
            return "EUR_USD"
    
    def generate_trading_signal(self, market_data):
        """Generate trading signal using custom logic"""
        try:
            if not market_data:
                return None
            
            current_price = market_data['price']
            
            # Use custom signal logic from config
            signal = custom_signal_logic(
                indicators=market_data,
                current_price=current_price,
                previous_signals=self.signal_history[-10:]  # Last 10 signals
            )
            
            if signal and signal.get('confidence', 0) >= CONFIDENCE_THRESHOLD:
                # Complete the signal with required fields
                complete_signal = {
                    "action": signal['action'],
                    "symbol": market_data['symbol'],
                    "confidence": signal['confidence'],
                    "price": current_price,
                    "timestamp": market_data['timestamp'],
                    "source": "tradingview_free_enhanced",
                    "risk_percentage": DEFAULT_RISK_PERCENTAGE,
                    "stop_loss_pips": DEFAULT_STOP_LOSS_PIPS,
                    "take_profit_pips": DEFAULT_TAKE_PROFIT_PIPS,
                    "reason": signal.get('reason', 'Custom strategy signal')
                }
                
                self.logger.info(f"📡 Generated trading signal: {complete_signal}")
                return complete_signal
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Error generating signal: {e}")
            return None
    
    def send_to_jarvis(self, signal):
        """Send trading signal to JARVIS with retry logic"""
        try:
            # Avoid duplicate signals within short time window
            if self.last_signal_time:
                time_diff = datetime.now() - self.last_signal_time
                if time_diff.total_seconds() < 60:  # 1 minute cooldown
                    self.logger.info("🔄 Signal cooldown active, skipping...")
                    return False
            
            self.logger.info(f"📤 Sending signal to JARVIS: {signal}")
            
            response = requests.post(
                JARVIS_WEBHOOK_URL,
                json=signal,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            if response.status_code == 200:
                self.logger.info("✅ Signal sent successfully to JARVIS")
                self.signal_history.append(signal)
                self.last_signal_time = datetime.now()
                
                # Keep only recent signals in memory
                if len(self.signal_history) > 50:
                    self.signal_history = self.signal_history[-25:]
                
                return True
            else:
                self.logger.error(f"❌ JARVIS returned error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error sending to JARVIS: {e}")
            return False
    
    def monitor_and_signal(self):
        """Main monitoring and signal generation loop"""
        try:
            self.logger.info("🔍 Checking for trading opportunities...")
            
            # Extract current market data
            market_data = self.extract_price_data()
            if not market_data:
                self.logger.warning("⚠️ No market data available")
                return
            
            # Generate trading signal
            signal = self.generate_trading_signal(market_data)
            
            if signal:
                # Send to JARVIS
                success = self.send_to_jarvis(signal)
                if success:
                    self.logger.info(f"🎯 Signal processed: {signal['action'].upper()} {signal['symbol']}")
                else:
                    self.logger.error("❌ Failed to send signal to JARVIS")
            else:
                self.logger.info("📊 No trading opportunities found")
            
            self.error_count = 0  # Reset error count on success
            
        except Exception as e:
            self.logger.error(f"❌ Error in monitoring loop: {e}")
            self.error_count += 1
            
            if self.error_count >= ERROR_SETTINGS['max_retries']:
                if ERROR_SETTINGS['restart_on_error']:
                    self.logger.info("🔄 Too many errors, restarting...")
                    self.restart()
                else:
                    raise e
    
    def restart(self):
        """Restart the monitoring system"""
        try:
            self.logger.info("🔄 Restarting TradingView reader...")
            
            if self.driver:
                self.driver.quit()
            
            time.sleep(5)
            self.setup_driver()
            self.load_chart()
            self.error_count = 0
            
            self.logger.info("✅ Restart completed successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Restart failed: {e}")
            raise e
    
    def start_monitoring(self):
        """Start the continuous monitoring system"""
        self.logger.info("🚀 Starting Enhanced TradingView Free Signal Reader")
        self.logger.info(f"📊 Check interval: {CHECK_INTERVAL_SECONDS} seconds")
        self.logger.info(f"🎯 Confidence threshold: {CONFIDENCE_THRESHOLD}")
        self.logger.info(f"📡 JARVIS webhook: {JARVIS_WEBHOOK_URL}")
        self.logger.info(f"💰 Risk per trade: {DEFAULT_RISK_PERCENTAGE}%")
        
        # Load chart first
        if not self.load_chart():
            self.logger.error("❌ Failed to load chart - cannot start monitoring")
            return
        
        # Schedule monitoring
        schedule.every(CHECK_INTERVAL_SECONDS).seconds.do(self.monitor_and_signal)
        
        # Run initial check
        self.monitor_and_signal()
        
        # Keep running
        self.logger.info("🔄 Entering monitoring loop...")
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except KeyboardInterrupt:
                self.logger.info("⏹️ Monitoring stopped by user")
                break
            except Exception as e:
                self.logger.error(f"❌ Unexpected error in main loop: {e}")
                if ERROR_SETTINGS['restart_on_error']:
                    self.restart()
                else:
                    break
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.driver:
                self.driver.quit()
            self.logger.info("🧹 Cleanup completed")
        except:
            pass

def main():
    """Main function to start the enhanced reader"""
    reader = None
    try:
        reader = EnhancedTradingViewReader()
        reader.start_monitoring()
    except Exception as e:
        logging.error(f"❌ Fatal error: {e}")
    finally:
        if reader:
            reader.cleanup()

if __name__ == "__main__":
    main()
