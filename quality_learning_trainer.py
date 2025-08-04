#!/usr/bin/env python3
"""
JARVIS AI QUALITY-FIRST LEARNING SYSTEM
Enhanced training system designed to achieve 65%+ win rate through selective learning
"""
import sys
import time
from train_and_trade_100_sessions import ContinuousTrainingSystem
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

def run_quality_learning_session():
    """Run a single quality-focused learning session"""
    print(f"{Back.BLUE}{Fore.WHITE}                                                      {Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}    JARVIS AI QUALITY-FIRST LEARNING SYSTEM          {Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}    TARGET: 65%+ WIN RATE THROUGH SELECTIVE TRAINING  {Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}                                                      {Style.RESET_ALL}")
    print()
    
    # Initialize system
    print(f"{Fore.CYAN}🚀 Initializing Quality-First Learning System...{Style.RESET_ALL}")
    trader = ContinuousTrainingSystem()
    
    # Reset for quality learning
    trader.reset_for_quality_learning()
    
    print(f"\n{Fore.GREEN}🎯 QUALITY LEARNING SESSION STARTED{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Expected behavior:{Style.RESET_ALL}")
    print(f"  • FEWER trades (quality over quantity)")
    print(f"  • HIGHER win rates (selective execution)")
    print(f"  • PROGRESSIVE improvement (65% target)")
    print(f"  • STRICT filtering (premium setups only)")
    
    # Session statistics
    session_trades = 0
    session_wins = 0
    quality_rejected = 0
    target_trades = 2000  # Reduced target for quality focus
    
    print(f"\n{Fore.CYAN}🎯 Target: {target_trades} QUALITY trades (vs 8000 quantity trades){Style.RESET_ALL}")
    
    # Main quality learning loop
    for i in range(target_trades):
        try:
            # Generate quality trade
            trade = trader.generate_realistic_trade()
            
            if trade is None:
                quality_rejected += 1
                continue
            
            session_trades += 1
            
            # Execute trade with quality metrics
            outcome = trader.simulate_trade_outcome(trade)
            if outcome == 1:
                session_wins += 1
                if hasattr(trader, 'quality_metrics'):
                    trader.quality_metrics['quality_trades_won'] += 1
            
            # Update quality metrics
            if hasattr(trader, 'quality_metrics'):
                trader.quality_metrics['quality_trades_executed'] += 1
            
            # Progress reporting every 100 trades
            if session_trades % 100 == 0:
                current_wr = (session_wins / session_trades * 100) if session_trades > 0 else 0
                rejection_rate = (quality_rejected / (session_trades + quality_rejected) * 100)
                
                print(f"{Fore.GREEN}📊 Progress: {session_trades}/{target_trades} trades | " +
                      f"Win Rate: {current_wr:.1f}% | " +
                      f"Quality Filter: {rejection_rate:.1f}% rejected{Style.RESET_ALL}")
                
                # AI accuracy check
                ai_accuracy = trader.get_ai_accuracy()
                if ai_accuracy > 0:
                    progress_to_target = (ai_accuracy / 65) * 100
                    print(f"🧠 AI Model: {ai_accuracy:.1f}% accuracy ({progress_to_target:.1f}% of 65% target)")
            
            # Small delay for quality processing
            time.sleep(0.5)  # Reduced delay for quality focus
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⚠️ Session interrupted by user{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ Error in quality learning: {e}{Style.RESET_ALL}")
            continue
    
    # Final session report
    final_win_rate = (session_wins / session_trades * 100) if session_trades > 0 else 0
    final_rejection_rate = (quality_rejected / (session_trades + quality_rejected) * 100)
    
    print(f"\n{Back.GREEN}{Fore.WHITE}📊 QUALITY LEARNING SESSION COMPLETE{Style.RESET_ALL}")
    print(f"")
    print(f"📈 SESSION RESULTS:")
    print(f"   Quality Trades Executed: {session_trades:,}")
    print(f"   Session Win Rate: {final_win_rate:.1f}%")
    print(f"   Quality Filtering: {quality_rejected:,} trades rejected ({final_rejection_rate:.1f}%)")
    
    # AI progress report
    ai_accuracy = trader.get_ai_accuracy()
    if ai_accuracy > 0:
        progress_to_target = (ai_accuracy / 65) * 100
        print(f"   AI Model Accuracy: {ai_accuracy:.1f}%")
        print(f"   Progress to 65% Target: {progress_to_target:.1f}%")
        
        if ai_accuracy >= 65:
            print(f"\n{Back.GREEN}{Fore.WHITE}🎉 65%+ WIN RATE TARGET ACHIEVED! 🎉{Style.RESET_ALL}")
        elif ai_accuracy >= 60:
            print(f"\n{Fore.GREEN}🎯 EXCELLENT PROGRESS - Close to 65% target!{Style.RESET_ALL}")
        elif ai_accuracy >= 55:
            print(f"\n{Fore.YELLOW}📈 GOOD PROGRESS - Continue quality learning{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.CYAN}🔄 BUILDING FOUNDATION - Quality data accumulating{Style.RESET_ALL}")
    
    # Quality metrics report
    if hasattr(trader, 'quality_metrics'):
        print(trader.get_quality_metrics())
    
    print(f"\n{Fore.GREEN}✅ Quality learning session complete! Run again to continue progress toward 65%{Style.RESET_ALL}")
    
    return {
        'session_trades': session_trades,
        'session_win_rate': final_win_rate,
        'ai_accuracy': ai_accuracy,
        'quality_rejected': quality_rejected,
        'target_progress': (ai_accuracy / 65) * 100 if ai_accuracy > 0 else 0
    }

if __name__ == "__main__":
    print(f"{Fore.CYAN}🎯 JARVIS Quality-First Learning System{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}This system focuses on QUALITY over QUANTITY to achieve 65% win rate{Style.RESET_ALL}")
    print()
    
    try:
        results = run_quality_learning_session()
        
        print(f"\n{Fore.GREEN}🚀 NEXT STEPS:{Style.RESET_ALL}")
        if results['ai_accuracy'] < 65:
            print(f"   • Run more quality learning sessions")
            print(f"   • Each session improves AI with premium data")
            print(f"   • Expected: 3-5 sessions to reach 65% target")
        else:
            print(f"   • 65% target achieved! Ready for live trading")
            print(f"   • Consider validation with live market data")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Quality learning system error: {e}{Style.RESET_ALL}")
        sys.exit(1)
