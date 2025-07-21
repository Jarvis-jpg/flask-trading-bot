import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from collections import deque

logger = logging.getLogger(__name__)

class TradingFailsafe:
    def __init__(self, risk_manager, position_manager, system_monitor):
        self.risk_manager = risk_manager
        self.position_manager = position_manager
        self.system_monitor = system_monitor
        
        self.shutdown_triggers = {
            'max_daily_loss': False,
            'max_drawdown': False,
            'system_error': False,
            'network_issue': False,
            'api_error': False
        }
        
        # Thresholds
        self.max_daily_loss_percent = 0.05  # 5% max daily loss
        self.max_drawdown_percent = 0.15    # 15% max drawdown
        self.system_error_threshold = 5      # errors per minute
        self.network_latency_threshold = 1000  # 1 second
        self.consecutive_api_errors = 3      # maximum consecutive API errors
        
        # State tracking
        self.api_error_count = 0
        self.last_check_time = datetime.now()
        self.is_shutdown = False
        self.error_log = deque(maxlen=100)
        
    async def monitor_trading_conditions(self):
        """Main monitoring loop"""
        while not self.is_shutdown:
            try:
                await self.check_failsafe_conditions()
                await asyncio.sleep(1)  # Check every second
            except Exception as e:
                logger.error(f"Failsafe monitoring error: {str(e)}")
                self.error_log.append({
                    'timestamp': datetime.now(),
                    'error': str(e)
                })
                
    async def check_failsafe_conditions(self):
        """Check all failsafe conditions"""
        # Get current metrics
        risk_metrics = self.risk_manager.get_risk_metrics()
        system_health = self.system_monitor.get_system_health()
        
        # Check daily loss
        if abs(risk_metrics['daily_pl']) > self.risk_manager.initial_balance * self.max_daily_loss_percent:
            self.shutdown_triggers['max_daily_loss'] = True
            
        # Check drawdown
        if risk_metrics['total_drawdown'] > self.max_drawdown_percent:
            self.shutdown_triggers['max_drawdown'] = True
            
        # Check system health
        if system_health['error_count'] > self.system_error_threshold:
            self.shutdown_triggers['system_error'] = True
            
        # Check network health
        if system_health['network_latency'] > self.network_latency_threshold:
            self.shutdown_triggers['network_issue'] = True
            
        # Check API health
        if self.api_error_count >= self.consecutive_api_errors:
            self.shutdown_triggers['api_error'] = True
            
        # Check if any shutdown conditions are met
        if any(self.shutdown_triggers.values()):
            await self.initiate_emergency_shutdown()
            
    async def initiate_emergency_shutdown(self):
        """Emergency shutdown procedure"""
        if self.is_shutdown:
            return  # Prevent multiple shutdowns
            
        try:
            logger.critical("🚨 EMERGENCY SHUTDOWN INITIATED")
            self.is_shutdown = True
            
            # Log shutdown reason
            reasons = [key for key, value in self.shutdown_triggers.items() if value]
            logger.critical(f"Shutdown triggered by: {', '.join(reasons)}")
            
            # 1. Stop accepting new trades
            logger.info("Stopping new trades...")
            
            # 2. Close all positions
            logger.info("Closing all open positions...")
            await self.position_manager.emergency_close_all()
            
            # 3. Cancel all pending orders
            logger.info("Cancelling pending orders...")
            await self.position_manager.cancel_all_pending()
            
            # 4. Save system state
            logger.info("Saving system state...")
            await self.save_emergency_state()
            
            # 5. Send notifications
            await self.notify_administrators()
            
            logger.critical("Emergency shutdown completed")
            
        except Exception as e:
            logger.critical(f"Emergency shutdown error: {str(e)}")
            # Even if there's an error, we want to maintain shutdown state
            self.is_shutdown = True
            
    async def save_emergency_state(self):
        """Save system state during emergency shutdown"""
        state = {
            'timestamp': datetime.now().isoformat(),
            'triggers': self.shutdown_triggers,
            'risk_metrics': self.risk_manager.get_risk_metrics(),
            'system_health': self.system_monitor.get_system_health(),
            'error_log': list(self.error_log)
        }
        
        # Save to file
        try:
            import json
            from pathlib import Path
            
            # Create emergency folder if it doesn't exist
            emergency_dir = Path('data/emergency')
            emergency_dir.mkdir(parents=True, exist_ok=True)
            
            # Save state
            filename = f"emergency_state_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(emergency_dir / filename, 'w') as f:
                json.dump(state, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save emergency state: {str(e)}")
            
    async def notify_administrators(self):
        """Send notifications about the emergency shutdown"""
        message = (
            "🚨 EMERGENCY TRADING SHUTDOWN 🚨\n"
            f"Time: {datetime.now().isoformat()}\n"
            f"Triggers: {[k for k, v in self.shutdown_triggers.items() if v]}\n"
            f"Open Positions: {len(self.position_manager.open_positions)}\n"
            f"Daily P/L: {self.risk_manager.daily_pl:.2f}\n"
            f"Error Count: {self.system_monitor.metrics['error_count']}"
        )
        
        logger.critical(message)
        # Add your notification mechanism here (email, Slack, etc.)
        
    def record_api_error(self):
        """Record an API error"""
        self.api_error_count += 1
        
    def reset_api_error_count(self):
        """Reset API error count after successful operation"""
        self.api_error_count = 0
        
    def get_status(self) -> Dict:
        """Get current failsafe status"""
        return {
            'is_shutdown': self.is_shutdown,
            'triggers': self.shutdown_triggers,
            'api_error_count': self.api_error_count,
            'last_check': self.last_check_time.isoformat()
        }
