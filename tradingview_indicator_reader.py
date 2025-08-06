#!/usr/bin/env python3
"""
TradingView Indicator Reader
Reads the same indicators your Pine Script uses and generates identical signals
"""

import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TradingViewIndicatorReader:
    def __init__(self, driver):
        self.driver = driver
        self.indicators = {}
        
    def read_pine_script_indicators(self):
        """Read the exact same indicators your Pine Script uses"""
        try:
            # Wait for indicators panel to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".legend-source-item"))
            )
            
            indicators = {}
            
            # Read current price first
            current_price = self.read_current_price()
            indicators['price'] = current_price
            
            if not current_price:
                return None
                
            # Read EMA values (matching your Pine Script EMA 12, 26)
            ema_values = self.read_ema_indicators()
            indicators.update(ema_values)
            
            # Read RSI (matching your Pine Script RSI 14)
            rsi_value = self.read_rsi_indicator()
            if rsi_value:
                indicators['rsi'] = rsi_value
                
            # Read MACD (matching your Pine Script MACD)
            macd_values = self.read_macd_indicator()
            indicators.update(macd_values)
            
            # Read Bollinger Bands (matching your Pine Script)
            bb_values = self.read_bollinger_bands()
            indicators.update(bb_values)
            
            # Add session information (London/NY hours like your Pine Script)
            indicators['session'] = self.get_trading_session()
            
            print(f"📊 Indicators read: {indicators}")
            return indicators
            
        except Exception as e:
            print(f"❌ Error reading indicators: {e}")
            return None
    
    def read_current_price(self):
        """Read current price from multiple possible locations"""
        price_selectors = [
            ".tv-symbol-price-quote__value",
            ".js-symbol-last", 
            "[data-field='last_price']",
            ".chart-markup-table .apply-common-tooltip"
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
    
    def read_ema_indicators(self):
        """Read EMA 12 and EMA 26 values (matching your Pine Script)"""
        emas = {}
        
        try:
            # Look for EMA indicators in the legend
            legend_items = self.driver.find_elements(By.CSS_SELECTOR, ".legend-source-item")
            
            for item in legend_items:
                text = item.text.lower()
                
                # Look for EMA 12
                if 'ema' in text and ('12' in text or 'exponential' in text):
                    value_match = re.search(r'([\d,]+\.?\d*)', text.replace(',', ''))
                    if value_match:
                        emas['ema_12'] = float(value_match.group(1))
                
                # Look for EMA 26  
                elif 'ema' in text and '26' in text:
                    value_match = re.search(r'([\d,]+\.?\d*)', text.replace(',', ''))
                    if value_match:
                        emas['ema_26'] = float(value_match.group(1))
                        
        except Exception as e:
            print(f"⚠️ Could not read EMA values: {e}")
            
        return emas
    
    def read_rsi_indicator(self):
        """Read RSI 14 value (matching your Pine Script)"""
        try:
            legend_items = self.driver.find_elements(By.CSS_SELECTOR, ".legend-source-item")
            
            for item in legend_items:
                text = item.text.lower()
                
                if 'rsi' in text or 'relative strength' in text:
                    # Look for RSI value (usually 0-100)
                    value_match = re.search(r'(\d{1,2}\.?\d*)', text)
                    if value_match:
                        rsi_value = float(value_match.group(1))
                        if 0 <= rsi_value <= 100:
                            return rsi_value
                            
        except Exception as e:
            print(f"⚠️ Could not read RSI value: {e}")
            
        return 50  # Default neutral RSI
    
    def read_macd_indicator(self):
        """Read MACD values (matching your Pine Script)"""
        macd_values = {}
        
        try:
            legend_items = self.driver.find_elements(By.CSS_SELECTOR, ".legend-source-item")
            
            for item in legend_items:
                text = item.text.lower()
                
                if 'macd' in text:
                    # Extract MACD line and signal line values
                    numbers = re.findall(r'([-]?[\d,]+\.?\d*)', text.replace(',', ''))
                    
                    if len(numbers) >= 2:
                        macd_values['macd'] = float(numbers[0])
                        macd_values['macd_signal'] = float(numbers[1])
                        
                        if len(numbers) >= 3:
                            macd_values['macd_histogram'] = float(numbers[2])
                            
        except Exception as e:
            print(f"⚠️ Could not read MACD values: {e}")
            
        return macd_values
    
    def read_bollinger_bands(self):
        """Read Bollinger Bands values (matching your Pine Script)"""
        bb_values = {}
        
        try:
            legend_items = self.driver.find_elements(By.CSS_SELECTOR, ".legend-source-item")
            
            for item in legend_items:
                text = item.text.lower()
                
                if 'bollinger' in text or 'bb' in text:
                    # Extract upper, middle, lower band values
                    numbers = re.findall(r'([\d,]+\.?\d*)', text.replace(',', ''))
                    
                    if len(numbers) >= 3:
                        bb_values['bb_upper'] = float(numbers[0])
                        bb_values['bb_middle'] = float(numbers[1]) 
                        bb_values['bb_lower'] = float(numbers[2])
                    elif len(numbers) >= 2:
                        # Sometimes only upper and lower are shown
                        bb_values['bb_upper'] = float(numbers[0])
                        bb_values['bb_lower'] = float(numbers[1])
                        
        except Exception as e:
            print(f"⚠️ Could not read Bollinger Bands: {e}")
            
        return bb_values
    
    def get_trading_session(self):
        """Determine current trading session (matching your Pine Script session filters)"""
        from datetime import datetime, timezone
        
        current_time = datetime.now(timezone.utc)
        hour = current_time.hour
        
        # London session: 8:00-17:00 UTC
        if 8 <= hour < 17:
            return "london"
        # New York session: 13:00-22:00 UTC (overlaps with London)
        elif 13 <= hour < 22:
            return "newyork" 
        # Tokyo session: 23:00-8:00 UTC (next day)
        elif hour >= 23 or hour < 8:
            return "tokyo"
        else:
            return "inactive"
    
    def validate_indicators(self, indicators):
        """Ensure we have minimum required indicators for Pine Script logic"""
        required = ['price']
        
        for req in required:
            if req not in indicators or indicators[req] is None:
                return False
                
        # Set defaults for missing indicators (using current price as base)
        current_price = indicators['price']
        
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
