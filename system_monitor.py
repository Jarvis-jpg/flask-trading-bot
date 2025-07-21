import logging
import psutil
import asyncio
import numpy as np
from datetime import datetime, timedelta
from collections import deque
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class SystemMonitor:
    def __init__(self):
        self.metrics = {
            'cpu_usage': deque(maxlen=60),  # 1 minute of data
            'memory_usage': deque(maxlen=60),
            'network_latency': deque(maxlen=60),
            'order_latency': deque(maxlen=60),
            'price_feed_latency': deque(maxlen=60),
            'error_count': 0
        }
        
        # Thresholds
        self.cpu_threshold = 80  # 80% CPU usage
        self.memory_threshold = 85  # 85% memory usage
        self.network_latency_threshold = 500  # 500ms
        self.order_latency_threshold = 1000  # 1000ms
        self.price_feed_latency_threshold = 200  # 200ms
        self.error_threshold = 5  # errors per minute
        
        # State tracking
        self.last_alert_time = datetime.now()
        self.alert_cooldown = timedelta(minutes=5)
        self.is_healthy = True
        
    async def monitor_system_health(self):
        """Main monitoring loop"""
        while True:
            try:
                # System metrics
                self.metrics['cpu_usage'].append(psutil.cpu_percent())
                self.metrics['memory_usage'].append(psutil.virtual_memory().percent)
                
                # Calculate average metrics
                avg_cpu = np.mean(list(self.metrics['cpu_usage']))
                avg_memory = np.mean(list(self.metrics['memory_usage']))
                avg_network = np.mean(list(self.metrics['network_latency'])) if self.metrics['network_latency'] else 0
                avg_order = np.mean(list(self.metrics['order_latency'])) if self.metrics['order_latency'] else 0
                avg_price = np.mean(list(self.metrics['price_feed_latency'])) if self.metrics['price_feed_latency'] else 0
                
                # Check thresholds
                system_stress = False
                alerts = []
                
                if avg_cpu > self.cpu_threshold:
                    system_stress = True
                    alerts.append(f"High CPU usage: {avg_cpu:.1f}%")
                    
                if avg_memory > self.memory_threshold:
                    system_stress = True
                    alerts.append(f"High memory usage: {avg_memory:.1f}%")
                    
                if avg_network > self.network_latency_threshold:
                    system_stress = True
                    alerts.append(f"High network latency: {avg_network:.0f}ms")
                    
                if avg_order > self.order_latency_threshold:
                    system_stress = True
                    alerts.append(f"High order latency: {avg_order:.0f}ms")
                    
                if avg_price > self.price_feed_latency_threshold:
                    system_stress = True
                    alerts.append(f"High price feed latency: {avg_price:.0f}ms")
                    
                # Update system health status
                self.is_healthy = not system_stress
                
                # Send alerts if needed
                if system_stress and self._should_send_alert():
                    await self._send_alerts(alerts)
                    
                # Log metrics
                logger.debug(f"System Metrics - CPU: {avg_cpu:.1f}%, Memory: {avg_memory:.1f}%, " +
                           f"Network: {avg_network:.0f}ms, Orders: {avg_order:.0f}ms, " +
                           f"Price Feed: {avg_price:.0f}ms")
                    
            except Exception as e:
                logger.error(f"Monitoring error: {str(e)}")
                self.metrics['error_count'] += 1
                
            await asyncio.sleep(1)  # Check every second
            
    def record_latency(self, latency_type: str, value: float):
        """Record a latency measurement"""
        if latency_type in self.metrics:
            self.metrics[latency_type].append(value)
            
    def _should_send_alert(self) -> bool:
        """Check if we should send an alert based on cooldown"""
        now = datetime.now()
        if now - self.last_alert_time > self.alert_cooldown:
            self.last_alert_time = now
            return True
        return False
        
    async def _send_alerts(self, alerts: List[str]):
        """Send system alerts"""
        alert_msg = "⚠️ System Stress Detected:\n" + "\n".join(alerts)
        logger.warning(alert_msg)
        # Add your alert sending mechanism here (email, Slack, etc.)
        
    def get_system_health(self) -> Dict:
        """Get current system health metrics"""
        return {
            'is_healthy': self.is_healthy,
            'cpu_usage': np.mean(list(self.metrics['cpu_usage'])) if self.metrics['cpu_usage'] else 0,
            'memory_usage': np.mean(list(self.metrics['memory_usage'])) if self.metrics['memory_usage'] else 0,
            'network_latency': np.mean(list(self.metrics['network_latency'])) if self.metrics['network_latency'] else 0,
            'order_latency': np.mean(list(self.metrics['order_latency'])) if self.metrics['order_latency'] else 0,
            'price_feed_latency': np.mean(list(self.metrics['price_feed_latency'])) if self.metrics['price_feed_latency'] else 0,
            'error_count': self.metrics['error_count']
        }
