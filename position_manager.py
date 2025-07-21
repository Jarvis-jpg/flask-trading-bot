import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from collections import deque

logger = logging.getLogger(__name__)

class PositionManager:
    def __init__(self, risk_manager):
        self.risk_manager = risk_manager
        self.positions = {}
        self.pending_orders = {}
        self.position_history = deque(maxlen=1000)
        self.emergency_close_attempts = 0
        self.max_retry_attempts = 3
        
    async def open_position(self, trade_params: Dict) -> Optional[Dict]:
        """Open a new position with safety checks"""
        try:
            # Validate position
            position_size = self.risk_manager.calculate_position_size(trade_params)
            if position_size <= 0:
                logger.warning("Position size too small")
                return None
                
            # Create position object
            position = {
                'id': self._generate_position_id(),
                'symbol': trade_params['pair'],
                'type': trade_params.get('type', 'market'),
                'direction': trade_params.get('direction', 'long'),
                'size': position_size,
                'entry_price': trade_params['entry'],
                'stop_loss': trade_params['stop_loss'],
                'take_profit': trade_params.get('take_profit'),
                'open_time': datetime.now(),
                'status': 'pending'
            }
            
            # Execute the order
            executed_position = await self._execute_order(position)
            if executed_position:
                self.positions[position['id']] = executed_position
                self.position_history.append(executed_position)
                logger.info(f"Position opened: {position['id']}")
                return executed_position
                
        except Exception as e:
            logger.error(f"Error opening position: {str(e)}")
            
        return None
        
    async def close_position(self, position_id: str, emergency: bool = False) -> bool:
        """Close a position"""
        try:
            if position_id not in self.positions:
                logger.warning(f"Position not found: {position_id}")
                return False
                
            position = self.positions[position_id]
            position['close_time'] = datetime.now()
            position['status'] = 'closing'
            
            # Execute close order
            success = await self._execute_close_order(position, emergency)
            if success:
                position['status'] = 'closed'
                self.position_history.append(position)
                del self.positions[position_id]
                logger.info(f"Position closed: {position_id}")
                return True
                
            position['status'] = 'open'  # Reset status if close failed
            return False
            
        except Exception as e:
            logger.error(f"Error closing position: {str(e)}")
            return False
            
    async def emergency_close_all(self) -> bool:
        """Emergency closure of all positions"""
        logger.warning("Emergency closing all positions...")
        success = True
        
        for position_id in list(self.positions.keys()):
            for attempt in range(self.max_retry_attempts):
                try:
                    if await self.close_position(position_id, emergency=True):
                        break
                except Exception as e:
                    logger.error(f"Emergency close attempt {attempt + 1} failed for {position_id}: {str(e)}")
                    if attempt == self.max_retry_attempts - 1:
                        success = False
                        
                await asyncio.sleep(1)  # Brief delay between attempts
                
        # Cancel all pending orders
        await self.cancel_all_pending()
        
        return success and not self.positions
        
    async def cancel_all_pending(self) -> bool:
        """Cancel all pending orders"""
        success = True
        for order_id in list(self.pending_orders.keys()):
            if not await self._cancel_order(order_id):
                success = False
        return success
        
    async def update_position(self, position_id: str, updates: Dict) -> bool:
        """Update position parameters (e.g., stop loss, take profit)"""
        if position_id not in self.positions:
            return False
            
        position = self.positions[position_id]
        
        # Validate updates
        if 'stop_loss' in updates:
            # Ensure new stop loss is valid
            if not self._validate_stop_loss(position, updates['stop_loss']):
                return False
                
        if 'take_profit' in updates:
            # Ensure new take profit is valid
            if not self._validate_take_profit(position, updates['take_profit']):
                return False
                
        # Apply updates
        position.update(updates)
        
        # Update order in the market
        success = await self._update_order(position)
        return success
        
    def get_position_metrics(self) -> Dict:
        """Get current position metrics"""
        return {
            'total_positions': len(self.positions),
            'pending_orders': len(self.pending_orders),
            'position_values': {
                pos_id: {
                    'symbol': pos['symbol'],
                    'size': pos['size'],
                    'direction': pos['direction'],
                    'entry_price': pos['entry_price'],
                    'current_price': pos.get('current_price', pos['entry_price']),
                    'unrealized_pl': pos.get('unrealized_pl', 0)
                }
                for pos_id, pos in self.positions.items()
            }
        }
        
    def _generate_position_id(self) -> str:
        """Generate a unique position ID"""
        return f"pos_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
    async def _execute_order(self, position: Dict) -> Optional[Dict]:
        """Execute a new order - implement broker-specific logic here"""
        # Placeholder for broker integration
        position['status'] = 'open'
        return position
        
    async def _execute_close_order(self, position: Dict, emergency: bool = False) -> bool:
        """Execute a close order - implement broker-specific logic here"""
        # Placeholder for broker integration
        return True
        
    async def _update_order(self, position: Dict) -> bool:
        """Update an existing order - implement broker-specific logic here"""
        # Placeholder for broker integration
        return True
        
    async def _cancel_order(self, order_id: str) -> bool:
        """Cancel a pending order - implement broker-specific logic here"""
        # Placeholder for broker integration
        if order_id in self.pending_orders:
            del self.pending_orders[order_id]
            return True
        return False
        
    def _validate_stop_loss(self, position: Dict, stop_loss: float) -> bool:
        """Validate new stop loss level"""
        if position['direction'] == 'long':
            return stop_loss < position['entry_price']
        else:
            return stop_loss > position['entry_price']
            
    def _validate_take_profit(self, position: Dict, take_profit: float) -> bool:
        """Validate new take profit level"""
        if position['direction'] == 'long':
            return take_profit > position['entry_price']
        else:
            return take_profit < position['entry_price']
