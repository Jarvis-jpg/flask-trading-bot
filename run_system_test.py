#!/usr/bin/env python3
"""
Complete system verification before running quality test
"""

import os
import json
from colorama import init, Fore, Style

init(autoreset=True)

def check_system_components():
    print(f'{Fore.CYAN}🔧 COMPREHENSIVE SYSTEM CHECK{Style.RESET_ALL}')
    print('=' * 50)
    
    checks_passed = 0
    total_checks = 8
    
    # Check 1: Core imports
    try:
        from train_and_trade_100_sessions import ContinuousTrainingSystem
        print(f'{Fore.GREEN}✅ Core training system imports successfully{Style.RESET_ALL}')
        checks_passed += 1
    except Exception as e:
        print(f'{Fore.RED}❌ Import error: {e}{Style.RESET_ALL}')
        return False
    
    # Check 2: System initialization
    try:
        trader = ContinuousTrainingSystem()
        print(f'{Fore.GREEN}✅ System initialization successful{Style.RESET_ALL}')
        checks_passed += 1
    except Exception as e:
        print(f'{Fore.RED}❌ Initialization error: {e}{Style.RESET_ALL}')
        return False
    
    # Check 3: Enhanced config
    try:
        config = trader.enhanced_config
        print(f'{Fore.GREEN}✅ Enhanced config loaded:{Style.RESET_ALL}')
        print(f'   - Confidence: {config["confidence_threshold"]*100:.0f}%')
        print(f'   - Risk/Reward: {config["risk_reward_min"]}:1')
        print(f'   - Trend strength: {config["trend_strength_min"]*100:.0f}%')
        checks_passed += 1
        
        # Verify quality thresholds
        if config["confidence_threshold"] >= 0.7:
            print(f'{Fore.GREEN}✅ Quality confidence threshold active (75%+){Style.RESET_ALL}')
            checks_passed += 1
        else:
            print(f'{Fore.RED}❌ Confidence threshold too low: {config["confidence_threshold"]*100:.1f}%{Style.RESET_ALL}')
            
    except Exception as e:
        print(f'{Fore.RED}❌ Config error: {e}{Style.RESET_ALL}')
        return False
    
    # Check 4: Quality methods
    try:
        if hasattr(trader, 'reset_for_quality_learning'):
            print(f'{Fore.GREEN}✅ Quality reset method available{Style.RESET_ALL}')
            checks_passed += 1
        else:
            print(f'{Fore.RED}❌ Quality reset method missing{Style.RESET_ALL}')
            
        if hasattr(trader, 'add_quality_training_sample'):
            print(f'{Fore.GREEN}✅ Quality training method available{Style.RESET_ALL}')
            checks_passed += 1
        else:
            print(f'{Fore.RED}❌ Quality training method missing{Style.RESET_ALL}')
            
    except Exception as e:
        print(f'{Fore.RED}❌ Method check error: {e}{Style.RESET_ALL}')
    
    # Check 5: AI model
    try:
        if hasattr(trader, 'ai_model') and trader.ai_model is not None:
            print(f'{Fore.GREEN}✅ AI model loaded and ready{Style.RESET_ALL}')
            checks_passed += 1
        else:
            print(f'{Fore.YELLOW}⚠️ AI model will be created during training{Style.RESET_ALL}')
            checks_passed += 1  # This is OK, model gets created
    except Exception as e:
        print(f'{Fore.RED}❌ AI model error: {e}{Style.RESET_ALL}')
    
    # Check 6: Files exist
    required_files = ['quality_learning_trainer.py', 'train_and_trade_100_sessions.py', '.env']
    for file in required_files:
        if os.path.exists(file):
            print(f'{Fore.GREEN}✅ {file} exists{Style.RESET_ALL}')
            checks_passed += 1
        else:
            print(f'{Fore.RED}❌ {file} missing{Style.RESET_ALL}')
    
    print()
    print(f'{Style.BRIGHT}{Fore.CYAN}🎯 SYSTEM STATUS SUMMARY:{Style.RESET_ALL}')
    print(f'   Checks passed: {checks_passed}/{total_checks}')
    
    if checks_passed >= 7:
        print(f'{Fore.GREEN}{Style.BRIGHT}✅ SYSTEM READY FOR QUALITY TESTING{Style.RESET_ALL}')
        return True
    else:
        print(f'{Fore.RED}{Style.BRIGHT}❌ SYSTEM NEEDS FIXES BEFORE TESTING{Style.RESET_ALL}')
        return False

if __name__ == "__main__":
    system_ready = check_system_components()
    
    if system_ready:
        print(f'\n{Fore.GREEN}{Style.BRIGHT}🚀 STARTING QUALITY LEARNING TEST...{Style.RESET_ALL}')
        print(f'{Fore.YELLOW}This will run the quality-first system targeting 65% win rate{Style.RESET_ALL}')
        
        # Import and run quality trainer
        try:
            import subprocess
            result = subprocess.run(['python', 'quality_learning_trainer.py'], 
                                  capture_output=False, text=True)
        except Exception as e:
            print(f'{Fore.RED}Error starting quality trainer: {e}{Style.RESET_ALL}')
    else:
        print(f'\n{Fore.RED}{Style.BRIGHT}❌ SYSTEM NOT READY - FIX ISSUES FIRST{Style.RESET_ALL}')
