#!/usr/bin/env python3
"""
JARVIS System Health Monitor
Continuously monitors system health and performance
"""
import os
import sys
import json
import time
import psutil
import logging
from datetime import datetime, timedelta
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class HealthMonitor:
    """Comprehensive system health monitoring"""
    
    def __init__(self):
        self.health_log = "logs/health_monitor.log"
        self.alerts_sent = {}
        self.monitoring = True
        self.ensure_directories()
        
        # Health thresholds
        self.thresholds = {
            'cpu_usage': 85.0,
            'memory_usage': 90.0,
            'disk_usage': 95.0,
            'response_time': 5.0,
            'error_rate': 10.0
        }
        
    def ensure_directories(self):
        """Create necessary directories"""
        os.makedirs("logs", exist_ok=True)
        
    def log_health(self, level, message):
        """Log health information"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        with open(self.health_log, "a") as f:
            f.write(log_entry)
            
    def check_system_resources(self):
        """Monitor system CPU, memory, and disk usage"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            health_data = {
                'timestamp': datetime.now().isoformat(),
                'cpu_usage': cpu_percent,
                'memory_usage': memory_percent,
                'disk_usage': disk_percent,
                'memory_available_mb': memory.available / (1024 * 1024),
                'disk_free_gb': disk.free / (1024 * 1024 * 1024)
            }
            
            # Check thresholds
            alerts = []
            if cpu_percent > self.thresholds['cpu_usage']:
                alerts.append(f"High CPU usage: {cpu_percent:.1f}%")
                
            if memory_percent > self.thresholds['memory_usage']:
                alerts.append(f"High memory usage: {memory_percent:.1f}%")
                
            if disk_percent > self.thresholds['disk_usage']:
                alerts.append(f"High disk usage: {disk_percent:.1f}%")
                
            return health_data, alerts
            
        except Exception as e:
            self.log_health("ERROR", f"Failed to check system resources: {e}")
            return None, []
            
    def check_trading_processes(self):
        """Monitor trading-related processes"""
        try:
            trading_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
                try:
                    if proc.info['name'] in ['python', 'python.exe']:
                        # Check if it's a trading process
                        cmdline = ' '.join(proc.cmdline())
                        if any(script in cmdline for script in [
                            'start_trading_bot.py',
                            'autonomous_trading_engine.py',
                            'app.py',
                            'train_and_trade.py'
                        ]):
                            proc_info = proc.info.copy()
                            proc_info['cmdline'] = cmdline
                            trading_processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            return trading_processes
            
        except Exception as e:
            self.log_health("ERROR", f"Failed to check trading processes: {e}")
            return []
            
    def check_flask_server(self):
        """Check if Flask server is responding"""
        try:
            import requests
            start_time = time.time()
            
            response = requests.get("http://localhost:5000/health", timeout=10)
            response_time = time.time() - start_time
            
            server_health = {
                'status': 'online' if response.status_code == 200 else 'error',
                'response_time': response_time,
                'status_code': response.status_code
            }
            
            alerts = []
            if response_time > self.thresholds['response_time']:
                alerts.append(f"Slow Flask response: {response_time:.2f}s")
                
            if response.status_code != 200:
                alerts.append(f"Flask server error: HTTP {response.status_code}")
                
            return server_health, alerts
            
        except requests.exceptions.ConnectionError:
            self.log_health("WARNING", "Flask server not responding")
            return {'status': 'offline', 'response_time': 0, 'status_code': 0}, ["Flask server offline"]
        except Exception as e:
            self.log_health("ERROR", f"Failed to check Flask server: {e}")
            return None, []
            
    def check_oanda_connection(self):
        """Check OANDA API connectivity"""
        try:
            from oanda_client import OandaClient
            
            client = OandaClient()
            start_time = time.time()
            
            # Try to get account summary
            account_info = client.get_account_summary()
            response_time = time.time() - start_time
            
            oanda_health = {
                'status': 'connected',
                'response_time': response_time,
                'account_balance': account_info.get('balance', 0)
            }
            
            alerts = []
            if response_time > self.thresholds['response_time']:
                alerts.append(f"Slow OANDA response: {response_time:.2f}s")
                
            return oanda_health, alerts
            
        except Exception as e:
            self.log_health("ERROR", f"OANDA connection failed: {e}")
            return {'status': 'disconnected', 'response_time': 0}, ["OANDA connection failed"]
            
    def check_log_files(self):
        """Monitor log files for errors"""
        try:
            log_files = [
                "logs/trading_system.log",
                "logs/error.log",
                "logs/performance.log"
            ]
            
            recent_errors = 0
            cutoff_time = datetime.now() - timedelta(minutes=30)
            
            for log_file in log_files:
                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                        for line in lines[-100:]:  # Check last 100 lines
                            if 'ERROR' in line or 'CRITICAL' in line:
                                try:
                                    # Extract timestamp and check if recent
                                    timestamp_str = line.split(']')[0][1:]
                                    log_time = datetime.fromisoformat(timestamp_str.replace(',', '.'))
                                    if log_time > cutoff_time:
                                        recent_errors += 1
                                except:
                                    continue
                                    
            log_health = {
                'recent_errors': recent_errors,
                'error_rate': recent_errors / 30  # errors per minute
            }
            
            alerts = []
            if log_health['error_rate'] > self.thresholds['error_rate']:
                alerts.append(f"High error rate: {recent_errors} errors in 30 minutes")
                
            return log_health, alerts
            
        except Exception as e:
            self.log_health("ERROR", f"Failed to check log files: {e}")
            return None, []
            
    def generate_health_report(self):
        """Generate comprehensive health report"""
        print(f"\n{Style.BRIGHT}{Fore.CYAN}🏥 JARVIS SYSTEM HEALTH REPORT{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}")
        print(f"{Fore.YELLOW}Timestamp: {datetime.now()}")
        
        all_alerts = []
        
        # System Resources
        print(f"\n{Fore.CYAN}💻 System Resources:")
        system_health, sys_alerts = self.check_system_resources()
        if system_health:
            print(f"   CPU Usage: {system_health['cpu_usage']:.1f}%")
            print(f"   Memory Usage: {system_health['memory_usage']:.1f}%")
            print(f"   Disk Usage: {system_health['disk_usage']:.1f}%")
            print(f"   Available Memory: {system_health['memory_available_mb']:.0f} MB")
            print(f"   Free Disk Space: {system_health['disk_free_gb']:.1f} GB")
        all_alerts.extend(sys_alerts)
        
        # Trading Processes
        print(f"\n{Fore.CYAN}🤖 Trading Processes:")
        processes = self.check_trading_processes()
        if processes:
            for proc in processes:
                print(f"   PID {proc['pid']}: {proc['status']} (CPU: {proc['cpu_percent']:.1f}%)")
        else:
            print(f"   {Fore.YELLOW}No trading processes detected")
            
        # Flask Server
        print(f"\n{Fore.CYAN}🌐 Flask Server:")
        flask_health, flask_alerts = self.check_flask_server()
        if flask_health:
            status_color = Fore.GREEN if flask_health['status'] == 'online' else Fore.RED
            print(f"   Status: {status_color}{flask_health['status']}")
            print(f"   Response Time: {flask_health['response_time']:.2f}s")
        all_alerts.extend(flask_alerts)
        
        # OANDA Connection
        print(f"\n{Fore.CYAN}🏦 OANDA Connection:")
        oanda_health, oanda_alerts = self.check_oanda_connection()
        if oanda_health:
            status_color = Fore.GREEN if oanda_health['status'] == 'connected' else Fore.RED
            print(f"   Status: {status_color}{oanda_health['status']}")
            print(f"   Response Time: {oanda_health['response_time']:.2f}s")
            if 'account_balance' in oanda_health:
                print(f"   Account Balance: ${oanda_health['account_balance']:.2f}")
        all_alerts.extend(oanda_alerts)
        
        # Log Analysis
        print(f"\n{Fore.CYAN}📋 Log Analysis:")
        log_health, log_alerts = self.check_log_files()
        if log_health:
            error_color = Fore.GREEN if log_health['recent_errors'] == 0 else Fore.YELLOW if log_health['recent_errors'] < 5 else Fore.RED
            print(f"   Recent Errors (30min): {error_color}{log_health['recent_errors']}")
            print(f"   Error Rate: {log_health['error_rate']:.2f} errors/min")
        all_alerts.extend(log_alerts)
        
        # Overall Status
        print(f"\n{Fore.CYAN}🎯 Overall Status:")
        if all_alerts:
            print(f"   {Fore.RED}⚠️  {len(all_alerts)} alerts detected:")
            for alert in all_alerts:
                print(f"      • {alert}")
        else:
            print(f"   {Fore.GREEN}✅ All systems healthy")
            
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")
        
        return len(all_alerts) == 0
        
    def start_monitoring(self, interval=300):
        """Start continuous monitoring"""
        print(f"{Style.BRIGHT}{Fore.GREEN}🚀 Starting JARVIS Health Monitor...")
        print(f"{Fore.WHITE}Monitoring interval: {interval} seconds")
        print(f"{Fore.YELLOW}Press Ctrl+C to stop{Style.RESET_ALL}\n")
        
        try:
            while self.monitoring:
                is_healthy = self.generate_health_report()
                
                if not is_healthy:
                    self.log_health("WARNING", "System health issues detected")
                    
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Health monitoring stopped by user{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}Health monitoring error: {e}{Style.RESET_ALL}")

def main():
    """Main health monitor execution"""
    monitor = HealthMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
        monitor.start_monitoring(interval)
    else:
        monitor.generate_health_report()

if __name__ == "__main__":
    main()
