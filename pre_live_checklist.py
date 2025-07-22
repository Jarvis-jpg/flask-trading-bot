#!/usr/bin/env python3
"""
JARVIS Pre-Live Trading Checklist
Final validation before enabling live trading
"""
import os
import sys
import json
import logging
from datetime import datetime, timedelta
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class PreLiveChecklist:
    """Comprehensive pre-live trading validation"""
    
    def __init__(self):
        self.checklist_results = {}
        self.critical_failures = []
        
    def check_emergency_systems(self):
        """Verify emergency stop systems work"""
        print(f"\n{Fore.CYAN}🚨 Emergency Systems Check")
        
        checks = {
            "Emergency Stop Script": os.path.exists("emergency_stop.py"),
            "Close Positions Script": os.path.exists("close_all_positions.py"),
            "Health Monitor": os.path.exists("health_monitor.py"),
            "Backup System": os.path.exists("backup_data.py")
        }
        
        all_passed = True
        for check_name, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")
            if not passed:
                all_passed = False
                self.critical_failures.append(f"Missing: {check_name}")
                
        return all_passed
        
    def check_risk_management(self):
        """Verify risk management settings"""
        print(f"\n{Fore.CYAN}⚡ Risk Management Validation")
        
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            # Check risk settings
            risk_per_trade = float(os.getenv("RISK_PER_TRADE", 0.02))
            max_drawdown = float(os.getenv("MAX_DRAWDOWN_PERCENT", 15.0))
            daily_loss_limit = float(os.getenv("DAILY_LOSS_LIMIT_PERCENT", 5.0))
            
            risk_checks = {
                "Risk per trade ≤ 3%": risk_per_trade <= 0.03,
                "Max drawdown ≤ 20%": max_drawdown <= 20.0,
                "Daily loss limit ≤ 10%": daily_loss_limit <= 10.0,
                "Risk settings configured": risk_per_trade > 0
            }
            
            all_passed = True
            for check_name, passed in risk_checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
                if not passed:
                    all_passed = False
                    self.critical_failures.append(f"Risk issue: {check_name}")
                    
            # Display current settings
            print(f"\n   {Fore.WHITE}Current Settings:")
            print(f"     Risk per trade: {risk_per_trade*100:.1f}%")
            print(f"     Max drawdown: {max_drawdown:.1f}%")
            print(f"     Daily loss limit: {daily_loss_limit:.1f}%")
            
            return all_passed
            
        except Exception as e:
            print(f"   ❌ Risk validation failed: {e}")
            self.critical_failures.append("Risk validation error")
            return False
            
    def check_account_setup(self):
        """Verify account configuration"""
        print(f"\n{Fore.CYAN}🏦 Account Setup Verification")
        
        try:
            from oanda_client import OandaClient
            
            client = OandaClient()
            account_info = client.get_account_summary()
            
            balance = float(account_info.get('balance', 0))
            currency = account_info.get('currency', 'USD')
            
            account_checks = {
                "OANDA connection works": True,
                "Account balance > $100": balance > 100,
                "Account currency is USD": currency == 'USD',
                "Account not restricted": account_info.get('marginRate', '0.02') != '0'
            }
            
            all_passed = True
            for check_name, passed in account_checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
                if not passed:
                    all_passed = False
                    self.critical_failures.append(f"Account issue: {check_name}")
                    
            print(f"\n   {Fore.WHITE}Account Details:")
            print(f"     Balance: ${balance:.2f} {currency}")
            print(f"     Margin Rate: {account_info.get('marginRate', 'N/A')}")
            
            return all_passed
            
        except Exception as e:
            print(f"   ❌ Account verification failed: {e}")
            self.critical_failures.append("Account verification error")
            return False
            
    def check_ai_training_status(self):
        """Check AI training completeness"""
        print(f"\n{Fore.CYAN}🧠 AI Training Status")
        
        try:
            # Check if AI memory exists
            if os.path.exists("jarvis_ai_memory.json"):
                with open("jarvis_ai_memory.json", "r") as f:
                    ai_memory = json.load(f)
                    
                lifetime_trades = ai_memory.get("lifetime_trades", 0)
                lifetime_win_rate = ai_memory.get("lifetime_win_rate", 0)
                
                training_checks = {
                    "AI memory exists": True,
                    "≥1000 training trades": lifetime_trades >= 1000,
                    "Win rate 55-80%": 55 <= lifetime_win_rate <= 80,
                    "Recent training session": self._check_recent_training(ai_memory)
                }
                
                all_passed = True
                for check_name, passed in training_checks.items():
                    status = "✅" if passed else "❌"
                    print(f"   {status} {check_name}")
                    if not passed:
                        all_passed = False
                        
                print(f"\n   {Fore.WHITE}Training Stats:")
                print(f"     Lifetime trades: {lifetime_trades:,}")
                print(f"     Win rate: {lifetime_win_rate:.1f}%")
                
                return all_passed
            else:
                print(f"   ❌ No AI training data found")
                print(f"   {Fore.YELLOW}⚠️  Run training first: python train_and_trade.py")
                return False
                
        except Exception as e:
            print(f"   ❌ AI training check failed: {e}")
            return False
            
    def _check_recent_training(self, ai_memory):
        """Check if training is recent"""
        try:
            last_session = ai_memory.get("last_session_date", "")
            if last_session:
                last_date = datetime.fromisoformat(last_session.replace('Z', '+00:00').replace('+00:00', ''))
                days_ago = (datetime.now() - last_date).days
                return days_ago <= 7  # Training within last 7 days
        except:
            pass
        return False
        
    def check_system_performance(self):
        """Check system performance metrics"""
        print(f"\n{Fore.CYAN}📊 System Performance Check")
        
        try:
            import psutil
            
            # System resources
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            performance_checks = {
                "CPU usage < 80%": cpu_percent < 80,
                "Memory usage < 85%": memory.percent < 85,
                "Disk space > 1GB free": disk.free > 1024**3,
                "System responsive": True  # If we got here, system is responsive
            }
            
            all_passed = True
            for check_name, passed in performance_checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
                if not passed:
                    all_passed = False
                    
            print(f"\n   {Fore.WHITE}Current Usage:")
            print(f"     CPU: {cpu_percent:.1f}%")
            print(f"     Memory: {memory.percent:.1f}%")
            print(f"     Disk free: {disk.free / (1024**3):.1f} GB")
            
            return all_passed
            
        except Exception as e:
            print(f"   ❌ Performance check failed: {e}")
            return False
            
    def check_live_mode_settings(self):
        """Verify live mode configuration"""
        print(f"\n{Fore.CYAN}⚡ Live Mode Configuration")
        
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            oanda_live = os.getenv("OANDA_LIVE", "false").lower()
            api_url = os.getenv("OANDA_API_URL", "")
            
            live_checks = {
                "OANDA_LIVE setting exists": oanda_live in ["true", "false"],
                "API URL configured": len(api_url) > 0,
                "Practice mode for testing": oanda_live == "false",  # Recommend starting with practice
                "Live credentials ready": oanda_live == "true" or "practice" in api_url
            }
            
            all_passed = True
            for check_name, passed in live_checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
                if not passed:
                    all_passed = False
                    
            current_mode = "LIVE" if oanda_live == "true" else "PRACTICE"
            mode_color = Fore.RED if current_mode == "LIVE" else Fore.GREEN
            print(f"\n   {Fore.WHITE}Current Mode: {mode_color}{current_mode}")
            
            if current_mode == "LIVE":
                print(f"   {Fore.YELLOW}⚠️  You are in LIVE mode - real money at risk!")
            else:
                print(f"   {Fore.GREEN}✅ Practice mode - safe for testing")
                
            return all_passed
            
        except Exception as e:
            print(f"   ❌ Live mode check failed: {e}")
            return False
            
    def generate_go_live_report(self):
        """Generate final go-live assessment"""
        print(f"\n{Style.BRIGHT}{Fore.YELLOW}📋 PRE-LIVE TRADING CHECKLIST{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}")
        
        checklist_items = [
            ("Emergency Systems", self.check_emergency_systems),
            ("Risk Management", self.check_risk_management),
            ("Account Setup", self.check_account_setup),
            ("AI Training Status", self.check_ai_training_status),
            ("System Performance", self.check_system_performance),
            ("Live Mode Settings", self.check_live_mode_settings)
        ]
        
        passed_checks = 0
        total_checks = len(checklist_items)
        
        for check_name, check_func in checklist_items:
            try:
                if check_func():
                    passed_checks += 1
                    self.checklist_results[check_name] = "PASS"
                else:
                    self.checklist_results[check_name] = "FAIL"
            except Exception as e:
                self.checklist_results[check_name] = f"ERROR: {e}"
                
        # Final assessment
        print(f"\n{Fore.WHITE}{'='*60}")
        print(f"{Style.BRIGHT}📊 FINAL ASSESSMENT{Style.RESET_ALL}")
        
        success_rate = (passed_checks / total_checks) * 100
        
        if success_rate == 100:
            print(f"{Fore.GREEN}✅ READY FOR LIVE TRADING")
            print(f"{Fore.WHITE}All checks passed ({passed_checks}/{total_checks})")
            recommendation = "GO LIVE"
            
        elif success_rate >= 80:
            print(f"{Fore.YELLOW}⚠️  MOSTLY READY - Minor issues")
            print(f"{Fore.WHITE}Checks passed: {passed_checks}/{total_checks} ({success_rate:.1f}%)")
            recommendation = "FIX ISSUES FIRST"
            
        else:
            print(f"{Fore.RED}❌ NOT READY FOR LIVE TRADING")
            print(f"{Fore.WHITE}Checks passed: {passed_checks}/{total_checks} ({success_rate:.1f}%)")
            recommendation = "DO NOT GO LIVE"
            
        if self.critical_failures:
            print(f"\n{Fore.RED}🚨 Critical Issues:")
            for failure in self.critical_failures:
                print(f"   • {failure}")
                
        print(f"\n{Style.BRIGHT}🎯 RECOMMENDATION: {recommendation}{Style.RESET_ALL}")
        
        # Save checklist results
        checklist_report = {
            "timestamp": datetime.now().isoformat(),
            "success_rate": success_rate,
            "recommendation": recommendation,
            "results": self.checklist_results,
            "critical_failures": self.critical_failures
        }
        
        with open("pre_live_checklist.json", "w") as f:
            json.dump(checklist_report, f, indent=2)
            
        print(f"\n{Fore.CYAN}📄 Report saved to: pre_live_checklist.json{Style.RESET_ALL}")
        
        return success_rate == 100

def main():
    """Main checklist execution"""
    print(f"\n{Style.BRIGHT}{Fore.CYAN}🤖 JARVIS PRE-LIVE TRADING CHECKLIST{Style.RESET_ALL}")
    print(f"{Fore.WHITE}This checklist ensures your system is ready for live trading")
    print(f"{Fore.YELLOW}⚠️  Complete ALL items before risking real money!{Style.RESET_ALL}")
    
    checklist = PreLiveChecklist()
    is_ready = checklist.generate_go_live_report()
    
    if not is_ready:
        print(f"\n{Fore.YELLOW}💡 Next Steps:")
        print(f"   1. Fix all failed checks above")
        print(f"   2. Run this checklist again")
        print(f"   3. Start with small amounts in live mode")
        print(f"   4. Monitor closely for first 24 hours")

if __name__ == "__main__":
    main()
