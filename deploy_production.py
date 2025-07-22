#!/usr/bin/env python3
"""
JARVIS Production Deployment Script
Comprehensive system setup and validation for live trading
"""
import os
import sys
import json
import shutil
import logging
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Fix encoding for Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

class ProductionDeployment:
    """Production deployment and setup manager"""
    
    def __init__(self):
        self.deployment_log = "logs/deployment.log"
        self.ensure_directories()
        
    def ensure_directories(self):
        """Create all necessary directories"""
        directories = [
            "logs", "models", "trades", "data", "backups",
            "ai", "strategies", "templates", "journal",
            "docs", "utils", "tests", "scripts"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            
    def log_deployment(self, level, message):
        """Log deployment information"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        with open(self.deployment_log, "a") as f:
            f.write(log_entry)
            
        print(f"{Fore.WHITE}[{timestamp}] {message}")
        
    def check_python_environment(self):
        """Verify Python environment and dependencies"""
        print(f"\n{Fore.CYAN}Python Environment Check...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version < (3, 8):
            self.log_deployment("ERROR", f"Python {python_version.major}.{python_version.minor} detected. Minimum required: 3.8")
            return False
        else:
            self.log_deployment("INFO", f"Python {python_version.major}.{python_version.minor}.{python_version.micro} OK")
            
        # Check critical packages
        package_imports = {
            'flask': 'flask',
            'pandas': 'pandas', 
            'numpy': 'numpy',
            'scikit-learn': 'sklearn',
            'oandapyV20': 'oandapyV20',
            'colorama': 'colorama',
            'python-dotenv': 'dotenv'
        }
        
        missing_packages = []
        for package, import_name in package_imports.items():
            try:
                __import__(import_name)
                self.log_deployment("INFO", f"Package {package} OK")
            except ImportError:
                missing_packages.append(package)
                self.log_deployment("ERROR", f"Package {package} MISSING")
                
        if missing_packages:
            self.log_deployment("ERROR", f"Missing packages: {', '.join(missing_packages)}")
            print(f"{Fore.RED}Run: pip install {' '.join(missing_packages)}")
            return False
            
        return True
        
    def setup_environment_file(self):
        """Set up environment configuration"""
        print(f"\n{Fore.CYAN}Environment Configuration Setup...")
        
        if os.path.exists(".env"):
            self.log_deployment("INFO", "Environment file already exists")
            print(f"{Fore.GREEN}Environment Setup Complete")
            return True
            
        if os.path.exists(".env.template"):
            # Copy template to .env
            shutil.copy(".env.template", ".env")
            self.log_deployment("INFO", "Created .env from template")
            
            print(f"{Fore.YELLOW}IMPORTANT: Edit .env file with your actual credentials!")
            print(f"{Fore.WHITE}Required settings:")
            print(f"   • OANDA_API_KEY")
            print(f"   • OANDA_ACCOUNT_ID")
            print(f"   • FLASK_SECRET_KEY")
            print(f"   • API_SECRET_KEY")
            
            return False  # Needs manual configuration
        else:
            self.log_deployment("ERROR", "No .env.template found")
            return False
            
    def validate_configuration(self):
        """Validate system configuration"""
        print(f"\n{Fore.CYAN}Configuration Validation...")
        
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            required_env = [
                'OANDA_API_KEY',
                'OANDA_ACCOUNT_ID',
                'FLASK_SECRET_KEY'
            ]
            
            missing_env = []
            for env_var in required_env:
                if not os.getenv(env_var) or os.getenv(env_var) == f"your_{env_var.lower()}_here":
                    missing_env.append(env_var)
                    
            if missing_env:
                self.log_deployment("ERROR", f"Missing environment variables: {', '.join(missing_env)}")
                return False
            else:
                self.log_deployment("INFO", "Environment configuration validated")
                print(f"{Fore.GREEN}Configuration Validation Complete")
                return True
                
        except Exception as e:
            self.log_deployment("ERROR", f"Configuration validation failed: {e}")
            return False
            
    def test_oanda_connection(self):
        """Test OANDA API connection"""
        print(f"\n{Fore.CYAN}OANDA Connection Test...")
        
        try:
            from oanda_client import OandaClient
            
            client = OandaClient()
            # Fix the method call - use get_account_details instead
            account_info = client.get_account_details()
            
            self.log_deployment("INFO", f"OANDA connection successful")
            self.log_deployment("INFO", f"Account Balance: ${account_info.get('balance', 0):.2f}")
            print(f"{Fore.GREEN}OANDA Connection Complete")
            return True
            
        except Exception as e:
            self.log_deployment("ERROR", f"OANDA connection failed: {e}")
            return False
            
    def setup_security(self):
        """Configure security settings"""
        print(f"\n{Fore.CYAN}Security Setup...")
        
        try:
            # Create security configuration
            security_config = {
                "rate_limiting": True,
                "webhook_authentication": True,
                "admin_authentication": True,
                "ssl_required": False,  # Set to True for production
                "ip_whitelist": [],     # Add your IPs
                "max_login_attempts": 3,
                "session_timeout": 3600
            }
            
            with open("security_config.json", "w") as f:
                json.dump(security_config, f, indent=2)
                
            self.log_deployment("INFO", "Security configuration created")
            print(f"{Fore.GREEN}Security Setup Complete")
            return True
        except Exception as e:
            self.log_deployment("ERROR", f"Security setup failed: {e}")
            return False
        
    def create_startup_script(self):
        """Create system startup script"""
        print(f"\n{Fore.CYAN}Creating Startup Scripts...")
        
    def create_startup_script(self):
        """Create system startup script"""
        print(f"\n{Fore.CYAN}Creating Startup Scripts...")
        
        try:
            startup_script = """#!/bin/bash
# JARVIS Trading System Startup Script

echo "Starting JARVIS AI Trading System..."

# Check if emergency stop flag exists
if [ -f "EMERGENCY_STOP.flag" ]; then
    echo "Emergency stop flag detected! Remove flag file to start."
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Virtual environment activated"
fi

# Run system validation
echo "Running system validation..."
python validate_system.py
if [ $? -ne 0 ]; then
    echo "System validation failed!"
    exit 1
fi

# Start health monitor in background
echo "Starting health monitor..."
python health_monitor.py --continuous 300 &
HEALTH_MONITOR_PID=$!
echo $HEALTH_MONITOR_PID > health_monitor.pid

# Start trading system
echo "Starting trading system..."
python start_trading_bot.py

# Cleanup on exit
kill $HEALTH_MONITOR_PID 2>/dev/null
rm -f health_monitor.pid

echo "JARVIS Trading System stopped"
"""
            
            with open("start_jarvis.sh", "w") as f:
                f.write(startup_script)
                
            # Make executable on Unix systems
            try:
                os.chmod("start_jarvis.sh", 0o755)
            except:
                pass
                
            # Create Windows batch file
            windows_script = """@echo off
REM JARVIS Trading System Startup Script for Windows

echo Starting JARVIS AI Trading System...

REM Check if emergency stop flag exists
if exist "EMERGENCY_STOP.flag" (
    echo Emergency stop flag detected! Remove flag file to start.
    pause
    exit /b 1
)

REM Activate virtual environment if it exists
if exist "venv\\Scripts\\activate.bat" (
    call venv\\Scripts\\activate.bat
    echo Virtual environment activated
)

REM Run system validation
echo Running system validation...
python validate_system.py
if %errorlevel% neq 0 (
    echo System validation failed!
    pause
    exit /b 1
)

REM Start health monitor in background
echo Starting health monitor...
start /b python health_monitor.py --continuous 300

REM Start trading system
echo Starting trading system...
python start_trading_bot.py

echo JARVIS Trading System stopped
pause
"""
            
            with open("start_jarvis.bat", "w") as f:
                f.write(windows_script)
                
            self.log_deployment("INFO", "Startup scripts created")
            print(f"{Fore.GREEN}Startup Scripts Complete")
            return True
            
        except Exception as e:
            self.log_deployment("ERROR", f"Startup script creation failed: {e}")
            return False
        
    def create_backup_schedule(self):
        """Set up automated backup schedule"""
        print(f"\n{Fore.CYAN}Backup Schedule Setup...")
        
        try:
            # Create backup configuration
            backup_config = {
                "enabled": True,
                "frequency_hours": 24,
                "retention_days": 30,
                "backup_location": "backups/",
                "include_files": [
                    "*.py", "*.json", "*.log", "*.pine",
                    ".env", "requirements.txt"
                ],
                "exclude_patterns": [
                    "__pycache__/", "*.pyc", "temp/", "logs/debug.log"
                ]
            }
            
            with open("backup_config.json", "w") as f:
                json.dump(backup_config, f, indent=2)
                
            self.log_deployment("INFO", "Backup configuration created")
            print(f"{Fore.GREEN}Backup Schedule Complete")
            return True
            
        except Exception as e:
            self.log_deployment("ERROR", f"Backup setup failed: {e}")
            return False
        
    def run_deployment(self):
        """Execute complete deployment process"""
        print(f"\n{Style.BRIGHT}{Fore.GREEN}JARVIS PRODUCTION DEPLOYMENT{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}")
        
        deployment_steps = [
            ("Python Environment", self.check_python_environment),
            ("Environment Setup", self.setup_environment_file),
            ("Configuration Validation", self.validate_configuration),
            ("OANDA Connection", self.test_oanda_connection),
            ("Security Setup", self.setup_security),
            ("Startup Scripts", self.create_startup_script),
            ("Backup Schedule", self.create_backup_schedule)
        ]
        
        failed_steps = []
        
        for step_name, step_func in deployment_steps:
            try:
                if step_func():
                    print(f"{Fore.GREEN}OK {step_name}")
                else:
                    print(f"{Fore.RED}FAILED {step_name}")
                    failed_steps.append(step_name)
            except Exception as e:
                print(f"{Fore.RED}ERROR {step_name}: {e}")
                failed_steps.append(step_name)
                
        print(f"\n{Fore.WHITE}{'='*60}")
        
        if failed_steps:
            print(f"{Fore.RED}Deployment completed with {len(failed_steps)} failures:")
            for step in failed_steps:
                print(f"   • {step}")
            print(f"\n{Fore.YELLOW}Fix the issues above before going live!")
        else:
            print(f"{Fore.GREEN}Deployment completed successfully!")
            print(f"\n{Fore.CYAN}Next Steps:")
            print(f"   1. Review and edit .env file with your credentials")
            print(f"   2. Run: python validate_system.py")
            print(f"   3. Test with: python train_and_trade.py")
            print(f"   4. Go live with: ./start_jarvis.sh (Linux/Mac) or start_jarvis.bat (Windows)")
            
        print(f"{Style.RESET_ALL}")

def main():
    """Main deployment execution"""
    deployment = ProductionDeployment()
    deployment.run_deployment()

if __name__ == "__main__":
    main()
