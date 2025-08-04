#!/usr/bin/env python3
"""
JARVIS Live Trading System
Autonomous live trading with AI decision making and comprehensive safety systems
"""

import time
import json
import logging
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import system components
try:
    from train_and_trade_100_sessions import ContinuousTrainingSystem
    from comprehensive_safety_system import TradingSafetyFramework
    from oanda_client import OandaClient
    from trade_analyzer import TradeAnalyzer
    AI_SYSTEM_AVAILABLE = True
except ImportError as e:
    logging.warning(f"AI system not available: {e}")
    AI_SYSTEM_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('live_trading.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LiveTradingSystem:
    """
    Autonomous live trading system with AI integration
    """
    
    def __init__(self):
        self.is_running = False
        self.trading_thread = None
        
        # Initialize core systems
        self.oanda = OandaClient()
        self.analyzer = TradeAnalyzer()
        self.safety = TradingSafetyFramework()
        
        # Initialize AI system if available
        self.ai_trader = None
        if AI_SYSTEM_AVAILABLE:
            try:
                self.ai_trader = ContinuousTrainingSystem()
                logger.info("✅ AI trading system initialized")
            except Exception as e:
                logger.warning(f"AI system initialization failed: {e}")
        
        # Trading configuration
        self.config = {
            'max_concurrent_trades': 3,
            'max_daily_trades': 10,
            'max_daily_loss': 50.0,  # $50 maximum daily loss
            'min_confidence': float(os.getenv('MIN_CONFIDENCE_THRESHOLD', '0.7')),
            'scan_interval': 30,  # seconds
            'active_pairs': [
                'EUR_USD', 'GBP_USD', 'USD_JPY', 'USD_CHF', 
                'AUD_USD', 'USD_CAD', 'NZD_USD', 'EUR_GBP'
            ],
            'trading_hours': {
                'start': 8,  # 8 AM
                'end': 17    # 5 PM
            }
        }
        
        # Daily statistics
        self.daily_stats = {
            'trades_count': 0,
            'wins': 0,
            'losses': 0,
            'profit_loss': 0.0,
            'last_reset': datetime.now().date()
        }
        
        # Active trades tracking
        self.active_trades = []
        
        logger.info("Live trading system initialized")
    
    def is_trading_hours(self) -> bool:
        """Check if currently within trading hours"""
        now = datetime.now()
        current_hour = now.hour
        weekday = now.weekday()  # 0 = Monday, 6 = Sunday
        
        # No trading on weekends
        if weekday >= 5:
            return False
        
        # Check trading hours
        return self.config['trading_hours']['start'] <= current_hour <= self.config['trading_hours']['end']
    
    def reset_daily_stats_if_needed(self):
        """Reset daily stats if it's a new day"""
        today = datetime.now().date()
        if today != self.daily_stats['last_reset']:
            self.daily_stats = {
                'trades_count': 0,
                'wins': 0,
                'losses': 0,
                'profit_loss': 0.0,
                'last_reset': today
            }
            self.safety.reset_daily_stats(200.0)  # Assuming $200 starting balance
            logger.info("Daily stats reset for new trading day")
    
    def can_place_new_trade(self) -> tuple[bool, str]:
        """Check if we can place a new trade based on safety limits"""
        
        # Check daily trade limit
        if self.daily_stats['trades_count'] >= self.config['max_daily_trades']:
            return False, "Daily trade limit reached"
        
        # Check concurrent trade limit
        if len(self.active_trades) >= self.config['max_concurrent_trades']:
            return False, "Maximum concurrent trades reached"
        
        # Check daily loss limit
        if abs(self.daily_stats['profit_loss']) >= self.config['max_daily_loss']:
            return False, "Daily loss limit reached"
        
        # Check trading hours
        if not self.is_trading_hours():
            return False, "Outside trading hours"
        
        return True, "Ready to trade"
    
    def generate_trade_signal(self, pair: str) -> Optional[Dict]:
        """Generate trade signal using AI system"""
        try:
            if not self.ai_trader:
                return None
            
            # Get current market data
            current_price = self.oanda.get_current_price(pair)
            if not current_price:
                return None
            
            # Generate AI trade signal
            trade = self.ai_trader.generate_realistic_trade()
            if not trade:
                return None
            
            # Ensure the trade is for the requested pair
            if trade.get('pair') != pair:
                return None
            
            # Apply safety validation
            trade_signal = {
                'pair': pair,
                'confidence': trade.get('confidence', 0.5),
                'risk_reward_ratio': trade.get('risk_reward_ratio', 2.0),
                'trend_strength': trade.get('trend_strength', 0.5),
                'risk_amount': 200.0 * 0.02,  # 2% risk per trade
            }
            
            is_safe, safety_message = self.safety.validate_trade_safety(trade_signal, 200.0)
            if not is_safe:
                logger.info(f"Trade rejected by safety system: {safety_message}")
                return None
            
            # Convert AI trade to executable format
            action = trade.get('action', 'BUY')
            entry_price = current_price['ask'] if action == 'BUY' else current_price['bid']
            
            # Calculate position size
            position_info = self.safety.calculate_safe_position_size(
                200.0, 50, pair  # $200 balance, 50 pip stop loss
            )
            
            executable_trade = {
                'pair': pair,
                'action': action.lower(),
                'entry': entry_price,
                'stop_loss': entry_price - 0.005 if action == 'BUY' else entry_price + 0.005,
                'take_profit': entry_price + 0.010 if action == 'BUY' else entry_price - 0.010,
                'units': int(position_info['position_size']),
                'confidence': trade.get('confidence', 0.7),
                'ai_prediction': trade.get('ai_win_probability', 0.6),
                'timestamp': datetime.now().isoformat()
            }
            
            return executable_trade
            
        except Exception as e:
            logger.error(f"Error generating trade signal for {pair}: {e}")
            return None
    
    def execute_trade(self, trade_data: Dict) -> bool:
        """Execute a trade on OANDA"""
        try:
            # Place the trade
            result = self.oanda.place_trade(trade_data)
            
            if result.get('success', False):
                # Add to active trades
                trade_record = {
                    'id': result.get('trade_id'),
                    'pair': trade_data['pair'],
                    'action': trade_data['action'],
                    'entry_price': result.get('filled_price', trade_data['entry']),
                    'units': trade_data['units'],
                    'timestamp': datetime.now(),
                    'confidence': trade_data.get('confidence', 0.7),
                    'ai_prediction': trade_data.get('ai_prediction', 0.6)
                }
                
                self.active_trades.append(trade_record)
                self.daily_stats['trades_count'] += 1
                
                logger.info(f"✅ Trade executed: {trade_data['pair']} {trade_data['action']} "
                           f"{trade_data['units']} units at {result.get('filled_price')}")
                
                return True
            else:
                logger.error(f"❌ Trade execution failed: {result.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            logger.error(f"Error executing trade: {e}")
            return False
    
    def update_active_trades(self):
        """Update status of active trades and handle closures"""
        try:
            trades_to_remove = []
            
            for i, trade in enumerate(self.active_trades):
                # Check if trade is still open
                trade_status = self.oanda.get_trade_status(trade['id'])
                
                if trade_status and trade_status.get('state') == 'CLOSED':
                    # Trade was closed, update statistics
                    profit = trade_status.get('profit', 0.0)
                    self.daily_stats['profit_loss'] += profit
                    
                    if profit > 0:
                        self.daily_stats['wins'] += 1
                        logger.info(f"✅ Trade closed with profit: {trade['pair']} +${profit:.2f}")
                    else:
                        self.daily_stats['losses'] += 1
                        logger.info(f"❌ Trade closed with loss: {trade['pair']} ${profit:.2f}")
                    
                    # Record trade outcome for safety system
                    self.safety.record_trade_outcome({
                        'outcome': 'win' if profit > 0 else 'loss',
                        'pnl': profit
                    })
                    
                    trades_to_remove.append(i)
            
            # Remove closed trades from active list
            for i in reversed(trades_to_remove):
                self.active_trades.pop(i)
                
        except Exception as e:
            logger.error(f"Error updating active trades: {e}")
    
    def trading_loop(self):
        """Main trading loop"""
        logger.info("🚀 Starting autonomous trading loop")
        
        while self.is_running:
            try:
                # Reset daily stats if needed
                self.reset_daily_stats_if_needed()
                
                # Update active trades
                self.update_active_trades()
                
                # Check if we can place new trades
                can_trade, reason = self.can_place_new_trade()
                
                if can_trade:
                    # Scan for trading opportunities
                    for pair in self.config['active_pairs']:
                        if len(self.active_trades) >= self.config['max_concurrent_trades']:
                            break
                        
                        # Generate trade signal
                        trade_signal = self.generate_trade_signal(pair)
                        
                        if trade_signal and trade_signal.get('confidence', 0) >= self.config['min_confidence']:
                            logger.info(f"🎯 Trade opportunity found: {pair} "
                                       f"(confidence: {trade_signal.get('confidence', 0):.2f})")
                            
                            # Execute the trade
                            if self.execute_trade(trade_signal):
                                # Wait a bit before looking for next trade
                                time.sleep(5)
                else:
                    if reason != "Outside trading hours":  # Don't spam log during off hours
                        logger.info(f"⏸️ Trading paused: {reason}")
                
                # Wait before next scan
                time.sleep(self.config['scan_interval'])
                
            except Exception as e:
                logger.error(f"Error in trading loop: {e}")
                time.sleep(60)  # Wait longer on error
        
        logger.info("🛑 Trading loop stopped")
    
    def start_trading(self) -> bool:
        """Start autonomous trading"""
        if self.is_running:
            logger.warning("Trading system is already running")
            return False
        
        try:
            # Verify OANDA connection
            account_info = self.oanda.get_account_info()
            if not account_info:
                logger.error("❌ Cannot connect to OANDA - trading not started")
                return False
            
            # Verify we're in live mode
            if not os.getenv('OANDA_LIVE', 'false').lower() == 'true':
                logger.error("❌ System not configured for live trading - check .env file")
                return False
            
            logger.info("✅ OANDA connection verified - LIVE TRADING MODE")
            logger.info(f"Account Balance: ${account_info.get('balance', 'Unknown')}")
            
            # Start trading thread
            self.is_running = True
            self.trading_thread = threading.Thread(target=self.trading_loop, daemon=True)
            self.trading_thread.start()
            
            logger.info("🚀 Autonomous trading started!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start trading: {e}")
            return False
    
    def stop_trading(self):
        """Stop autonomous trading"""
        if not self.is_running:
            logger.warning("Trading system is not running")
            return
        
        logger.info("🛑 Stopping autonomous trading...")
        self.is_running = False
        
        if self.trading_thread and self.trading_thread.is_alive():
            self.trading_thread.join(timeout=5)
        
        logger.info("✅ Autonomous trading stopped")
    
    def get_status(self) -> Dict:
        """Get current system status"""
        return {
            'is_running': self.is_running,
            'trading_hours': self.is_trading_hours(),
            'daily_stats': self.daily_stats.copy(),
            'active_trades': len(self.active_trades),
            'config': {
                'max_concurrent_trades': self.config['max_concurrent_trades'],
                'max_daily_trades': self.config['max_daily_trades'],
                'max_daily_loss': self.config['max_daily_loss'],
                'scan_interval': self.config['scan_interval'],
                'active_pairs': self.config['active_pairs']
            },
            'ai_system_available': AI_SYSTEM_AVAILABLE and self.ai_trader is not None
        }

# Global instance for Flask app integration
live_trading_system = LiveTradingSystem()

def main():
    """Main function for standalone execution"""
    try:
        print("🤖 JARVIS Live Trading System")
        print("=" * 40)
        
        # Start the trading system
        if live_trading_system.start_trading():
            print("✅ Trading system started successfully")
            print("Press Ctrl+C to stop...")
            
            try:
                # Keep the main thread alive
                while live_trading_system.is_running:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutdown requested...")
                live_trading_system.stop_trading()
        else:
            print("❌ Failed to start trading system")
            
    except Exception as e:
        logger.error(f"Main execution error: {e}")
    finally:
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
