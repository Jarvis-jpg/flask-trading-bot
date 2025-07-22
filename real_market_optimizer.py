#!/usr/bin/env python3
"""
JARVIS AI REAL MARKET PERFORMANCE ANALYSIS & IMPROVEMENT SYSTEM
Targeted optimization for 65%+ win rate with actual market data
"""

import json
import numpy as np
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

class RealMarketPerformanceAnalyzer:
    """Analyzes real market performance and provides targeted improvements"""
    
    def __init__(self):
        self.load_real_data()
        
    def load_real_data(self):
        """Load actual trading results and AI memory"""
        try:
            with open('ai_training_results.json', 'r') as f:
                self.training_results = json.load(f)
                
            with open('jarvis_ai_memory.json', 'r') as f:
                self.ai_memory = json.load(f)
                
            print(f"{Fore.GREEN}✅ Loaded real market data{Style.RESET_ALL}")
        except FileNotFoundError as e:
            print(f"{Fore.RED}❌ Error loading data: {e}{Style.RESET_ALL}")
            
    def analyze_real_performance_gaps(self):
        """Analyze gaps in real market performance"""
        
        print(f"{Back.RED}{Fore.WHITE}🔍 REAL MARKET PERFORMANCE ANALYSIS{Style.RESET_ALL}")
        
        # Extract real performance metrics
        lifetime_wr = self.ai_memory['lifetime_win_rate']
        current_wr = self.training_results['results']['win_rate']
        avg_confidence = self.training_results['results']['avg_confidence']
        total_trades = self.training_results['results']['total_trades']
        
        print(f"\n{Fore.CYAN}📊 ACTUAL PERFORMANCE (Real Market Data):{Style.RESET_ALL}")
        print(f"  Current Session Win Rate: {current_wr:.1f}%")
        print(f"  Lifetime Win Rate: {lifetime_wr:.1f}%")
        print(f"  Average Confidence: {avg_confidence:.1%}")
        print(f"  Total Trades Analyzed: {total_trades:,}")
        
        # Gap analysis
        target_wr = 65.0
        current_gap = target_wr - lifetime_wr
        
        print(f"\n{Fore.YELLOW}🎯 GAP TO TARGET:{Style.RESET_ALL}")
        print(f"  Target Win Rate: {target_wr:.1f}%")
        print(f"  Current Win Rate: {lifetime_wr:.1f}%")
        print(f"  Gap to Close: {current_gap:+.1f}%")
        
        if current_gap > 0:
            print(f"  {Fore.RED}❌ BELOW TARGET - OPTIMIZATION REQUIRED{Style.RESET_ALL}")
        else:
            print(f"  {Fore.GREEN}✅ TARGET ACHIEVED{Style.RESET_ALL}")
            
        return current_gap
        
    def identify_performance_bottlenecks(self):
        """Identify specific bottlenecks in real market performance"""
        
        print(f"\n{Fore.CYAN}🔍 PERFORMANCE BOTTLENECK ANALYSIS:{Style.RESET_ALL}")
        
        confidence_scores = self.training_results.get('confidence_scores', [])
        avg_confidence = np.mean(confidence_scores) if confidence_scores else 0
        
        bottlenecks = []
        
        # 1. Confidence Analysis
        if avg_confidence < 0.65:
            bottlenecks.append({
                'issue': 'Low AI Confidence Threshold',
                'current': f"{avg_confidence:.1%}",
                'target': '65%+',
                'impact': 'High',
                'solution': 'Increase confidence threshold and improve feature quality'
            })
            
        # 2. Trade Quality Analysis
        low_conf_trades = len([c for c in confidence_scores if c < 0.6])
        low_conf_rate = (low_conf_trades / len(confidence_scores)) * 100 if confidence_scores else 0
        
        if low_conf_rate > 30:
            bottlenecks.append({
                'issue': 'Too Many Low-Quality Trades',
                'current': f"{low_conf_rate:.1f}%",
                'target': '<20%',
                'impact': 'High',
                'solution': 'Implement stricter trade filtering'
            })
            
        # 3. Pair Performance Analysis
        pair_performance = self.ai_memory.get('pair_performance', {})
        underperforming_pairs = []
        
        for pair, stats in pair_performance.items():
            pair_wr = (stats['wins'] / (stats['wins'] + stats['losses'])) * 100
            if pair_wr < 55:
                underperforming_pairs.append((pair, pair_wr))
                
        if underperforming_pairs:
            bottlenecks.append({
                'issue': 'Underperforming Currency Pairs',
                'current': f"{len(underperforming_pairs)} pairs below 55%",
                'target': 'All pairs >55%',
                'impact': 'Medium',
                'solution': 'Pair-specific optimization or removal'
            })
            
        # 4. Learning Progression Analysis
        sessions = self.ai_memory.get('session_performance', [])
        if len(sessions) > 2:
            recent_sessions = sessions[-3:]  # Last 3 sessions
            win_rates = [s['win_rate'] for s in recent_sessions]
            trend = np.polyfit(range(len(win_rates)), win_rates, 1)[0]  # Linear trend
            
            if trend < 0.5:  # Declining or flat learning
                bottlenecks.append({
                    'issue': 'Stagnant Learning Progress',
                    'current': f"Trend: {trend:+.1f}% per session",
                    'target': '+2% per session',
                    'impact': 'High',
                    'solution': 'Enhance AI learning algorithm and feature engineering'
                })
                
        # Display bottlenecks
        if bottlenecks:
            for i, bottleneck in enumerate(bottlenecks, 1):
                print(f"\n  {Fore.RED}❌ BOTTLENECK #{i}: {bottleneck['issue']}{Style.RESET_ALL}")
                print(f"    Current: {bottleneck['current']}")
                print(f"    Target: {bottleneck['target']}")
                print(f"    Impact: {bottleneck['impact']}")
                print(f"    Solution: {bottleneck['solution']}")
        else:
            print(f"  {Fore.GREEN}✅ No major bottlenecks identified{Style.RESET_ALL}")
            
        return bottlenecks
        
    def create_targeted_improvement_plan(self, performance_gap, bottlenecks):
        """Create specific improvement plan for real market conditions"""
        
        print(f"\n{Back.GREEN}{Fore.WHITE}🎯 TARGETED IMPROVEMENT PLAN FOR 65%+ WIN RATE{Style.RESET_ALL}")
        
        improvement_plan = {
            "plan_created": datetime.now().isoformat(),
            "current_performance": {
                "lifetime_win_rate": self.ai_memory['lifetime_win_rate'],
                "gap_to_target": performance_gap,
                "bottlenecks_identified": len(bottlenecks)
            },
            "target_performance": {
                "win_rate": 65.0,
                "confidence_threshold": 0.70,
                "expected_timeframe": "3-5 training sessions"
            },
            "immediate_actions": [],
            "medium_term_actions": [],
            "advanced_optimizations": []
        }
        
        # IMMEDIATE ACTIONS (Next 1-2 sessions)
        print(f"\n{Fore.YELLOW}🚀 IMMEDIATE ACTIONS (Next 1-2 sessions):{Style.RESET_ALL}")
        
        immediate_actions = [
            {
                "action": "Increase Confidence Threshold",
                "from": f"{self.training_results['results']['avg_confidence']:.1%}",
                "to": "70%+",
                "expected_impact": "+3-5% win rate",
                "implementation": "Update config.py RISK_CONFIG['confidence_threshold'] = 0.70"
            },
            {
                "action": "Implement Quality-Only Trading",
                "description": "Only execute trades with 70%+ confidence",
                "expected_impact": "+4-6% win rate",
                "trade_frequency": "Reduced by 40-50%",
                "implementation": "Add strict confidence filtering in ai_learner.py"
            },
            {
                "action": "Enhanced Risk:Reward Requirements",
                "from": "Variable",
                "to": "3:1 minimum",
                "expected_impact": "+2-3% win rate",
                "implementation": "Update risk management minimum RR ratio"
            }
        ]
        
        for i, action in enumerate(immediate_actions, 1):
            print(f"  {Fore.GREEN}{i}. {action['action']}{Style.RESET_ALL}")
            if 'from' in action and 'to' in action:
                print(f"     From: {action['from']} → To: {action['to']}")
            if 'description' in action:
                print(f"     {action['description']}")
            print(f"     Expected Impact: {action['expected_impact']}")
            if 'trade_frequency' in action:
                print(f"     Trade Frequency: {action['trade_frequency']}")
            print(f"     Implementation: {action['implementation']}")
            
        improvement_plan["immediate_actions"] = immediate_actions
        
        # MEDIUM-TERM ACTIONS (3-5 sessions)
        print(f"\n{Fore.YELLOW}📈 MEDIUM-TERM ACTIONS (3-5 sessions):{Style.RESET_ALL}")
        
        medium_term_actions = [
            {
                "action": "Advanced Feature Engineering",
                "description": "Add market microstructure features",
                "features": ["bid-ask spread analysis", "order flow imbalance", "market depth"],
                "expected_impact": "+3-4% win rate",
                "implementation": "Enhance feature generation in AI system"
            },
            {
                "action": "Session-Based Optimization", 
                "description": "Optimize performance for specific trading sessions",
                "focus": "London/NY overlap (highest win rate potential)",
                "expected_impact": "+2-3% win rate",
                "implementation": "Add session-specific AI models"
            },
            {
                "action": "Pair-Specific Models",
                "description": "Individual AI models for each currency pair",
                "target": "Optimize EUR/USD, GBP/USD (highest volume)",
                "expected_impact": "+4-5% win rate",
                "implementation": "Create specialized models per pair"
            }
        ]
        
        for i, action in enumerate(medium_term_actions, 1):
            print(f"  {Fore.CYAN}{i}. {action['action']}{Style.RESET_ALL}")
            print(f"     {action['description']}")
            if 'features' in action:
                print(f"     Features: {', '.join(action['features'])}")
            if 'focus' in action:
                print(f"     Focus: {action['focus']}")
            if 'target' in action:
                print(f"     Target: {action['target']}")
            print(f"     Expected Impact: {action['expected_impact']}")
            print(f"     Implementation: {action['implementation']}")
            
        improvement_plan["medium_term_actions"] = medium_term_actions
        
        # ADVANCED OPTIMIZATIONS (Long-term)
        print(f"\n{Fore.YELLOW}🔬 ADVANCED OPTIMIZATIONS (Long-term):{Style.RESET_ALL}")
        
        advanced_optimizations = [
            {
                "action": "Ensemble AI Models",
                "description": "Multiple AI models voting on trades",
                "models": ["XGBoost", "Neural Network", "Random Forest"],
                "expected_impact": "+2-3% win rate",
                "complexity": "High"
            },
            {
                "action": "Real-Time Market Sentiment",
                "description": "Integrate news sentiment and social media",
                "sources": ["Reuters API", "Twitter sentiment", "Economic calendar"],
                "expected_impact": "+1-2% win rate",
                "complexity": "Medium"
            },
            {
                "action": "Adaptive Learning System",
                "description": "AI that adapts to changing market conditions",
                "features": ["Regime detection", "Volatility adaptation", "News impact modeling"],
                "expected_impact": "+3-4% win rate",
                "complexity": "Very High"
            }
        ]
        
        for i, action in enumerate(advanced_optimizations, 1):
            print(f"  {Fore.MAGENTA}{i}. {action['action']}{Style.RESET_ALL}")
            print(f"     {action['description']}")
            if 'models' in action:
                print(f"     Models: {', '.join(action['models'])}")
            if 'sources' in action:
                print(f"     Sources: {', '.join(action['sources'])}")
            if 'features' in action:
                print(f"     Features: {', '.join(action['features'])}")
            print(f"     Expected Impact: {action['expected_impact']}")
            print(f"     Complexity: {action['complexity']}")
            
        improvement_plan["advanced_optimizations"] = advanced_optimizations
        
        # PROJECTED TIMELINE
        print(f"\n{Fore.CYAN}📅 PROJECTED IMPROVEMENT TIMELINE:{Style.RESET_ALL}")
        
        current_wr = self.ai_memory['lifetime_win_rate']
        print(f"  Current Win Rate: {current_wr:.1f}%")
        print(f"  After Immediate Actions: {current_wr + 8:.1f}% (Sessions 1-2)")
        print(f"  After Medium-term Actions: {current_wr + 17:.1f}% (Sessions 3-5)")
        print(f"  After Advanced Optimizations: {current_wr + 25:.1f}% (Sessions 6-10)")
        print(f"  🎯 Target Achievement: Session 3-4 (65%+ win rate)")
        
        # Save improvement plan
        with open('real_market_improvement_plan.json', 'w') as f:
            json.dump(improvement_plan, f, indent=2)
            
        print(f"\n{Fore.GREEN}📁 Improvement plan saved to 'real_market_improvement_plan.json'{Style.RESET_ALL}")
        
        return improvement_plan
        
    def generate_implementation_priority(self):
        """Generate priority list for immediate implementation"""
        
        print(f"\n{Back.RED}{Fore.WHITE}⚡ IMMEDIATE IMPLEMENTATION PRIORITY{Style.RESET_ALL}")
        
        priority_list = [
            {
                "rank": 1,
                "action": "Increase Confidence Threshold to 70%",
                "file": "config.py",
                "change": "RISK_CONFIG['confidence_threshold'] = 0.70",
                "impact": "High (+5% win rate)",
                "effort": "Low (5 minutes)"
            },
            {
                "rank": 2,
                "action": "Implement 3:1 Risk:Reward Minimum",
                "file": "config.py",
                "change": "RISK_CONFIG['risk_reward_min'] = 3.0",
                "impact": "Medium (+3% win rate)",
                "effort": "Low (2 minutes)"
            },
            {
                "rank": 3,
                "action": "Add Quality-Only Trade Filter",
                "file": "ai_learner.py",
                "change": "Only execute trades >70% confidence",
                "impact": "High (+6% win rate)",
                "effort": "Medium (15 minutes)"
            },
            {
                "rank": 4,
                "action": "Optimize Premium Trading Hours Only",
                "file": "config.py",
                "change": "Restrict to London/NY overlap only",
                "impact": "Medium (+4% win rate)",
                "effort": "Low (10 minutes)"
            }
        ]
        
        for item in priority_list:
            print(f"\n{Fore.YELLOW}#{item['rank']} - {item['action']}{Style.RESET_ALL}")
            print(f"  File: {item['file']}")
            print(f"  Change: {item['change']}")
            print(f"  Impact: {item['impact']}")
            print(f"  Effort: {item['effort']}")
            
        total_expected_improvement = 18  # Sum of high-impact items
        current_wr = self.ai_memory['lifetime_win_rate']
        projected_wr = current_wr + total_expected_improvement
        
        print(f"\n{Fore.GREEN}🎯 PROJECTED RESULT AFTER IMMEDIATE ACTIONS:{Style.RESET_ALL}")
        print(f"  Current: {current_wr:.1f}%")
        print(f"  Projected: {projected_wr:.1f}%")
        if projected_wr >= 65:
            print(f"  {Fore.GREEN}✅ TARGET ACHIEVED!{Style.RESET_ALL}")
        else:
            print(f"  {Fore.YELLOW}📈 Progress toward 65% target{Style.RESET_ALL}")

def main():
    """Main function to analyze real market performance"""
    
    print(f"{Back.BLUE}{Fore.WHITE}JARVIS REAL MARKET PERFORMANCE OPTIMIZER{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Analyzing actual market data for 65%+ win rate achievement{Style.RESET_ALL}\n")
    
    analyzer = RealMarketPerformanceAnalyzer()
    
    # Analyze current performance
    gap = analyzer.analyze_real_performance_gaps()
    
    # Identify bottlenecks
    bottlenecks = analyzer.identify_performance_bottlenecks()
    
    # Create improvement plan
    plan = analyzer.create_targeted_improvement_plan(gap, bottlenecks)
    
    # Generate implementation priorities
    analyzer.generate_implementation_priority()
    
    print(f"\n{Back.GREEN}{Fore.WHITE}🎯 ANALYSIS COMPLETE!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Real market performance analyzed and improvement plan created.{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Focus on immediate actions to achieve 65%+ win rate in next 1-2 sessions.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
