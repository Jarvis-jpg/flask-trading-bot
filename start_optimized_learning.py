#!/usr/bin/env python3
"""
JARVIS AI - Optimized Learning Configuration
Run this to start improved AI training with better data acquisition
"""

import subprocess
import sys
import os
from colorama import init, Fore, Style

init(autoreset=True)

def main():
    print(f"{Style.BRIGHT}{Fore.CYAN}🤖 JARVIS AI - OPTIMIZED LEARNING MODE")
    print(f"{Fore.GREEN}✅ Learning optimizations applied:")
    print(f"{Fore.WHITE}   • Dynamic confidence thresholds")
    print(f"{Fore.WHITE}   • Aggressive confidence boosting")
    print(f"{Fore.WHITE}   • Frequent AI retraining (250 trades)")
    print(f"{Fore.WHITE}   • Disabled restrictive market filters")
    print(f"{Fore.WHITE}   • Optimized for data acquisition")
    print(f"{Fore.YELLOW}🎯 Expected: 65%+ win rates with better learning")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    response = input(f"{Fore.GREEN}🚀 Start optimized learning session? (y/n): {Style.RESET_ALL}")
    
    if response.lower().startswith('y'):
        print(f"\n{Fore.CYAN}🚀 Launching optimized training system...{Style.RESET_ALL}")
        
        # Run the main training system
        script_path = os.path.join(os.path.dirname(__file__), "train_and_trade_100_sessions.py")
        
        try:
            subprocess.run([sys.executable, script_path], check=True)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⏹️ Training stopped by user{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}👋 Optimized learning cancelled{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
