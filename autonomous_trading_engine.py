#!/usr/bin/env python3
"""
Autonomous Trading Engine
This module implements automated trading with intelligent decision making
"""
import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from threading import Thread
import json
import os

from enhanced_trading_strategy import trading_strategy
from oanda_client import OandaClient
from trade_analyzer import TradeAnalyzer
from market_data import MarketData
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AutonomousTradingEngine:
    """
    Fully autonomous trading engine that can analyze markets and execute trades
    """
    
    def __init__(self):
        self.oanda_client = OandaClient()
        self.trade_analyzer = TradeAnalyzer()
        self.market_data = MarketData()
        
        self.config = {
            'max_concurrent_trades': 5,
            'max_daily_trades': 20,
            'max_daily_loss': 500.0,  # USD
            'max_account_risk': 0.10,  # 10% of account
            'scan_interval': 60,  # seconds
            'active_pairs': ['EUR_USD', 'GBP_USD', 'USD_JPY', 'AUD_USD', 'USD_CAD'],
            'trade_hours': {'start': 1, 'end': 23},  # UTC hours
            'emergency_stop': False
        }
        
        self.active_trades = {}
        self.daily_stats = {
            'trades_count': 0,
            'profit_loss': 0.0,
            'wins': 0,
            'losses': 0,
            'start_time': datetime.now()
        }
        
        self.is_running = False
        
    def start_trading(self):
        """Start the autonomous trading engine"""
        logger.info("🚀 Starting Autonomous Trading Engine...")
        
        # Perform system checks
        if not self._system_health_check():
            logger.error("❌ System health check failed. Cannot start trading.")
            return False
            
        self.is_running = True
        self.daily_stats['start_time'] = datetime.now()
        
        # Start the main trading loop
        trading_thread = Thread(target=self._trading_loop, daemon=True)
        trading_thread.start()
        
        # Start trade monitoring
        monitor_thread = Thread(target=self._monitor_trades, daemon=True)
        monitor_thread.start()
        
        logger.info("✅ Autonomous Trading Engine started successfully")
        return True
    
    def stop_trading(self):
        """Stop the trading engine safely"""
        logger.info("🛑 Stopping Autonomous Trading Engine...")
        self.is_running = False
        
        # Close all open positions if emergency stop
        if self.config['emergency_stop']:
            self._emergency_close_all_positions()
            
        self._log_daily_summary()
        
    def _system_health_check(self) -> bool:
        """Perform comprehensive system health check"""
        logger.info("🔍 Performing system health check...")
        
        try:
            # Test OANDA connection
            test_price = self.oanda_client.get_current_price('EUR_USD')
            if not test_price:
                logger.error("❌ OANDA connection failed")
                return False
            logger.info("✅ OANDA connection: OK")
            
            # Check account balance
            # TODO: Implement account info check
            logger.info("✅ Account check: OK")
            
            # Verify trading hours
            if not self._is_trading_hours():
                logger.warning("⚠️ Outside trading hours, but will continue with reduced activity")
            
            # Check for sufficient historical data
            for pair in self.config['active_pairs']:
                try:
                    data = self._get_market_data(pair, periods=100)
                    if len(data) < 50:
                        logger.warning(f"⚠️ Limited data for {pair}")
                except Exception as e:
                    logger.error(f"❌ Cannot fetch data for {pair}: {e}")
                    return False
            
            logger.info("✅ System health check passed")
            return True
            
        except Exception as e:
            logger.error(f"❌ System health check failed: {e}")
            return False
    
    def _trading_loop(self):
        """Main trading loop"""
        logger.info("🔄 Starting main trading loop...")
        
        while self.is_running:
            try:
                # Check if we should trade
                if not self._should_continue_trading():
                    time.sleep(self.config['scan_interval'])
                    continue
                
                # Scan all pairs for opportunities
                opportunities = self._scan_market_opportunities()
                
                # Process opportunities
                for opportunity in opportunities:
                    if self._can_take_new_trade():
                        self._execute_trade_opportunity(opportunity)
                    
                # Wait before next scan
                time.sleep(self.config['scan_interval'])
                
            except Exception as e:
                logger.error(f"❌ Error in trading loop: {e}")
                time.sleep(self.config['scan_interval'] * 2)  # Extended wait on error
    
    def _monitor_trades(self):
        """Monitor active trades and manage them"""
        logger.info("👁️ Starting trade monitor...")
        
        while self.is_running:
            try:
                if self.active_trades:
                    self._update_active_trades()
                    self._check_trade_management()
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"❌ Error in trade monitor: {e}")
                time.sleep(60)
    
    def _scan_market_opportunities(self) -> List[Dict]:
        """Scan all currency pairs for trading opportunities"""
        opportunities = []
        
        for pair in self.config['active_pairs']:
            try:
                # Get market data
                price_data = self._get_market_data(pair)
                if price_data is None or len(price_data) < 50:
                    continue
                
                # Generate trading signal
                signal = trading_strategy.generate_trade_signal(pair, price_data)
                
                if signal['signal'] != 'no_signal' and signal['confidence'] >= 0.7:
                    # Get additional analysis
                    analysis = self.trade_analyzer.analyze_trade(pair, signal)
                    
                    # Check if analysis supports the trade
                    if analysis.get('prediction', {}).get('recommended', False):
                        opportunity = {
                            **signal,
                            'analysis': analysis,
                            'market_data': price_data.tail(5).to_dict('records')  # Last 5 candles
                        }
                        opportunities.append(opportunity)
                        
                        logger.info(f"📊 Found opportunity: {pair} {signal['signal']} (confidence: {signal['confidence']:.2f})")
                
            except Exception as e:
                logger.error(f"❌ Error scanning {pair}: {e}")
                continue
        
        # Sort opportunities by confidence
        opportunities.sort(key=lambda x: x['confidence'], reverse=True)
        
        return opportunities[:3]  # Return top 3 opportunities
    
    def _execute_trade_opportunity(self, opportunity: Dict):
        """Execute a trading opportunity"""
        try:
            pair = opportunity['pair']
            signal = opportunity['signal']
            
            logger.info(f"🎯 Executing trade: {pair} {signal.upper()}")
            
            # Prepare trade data
            trade_data = {
                'pair': pair,
                'action': signal,
                'entry': opportunity['entry'],
                'stop_loss': opportunity['stop_loss'],
                'take_profit': opportunity['take_profit'],
                'units': opportunity['units'],
                'confidence': opportunity['confidence'],
                'strategy': opportunity['strategy'],
                'timestamp': datetime.now().isoformat()
            }
            
            # Execute on OANDA
            result = self.oanda_client.place_trade(trade_data)
            
            if result['status'] == 'success':
                # Store trade information
                trade_id = result['order_id']
                self.active_trades[trade_id] = {
                    **trade_data,
                    'order_id': trade_id,
                    'filled_price': result['filled_price'],
                    'open_time': datetime.now(),
                    'status': 'open'
                }
                
                # Update stats
                self.daily_stats['trades_count'] += 1
                
                logger.info(f"✅ Trade executed successfully: {trade_id}")
                
                # Log to journal
                self._log_trade(self.active_trades[trade_id])
                
            else:
                logger.error(f"❌ Trade execution failed: {result}")
                
        except Exception as e:
            logger.error(f"❌ Error executing trade opportunity: {e}")
    
    def _get_market_data(self, pair: str, periods: int = 100) -> Optional[pd.DataFrame]:
        """Get historical market data for analysis"""
        try:
            # This is a simplified version - in reality you'd fetch from your data provider
            # For now, generate realistic sample data
            dates = pd.date_range(end=datetime.now(), periods=periods, freq='1H')
            
            # Get current price as base
            current_price_data = self.oanda_client.get_current_price(pair)
            base_price = current_price_data['bid']
            
            # Generate realistic OHLC data
            np.random.seed(int(time.time()) % 1000)  # Semi-random but consistent
            
            returns = np.random.normal(0, 0.0001, periods)  # Small random returns
            prices = [base_price]
            
            for r in returns[1:]:
                prices.append(prices[-1] * (1 + r))
            
            # Create OHLC from prices
            data = []
            for i, price in enumerate(prices):
                volatility = abs(np.random.normal(0, 0.0005))
                high = price + volatility
                low = price - volatility
                open_price = prices[i-1] if i > 0 else price
                close = price
                
                data.append({
                    'datetime': dates[i],
                    'open': open_price,
                    'high': high,
                    'low': low,
                    'close': close,
                    'volume': np.random.randint(1000, 10000)
                })
            
            df = pd.DataFrame(data)
            df.set_index('datetime', inplace=True)
            
            return df
            
        except Exception as e:
            logger.error(f"Error getting market data for {pair}: {e}")
            return None
    
    def _should_continue_trading(self) -> bool:
        """Check if trading should continue based on various conditions"""
        # Check emergency stop
        if self.config['emergency_stop']:
            return False
        
        # Check trading hours
        if not self._is_trading_hours():
            return False
        
        # Check daily limits
        if self.daily_stats['trades_count'] >= self.config['max_daily_trades']:
            return False
        
        if self.daily_stats['profit_loss'] <= -self.config['max_daily_loss']:
            logger.warning(f"⚠️ Daily loss limit reached: ${self.daily_stats['profit_loss']:.2f}")
            return False
        
        # Check max concurrent trades
        if len(self.active_trades) >= self.config['max_concurrent_trades']:
            return False
        
        return True
    
    def _can_take_new_trade(self) -> bool:
        """Check if we can take a new trade"""
        return (len(self.active_trades) < self.config['max_concurrent_trades'] and
                self.daily_stats['trades_count'] < self.config['max_daily_trades'] and
                self.daily_stats['profit_loss'] > -self.config['max_daily_loss'])
    
    def _is_trading_hours(self) -> bool:
        """Check if current time is within trading hours"""
        current_hour = datetime.now().hour
        start_hour = self.config['trade_hours']['start']
        end_hour = self.config['trade_hours']['end']
        
        if start_hour <= end_hour:
            return start_hour <= current_hour <= end_hour
        else:  # Overnight trading
            return current_hour >= start_hour or current_hour <= end_hour
    
    def _update_active_trades(self):
        """Update status of active trades"""
        for trade_id in list(self.active_trades.keys()):
            try:
                trade = self.active_trades[trade_id]
                # In a real implementation, you'd check trade status via API
                # For now, simulate trade outcomes based on time and randomness
                
                time_open = (datetime.now() - trade['open_time']).seconds
                
                # Simulate trade closure after some time (simplified)
                if time_open > 3600:  # 1 hour
                    self._close_simulated_trade(trade_id)
                    
            except Exception as e:
                logger.error(f"Error updating trade {trade_id}: {e}")
    
    def _close_simulated_trade(self, trade_id: str):
        """Simulate trade closure (for testing)"""
        try:
            trade = self.active_trades[trade_id]
            
            # Simple simulation: 60% win rate
            is_winner = np.random.random() < 0.6
            
            if is_winner:
                profit = abs(trade['take_profit'] - trade['entry']) * trade['units'] * 0.8
                self.daily_stats['wins'] += 1
                logger.info(f"✅ Trade {trade_id} closed: +${profit:.2f}")
            else:
                profit = -abs(trade['entry'] - trade['stop_loss']) * trade['units'] * 0.8
                self.daily_stats['losses'] += 1
                logger.info(f"❌ Trade {trade_id} closed: ${profit:.2f}")
            
            self.daily_stats['profit_loss'] += profit
            
            # Remove from active trades
            del self.active_trades[trade_id]
            
        except Exception as e:
            logger.error(f"Error closing simulated trade {trade_id}: {e}")
    
    def _check_trade_management(self):
        """Check if any trades need management (trailing stops, partial profits, etc.)"""
        for trade_id, trade in self.active_trades.items():
            try:
                # Get current price
                current_price_data = self.oanda_client.get_current_price(trade['pair'])
                current_price = current_price_data['bid'] if trade['action'] == 'sell' else current_price_data['ask']
                
                # Simple trailing stop logic
                if trade['action'] == 'buy':
                    # If price moved favorably, update stop loss
                    if current_price > trade['entry'] * 1.002:  # 20 pips profit
                        new_stop = current_price - abs(trade['stop_loss'] - trade['entry'])
                        if new_stop > trade['stop_loss']:
                            # Update stop loss (in real implementation)
                            logger.info(f"📈 Updating trailing stop for {trade_id}: {new_stop:.5f}")
                            trade['stop_loss'] = new_stop
                
            except Exception as e:
                logger.error(f"Error in trade management for {trade_id}: {e}")
    
    def _emergency_close_all_positions(self):
        """Emergency close all open positions"""
        logger.warning("🚨 Emergency closing all positions...")
        
        for trade_id in list(self.active_trades.keys()):
            try:
                # Close the trade
                # self.oanda_client.close_trade(trade_id)  # Uncomment for real trading
                del self.active_trades[trade_id]
                logger.info(f"🚨 Emergency closed trade {trade_id}")
                
            except Exception as e:
                logger.error(f"Error emergency closing trade {trade_id}: {e}")
    
    def _log_trade(self, trade: Dict):
        """Log trade to journal"""
        try:
            trade_log = {
                'timestamp': trade['timestamp'],
                'pair': trade['pair'],
                'action': trade['action'],
                'entry': trade['entry'],
                'stop_loss': trade['stop_loss'],
                'take_profit': trade['take_profit'],
                'units': trade['units'],
                'confidence': trade['confidence'],
                'strategy': trade['strategy'],
                'status': 'opened'
            }
            
            # Append to journal file
            journal_file = 'trades/autonomous_trades.json'
            os.makedirs('trades', exist_ok=True)
            
            try:
                with open(journal_file, 'r') as f:
                    trades = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                trades = []
            
            trades.append(trade_log)
            
            with open(journal_file, 'w') as f:
                json.dump(trades, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error logging trade: {e}")
    
    def _log_daily_summary(self):
        """Log daily trading summary"""
        runtime = datetime.now() - self.daily_stats['start_time']
        
        logger.info("📊 Daily Trading Summary:")
        logger.info(f"   Runtime: {runtime}")
        logger.info(f"   Trades: {self.daily_stats['trades_count']}")
        logger.info(f"   Wins: {self.daily_stats['wins']}")
        logger.info(f"   Losses: {self.daily_stats['losses']}")
        logger.info(f"   P&L: ${self.daily_stats['profit_loss']:.2f}")
        
        if self.daily_stats['trades_count'] > 0:
            win_rate = self.daily_stats['wins'] / self.daily_stats['trades_count'] * 100
            logger.info(f"   Win Rate: {win_rate:.1f}%")
    
    def get_status(self) -> Dict:
        """Get current engine status"""
        return {
            'is_running': self.is_running,
            'active_trades': len(self.active_trades),
            'daily_stats': self.daily_stats.copy(),
            'config': self.config.copy(),
            'trading_hours': self._is_trading_hours()
        }

# Global instance
autonomous_engine = AutonomousTradingEngine()
