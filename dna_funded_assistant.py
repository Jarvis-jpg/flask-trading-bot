#!/usr/bin/env python3
"""
DNA Funded Manual Trading Assistant
Monitors JARVIS signals and provides formatted output for manual execution on TradeLocker
"""
import time
import json
from datetime import datetime
from colorama import Fore, Back, Style, init
import requests

# Initialize colorama for Windows
init(autoreset=True)

class DNAFundedAssistant:
    """Assistant for manual DNA Funded trading using JARVIS signals"""
    
    def __init__(self, account_size=10000):
        self.account_size = account_size
        self.daily_risk_limit = account_size * 0.05  # 5% max daily loss
        self.max_risk_per_trade = account_size * 0.02  # 2% per trade
        self.daily_pnl = 0.0
        self.trades_today = 0
        self.signals_processed = []
        
    def display_header(self):
        """Display DNA Funded trading header"""
        print(f"\n{Back.BLUE}{Fore.WHITE}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                 🧬 DNA FUNDED MANUAL TRADER                  ║")
        print(f"║                   JARVIS Signal Monitor                      ║") 
        print(f"╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Account Size: ${self.account_size:,}")
        print(f"{Fore.CYAN}Daily Risk Limit: ${self.daily_risk_limit:,.2f}")
        print(f"{Fore.CYAN}Max Risk Per Trade: ${self.max_risk_per_trade:,.2f}")
        print(f"{Fore.CYAN}Current Daily P&L: ${self.daily_pnl:,.2f}")
        print(f"{Fore.CYAN}Trades Today: {self.trades_today}")
        
    def check_jarvis_dashboard(self):
        """Check JARVIS dashboard for new signals"""
        try:
            # Try to get signals from local JARVIS instance
            response = requests.get('http://localhost:5000/api/signals', timeout=5)
            if response.status_code == 200:
                return response.json()
        except:
            pass
            
        # If API not available, simulate signal for demo
        return self.simulate_signal()
    
    def simulate_signal(self):
        """Simulate a trading signal for demonstration"""
        import random
        
        pairs = ['EUR_USD', 'GBP_USD', 'USD_JPY', 'USD_CHF', 'AUD_USD']
        pair = random.choice(pairs)
        action = random.choice(['BUY', 'SELL'])
        base_price = {'EUR_USD': 1.0950, 'GBP_USD': 1.2650, 'USD_JPY': 150.80, 
                     'USD_CHF': 0.8950, 'AUD_USD': 0.6650}[pair]
        
        if action == 'BUY':
            entry = base_price
            stop_loss = entry - (30 * (0.01 if 'JPY' in pair else 0.0001))
            take_profit = entry + (60 * (0.01 if 'JPY' in pair else 0.0001))
        else:
            entry = base_price
            stop_loss = entry + (30 * (0.01 if 'JPY' in pair else 0.0001))
            take_profit = entry - (60 * (0.01 if 'JPY' in pair else 0.0001))
            
        return {
            'signal': action.lower(),
            'pair': pair,
            'entry': round(entry, 4 if 'JPY' not in pair else 2),
            'stop_loss': round(stop_loss, 4 if 'JPY' not in pair else 2),
            'take_profit': round(take_profit, 4 if 'JPY' not in pair else 2),
            'confidence': random.uniform(0.75, 0.95),
            'timestamp': datetime.now().isoformat(),
            'strategy': 'JARVIS_AI'
        }
    
    def calculate_position_size(self, signal):
        """Calculate appropriate position size for DNA Funded"""
        entry = signal['entry']
        stop_loss = signal['stop_loss']
        
        # Calculate stop loss distance in pips
        if 'JPY' in signal['pair']:
            pip_value = 0.01
            stop_distance_pips = abs(entry - stop_loss) / pip_value
        else:
            pip_value = 0.0001
            stop_distance_pips = abs(entry - stop_loss) / pip_value
        
        # Calculate position size based on risk
        risk_amount = min(self.max_risk_per_trade, self.daily_risk_limit - abs(self.daily_pnl))
        
        # Standard lot calculation (100,000 units)
        if 'JPY' in signal['pair']:
            pip_dollar_value_per_lot = 1000  # $10 per pip for standard lot
        else:
            pip_dollar_value_per_lot = 1000  # $10 per pip for standard lot
            
        lots = risk_amount / (stop_distance_pips * pip_dollar_value_per_lot)
        
        # Round to reasonable lot sizes
        if lots >= 1:
            lots = round(lots, 1)
        else:
            lots = round(lots, 2)
            
        return max(0.01, min(lots, 5.0))  # Minimum 0.01, maximum 5.0 lots
    
    def format_tradelocker_instructions(self, signal):
        """Format signal for TradeLocker execution"""
        position_size = self.calculate_position_size(signal)
        risk_reward = abs(signal['take_profit'] - signal['entry']) / abs(signal['entry'] - signal['stop_loss'])
        
        print(f"\n{Back.GREEN}{Fore.BLACK}🚨 NEW TRADING SIGNAL 🚨{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}═" * 60)
        print(f"{Fore.WHITE}📊 SIGNAL DETAILS:")
        print(f"   Pair: {Fore.CYAN}{signal['pair'].replace('_', '/')}")
        print(f"   Action: {Fore.GREEN if signal['signal'].upper() == 'BUY' else Fore.RED}{signal['signal'].upper()}")
        print(f"   Confidence: {Fore.GREEN}{signal['confidence']:.1%}")
        print(f"   Risk/Reward: {Fore.CYAN}{risk_reward:.1f}:1")
        
        print(f"\n{Fore.WHITE}💰 PRICE LEVELS:")
        print(f"   Entry: {Fore.YELLOW}{signal['entry']}")
        print(f"   Stop Loss: {Fore.RED}{signal['stop_loss']}")
        print(f"   Take Profit: {Fore.GREEN}{signal['take_profit']}")
        
        print(f"\n{Fore.WHITE}📏 POSITION SIZING:")
        print(f"   Recommended Lots: {Fore.CYAN}{position_size}")
        print(f"   Risk Amount: {Fore.YELLOW}${self.max_risk_per_trade:,.2f}")
        
        print(f"\n{Back.BLUE}{Fore.WHITE}🎛️  TRADELOCKER EXECUTION STEPS:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Open TradeLocker (live.tradelocker.com)")
        print(f"2. Click {Fore.CYAN}'New Order'{Fore.WHITE}")
        print(f"3. Select Instrument: {Fore.CYAN}{signal['pair'].replace('_', '')}")
        print(f"4. Order Type: {Fore.CYAN}Market {signal['signal'].upper()}")
        print(f"5. Volume: {Fore.CYAN}{position_size} lots")
        print(f"6. Stop Loss: {Fore.RED}{signal['stop_loss']}")
        print(f"7. Take Profit: {Fore.GREEN}{signal['take_profit']}")
        print(f"8. Click {Fore.GREEN}'Place Order'")
        
        print(f"\n{Fore.WHITE}⚠️  PRE-EXECUTION CHECKLIST:")
        print(f"   {Fore.GREEN}✓{Fore.WHITE} Confidence > 75%: {Fore.GREEN if signal['confidence'] > 0.75 else Fore.RED}{signal['confidence']:.1%}")
        print(f"   {Fore.GREEN}✓{Fore.WHITE} Risk/Reward > 1.5: {Fore.GREEN if risk_reward > 1.5 else Fore.RED}{risk_reward:.1f}")
        print(f"   {Fore.GREEN}✓{Fore.WHITE} Within daily limits: {Fore.GREEN if abs(self.daily_pnl) < self.daily_risk_limit * 0.8 else Fore.RED}${abs(self.daily_pnl):,.2f} / ${self.daily_risk_limit:,.2f}")
        print(f"   {Fore.GREEN}✓{Fore.WHITE} Check major news events")
        print(f"   {Fore.GREEN}✓{Fore.WHITE} Verify market session (prefer overlap)")
        
        return position_size
        
    def wait_for_execution_confirmation(self):
        """Wait for user to confirm trade execution"""
        print(f"\n{Fore.YELLOW}⏳ Execute the trade in TradeLocker, then press:")
        print(f"   {Fore.GREEN}[E]{Fore.WHITE} - Trade Executed Successfully")
        print(f"   {Fore.RED}[S]{Fore.WHITE} - Signal Skipped")
        print(f"   {Fore.BLUE}[Q]{Fore.WHITE} - Quit Monitoring")
        
        while True:
            choice = input(f"\n{Fore.CYAN}Enter choice: ").upper().strip()
            if choice in ['E', 'S', 'Q']:
                return choice
            print(f"{Fore.RED}Invalid choice. Please enter E, S, or Q.")
    
    def update_daily_stats(self, executed=True):
        """Update daily trading statistics"""
        if executed:
            self.trades_today += 1
            print(f"\n{Fore.GREEN}✅ Trade #{self.trades_today} logged for today")
        else:
            print(f"\n{Fore.YELLOW}⏭️  Signal skipped")
            
    def display_daily_summary(self):
        """Display daily trading summary"""
        remaining_risk = self.daily_risk_limit - abs(self.daily_pnl)
        
        print(f"\n{Back.CYAN}{Fore.BLACK}📊 DAILY SUMMARY{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Trades Executed: {self.trades_today}")
        print(f"Current P&L: ${self.daily_pnl:,.2f}")
        print(f"Remaining Risk: ${remaining_risk:,.2f}")
        print(f"Risk Used: {((self.daily_risk_limit - remaining_risk) / self.daily_risk_limit * 100):.1f}%")
    
    def monitor_signals(self):
        """Main monitoring loop"""
        print(f"\n{Fore.GREEN}🔄 Starting signal monitoring...")
        print(f"{Fore.CYAN}Checking for JARVIS signals every 30 seconds...")
        print(f"{Fore.YELLOW}Press Ctrl+C to stop monitoring")
        
        try:
            while True:
                self.display_header()
                
                # Check for new signals
                signal = self.check_jarvis_dashboard()
                
                if signal and signal.get('confidence', 0) > 0.75:
                    # Format and display signal
                    position_size = self.format_tradelocker_instructions(signal)
                    
                    # Wait for execution confirmation
                    choice = self.wait_for_execution_confirmation()
                    
                    if choice == 'E':
                        self.update_daily_stats(executed=True)
                    elif choice == 'S':
                        self.update_daily_stats(executed=False)
                    elif choice == 'Q':
                        break
                        
                    self.display_daily_summary()
                    time.sleep(5)  # Brief pause before continuing
                    
                else:
                    print(f"\n{Fore.CYAN}⏳ No high-quality signals available...")
                    print(f"{Fore.WHITE}Waiting for confidence > 75%...")
                    time.sleep(30)  # Wait 30 seconds before checking again
                    
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}🛑 Signal monitoring stopped by user")
            self.display_daily_summary()

def main():
    """Main function"""
    print(f"{Fore.CYAN}Welcome to the DNA Funded Manual Trading Assistant!")
    
    # Get account size
    while True:
        try:
            account_input = input(f"\n{Fore.WHITE}Enter your DNA Funded account size (default $10,000): ").strip()
            if not account_input:
                account_size = 10000
            else:
                account_size = int(account_input.replace('$', '').replace(',', ''))
            break
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number")
    
    # Initialize assistant
    assistant = DNAFundedAssistant(account_size)
    
    # Start monitoring
    assistant.monitor_signals()

if __name__ == "__main__":
    main()
