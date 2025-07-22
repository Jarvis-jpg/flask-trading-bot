#!/usr/bin/env python3
"""
JARVIS Emergency Stop System
Immediately halts all trading activities and closes positions
"""
import os
import sys
import json
import logging
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmergencyStop:
    """Emergency shutdown system for trading bot"""
    
    def __init__(self):
        self.emergency_log = "logs/emergency_stop.log"
        self.ensure_log_directory()
        
    def ensure_log_directory(self):
        """Create logs directory if it doesn't exist"""
        os.makedirs("logs", exist_ok=True)
        
    def log_emergency(self, message):
        """Log emergency action with timestamp"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] EMERGENCY: {message}\n"
        
        with open(self.emergency_log, "a") as f:
            f.write(log_entry)
        
        logger.critical(message)
        
    def stop_flask_server(self):
        """Attempt to stop Flask server"""
        try:
            import requests
            response = requests.post("http://localhost:5000/emergency_stop", timeout=5)
            if response.status_code == 200:
                self.log_emergency("Flask server shutdown signal sent")
                return True
        except Exception as e:
            self.log_emergency(f"Failed to stop Flask server: {e}")
        return False
        
    def close_all_positions(self):
        """Close all open trading positions"""
        try:
            # Import OANDA client
            from oanda_client import OandaClient
            
            client = OandaClient()
            positions = client.get_open_positions()
            
            if positions:
                self.log_emergency(f"Found {len(positions)} open positions - closing all")
                for position in positions:
                    try:
                        client.close_position(position['instrument'])
                        self.log_emergency(f"Closed position: {position['instrument']}")
                    except Exception as e:
                        self.log_emergency(f"Failed to close {position['instrument']}: {e}")
            else:
                self.log_emergency("No open positions found")
                
        except Exception as e:
            self.log_emergency(f"Failed to access OANDA client: {e}")
            
    def stop_all_processes(self):
        """Stop all Python processes related to trading"""
        try:
            import psutil
            
            trading_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['cmdline']:
                        cmdline = ' '.join(proc.info['cmdline'])
                        if any(script in cmdline for script in [
                            'start_trading_bot.py',
                            'autonomous_trading_engine.py',
                            'app.py',
                            'train_and_trade.py'
                        ]):
                            trading_processes.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            if trading_processes:
                self.log_emergency(f"Terminating {len(trading_processes)} trading processes")
                for proc in trading_processes:
                    try:
                        proc.terminate()
                        self.log_emergency(f"Terminated process: {proc.info['name']} (PID: {proc.info['pid']})")
                    except Exception as e:
                        self.log_emergency(f"Failed to terminate process {proc.info['pid']}: {e}")
            else:
                self.log_emergency("No trading processes found running")
                
        except ImportError:
            self.log_emergency("psutil not available - cannot stop processes automatically")
        except Exception as e:
            self.log_emergency(f"Error stopping processes: {e}")
            
    def create_emergency_flag(self):
        """Create emergency stop flag file"""
        try:
            flag_data = {
                "emergency_stop": True,
                "timestamp": datetime.now().isoformat(),
                "reason": "Manual emergency stop activated",
                "operator": os.getenv("USERNAME", "unknown")
            }
            
            with open("EMERGENCY_STOP.flag", "w") as f:
                json.dump(flag_data, f, indent=2)
                
            self.log_emergency("Emergency stop flag created")
            
        except Exception as e:
            self.log_emergency(f"Failed to create emergency flag: {e}")
            
    def send_alerts(self):
        """Send emergency alerts via configured channels"""
        try:
            # Email alert
            self.send_email_alert()
            
            # Console alert
            print(f"\n{Style.BRIGHT}{Fore.RED}{'='*60}")
            print(f"{Fore.WHITE}🚨 EMERGENCY STOP ACTIVATED 🚨")
            print(f"{Fore.RED}All trading activities have been halted!")
            print(f"{Fore.WHITE}Timestamp: {datetime.now()}")
            print(f"{Fore.RED}{'='*60}{Style.RESET_ALL}\n")
            
        except Exception as e:
            self.log_emergency(f"Failed to send alerts: {e}")
            
    def send_email_alert(self):
        """Send emergency email notification"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            from dotenv import load_dotenv
            
            load_dotenv()
            
            smtp_server = os.getenv("SMTP_SERVER")
            smtp_port = int(os.getenv("SMTP_PORT", 587))
            email_user = os.getenv("EMAIL_USER")
            email_password = os.getenv("EMAIL_PASSWORD")
            alert_email = os.getenv("ALERT_EMAIL")
            
            if all([smtp_server, email_user, email_password, alert_email]):
                msg = MIMEMultipart()
                msg['From'] = email_user
                msg['To'] = alert_email
                msg['Subject'] = "🚨 JARVIS TRADING BOT - EMERGENCY STOP ACTIVATED"
                
                body = f"""
EMERGENCY STOP ACTIVATED!

Timestamp: {datetime.now()}
System: JARVIS AI Trading Bot
Action: All trading activities halted
Positions: Closed (if accessible)
Status: EMERGENCY SHUTDOWN

Please investigate immediately and restart manually when safe.

This is an automated alert from your JARVIS Trading System.
                """
                
                msg.attach(MIMEText(body, 'plain'))
                
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(email_user, email_password)
                text = msg.as_string()
                server.sendmail(email_user, alert_email, text)
                server.quit()
                
                self.log_emergency("Emergency email alert sent")
            else:
                self.log_emergency("Email configuration incomplete - skipping email alert")
                
        except Exception as e:
            self.log_emergency(f"Failed to send email alert: {e}")
            
    def execute_emergency_stop(self):
        """Execute complete emergency stop procedure"""
        print(f"\n{Style.BRIGHT}{Fore.RED}🚨 INITIATING EMERGENCY STOP SEQUENCE 🚨{Style.RESET_ALL}")
        
        self.log_emergency("=== EMERGENCY STOP SEQUENCE INITIATED ===")
        
        # Step 1: Create emergency flag
        print(f"{Fore.YELLOW}Step 1: Creating emergency stop flag...")
        self.create_emergency_flag()
        
        # Step 2: Stop Flask server
        print(f"{Fore.YELLOW}Step 2: Stopping Flask server...")
        self.stop_flask_server()
        
        # Step 3: Close all positions
        print(f"{Fore.YELLOW}Step 3: Closing all open positions...")
        self.close_all_positions()
        
        # Step 4: Stop all processes
        print(f"{Fore.YELLOW}Step 4: Stopping trading processes...")
        self.stop_all_processes()
        
        # Step 5: Send alerts
        print(f"{Fore.YELLOW}Step 5: Sending emergency alerts...")
        self.send_alerts()
        
        self.log_emergency("=== EMERGENCY STOP SEQUENCE COMPLETED ===")
        
        print(f"\n{Style.BRIGHT}{Fore.GREEN}✅ EMERGENCY STOP COMPLETED")
        print(f"{Fore.WHITE}Check logs/emergency_stop.log for details")
        print(f"{Fore.YELLOW}⚠️  Remove EMERGENCY_STOP.flag file to enable restart{Style.RESET_ALL}\n")

def main():
    """Main emergency stop execution"""
    try:
        print(f"\n{Style.BRIGHT}{Fore.RED}⚠️  JARVIS EMERGENCY STOP SYSTEM ⚠️{Style.RESET_ALL}")
        print(f"{Fore.WHITE}This will immediately halt ALL trading activities!")
        print(f"{Fore.RED}• Close all open positions")
        print(f"{Fore.RED}• Stop all trading processes")
        print(f"{Fore.RED}• Send emergency alerts")
        print(f"{Fore.RED}• Create emergency stop flag")
        
        response = input(f"\n{Fore.YELLOW}Are you sure you want to execute emergency stop? (type 'EMERGENCY' to confirm): {Style.RESET_ALL}")
        
        if response.upper() == "EMERGENCY":
            emergency_stop = EmergencyStop()
            emergency_stop.execute_emergency_stop()
        else:
            print(f"{Fore.GREEN}Emergency stop cancelled.{Style.RESET_ALL}")
            
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Emergency stop interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Emergency stop failed: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
