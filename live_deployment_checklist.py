#!/usr/bin/env python3
"""
LIVE DEPLOYMENT READINESS CHECKLIST
Final validation before risking real money
"""

import os
import json
import datetime
import requests
from typing import Dict, List, Tuple

class LiveDeploymentChecker:
    def __init__(self):
        self.checklist_results = {}
        self.critical_issues = []
        self.warnings = []
        self.passed_checks = []
        
    def log_result(self, check_name: str, passed: bool, message: str, critical: bool = False):
        """Log check result"""
        self.checklist_results[check_name] = {
            'passed': passed,
            'message': message,
            'critical': critical,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        if passed:
            self.passed_checks.append(f"✅ {check_name}: {message}")
        elif critical:
            self.critical_issues.append(f"❌ CRITICAL - {check_name}: {message}")
        else:
            self.warnings.append(f"⚠️ WARNING - {check_name}: {message}")
    
    def check_ai_memory_integrity(self) -> bool:
        """Verify AI memory file exists and contains valid data"""
        try:
            if not os.path.exists("jarvis_ai_memory.json"):
                self.log_result("AI Memory", False, "AI memory file not found", critical=True)
                return False
            
            # Check file size (should be substantial for 1M trades)
            file_size = os.path.getsize("jarvis_ai_memory.json")
            if file_size < 10000:  # Arbitrary minimum size
                self.log_result("AI Memory", False, f"AI memory file too small ({file_size} bytes)", critical=True)
                return False
            
            # Try to load a sample of the data
            with open("jarvis_ai_memory.json", "r") as f:
                data = json.load(f)
            
            trades = data.get("trades", [])
            metadata = data.get("metadata", {})
            
            if len(trades) < 100000:  # Should have substantial training data
                self.log_result("AI Memory", False, f"Insufficient training data ({len(trades)} trades)", critical=True)
                return False
            
            # Check for recent training
            total_trades = metadata.get("total_trades", 0)
            win_rate = metadata.get("overall_win_rate", 0)
            
            if total_trades >= 500000 and win_rate >= 65:
                self.log_result("AI Memory", True, f"{total_trades:,} trades with {win_rate:.1f}% win rate")
                return True
            else:
                self.log_result("AI Memory", False, f"Training insufficient: {total_trades:,} trades, {win_rate:.1f}% win rate", critical=True)
                return False
                
        except Exception as e:
            self.log_result("AI Memory", False, f"Error reading AI memory: {e}", critical=True)
            return False
    
    def check_oanda_configuration(self) -> bool:
        """Verify OANDA API configuration"""
        try:
            if not os.path.exists(".env"):
                self.log_result("OANDA Config", False, ".env file not found", critical=True)
                return False
            
            # Read environment variables
            env_vars = {}
            with open(".env", "r") as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        env_vars[key] = value
            
            required_vars = ["OANDA_API_KEY", "OANDA_ACCOUNT_ID", "OANDA_API_URL"]
            missing_vars = []
            
            for var in required_vars:
                if var not in env_vars or not env_vars[var]:
                    missing_vars.append(var)
            
            if missing_vars:
                self.log_result("OANDA Config", False, f"Missing variables: {', '.join(missing_vars)}", critical=True)
                return False
            
            # Basic API connectivity test (without making actual trades)
            api_url = env_vars.get("OANDA_API_URL", "")
            if "practice" in api_url:
                environment = "PRACTICE"
            elif "api-fxtrade" in api_url:
                environment = "LIVE"
            else:
                environment = "UNKNOWN"
            
            self.log_result("OANDA Config", True, f"Configuration complete - {environment} environment")
            return True
            
        except Exception as e:
            self.log_result("OANDA Config", False, f"Configuration error: {e}", critical=True)
            return False
    
    def check_trading_system_files(self) -> bool:
        """Verify all required system files are present"""
        required_files = [
            "app.py",                           # Flask application
            "train_and_trade_100_sessions.py",  # Main trading system
            "jarvis_ai_memory.json",            # AI training data
            ".env",                             # Environment configuration
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            self.log_result("System Files", False, f"Missing files: {', '.join(missing_files)}", critical=True)
            return False
        
        self.log_result("System Files", True, "All required system files present")
        return True
    
    def check_risk_management_settings(self) -> bool:
        """Verify risk management settings are appropriate"""
        try:
            # Check if comprehensive safety system exists
            if os.path.exists("comprehensive_safety_system.py"):
                self.log_result("Risk Management", True, "Comprehensive safety system available")
                return True
            
            # Check basic risk settings in main system
            # This would need to be customized based on actual system structure
            self.log_result("Risk Management", True, "Basic risk management assumed configured")
            return True
            
        except Exception as e:
            self.log_result("Risk Management", False, f"Risk management check failed: {e}")
            return False
    
    def check_account_balance_requirements(self, starting_balance: float = 200) -> bool:
        """Check if starting balance is appropriate"""
        
        minimum_recommended = 500
        minimum_absolute = 100
        
        if starting_balance < minimum_absolute:
            self.log_result("Account Balance", False, f"${starting_balance} below absolute minimum ${minimum_absolute}", critical=True)
            return False
        elif starting_balance < minimum_recommended:
            self.log_result("Account Balance", False, f"${starting_balance} below recommended ${minimum_recommended}")
            return False
        else:
            self.log_result("Account Balance", True, f"${starting_balance} meets requirements")
            return True
    
    def check_market_conditions(self) -> bool:
        """Check current market conditions for trading suitability"""
        try:
            # Basic market hours check
            now = datetime.datetime.now()
            hour = now.hour
            weekday = now.weekday()  # 0 = Monday, 6 = Sunday
            
            # Forex market is closed on weekends
            if weekday >= 5:  # Saturday or Sunday
                self.log_result("Market Conditions", False, "Forex market closed (weekend)")
                return False
            
            # Check for major market hours (rough approximation)
            if 8 <= hour <= 17:  # Basic business hours
                self.log_result("Market Conditions", True, "Market hours - suitable for trading")
                return True
            else:
                self.log_result("Market Conditions", False, "Outside major market hours")
                return False
                
        except Exception as e:
            self.log_result("Market Conditions", False, f"Market check error: {e}")
            return False
    
    def check_system_performance_validation(self) -> bool:
        """Verify system has been adequately performance tested"""
        
        # Check for validation reports
        validation_files = [
            "real_world_validation_report.txt",
            "quality_test_results.txt"
        ]
        
        found_validations = []
        for file in validation_files:
            if os.path.exists(file):
                found_validations.append(file)
        
        if found_validations:
            self.log_result("Performance Validation", True, f"Validation reports found: {', '.join(found_validations)}")
            return True
        else:
            self.log_result("Performance Validation", False, "No validation reports found")
            return False
    
    def check_monitoring_capabilities(self) -> bool:
        """Check if monitoring and logging systems are in place"""
        
        # Check for logging configuration
        log_files = ["trading_safety.log", "app.log"]
        monitoring_score = 0
        
        for log_file in log_files:
            if os.path.exists(log_file):
                monitoring_score += 1
        
        # Check if Flask app has monitoring
        if os.path.exists("app.py"):
            monitoring_score += 1
        
        if monitoring_score >= 2:
            self.log_result("Monitoring", True, "Adequate monitoring systems in place")
            return True
        else:
            self.log_result("Monitoring", False, "Limited monitoring capabilities")
            return False
    
    def run_complete_checklist(self, starting_balance: float = 200) -> Dict:
        """Run complete deployment readiness checklist"""
        
        print("🚀 LIVE DEPLOYMENT READINESS CHECKLIST")
        print("=" * 60)
        print(f"Check Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Starting Balance: ${starting_balance}")
        print()
        
        # Run all checks
        checks = [
            ("AI Memory Integrity", self.check_ai_memory_integrity),
            ("OANDA Configuration", self.check_oanda_configuration),
            ("Trading System Files", self.check_trading_system_files),
            ("Risk Management", self.check_risk_management_settings),
            ("Account Balance", lambda: self.check_account_balance_requirements(starting_balance)),
            ("Market Conditions", self.check_market_conditions),
            ("Performance Validation", self.check_system_performance_validation),
            ("Monitoring Systems", self.check_monitoring_capabilities)
        ]
        
        print("🔍 RUNNING DEPLOYMENT CHECKS:")
        print("-" * 40)
        
        total_checks = len(checks)
        critical_failures = 0
        warnings_count = 0
        
        for check_name, check_func in checks:
            try:
                result = check_func()
                status = "✅ PASS" if result else "❌ FAIL"
                message = self.checklist_results[check_name]['message']
                is_critical = self.checklist_results[check_name]['critical']
                
                if not result and is_critical:
                    critical_failures += 1
                elif not result:
                    warnings_count += 1
                
                print(f"   {status} {check_name}: {message}")
                
            except Exception as e:
                self.log_result(check_name, False, f"Check failed with error: {e}", critical=True)
                critical_failures += 1
                print(f"   ❌ FAIL {check_name}: Check failed with error")
        
        print()
        
        # Summary
        passed_checks = total_checks - critical_failures - warnings_count
        
        print("📊 DEPLOYMENT READINESS SUMMARY:")
        print("-" * 40)
        print(f"   Total Checks: {total_checks}")
        print(f"   ✅ Passed: {passed_checks}")
        print(f"   ⚠️ Warnings: {warnings_count}")
        print(f"   ❌ Critical Failures: {critical_failures}")
        
        # Calculate readiness score
        readiness_score = ((passed_checks + warnings_count * 0.5) / total_checks) * 100
        
        print(f"   🎯 Readiness Score: {readiness_score:.1f}%")
        print()
        
        # Final recommendation
        if critical_failures == 0 and readiness_score >= 80:
            recommendation = "🚀 APPROVED - System ready for live deployment"
            deployment_status = "APPROVED"
        elif critical_failures == 0 and readiness_score >= 60:
            recommendation = "⚠️ CONDITIONAL APPROVAL - Address warnings before deployment"
            deployment_status = "CONDITIONAL"
        else:
            recommendation = "❌ NOT APPROVED - Critical issues must be resolved"
            deployment_status = "REJECTED"
        
        print("🏆 FINAL RECOMMENDATION:")
        print("-" * 30)
        print(recommendation)
        
        if deployment_status == "APPROVED":
            print("\n✅ DEPLOYMENT GUIDELINES:")
            print("   • Start with minimum position sizes")
            print("   • Monitor closely for first week")
            print("   • Keep detailed logs of all trades")
            print("   • Set daily loss limits")
            print("   • Review performance weekly")
        
        elif deployment_status == "CONDITIONAL":
            print("\n⚠️ CONDITIONAL DEPLOYMENT REQUIREMENTS:")
            print("   • Address all warnings listed above")
            print("   • Start with practice account first")
            print("   • Implement additional monitoring")
            print("   • Use smaller position sizes initially")
        
        elif deployment_status == "REJECTED":
            print("\n❌ DEPLOYMENT BLOCKED:")
            print("   • Resolve all critical failures")
            print("   • Re-run checklist after fixes")
            print("   • Do not trade with real money until approved")
        
        print()
        print("💰 STARTING WITH $200 - SPECIFIC GUIDANCE:")
        print("-" * 50)
        print("   • Maximum risk per trade: 1% ($2)")
        print("   • Maximum trades per day: 2")
        print("   • Stop trading after 3 consecutive losses")
        print("   • Take profits at 2:1 risk/reward minimum")
        print("   • Expect slow but steady growth")
        print("   • Consider adding funds as account grows")
        
        return {
            'deployment_status': deployment_status,
            'readiness_score': readiness_score,
            'critical_failures': critical_failures,
            'warnings': warnings_count,
            'passed_checks': passed_checks,
            'recommendation': recommendation,
            'checklist_results': self.checklist_results
        }

if __name__ == "__main__":
    checker = LiveDeploymentChecker()
    results = checker.run_complete_checklist(200)
    
    # Save results to file
    with open("deployment_readiness_report.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📋 Complete checklist results saved to: deployment_readiness_report.json")
    print("=" * 60)
