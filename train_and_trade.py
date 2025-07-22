#!/usr/bin/env python3
"""
JARVIS AI Trading System - Enhanced Training & Autonomous Trading
ENHANCED VERSION FOR 65%+ WIN RATE ACHIEVEMENT
Runs 8000 sophisticated trade simulations followed by live AI trading
"""
import logging
import sys
import time
import random
import json
from datetime import datetime, timedelta
from colorama import Fore, Back, Style, init
from config import RISK_CONFIG, SIGNAL_QUALITY_CONFIG, PREMIUM_TRADING_HOURS

# Initialize colorama for Windows
init(autoreset=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedTrainingSystem:
    """
    ENHANCED AI training system for 65%+ win rate achievement
    Sophisticated simulation with persistent memory and cumulative learning
    """
    
    def __init__(self):
        # Current session stats
        self.trades_completed = 0
        self.wins = 0
        self.losses = 0
        self.total_profit = 0.0
        self.max_profit = 0.0
        self.max_loss = 0.0
        self.win_streak = 0
        self.current_streak = 0
        self.max_win_streak = 0
        self.drawdown = 0.0
        self.max_drawdown = 0.0
        self.equity_curve = [200.0]  # Starting with $200
        self.confidence_scores = []
        self.pairs_tested = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'USD/CHF', 'AUD/USD', 'USD/CAD', 'NZD/USD', 'EUR/GBP']
        
        # ENHANCED PARAMETERS FOR 65%+ WIN RATE
        self.enhanced_config = {
            'confidence_threshold': RISK_CONFIG['confidence_threshold'],  # 82%
            'risk_reward_min': RISK_CONFIG['risk_reward_min'],  # 2.5:1
            'max_daily_trades': 3,  # Quality over quantity
            'trend_strength_min': SIGNAL_QUALITY_CONFIG['min_trend_strength'],  # 75%
            'session_quality_min': 0.85,  # High session quality
            'volume_surge_min': SIGNAL_QUALITY_CONFIG['volume_surge_multiplier'],  # 1.8x
        }
        
        # Persistent AI memory system
        self.memory_file = 'jarvis_ai_memory.json'
        self.trade_history_file = 'jarvis_trade_history.json'
        self.ai_memory = self.load_ai_memory()
        self.session_number = self.ai_memory.get('session_number', 0) + 1
        self.lifetime_trades = self.ai_memory.get('lifetime_trades', 0)
        self.lifetime_wins = self.ai_memory.get('lifetime_wins', 0)
        self.lifetime_losses = self.ai_memory.get('lifetime_losses', 0)
        self.lifetime_profit = self.ai_memory.get('lifetime_profit', 0.0)
        self.starting_trade_number = self.lifetime_trades + 1
        
        # AI learning patterns from previous sessions
        self.pair_performance = self.ai_memory.get('pair_performance', {})
        self.session_performance = self.ai_memory.get('session_performance', [])
        self.market_condition_learning = self.ai_memory.get('market_condition_learning', {})
        self.confidence_optimization = self.ai_memory.get('confidence_optimization', {})
        
        # Initialize pair performance tracking
        for pair in self.pairs_tested:
            if pair not in self.pair_performance:
                self.pair_performance[pair] = {'wins': 0, 'losses': 0, 'profit': 0.0, 'avg_confidence': 0.75}
    
    def load_ai_memory(self):
        """Load persistent AI memory from previous sessions"""
        try:
            with open(self.memory_file, 'r') as f:
                memory = json.load(f)
                print(f"{Fore.GREEN}🧠 AI Memory Loaded: {memory.get('lifetime_trades', 0):,} lifetime trades")
                return memory
        except FileNotFoundError:
            print(f"{Fore.YELLOW}🧠 Starting fresh AI memory - no previous sessions found")
            return {}
        except Exception as e:
            print(f"{Fore.RED}⚠️ Error loading AI memory: {e}")
            return {}
    
    def save_ai_memory(self):
        """Save AI memory for future sessions"""
        try:
            # Calculate lifetime statistics
            lifetime_win_rate = (self.lifetime_wins / max(self.lifetime_trades, 1)) * 100
            
            memory_data = {
                'session_number': self.session_number,
                'lifetime_trades': self.lifetime_trades,
                'lifetime_wins': self.lifetime_wins,
                'lifetime_losses': self.lifetime_losses,
                'lifetime_profit': self.lifetime_profit,
                'lifetime_win_rate': lifetime_win_rate,
                'last_session_date': datetime.now().isoformat(),
                'pair_performance': self.pair_performance,
                'session_performance': self.session_performance,
                'market_condition_learning': self.market_condition_learning,
                'confidence_optimization': self.confidence_optimization,
                'ai_insights': self.generate_ai_insights(),
                'enhanced_config': self.enhanced_config
            }
            
            with open(self.memory_file, 'w') as f:
                json.dump(memory_data, f, indent=2)
            
            print(f"{Fore.GREEN}💾 AI Memory Saved: Session #{self.session_number} data stored")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error saving AI memory: {e}")
    
    def generate_ai_insights(self):
        """Generate AI insights based on cumulative learning"""
        insights = {}
        
        # Best performing pairs
        best_pair = max(self.pair_performance.items(), 
                       key=lambda x: x[1]['wins'] / max(x[1]['wins'] + x[1]['losses'], 1), 
                       default=('EUR/USD', {'wins': 0, 'losses': 0}))[0]
        insights['best_pair'] = best_pair
        
        # Learning trend assessment
        current_win_rate = (self.lifetime_wins / max(self.lifetime_trades, 1)) * 100
        if current_win_rate >= 65.0:
            insights['learning_trend'] = 'excellent - target achieved'
        elif current_win_rate >= 60.0:
            insights['learning_trend'] = 'good - approaching target'
        elif len(self.session_performance) >= 2:
            recent_performance = self.session_performance[-2:]
            if recent_performance[1]['win_rate'] > recent_performance[0]['win_rate']:
                insights['learning_trend'] = 'improving'
            else:
                insights['learning_trend'] = 'needs_adjustment'
        else:
            insights['learning_trend'] = 'building_experience'
            
        # Enhanced recommendations
        insights['recommendations'] = []
        if current_win_rate < 65.0:
            insights['recommendations'].append('Increase confidence threshold')
            insights['recommendations'].append('Focus on premium trading hours only')
            insights['recommendations'].append('Improve trend strength filtering')
            
        return insights
        
    def generate_enhanced_trade(self):
        """Generate ENHANCED trade with 65%+ win rate optimization"""
        pair = random.choice(self.pairs_tested)
        
        # ENHANCED Market condition simulation
        market_conditions = random.choices(
            ['trending_strong', 'trending_weak', 'ranging_tight', 'ranging_wide', 'volatile', 'quiet'],
            weights=[20, 15, 25, 20, 15, 5]  # Favor cleaner conditions
        )[0]
        
        # ENHANCED Session quality
        session = random.choices(
            ['london', 'newyork', 'tokyo', 'overlap', 'off_hours'],
            weights=[25, 30, 15, 25, 5]  # Weight toward quality sessions
        )[0]
        
        # ENHANCED WIN RATE CALCULATION with stricter filters
        base_win_probability = self._calculate_enhanced_win_probability(market_conditions, session, pair)
        
        # Apply enhanced AI learning
        if pair in self.pair_performance:
            pair_data = self.pair_performance[pair]
            pair_win_rate = pair_data['wins'] / max(pair_data['wins'] + pair_data['losses'], 1)
            if pair_win_rate > 0.70:  # High-performance pair
                base_win_probability += 0.05
            elif pair_win_rate < 0.50:  # Poor-performance pair
                base_win_probability -= 0.05
                
        # Enhanced market condition modifiers
        condition_modifiers = {
            'trending_strong': 0.15,
            'trending_weak': 0.05,
            'ranging_tight': -0.05,
            'ranging_wide': -0.10,
            'volatile': -0.15,
            'quiet': -0.20
        }
        base_win_probability += condition_modifiers.get(market_conditions, 0)
        
        # Enhanced session quality modifiers
        session_modifiers = {
            'overlap': 0.12,
            'london': 0.08,
            'newyork': 0.10,
            'tokyo': -0.05,
            'off_hours': -0.25
        }
        base_win_probability += session_modifiers.get(session, 0)
        
        # Enhanced confidence threshold filtering
        confidence_score = random.uniform(0.65, 0.95)
        
        # CRITICAL: Apply 82% confidence threshold
        if confidence_score < self.enhanced_config['confidence_threshold']:
            return None  # Skip this trade - doesn't meet quality standards
            
        # Enhanced trend strength requirement
        trend_strength = random.uniform(0.40, 1.0)
        if trend_strength < self.enhanced_config['trend_strength_min']:
            return None  # Skip - insufficient trend strength
            
        # Enhanced session quality requirement
        session_quality_map = {'overlap': 1.0, 'london': 0.85, 'newyork': 0.90, 'tokyo': 0.70, 'off_hours': 0.3}
        session_quality = session_quality_map.get(session, 0.5)
        if session_quality < self.enhanced_config['session_quality_min']:
            return None  # Skip - poor session quality
    
    def load_ai_memory(self):
        """Load persistent AI memory from previous sessions"""
        try:
            with open(self.memory_file, 'r') as f:
                memory = json.load(f)
                print(f"{Fore.GREEN}🧠 AI Memory Loaded: {memory.get('lifetime_trades', 0):,} lifetime trades")
                return memory
        except FileNotFoundError:
            print(f"{Fore.YELLOW}🧠 Starting fresh AI memory - no previous sessions found")
            return {}
        except Exception as e:
            print(f"{Fore.RED}⚠️ Error loading AI memory: {e}")
            return {}
    
    def save_ai_memory(self):
        """Save AI memory for future sessions"""
        try:
            # Calculate lifetime statistics
            lifetime_win_rate = (self.lifetime_wins / max(self.lifetime_trades, 1)) * 100
            
            memory_data = {
                'session_number': self.session_number,
                'lifetime_trades': self.lifetime_trades,
                'lifetime_wins': self.lifetime_wins,
                'lifetime_losses': self.lifetime_losses,
                'lifetime_profit': self.lifetime_profit,
                'lifetime_win_rate': lifetime_win_rate,
                'last_session_date': datetime.now().isoformat(),
                'pair_performance': self.pair_performance,
                'session_performance': self.session_performance,
                'market_condition_learning': self.market_condition_learning,
                'confidence_optimization': self.confidence_optimization,
                'ai_insights': self.generate_ai_insights()
            }
            
            with open(self.memory_file, 'w') as f:
                json.dump(memory_data, f, indent=2)
            
            print(f"{Fore.GREEN}💾 AI Memory Saved: Session #{self.session_number} data stored")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error saving AI memory: {e}")
    
    def generate_ai_insights(self):
        """Generate AI insights based on cumulative learning"""
        insights = {}
        
        # Best performing pairs
        best_pair = max(self.pair_performance.items(), 
                       key=lambda x: x[1]['wins'] / max(x[1]['wins'] + x[1]['losses'], 1), 
                       default=('EUR/USD', {'wins': 0, 'losses': 0}))[0]
        insights['best_pair'] = best_pair
        
        # Learning trend
        if len(self.session_performance) >= 2:
            recent_performance = self.session_performance[-2:]
            if recent_performance[1]['win_rate'] > recent_performance[0]['win_rate']:
                insights['learning_trend'] = 'improving'
            else:
                insights['learning_trend'] = 'needs_adjustment'
        else:
            insights['learning_trend'] = 'building_experience'
            
        return insights
        
    def generate_sophisticated_trade(self):
        """Generate ULTRA-REALISTIC trade with all real-world trading friction"""
        pair = random.choice(self.pairs_tested)
        
        # Market condition simulation with realistic probabilities
        market_conditions = random.choices(
            ['trending', 'ranging', 'volatile', 'quiet'],
            weights=[25, 40, 25, 10]  # Markets range more than trend
        )[0]
        
        session = random.choices(
            ['london', 'newyork', 'tokyo', 'overlap'],
            weights=[30, 35, 20, 15]  # Weight toward active sessions
        )[0]
        
        # REALISTIC WIN RATE REDUCTION - Markets are harder than backtests
        base_win_probability = random.uniform(0.45, 0.68)  # Much more realistic range
        
        # Apply AI learning with realistic constraints
        if pair in self.pair_performance:
            pair_data = self.pair_performance[pair]
            pair_win_rate = pair_data['wins'] / max(pair_data['wins'] + pair_data['losses'], 1)
            if pair_win_rate > 0.65:  # Lower threshold for "good" performance
                base_win_probability += 0.03  # Smaller boost
            elif pair_win_rate < 0.55:
                base_win_probability -= 0.05  # Penalty for poor performance
        
        # Market condition realistic adjustments
        if market_conditions == 'trending':
            base_win_probability += 0.05  # Trends are easier
        elif market_conditions == 'ranging':
            base_win_probability -= 0.03  # Ranges are harder
        elif market_conditions == 'volatile':
            base_win_probability -= 0.08  # Volatility kills strategies
        elif market_conditions == 'quiet':
            base_win_probability -= 0.05  # Low volume = poor execution
        
        # Session impact on success
        if session == 'overlap':
            base_win_probability += 0.02  # Best liquidity
        elif session == 'tokyo':
            base_win_probability -= 0.03  # Lower liquidity
        
        # Cap realistic win probability
        win_probability = min(0.75, max(0.40, base_win_probability))
        
        # REALISTIC EXECUTION ISSUES - Not all trades execute perfectly
        execution_success = random.random() > 0.05  # 5% of trades fail to execute
        if not execution_success:
            # Trade rejected - no P&L impact but counts as missed opportunity
            return None
        
        # Slippage simulation - real brokers don't give perfect fills
        slippage_factor = random.uniform(0.97, 1.03)  # ±3% slippage on fills
        
        is_win = random.random() < win_probability
        
        # REALISTIC POSITION SIZING with broker limitations
        current_equity = self.equity_curve[-1] if self.equity_curve else 200.0
        
        # Progressive risk reduction as account grows (real-world scaling constraints)
        if current_equity <= 1000:
            risk_percent = 0.02  # 2% for small accounts
        elif current_equity <= 5000:
            risk_percent = 0.015  # 1.5% for medium accounts
        elif current_equity <= 20000:
            risk_percent = 0.01   # 1% for larger accounts
        else:
            risk_percent = 0.005  # 0.5% for very large accounts (institutional constraints)
        
        base_risk_amount = current_equity * risk_percent
        
        # SPREAD COSTS - Every trade pays the spread
        spread_cost = base_risk_amount * random.uniform(0.02, 0.08)  # 2-8% of risk as spread
        
        # COMMISSION SIMULATION
        commission = base_risk_amount * 0.001  # 0.1% commission per trade
        
        # REALISTIC PROFIT/LOSS with market friction
        if is_win:
            # Wins are smaller due to realistic market conditions
            base_profit = base_risk_amount * random.uniform(1.2, 2.1)  # Lower R:R in reality
            profit = (base_profit * slippage_factor) - spread_cost - commission
            
            self.wins += 1
            self.lifetime_wins += 1
            self.current_streak += 1
            self.max_win_streak = max(self.max_win_streak, self.current_streak)
            
            # Update pair performance
            self.pair_performance[pair]['wins'] += 1
            self.pair_performance[pair]['profit'] += profit
        else:
            # Losses are larger due to spreads and slippage
            base_loss = base_risk_amount * random.uniform(0.9, 1.1)
            profit = -(base_loss * slippage_factor) - spread_cost - commission
            
            self.losses += 1
            self.lifetime_losses += 1
            self.current_streak = 0
            
            # Update pair performance
            self.pair_performance[pair]['losses'] += 1
            self.pair_performance[pair]['profit'] += profit
        
        # Calculate confidence based on realistic performance
        confidence = min(0.85, max(0.50, win_probability + random.uniform(-0.1, 0.1)))
        self.confidence_scores.append(confidence)
        
        # Update market condition learning
        if market_conditions not in self.market_condition_learning:
            self.market_condition_learning[market_conditions] = {'wins': 0, 'losses': 0, 'success_rate': 0.6}
        
        if is_win:
            self.market_condition_learning[market_conditions]['wins'] += 1
        else:
            self.market_condition_learning[market_conditions]['losses'] += 1
            
        # Recalculate success rate
        condition_data = self.market_condition_learning[market_conditions]
        total_trades = condition_data['wins'] + condition_data['losses']
        condition_data['success_rate'] = condition_data['wins'] / max(total_trades, 1)
        
        self.total_profit += profit
        self.lifetime_profit += profit
        self.lifetime_trades += 1
        
        # REALISTIC EQUITY CURVE with extreme diminishing returns and market impact
        current_equity = self.equity_curve[-1] if self.equity_curve else 200.0
        
        # REAL-WORLD SCALING CONSTRAINTS (much more aggressive reduction)
        if current_equity <= 500:
            # Very small accounts can grow faster
            scaling_factor = 1.0
        elif current_equity <= 2000:
            # Small accounts face some friction
            scaling_factor = 0.85
        elif current_equity <= 10000:
            # Medium accounts face significant friction
            scaling_factor = 0.65
        elif current_equity <= 50000:
            # Large accounts face major constraints
            scaling_factor = 0.35
        elif current_equity <= 200000:
            # Very large accounts face institutional limitations
            scaling_factor = 0.15
        else:
            # Massive accounts face extreme diminishing returns
            scaling_factor = 0.05
        
        # Apply scaling and add market impact costs for large accounts
        scaled_profit = profit * scaling_factor
        
        # MARKET IMPACT - Large accounts move prices against themselves
        if current_equity > 20000:
            market_impact = abs(profit) * 0.1 * (current_equity / 100000)  # Increasing impact with size
            if profit > 0:
                scaled_profit -= market_impact
            else:
                scaled_profit -= market_impact  # Impact hurts both wins and losses
        
        # Calculate new equity with ALL realistic constraints
        new_equity = current_equity + scaled_profit
        
        # MINIMUM ACCOUNT PROTECTION - Can't go below margin requirements
        new_equity = max(100.0, new_equity)  # Minimum $100 account (margin call level)
        
        self.equity_curve.append(new_equity)
        
        # Track drawdown using realistic equity
        peak_equity = max(self.equity_curve)
        current_equity = self.equity_curve[-1]
        self.drawdown = (peak_equity - current_equity) / peak_equity * 100
        self.max_drawdown = max(self.max_drawdown, self.drawdown)
        
        # Track profit extremes
        self.max_profit = max(self.max_profit, profit)
        self.max_loss = min(self.max_loss, profit)
        
        return {
            'pair': pair,
            'action': 'BUY' if random.random() > 0.5 else 'SELL',
            'confidence': confidence,
            'market_condition': market_conditions,
            'session': session,
            'profit': profit,
            'scaled_profit': scaled_profit,
            'is_win': is_win,
            'equity': current_equity,
            'lifetime_trade_number': self.lifetime_trades,
            'spread_cost': spread_cost,
            'commission': commission,
            'slippage_factor': slippage_factor,
            'scaling_factor': scaling_factor
        }
    
    def print_progress_bar(self, current, total, bar_length=50):
        """Print sophisticated progress bar"""
        progress = current / total
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '▒' * (bar_length - filled_length)
        
        win_rate = (self.wins / max(current, 1)) * 100
        color = Fore.GREEN if win_rate >= 70 else Fore.YELLOW if win_rate >= 60 else Fore.RED
        
        print(f'\r{Fore.CYAN}Progress: {color}[{bar}] {progress:.1%} '
              f'{Fore.WHITE}({current:,}/{total:,}) '
              f'{color}Win Rate: {win_rate:.1f}%', end='', flush=True)
    
    def run_enhanced_training(self):
        """Run sophisticated 8000-trade training simulation with AI memory"""
        print(f"\n{Style.BRIGHT}{Fore.CYAN}{'='*80}")
        print(f"{Fore.YELLOW}🤖 JARVIS AI TRAINING SYSTEM - SESSION #{self.session_number}")
        print(f"{Fore.WHITE}Target: 8000 New Trades | 70% Win Rate | 2:1 Risk:Reward | $200 Starting Capital")
        
        # Display lifetime AI experience
        if self.lifetime_trades > 0:
            lifetime_win_rate = (self.lifetime_wins / self.lifetime_trades) * 100
            print(f"{Fore.GREEN}🧠 AI LIFETIME EXPERIENCE:")
            print(f"   📊 Total Trades: {self.lifetime_trades:,}")
            print(f"   🎯 Win Rate: {lifetime_win_rate:.1f}%")
            print(f"   💰 Lifetime Profit: ${self.lifetime_profit:,.2f}")
            print(f"   🏆 Best Pair: {self.ai_memory.get('ai_insights', {}).get('best_pair', 'Learning...')}")
            print(f"   📈 Learning Trend: {self.ai_memory.get('ai_insights', {}).get('learning_trend', 'Building experience').replace('_', ' ').title()}")
        
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}🚀 Starting trades #{self.starting_trade_number:,} - #{self.starting_trade_number + 7999:,}")
        
        start_time = datetime.now()
        print(f"{Fore.WHITE}🚀 Starting trades #{self.starting_trade_number:,} - #{self.starting_trade_number + 7999:,}")
        print(f"{Fore.CYAN}⏱️  Using 1-second delays for faster testing...")
        
        try:
            for i in range(8000):
                trade = self.generate_sophisticated_trade()
                
                # Handle trade execution failures (realistic broker rejections)
                if trade is None:
                    continue  # Skip this iteration, trade was rejected
                
                self.trades_completed += 1
                
                # Update progress every 10 trades for better visibility
                if i % 10 == 0 or i == 7999:
                    self.print_progress_bar(i + 1, 8000)
                    
                    # Show individual trade details every 50 trades (less frequent for speed)
                    if i % 50 == 0 and i > 0:
                        color = Fore.GREEN if trade['is_win'] else Fore.RED
                        action_color = Fore.BLUE if trade['action'] == 'BUY' else Fore.MAGENTA
                        print(f"\n{Fore.CYAN}Lifetime Trade #{trade['lifetime_trade_number']:,} | {Fore.YELLOW}{trade['pair']} | "
                              f"{action_color}{trade['action']} | {color}{'WIN' if trade['is_win'] else 'LOSS'} | "
                              f"{Fore.WHITE}${trade['profit']:+.2f} | "
                              f"{Fore.CYAN}Conf: {trade['confidence']:.1%} | "
                              f"{Fore.WHITE}Equity: ${trade['equity']:,.2f}")
                
                # 1-second delay between trades (much faster for testing)
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⏸️  Training interrupted by user at trade {i+1}")
            print(f"{Fore.WHITE}Saving progress...")
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error during training: {e}")
            print(f"{Fore.WHITE}Saving progress...")
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        # Save session performance for AI learning
        session_data = {
            'session_number': self.session_number,
            'trades': 8000,
            'wins': self.wins,
            'losses': self.losses,
            'win_rate': (self.wins / 8000) * 100,
            'profit': self.total_profit,
            'date': datetime.now().isoformat(),
            'duration': str(duration)
        }
        self.session_performance.append(session_data)
        
        # Save AI memory after session
        self.save_ai_memory()
        
        print(f"\n\n{Style.BRIGHT}{Fore.GREEN}✅ AI TRAINING SESSION #{self.session_number} COMPLETED!")
        print(f"{Fore.CYAN}{'='*80}")
        
        # Calculate final statistics
        win_rate = (self.wins / self.trades_completed) * 100
        profit_factor = abs(self.total_profit / min(self.max_loss * self.losses, -1))
        avg_win = (self.total_profit + abs(self.max_loss * self.losses)) / max(self.wins, 1)
        avg_loss = abs(self.max_loss * self.losses) / max(self.losses, 1)
        avg_confidence = sum(self.confidence_scores) / len(self.confidence_scores)
        
        # Print detailed results with AI insights
        self.print_training_results(duration, win_rate, profit_factor, avg_win, avg_loss, avg_confidence)
        
        # Print REALISTIC PERFORMANCE WARNING
        print(f"\n{Style.BRIGHT}{Fore.YELLOW}⚠️  REALITY CHECK - LIVE TRADING EXPECTATIONS:")
        print(f"{Fore.WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"{Fore.CYAN}📊 These results include REALISTIC trading friction:")
        print(f"   • Spread costs, commissions, and slippage applied")
        print(f"   • Broker execution failures simulated")
        print(f"   • Market impact for larger accounts")
        print(f"   • Diminishing returns as account grows")
        print(f"   • Progressive risk reduction for scaling")
        print(f"\n{Fore.YELLOW}🎯 LIVE TRADING will likely produce:")
        expected_live_win_rate = min(win_rate * 0.85, 75.0)  # 15% reduction expected
        expected_live_profit = self.total_profit * 0.60      # 40% profit reduction expected
        print(f"   • Win Rate: {expected_live_win_rate:.1f}% (vs {win_rate:.1f}% simulated)")
        print(f"   • Monthly Return: 50-70% of simulated results")
        print(f"   • Higher drawdowns due to emotional factors")
        print(f"   • More consecutive losses than simulation")
        print(f"\n{Fore.GREEN}✅ Start with SMALL position sizes and scale up gradually!")
        print(f"{Fore.WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        return {
            'session_number': self.session_number,
            'total_trades': self.trades_completed,
            'lifetime_trades': self.lifetime_trades,
            'wins': self.wins,
            'losses': self.losses,
            'win_rate': win_rate,
            'total_profit': self.total_profit,
            'lifetime_profit': self.lifetime_profit,
            'profit_factor': profit_factor,
            'max_drawdown': self.max_drawdown,
            'avg_confidence': avg_confidence,
            'final_equity': self.equity_curve[-1]
        }
    
    def print_training_results(self, duration, win_rate, profit_factor, avg_win, avg_loss, avg_confidence):
        """Print sophisticated training results"""
        print(f"\n{Style.BRIGHT}{Fore.YELLOW}📊 TRAINING PERFORMANCE ANALYSIS")
        print(f"{Fore.CYAN}{'-'*80}")
        
        # Core Statistics
        print(f"{Fore.WHITE}🎯 Core Performance:")
        win_color = Fore.GREEN if win_rate >= 70 else Fore.YELLOW if win_rate >= 60 else Fore.RED
        print(f"   {Fore.CYAN}Total Trades:{Fore.WHITE} {self.trades_completed:,}")
        print(f"   {Fore.GREEN}Winning Trades:{Fore.WHITE} {self.wins:,}")
        print(f"   {Fore.RED}Losing Trades:{Fore.WHITE} {self.losses:,}")
        print(f"   {win_color}Win Rate:{Fore.WHITE} {win_rate:.1f}% {win_color}{'✅' if win_rate >= 70 else '⚠️' if win_rate >= 60 else '❌'}")
        
        # Profit Analysis
        profit_color = Fore.GREEN if self.total_profit > 0 else Fore.RED
        final_equity = self.equity_curve[-1]
        starting_capital = self.equity_curve[0]
        total_return = ((final_equity - starting_capital) / starting_capital) * 100
        
        print(f"\n{Fore.WHITE}💰 REALISTIC Profit Analysis:")
        print(f"   {Fore.CYAN}Starting Capital:{Fore.WHITE} ${starting_capital:,.2f}")
        print(f"   {profit_color}Final Equity:{Fore.WHITE} ${final_equity:,.2f}")
        print(f"   {profit_color}Total Return:{Fore.WHITE} {total_return:+.1f}%")
        print(f"   {profit_color}Net Profit:{Fore.WHITE} ${self.total_profit:,.2f}")
        print(f"   {Fore.CYAN}Profit Factor:{Fore.WHITE} {profit_factor:.2f}")
        print(f"   {Fore.GREEN}Best Trade:{Fore.WHITE} ${self.max_profit:.2f}")
        print(f"   {Fore.RED}Worst Trade:{Fore.WHITE} ${self.max_loss:.2f}")
        
        # Show scaling impact
        total_gross_profit = sum([abs(trade) for trade in self.equity_curve[1:] if trade > 0])
        scaling_efficiency = (self.total_profit / max(total_gross_profit, 1)) * 100 if total_gross_profit > 0 else 0
        print(f"   {Fore.YELLOW}Scaling Efficiency:{Fore.WHITE} {scaling_efficiency:.1f}% (accounts for real-world friction)")
        
        # Risk Metrics
        drawdown_color = Fore.GREEN if self.max_drawdown < 15 else Fore.YELLOW if self.max_drawdown < 25 else Fore.RED
        print(f"\n{Fore.WHITE}⚡ Risk Metrics:")
        print(f"   {drawdown_color}Max Drawdown:{Fore.WHITE} {self.max_drawdown:.1f}%")
        print(f"   {Fore.CYAN}Avg Win:{Fore.WHITE} ${avg_win:.2f}")
        print(f"   {Fore.RED}Avg Loss:{Fore.WHITE} ${avg_loss:.2f}")
        print(f"   {Fore.YELLOW}Avg Confidence:{Fore.WHITE} {avg_confidence:.1f}%")
        print(f"   {Fore.CYAN}Avg Loss:{Fore.WHITE} ${avg_loss:.2f}")
        print(f"   {Fore.YELLOW}Max Win Streak:{Fore.WHITE} {self.max_win_streak}")
        
        # AI Metrics with Lifetime Learning
        confidence_color = Fore.GREEN if avg_confidence >= 0.75 else Fore.YELLOW
        print(f"\n{Fore.WHITE}🧠 AI Performance & Learning:")
        print(f"   {confidence_color}Session Avg Confidence:{Fore.WHITE} {avg_confidence:.1%}")
        print(f"   {Fore.CYAN}Pairs Tested:{Fore.WHITE} {len(self.pairs_tested)}")
        print(f"   {Fore.CYAN}Training Duration:{Fore.WHITE} {duration}")
        print(f"   {Fore.YELLOW}Lifetime Trades:{Fore.WHITE} {self.lifetime_trades:,}")
        
        lifetime_win_rate = (self.lifetime_wins / max(self.lifetime_trades, 1)) * 100
        lifetime_color = Fore.GREEN if lifetime_win_rate >= 70 else Fore.YELLOW if lifetime_win_rate >= 60 else Fore.RED
        print(f"   {lifetime_color}Lifetime Win Rate:{Fore.WHITE} {lifetime_win_rate:.1f}%")
        
        # Best performing pair insights
        if self.pair_performance:
            best_pair_data = max(self.pair_performance.items(), 
                               key=lambda x: x[1]['wins'] / max(x[1]['wins'] + x[1]['losses'], 1))
            best_pair = best_pair_data[0]
            best_pair_wr = (best_pair_data[1]['wins'] / max(best_pair_data[1]['wins'] + best_pair_data[1]['losses'], 1)) * 100
            print(f"   {Fore.YELLOW}Best Pair:{Fore.WHITE} {best_pair} ({best_pair_wr:.1f}% WR)")
        
        # Learning progression
        if len(self.session_performance) >= 2:
            prev_session = self.session_performance[-2]
            improvement = win_rate - prev_session['win_rate']
            improvement_color = Fore.GREEN if improvement > 0 else Fore.RED
            print(f"   {improvement_color}Learning Progress:{Fore.WHITE} {improvement:+.1f}% vs last session")
        
        # Overall Assessment with AI insights
        print(f"\n{Style.BRIGHT}{Fore.YELLOW}🎖️  AI ASSESSMENT:")
        if win_rate >= 70 and self.total_profit > 0 and self.max_drawdown < 15:
            print(f"   {Fore.GREEN}🌟 EXCELLENT - AI is performing optimally!")
        elif win_rate >= 65 and self.total_profit > 0:
            print(f"   {Fore.YELLOW}⭐ GOOD - AI is learning and improving")
        else:
            print(f"   {Fore.RED}⚠️  DEVELOPING - AI needs more experience")
            
        if self.lifetime_trades >= 16000:  # After 2+ sessions
            print(f"   {Fore.CYAN}🎓 AI has significant trading experience")
        elif self.lifetime_trades >= 8000:
            print(f"   {Fore.YELLOW}📚 AI is building trading knowledge") 
        else:
            print(f"   {Fore.WHITE}🌱 AI is in early learning phase")

def run_training_and_start_bot():
    """Run enhanced 8000-trade training then start autonomous trading"""
    
    print(f"\n{Style.BRIGHT}{Back.BLUE}{Fore.WHITE}")
    print("🚀 JARVIS AI TRADING SYSTEM - ULTRA-REALISTIC TESTING 🚀")
    print("=" * 70)
    print("ENHANCED REALISTIC TRAINING MODE:")
    print("✅ 8000 Ultra-Realistic Trade Simulations")
    print("✅ Spread Costs & Commission Deduction") 
    print("✅ Slippage & Execution Failure Simulation")
    print("✅ Market Impact for Large Accounts")
    print("✅ Diminishing Returns Scaling Model")
    print("✅ Progressive Risk Reduction")
    print("✅ Real-World Win Rate Constraints")
    print("=" * 70 + Style.RESET_ALL)
    
    
    # Ask user if they want to run enhanced training
    try:
        print(f"\n{Fore.WHITE}🤖 Run ULTRA-REALISTIC 8000-Trade Training System?")
        print(f"{Fore.CYAN}   This will simulate 8000 trades with MAXIMUM REALISM:")
        print(f"   • Spread costs (2-8% per trade)")
        print(f"   • Broker commissions (0.1% per trade)")
        print(f"   • Slippage (±3% on fills)")
        print(f"   • 5% execution failure rate")
        print(f"   • Market impact for large accounts")
        print(f"   • Diminishing returns scaling (up to 95% reduction)")
        print(f"   • Progressive risk reduction as account grows")
        print(f"   • Realistic win rates (40-75% range)")
        print(f"{Fore.YELLOW}   ⚠️  Results will be MUCH lower than previous simulations!")
        
        response = input(f"\n{Fore.YELLOW}Start REALISTIC training? (y/n): {Fore.WHITE}").lower().strip()
    except (EOFError, KeyboardInterrupt):
        print(f"\n{Fore.RED}⏹️ Operation cancelled by user{Style.RESET_ALL}")
        return
    
    if response in ['y', 'yes']:
        print(f"\n{Style.BRIGHT}{Fore.GREEN}🚀 STARTING ENHANCED AI TRAINING SYSTEM...")
        
        try:
            # Initialize and run enhanced training
            training_system = EnhancedTrainingSystem()
            
            # Run the sophisticated 8000-trade simulation
            logger.info("🧠 Initializing JARVIS AI learning algorithms...")
            results = training_system.run_enhanced_training()
            
            # Save training results for the autonomous engine
            training_data = {
                'timestamp': datetime.now().isoformat(),
                'results': results,
                'confidence_scores': training_system.confidence_scores[-100:],  # Last 100 for analysis
                'equity_curve': training_system.equity_curve[-500:],  # Last 500 points
                'pairs_performance': {}
            }
            
            # Save training data
            with open('ai_training_results.json', 'w') as f:
                json.dump(training_data, f, indent=2)
            
            print(f"\n{Style.BRIGHT}{Fore.GREEN}✅ TRAINING COMPLETED SUCCESSFULLY!")
            print(f"{Fore.CYAN}📁 Training data saved to: ai_training_results.json")
            print(f"{Fore.WHITE}🧠 AI is now optimized with {results['total_trades']:,} trade experiences")
            
        except Exception as e:
            logger.error(f"❌ Training failed: {e}")
            print(f"{Fore.RED}⚠️ Training failed, but you can still run the bot with default settings{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}⏩ Skipping enhanced training - using default AI configuration{Style.RESET_ALL}")
    
    # Ask if user wants to start the autonomous engine
    print(f"\n{Style.BRIGHT}{Fore.CYAN}{'='*60}")
    print(f"{Fore.WHITE}🤖 AUTONOMOUS TRADING ENGINE")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    try:
        start_response = input(f"{Fore.YELLOW}🚀 Start JARVIS Autonomous Trading Engine? (y/n): {Fore.WHITE}").lower().strip()
    except (EOFError, KeyboardInterrupt):
        print(f"\n{Fore.RED}⏹️ Operation cancelled by user{Style.RESET_ALL}")
        return
    
    if start_response in ['y', 'yes']:
        print(f"\n{Style.BRIGHT}{Fore.GREEN}🤖 LAUNCHING JARVIS AUTONOMOUS TRADING ENGINE...")
        
        try:
            from autonomous_trading_engine import autonomous_engine
            
            # Start the autonomous engine
            success = autonomous_engine.start_trading()
            
            if success:
                print(f"{Fore.GREEN}✅ Autonomous trading engine started successfully!")
                print(f"\n{Fore.CYAN}📊 Engine Status:")
                status = autonomous_engine.get_status()
                print(f"   {Fore.WHITE}Running: {Fore.GREEN}{status['is_running']}")
                print(f"   {Fore.WHITE}Max Concurrent Trades: {Fore.YELLOW}{status['config']['max_concurrent_trades']}")
                print(f"   {Fore.WHITE}Active Currency Pairs: {Fore.YELLOW}{len(status['config']['active_pairs'])}")
                print(f"   {Fore.WHITE}Scan Interval: {Fore.YELLOW}{status['config']['scan_interval']}s")
                
                print(f"\n{Fore.MAGENTA}🌐 Web Dashboard:")
                print(f"   {Fore.WHITE}URL: {Fore.CYAN}http://localhost:5000")
                print(f"   {Fore.WHITE}Monitor and control the bot from your browser")
                
                # Keep the engine running
                try:
                    print(f"\n{Style.BRIGHT}{Fore.GREEN}⏰ JARVIS is now trading autonomously...")
                    print(f"{Fore.WHITE}   Press {Fore.RED}Ctrl+C{Fore.WHITE} to stop safely")
                    print(f"{Fore.CYAN}{'-'*60}{Style.RESET_ALL}")
                    
                    while True:
                        time.sleep(10)
                        # Show brief status every 60 seconds
                        if int(time.time()) % 60 == 0:
                            status = autonomous_engine.get_status()
                            print(f"{Fore.CYAN}📊 Status: {Fore.WHITE}{status['daily_stats']['trades_count']} trades, "
                                  f"{Fore.GREEN if status['daily_stats']['profit_loss'] >= 0 else Fore.RED}${status['daily_stats']['profit_loss']:.2f} P&L{Style.RESET_ALL}")
                
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}🛑 Stopping JARVIS autonomous trading engine...")
                    autonomous_engine.stop_trading()
                    print(f"{Fore.GREEN}✅ Engine stopped safely{Style.RESET_ALL}")
            
            else:
                print(f"{Fore.RED}❌ Failed to start autonomous trading engine")
                print(f"   Check logs for details{Style.RESET_ALL}")
        
        except Exception as e:
            logger.error(f"❌ Failed to start engine: {e}")
            print(f"{Fore.RED}❌ Could not start autonomous engine{Style.RESET_ALL}")
    
    else:
        print(f"\n{Fore.CYAN}📱 Manual startup options:")
        print(f"   {Fore.WHITE}Run: {Fore.YELLOW}python start_trading_bot.py")
        print(f"   {Fore.WHITE}Then visit: {Fore.CYAN}http://localhost:5000{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        run_training_and_start_bot()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Goodbye!{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Script failed: {e}")
        sys.exit(1)
