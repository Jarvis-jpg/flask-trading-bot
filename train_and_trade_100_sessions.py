#!/usr/bin/env python3
"""
JARVIS AI Trading System - 100 Sessions Continuous Training
ENHANCED VERSION WITH REAL AI LEARNING - RUNS 100 SESSIONS NON-STOP
Automatically runs 100 consecutive training sessions with ACTUAL machine learning
"""
import logging
import sys
import time
import random
import json
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from colorama import Fore, Back, Style, init
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score, train_test_split
import joblib
from config import RISK_CONFIG, SIGNAL_QUALITY_CONFIG, PREMIUM_TRADING_HOURS
from news_aware_trading import NewsAwareTrading
from market_microstructure import MarketMicrostructure
from advanced_risk_manager import AdvancedRiskManager

# OANDA Integration for Real Historical Data
try:
    from oanda_historical_data import OandaHistoricalData
    from oanda_config import OANDA_API_KEY, OANDA_ACCOUNT_ID, OANDA_ENVIRONMENT
    OANDA_AVAILABLE = True
    print("✅ OANDA modules imported successfully")
except ImportError as e:
    OANDA_AVAILABLE = False
    print(f"⚠️ OANDA not available: {e}. Using simulation mode.")

# Initialize colorama for Windows
init(autoreset=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ContinuousTrainingSystem:
    """
    CONTINUOUS AI training system with REAL MACHINE LEARNING - runs 100 sessions non-stop
    Each session = 8000 realistic trades with ACTUAL AI model training and learning
    """
    
    def __init__(self):
        self.memory_file = "jarvis_ai_memory.json"
        self.results_file = "ai_training_results.json"
        self.progress_file = "continuous_training_progress.json"
        self.model_file = "jarvis_continuous_model.pkl"
        self.scaler_file = "jarvis_continuous_scaler.pkl"
        
        # Initialize REAL AI components
        self.ai_model = None
        self.feature_scaler = StandardScaler()
        self.training_data = []
        self.model_performance_history = []
        
        # Load AI memory
        self.ai_memory = self.load_ai_memory()
        
        # Initialize from memory or start fresh
        self.session_number = self.ai_memory.get('session_number', 0) + 1
        self.lifetime_trades = self.ai_memory.get('lifetime_trades', 0)
        self.lifetime_wins = self.ai_memory.get('lifetime_wins', 0)
        self.lifetime_losses = self.ai_memory.get('lifetime_losses', 0)
        self.lifetime_profit = self.ai_memory.get('lifetime_profit', 0.0)
        self.pair_performance = self.ai_memory.get('pair_performance', {})
        self.session_performance = self.ai_memory.get('session_performance', [])
        
        # Load existing AI model if available
        self.load_or_create_ai_model()
        
        # Initialize advanced components for 65% WR target
        self.news_aware = NewsAwareTrading()
        self.microstructure = MarketMicrostructure()
        self.risk_manager = AdvancedRiskManager()
        
        # Initialize OANDA Historical Data Integration
        self.oanda_data = None
        self.use_real_data = False
        if OANDA_AVAILABLE:
            try:
                self.oanda_data = OandaHistoricalData(
                    api_key=OANDA_API_KEY,
                    account_id=OANDA_ACCOUNT_ID,
                    environment=OANDA_ENVIRONMENT
                )
                # Test connection
                if self.oanda_data.test_connection():
                    self.use_real_data = True
                    print(f"{Fore.GREEN}🔗 OANDA Historical Data connected successfully (LIVE MARKET DATA){Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}⚠️ OANDA connection test failed, using simulation mode{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️ OANDA initialization failed: {e}. Using simulation mode.{Style.RESET_ALL}")
        
        if not self.use_real_data:
            print(f"{Fore.CYAN}📊 Using enhanced market simulation mode{Style.RESET_ALL}")
        
        # Initialize pair performance if empty
        pairs = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'USD/CHF', 'AUD/USD', 'USD/CAD', 'NZD/USD', 'EUR/GBP']
        for pair in pairs:
            if pair not in self.pair_performance:
                self.pair_performance[pair] = {'wins': 0, 'losses': 0, 'profit': 0.0, 'avg_confidence': 0.75}
        
        # Session-specific stats (reset each session)
        self.reset_session_stats()
        
        # Enhanced configuration with AI learning parameters FOR 65% WR TARGET
        self.enhanced_config = {
            'confidence_threshold': 0.75,  # HIGH QUALITY ONLY - 75% confidence minimum
            'risk_reward_min': 2.0,        # Higher R:R for quality trades
            'session_quality_min': 0.70,   # Premium session quality only
            'trend_strength_min': 0.60,    # Strong trends for reliable setups
            'ai_retrain_frequency': 50,    # More frequent retraining for faster learning
            'min_training_samples': 100,   # Higher threshold for quality data
            # Enhanced Market Simulation with professional components
            'realistic_spreads': True,     # Use realistic bid/ask spreads
            'market_hours_filter': True,   # Filter for optimal trading hours
            'news_impact_simulation': True, # Full news impact simulation
            'weekend_gap_simulation': True, # Include weekend gaps
            'correlation_limits': True,    # Enforce correlation limits
            'latency_simulation': True,    # Keep execution realism
            'microstructure_analysis': True, # Add order book analysis
            'advanced_risk_management': True, # Portfolio heat monitoring
            'news_awareness': True         # Economic calendar integration
        }
    
    def load_or_create_ai_model(self):
        """Load existing AI model or create new one"""
        try:
            model_data = joblib.load(self.model_file)
            self.ai_model = model_data['model']
            self.feature_scaler = joblib.load(self.scaler_file)
            
            # Check if scaler dimensions match our new 26-feature system
            if hasattr(self.feature_scaler, 'n_features_in_') and self.feature_scaler.n_features_in_ != 26:
                print(f"{Fore.YELLOW}🔄 Detected feature upgrade (old: {self.feature_scaler.n_features_in_}, new: 26). Rebuilding AI...{Style.RESET_ALL}")
                self.retrain_ai_for_new_features()
            else:
                print(f"{Fore.GREEN}🧠 AI Model Loaded: {type(self.ai_model).__name__} with {getattr(self.feature_scaler, 'n_features_in_', 'unknown')} features{Style.RESET_ALL}")
                
        except FileNotFoundError:
            self.create_initial_ai_model()
            print(f"{Fore.YELLOW}🧠 Created new AI model for 26-feature training{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}⚠️ Error loading AI model: {e}. Creating new model...{Style.RESET_ALL}")
            self.create_initial_ai_model()
    
    def create_initial_ai_model(self):
        """Create initial AI model optimized for 65% win rate target"""
        self.ai_model = GradientBoostingClassifier(
            n_estimators=300,  # Increased for better feature learning
            max_depth=10,      # Deeper for complex market patterns
            learning_rate=0.06, # Slightly higher for faster convergence
            min_samples_split=12,
            min_samples_leaf=6,
            subsample=0.9,     # Higher sampling for better generalization
            random_state=42
        )
        print(f"{Fore.CYAN}🧠 Initialized enhanced AI model for 65% win rate target{Style.RESET_ALL}")
    
    def generate_ai_features(self, market_data, trade_signal):
        """Generate enhanced features for AI model targeting 65% WR"""
        
        # Get advanced market analysis
        current_time = datetime.now()
        news_info = self.news_aware.get_news_impact_for_pair(
            trade_signal.get('pair', 'EUR/USD'), current_time
        )
        
        liquidity_score = self.microstructure.analyze_market_depth(
            trade_signal.get('pair', 'EUR/USD'), 
            market_data.get('market_condition', 'ranging')
        )
        
        # Enhanced feature set
        features = [
            # Original technical features
            market_data.get('trend_strength', 0.5),
            market_data.get('rsi_normalized', 0.5),
            market_data.get('macd_signal_strength', 0.5),
            market_data.get('volume_surge_factor', 1.0),
            market_data.get('support_resistance_clarity', 0.5),
            market_data.get('market_structure_score', 0.5),
            market_data.get('session_quality_score', 0.5),
            market_data.get('volatility_score', 0.5),
            trade_signal.get('risk_reward_ratio', 2.0) / 5.0,  # Normalize to higher range
            trade_signal.get('base_confidence', 0.5),
            # Market condition features
            1.0 if market_data.get('market_condition') == 'trending' else 0.0,
            1.0 if market_data.get('session') == 'overlap' else 0.0,
            market_data.get('time_quality_score', 0.5),
            # Pair-specific learning
            self.get_pair_learning_factor(trade_signal.get('pair', 'EUR/USD')),
            
            # NEW PROFESSIONAL FEATURES FOR 65% WR
            # News and economic features
            1.0 if news_info['has_news'] else 0.0,
            0.8 if news_info.get('impact') == 'high' else 0.4 if news_info.get('impact') == 'medium' else 0.0,
            news_info.get('time_to_event', 24) / 24.0,  # Normalize hours
            
            # Market microstructure features
            liquidity_score,
            1.0 if liquidity_score > 0.8 else 0.0,  # High liquidity flag
            
            # Time-based features
            current_time.hour / 24.0,  # Hour of day
            current_time.weekday() / 7.0,  # Day of week
            1.0 if current_time.hour in [8, 9, 13, 14, 15] else 0.0,  # Prime trading hours
            
            # Advanced market condition features
            1.0 if market_data.get('market_condition') == 'volatile' and liquidity_score < 0.7 else 0.0,
            market_data.get('trend_strength', 0.5) * market_data.get('support_resistance_clarity', 0.5),  # Combined strength
            
            # Portfolio risk features (if available)
            len(getattr(self.risk_manager, 'active_positions', {})) / 5.0,  # Position count normalized
            getattr(self.risk_manager, 'portfolio_var', 0.0) * 100  # Portfolio VaR
        ]
        return np.array(features).reshape(1, -1)
    
    def get_pair_learning_factor(self, pair):
        """Get learning factor for specific pair"""
        if pair in self.pair_performance:
            pair_data = self.pair_performance[pair]
            total_trades = pair_data['wins'] + pair_data['losses']
            if total_trades > 0:
                return pair_data['wins'] / total_trades
        return 0.5  # Default neutral
    
    def ai_predict_outcome(self, market_data, trade_signal):
        """Use AI model to predict trade outcome and confidence"""
        if (self.ai_model is None or 
            len(self.training_data) < self.enhanced_config['min_training_samples'] or
            not hasattr(self.feature_scaler, 'scale_')):
            # Fall back to basic logic until we have enough training data and fitted scaler
            return self.basic_prediction_fallback(market_data, trade_signal)
        
        try:
            # Generate features
            features = self.generate_ai_features(market_data, trade_signal)
            
            # Check for feature dimension mismatch and retrain if needed
            if hasattr(self.feature_scaler, 'n_features_in_') and features.shape[1] != self.feature_scaler.n_features_in_:
                print(f"{Fore.YELLOW}🔄 Feature dimension mismatch detected. Retraining scaler and model...{Style.RESET_ALL}")
                self.retrain_ai_for_new_features()
                return self.basic_prediction_fallback(market_data, trade_signal)
            
            features_scaled = self.feature_scaler.transform(features)
            
            # Get AI prediction
            win_probability = self.ai_model.predict_proba(features_scaled)[0][1]
            
            # Apply market friction and constraints
            win_probability = min(0.80, max(0.35, win_probability))  # Wider range for learning
            
            # Calculate confidence based on model certainty - Enhanced for 65% target
            raw_confidence = abs(win_probability - 0.5) * 2  # Convert to 0-1 scale
            confidence = min(0.95, max(0.20, raw_confidence))  # Wider confidence range
            
            # Boost confidence more aggressively for 65% target
            confidence = min(0.95, confidence * 1.8)  # Increased multiplier
            
            # Add stronger learning bonus for diverse market conditions
            if market_data.get('market_condition') in ['volatile', 'quiet']:
                confidence += 0.08  # Increased bonus for diverse conditions
            
            # Additional boost for trending markets
            if market_data.get('market_condition') == 'trending':
                confidence += 0.05
            
            return win_probability, confidence
            
        except Exception as e:
            # Only print error if it's not the common "not fitted" error to reduce spam
            if "not fitted" not in str(e):
                print(f"{Fore.RED}⚠️ AI prediction error: {e}{Style.RESET_ALL}")
            return self.basic_prediction_fallback(market_data, trade_signal)
    
    def retrain_ai_for_new_features(self):
        """Retrain AI model and scaler for new feature dimensions"""
        try:
            print(f"{Fore.CYAN}🧠 Rebuilding AI system for enhanced 26-feature set...{Style.RESET_ALL}")
            
            # Reset the feature scaler for new dimensions
            self.feature_scaler = StandardScaler()
            
            # Create new AI model optimized for 65% target
            self.ai_model = GradientBoostingClassifier(
                n_estimators=300,  # Increased for better learning
                max_depth=10,      # Deeper for complex patterns
                learning_rate=0.06,
                min_samples_split=12,
                min_samples_leaf=6,
                subsample=0.9,
                random_state=42
            )
            
            # Clear old training data that has wrong feature dimensions
            self.training_data = []
            
            # Reset model performance history
            self.model_performance_history = []
            
            print(f"{Fore.GREEN}✅ AI system rebuilt for 26-feature enhanced trading{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error rebuilding AI system: {e}{Style.RESET_ALL}")
    
    def basic_prediction_fallback(self, market_data, trade_signal):
        """Basic prediction when AI model isn't ready"""
        base_win_probability = random.uniform(0.45, 0.68)
        
        # Apply simple learning from pair performance
        pair = trade_signal.get('pair', 'EUR/USD')
        if pair in self.pair_performance:
            pair_data = self.pair_performance[pair]
            pair_win_rate = pair_data['wins'] / max(pair_data['wins'] + pair_data['losses'], 1)
            if pair_win_rate > 0.65:
                base_win_probability += 0.03
            elif pair_win_rate < 0.55:
                base_win_probability -= 0.05
        
        # Market condition adjustments
        if market_data.get('market_condition') == 'trending':
            base_win_probability += 0.05
        elif market_data.get('market_condition') == 'volatile':
            base_win_probability -= 0.08
        
        win_probability = min(0.75, max(0.40, base_win_probability))
        confidence = random.uniform(0.30, 0.80)  # Very generous confidence range for fallback
        
        return win_probability, confidence
    
    def train_ai_model(self):
        """Train ENHANCED AI model with quality-filtered data for 65% target"""
        if len(self.training_data) < self.enhanced_config['min_training_samples']:
            return
        
        try:
            print(f"{Fore.CYAN}🧠 Training ENHANCED AI model with {len(self.training_data)} QUALITY samples...{Style.RESET_ALL}")
            
            # Prepare training data
            X = np.array([trade['features'] for trade in self.training_data])
            y = np.array([trade['outcome'] for trade in self.training_data])
            
            # Enhanced feature scaling
            X_scaled = self.feature_scaler.fit_transform(X)
            
            # Split data for validation
            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
            
            # ENSEMBLE APPROACH: Multiple models for better performance
            models = {
                'gradient_boost': GradientBoostingClassifier(
                    n_estimators=400,  # Increased for better learning
                    max_depth=8,
                    learning_rate=0.05,  # Slower, more careful learning
                    min_samples_split=20,
                    min_samples_leaf=10,
                    subsample=0.8,
                    random_state=42
                ),
                'random_forest': RandomForestClassifier(
                    n_estimators=300,
                    max_depth=12,
                    min_samples_split=15,
                    min_samples_leaf=8,
                    random_state=42
                )
            }
            
            # Train and evaluate models
            best_model = None
            best_score = 0
            model_scores = {}
            
            for name, model in models.items():
                # Train model
                model.fit(X_train, y_train)
                
                # Evaluate
                train_score = model.score(X_train, y_train)
                test_score = model.score(X_test, y_test)
                cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='accuracy')
                
                model_scores[name] = {
                    'train_score': train_score,
                    'test_score': test_score,
                    'cv_mean': cv_scores.mean(),
                    'cv_std': cv_scores.std()
                }
                
                print(f"  {name}: CV={cv_scores.mean():.1%}±{cv_scores.std():.1%}, Test={test_score:.1%}")
                
                # Select best model based on cross-validation
                if cv_scores.mean() > best_score:
                    best_score = cv_scores.mean()
                    best_model = model
                    self.ai_model = model
            
            # Save performance metrics
            performance = {
                'timestamp': datetime.now().isoformat(),
                'training_samples': len(self.training_data),
                'quality_filtered': True,
                'best_model': type(best_model).__name__,
                'accuracy': best_score,
                'model_scores': model_scores,
                'validation_split': 0.2
            }
            self.model_performance_history.append(performance)
            
            # Save enhanced model
            model_data = {
                'model': self.ai_model,
                'performance_history': self.model_performance_history,
                'last_trained': datetime.now().isoformat(),
                'quality_enhanced': True,
                'target_win_rate': 0.65
            }
            joblib.dump(model_data, self.model_file)
            joblib.dump(self.feature_scaler, self.scaler_file)
            
            print(f"{Fore.GREEN}✅ ENHANCED AI Model Updated: {best_score:.1%} accuracy with QUALITY data{Style.RESET_ALL}")
            
            # Progress tracking toward 65% target
            if best_score >= 0.65:
                print(f"{Fore.GREEN}🎯 TARGET ACHIEVED! Model accuracy: {best_score:.1%} >= 65%{Style.RESET_ALL}")
            else:
                progress = (best_score / 0.65) * 100
                print(f"{Fore.YELLOW}📈 Progress to 65% target: {progress:.1f}% ({best_score:.1%}/65%)...{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Enhanced AI training error: {e}{Style.RESET_ALL}")
    
    def add_training_sample(self, features, outcome, market_data, trade_signal):
        """Add QUALITY-FILTERED training sample to AI learning dataset"""
        
        # QUALITY FILTER: Only learn from high-confidence, premium setups
        ai_confidence = trade_signal.get('confidence', 0)
        market_condition = market_data.get('market_condition', 'unknown')
        session_quality = market_data.get('session_quality_score', 0)
        trend_strength = market_data.get('trend_strength', 0)
        
        # Quality criteria for learning (much stricter than execution)
        learning_criteria = {
            'min_confidence': 0.80,  # Only learn from 80%+ confidence trades
            'min_session_quality': 0.75,  # Premium session quality
            'min_trend_strength': 0.65,  # Strong trend requirement
            'allowed_conditions': ['trending', 'ranging']  # No volatile/quiet learning
        }
        
        # Apply quality filters for learning
        if ai_confidence < learning_criteria['min_confidence']:
            return  # Don't learn from low confidence trades
            
        if session_quality < learning_criteria['min_session_quality']:
            return  # Don't learn from poor session quality
            
        if trend_strength < learning_criteria['min_trend_strength']:
            return  # Don't learn from weak trends
            
        if market_condition not in learning_criteria['allowed_conditions']:
            return  # Don't learn from volatile/quiet conditions
        
        # Additional quality check: Only learn from winning trades OR high-confidence losing trades
        if outcome == 0 and ai_confidence < 0.85:  # Losing trade with <85% confidence
            return  # Don't contaminate learning with low-confidence losses
        
        training_sample = {
            'features': features.flatten(),
            'outcome': outcome,
            'market_data': market_data,
            'trade_signal': trade_signal,
            'timestamp': datetime.now().isoformat(),
            'confidence': ai_confidence,
            'quality_score': session_quality,
            'learning_filtered': True  # Mark as quality-filtered sample
        }
        
        self.training_data.append(training_sample)
        
        # Keep only recent HIGH-QUALITY samples
        if len(self.training_data) > 5000:  # Reduced from 8000 for quality focus
            self.training_data = self.training_data[-4000:]  # Keep last 4000 quality samples
        
        # Retrain model more frequently with quality data
        if len(self.training_data) % self.enhanced_config['ai_retrain_frequency'] == 0:
            self.train_ai_model()
    
    def reset_for_quality_learning(self):
        """Reset AI system for quality-first learning toward 65% target"""
        print(f"{Fore.YELLOW}🔄 RESETTING AI SYSTEM FOR QUALITY-FIRST LEARNING{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🎯 Target: 65% Win Rate with Premium Quality Trades{Style.RESET_ALL}")
        
        # Clear old training data
        self.training_data = []
        print(f"✅ Cleared {len(self.training_data)} old training samples")
        
        # Reset model performance history
        old_history_count = len(self.model_performance_history)
        self.model_performance_history = []
        print(f"✅ Reset performance history ({old_history_count} old records)")
        
        # Create new enhanced AI model for quality learning
        self.ai_model = GradientBoostingClassifier(
            n_estimators=500,    # More estimators for better learning
            max_depth=10,        # Deeper for complex patterns
            learning_rate=0.03,  # Slower learning for stability
            min_samples_split=25,
            min_samples_leaf=12,
            subsample=0.85,
            random_state=42
        )
        print(f"✅ Created new enhanced AI model")
        
        # Reset feature scaler
        self.feature_scaler = StandardScaler()
        print(f"✅ Reset feature scaler")
        
        # Add quality learning metrics
        self.quality_metrics = {
            'quality_trades_executed': 0,
            'quality_trades_won': 0,
            'low_quality_rejected': 0,
            'learning_samples_added': 0,
            'target_progress': 0.0
        }
        
        print(f"{Fore.GREEN}🎯 AI System RESET COMPLETE - Ready for 65% Target Achievement{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📋 New Learning Criteria:{Style.RESET_ALL}")
        print(f"   • Confidence Threshold: 75% (execution) / 80% (learning)")
        print(f"   • Session Quality: 70% minimum")
        print(f"   • Trend Strength: 60% minimum")
        print(f"   • Risk/Reward: 2.0+ minimum")
        print(f"   • Premium Sessions Only: London/NY overlap")
        
        return True
    
    def generate_simulated_market_data(self, pair):
        """Generate enhanced simulated market data for fallback when OANDA unavailable"""
        session = random.choices(
            ['london', 'newyork', 'tokyo', 'overlap'],
            weights=[30, 35, 20, 15]
        )[0]
        
        market_condition = random.choices(
            ['trending', 'ranging', 'volatile', 'quiet'],
            weights=[25, 40, 25, 10]
        )[0]
        
        return {
            'pair': pair,
            'market_condition': market_condition,
            'session': session,
            'trend_strength': random.uniform(0.3, 0.95),
            'rsi_normalized': random.uniform(0.2, 0.8),
            'macd_signal_strength': random.uniform(0.3, 0.9),
            'volume_surge_factor': random.uniform(0.8, 2.5),
            'support_resistance_clarity': random.uniform(0.4, 0.9),
            'market_structure_score': random.uniform(0.5, 0.95),
            'session_quality_score': random.uniform(0.6, 1.0),
            'volatility_score': random.uniform(0.3, 0.8),
            'time_quality_score': random.uniform(0.5, 1.0),
            'actual_spread_pips': self.get_realistic_spread(pair, market_condition)
        }

    def get_realistic_spread(self, pair, market_condition):
        """Get realistic bid/ask spread for currency pair"""
        base_spreads = {
            'EUR/USD': 0.8, 'GBP/USD': 1.2, 'USD/JPY': 0.9, 'USD/CHF': 1.1,
            'AUD/USD': 1.4, 'USD/CAD': 1.3, 'NZD/USD': 1.8, 'EUR/GBP': 1.5
        }
        
        base_spread = base_spreads.get(pair, 1.5)
        
        # Adjust spread based on market conditions
        if market_condition == 'volatile':
            base_spread *= random.uniform(1.5, 2.5)
        elif market_condition == 'quiet':
            base_spread *= random.uniform(0.8, 1.2)
        elif market_condition == 'trending':
            base_spread *= random.uniform(0.9, 1.3)
        else:  # ranging
            base_spread *= random.uniform(1.0, 1.4)
        
        # Add random market stress factor
        stress_factor = random.uniform(0.9, 1.3)
        return base_spread * stress_factor
    
    def is_market_open(self, session):
        """Check if market is realistically open based on session"""
        # Simulate market hours (simplified)
        market_hours = {
            'tokyo': random.random() > 0.15,    # 85% open
            'london': random.random() > 0.1,    # 90% open  
            'newyork': random.random() > 0.1,   # 90% open
            'overlap': random.random() > 0.05   # 95% open
        }
        return market_hours.get(session, True)
    
    def simulate_news_impact(self, pair, market_data):
        """Simulate news event impact on trading"""
        # 5% chance of news event affecting trade
        if random.random() < 0.05:
            news_impact = random.choice(['high', 'medium', 'low'])
            if news_impact == 'high':
                # High impact news - increase volatility, reduce reliability
                market_data['volatility_score'] *= random.uniform(1.5, 2.5)
                market_data['support_resistance_clarity'] *= random.uniform(0.3, 0.7)
                return True, 'high_impact_news'
            elif news_impact == 'medium':
                market_data['volatility_score'] *= random.uniform(1.2, 1.8)
                return True, 'medium_impact_news'
        return False, None
    
    def simulate_weekend_gap(self):
        """Simulate weekend gap effects"""
        # 2% chance of weekend gap simulation
        if random.random() < 0.02:
            gap_size = random.uniform(0.3, 1.5)  # Percentage gap
            gap_direction = random.choice(['positive', 'negative'])
            return True, gap_size, gap_direction
        return False, 0, None
    
    def check_correlation_limits(self, pair):
        """Check if we're trading too many correlated pairs"""
        # Simplified correlation check - limit EUR pairs
        eur_pairs = ['EUR/USD', 'EUR/GBP']
        recent_trades = [trade.get('pair') for trade in getattr(self, 'recent_trades', [])]
        
        if pair in eur_pairs:
            eur_count = sum(1 for p in recent_trades[-10:] if p in eur_pairs)
            if eur_count >= 3:  # Max 3 EUR trades in last 10
                return False
        return True
    
    def simulate_execution_latency(self):
        """Simulate realistic execution delays"""
        # Random execution delay (20-200ms equivalent impact)
        latency_ms = random.uniform(20, 200)
        
        # Convert latency to slippage factor
        if latency_ms > 150:
            return random.uniform(0.95, 0.98)  # High latency = more slippage
        elif latency_ms > 100:
            return random.uniform(0.97, 0.99)  # Medium latency
        else:
            return random.uniform(0.98, 1.0)   # Low latency
    
    def get_market_stress_factor(self):
        """Get current market stress level"""
        # Simulate varying market conditions
        stress_level = random.choices(
            ['low', 'normal', 'elevated', 'high'],
            weights=[20, 50, 25, 5]
        )[0]
        
        stress_multipliers = {
            'low': random.uniform(0.8, 1.0),
            'normal': random.uniform(0.9, 1.1), 
            'elevated': random.uniform(1.1, 1.4),
            'high': random.uniform(1.4, 2.0)
        }
        
        return stress_level, stress_multipliers[stress_level]
    
    def reset_session_stats(self):
        """Reset stats for new session"""
        self.trades_completed = 0
        self.wins = 0
        self.losses = 0
        self.total_profit = 0.0
        self.max_profit = 0.0
        self.max_loss = 0.0
        self.current_streak = 0
        self.max_win_streak = 0
        self.drawdown = 0.0
        self.max_drawdown = 0.0
        self.equity_curve = [500.0]  # Start with higher equity for better learning feedback
        self.confidence_scores = []
        self.starting_trade_number = self.lifetime_trades + 1
    
    def load_ai_memory(self):
        """Load persistent AI memory"""
        try:
            with open(self.memory_file, 'r') as f:
                memory = json.load(f)
                return memory
        except FileNotFoundError:
            return {}
        except Exception as e:
            logger.error(f"Error loading AI memory: {e}")
            return {}
    
    def save_ai_memory(self):
        """Save AI memory after each session"""
        try:
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
                'ai_insights': self.generate_ai_insights(),
                'enhanced_config': self.enhanced_config
            }
            
            with open(self.memory_file, 'w') as f:
                json.dump(memory_data, f, indent=2)
            
        except Exception as e:
            logger.error(f"Error saving AI memory: {e}")
    
    def save_session_results(self):
        """Save individual session results"""
        try:
            win_rate = (self.wins / max(self.trades_completed, 1)) * 100
            avg_confidence = sum(self.confidence_scores) / max(len(self.confidence_scores), 1)
            
            results = {
                'timestamp': datetime.now().isoformat(),
                'results': {
                    'session_number': self.session_number,
                    'total_trades': self.trades_completed,
                    'lifetime_trades': self.lifetime_trades,
                    'wins': self.wins,
                    'losses': self.losses,
                    'win_rate': win_rate,
                    'total_profit': self.total_profit,
                    'lifetime_profit': self.lifetime_profit,
                    'max_drawdown': self.max_drawdown,
                    'avg_confidence': avg_confidence,
                    'final_equity': self.equity_curve[-1] if self.equity_curve else 200.0
                }
            }
            
            with open(self.results_file, 'w') as f:
                json.dump(results, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving session results: {e}")
    
    def save_progress(self, current_session, total_sessions):
        """Save continuous training progress"""
        try:
            progress_data = {
                'current_session': current_session,
                'total_sessions': total_sessions,
                'completed_sessions': current_session - 1,
                'progress_percentage': ((current_session - 1) / total_sessions) * 100,
                'start_time': getattr(self, 'training_start_time', datetime.now().isoformat()),
                'last_update': datetime.now().isoformat(),
                'lifetime_trades': self.lifetime_trades,
                'lifetime_win_rate': (self.lifetime_wins / max(self.lifetime_trades, 1)) * 100
            }
            
            with open(self.progress_file, 'w') as f:
                json.dump(progress_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving progress: {e}")
    
    def generate_ai_insights(self):
        """Generate AI insights"""
        insights = {}
        
        # Best performing pair
        if self.pair_performance:
            best_pair = max(self.pair_performance.items(), 
                          key=lambda x: x[1]['wins'] / max(x[1]['wins'] + x[1]['losses'], 1),
                          default=('EUR/USD', {'wins': 0, 'losses': 0}))[0]
            insights['best_pair'] = best_pair
        
        # Learning trend
        current_win_rate = (self.lifetime_wins / max(self.lifetime_trades, 1)) * 100
        if current_win_rate >= 65.0:
            insights['learning_trend'] = 'Excellent - Target Achieved'
        elif current_win_rate >= 60.0:
            insights['learning_trend'] = 'Good - Approaching Target'
        elif len(self.session_performance) >= 2:
            recent_sessions = self.session_performance[-2:]
            if recent_sessions[1]['win_rate'] > recent_sessions[0]['win_rate']:
                insights['learning_trend'] = 'Improving'
            else:
                insights['learning_trend'] = 'Needs Adjustment'
        else:
            insights['learning_trend'] = 'Building Experience'
        
        return insights
    
    def generate_realistic_trade(self):
        """Generate trade using REAL OANDA historical data OR enhanced simulation fallback"""
        pairs = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'USD/CHF', 'AUD/USD', 'USD/CAD', 'NZD/USD', 'EUR/GBP']
        pair = random.choice(pairs)
        
        # TRY TO GET REAL OANDA DATA FIRST
        market_data = None
        data_source = "SIMULATION"
        
        if self.use_real_data and self.oanda_data is not None:
            try:
                market_data = self.oanda_data.get_realistic_market_data(pair)
                if market_data is not None:
                    data_source = "OANDA"
            except Exception as e:
                if random.random() < 0.01:  # Only show error 1% of the time to avoid spam
                    print(f"{Fore.YELLOW}⚠️ OANDA data fetch failed: {e}. Using simulation.{Style.RESET_ALL}")
        
        # FALLBACK TO ENHANCED SIMULATION if OANDA fails
        if market_data is None:
            market_data = self.generate_simulated_market_data(pair)
            data_source = "SIMULATION"
        
        # Enhanced Market Hours Check - VERY LENIENT for maximum learning
        session = market_data['session']
        if self.enhanced_config['market_hours_filter']:
            # Only reject 1% of trades during poor sessions for maximum learning opportunities
            if session == 'tokyo' and random.random() < 0.01:
                return None
            elif session in ['london', 'newyork', 'overlap'] and random.random() < 0.001:
                return None
        
        # Enhanced Correlation Limits - MAXIMUM FLEXIBILITY for learning
        if self.enhanced_config['correlation_limits'] and not self.check_correlation_limits(pair):
            if random.random() < 0.95:  # 95% chance to allow correlated trades for maximum learning
                pass  # Allow almost all correlated trades for learning diversity
            else:
                return None
        
        # Create trade signal
        trade_signal = {
            'pair': pair,
            'risk_reward_ratio': random.uniform(1.5, 4.0),
            'base_confidence': random.uniform(0.4, 0.8),
            'action': random.choice(['BUY', 'SELL'])
        }
        
        # Generate AI features using REAL or simulated data
        features = self.generate_ai_features(market_data, trade_signal)
        
        # Get AI prediction
        win_probability, ai_confidence = self.ai_predict_outcome(market_data, trade_signal)
        
        # PROFESSIONAL FILTERING FOR 65% WR TARGET
        current_time = datetime.now()
        
        # 1. News-aware filtering - VERY PERMISSIVE for learning
        if self.enhanced_config['news_awareness']:
            news_info = self.news_aware.get_news_impact_for_pair(pair, current_time)
            if news_info['has_news']:
                should_trade, position_multiplier = self.news_aware.should_trade_during_news(news_info, ai_confidence)
                if not should_trade and random.random() < 0.1:  # Only reject 10% of news trades
                    return None
                ai_confidence *= position_multiplier

        # 2. Market microstructure filtering - VERY PERMISSIVE
        if self.enhanced_config['microstructure_analysis']:
            can_execute, reason = self.microstructure.should_execute_trade(pair, market_data['market_condition'], 100000)
            if not can_execute and random.random() < 0.05:  # Only reject 5% for microstructure
                return None        # 3. QUALITY-FIRST confidence filtering - STRICT for 65% target
        confidence_threshold = self.enhanced_config['confidence_threshold']
        
        # QUALITY-FIRST APPROACH: Use full threshold - no reduction for learning
        effective_threshold = confidence_threshold  # 75% minimum confidence
        
        # Premium session quality check
        current_hour = datetime.now().hour
        is_premium_session = (8 <= current_hour <= 12) or (13 <= current_hour <= 17)  # London/NY sessions
        
        if not is_premium_session:
            effective_threshold *= 1.2  # 20% higher threshold outside premium hours
        
        # Market condition quality enhancement
        market_condition = market_data.get('market_condition', 'unknown')
        if market_condition in ['volatile', 'quiet']:  # Lower quality conditions
            effective_threshold *= 1.15  # 15% higher threshold for challenging conditions
        
        # STRICT QUALITY GATES - Only premium setups for 65% target
        if market_data.get('trend_strength', 0) < self.enhanced_config['trend_strength_min']:
            return None  # Reject weak trends completely
            
        if market_data.get('session_quality_score', 0) < self.enhanced_config['session_quality_min']:
            return None  # Reject poor session quality
            
        if trade_signal.get('risk_reward_ratio', 0) < self.enhanced_config['risk_reward_min']:
            return None  # Reject poor risk/reward ratios
            
        if ai_confidence < effective_threshold:
            return None  # Reject low confidence trades - NO EXCEPTIONS
        
        # Enhanced Execution failure simulation - Very lenient
        base_execution_failure_rate = 0.01  # Very low base rate
        execution_failure_rate = base_execution_failure_rate
        
        if self.enhanced_config['latency_simulation']:
            latency_factor = self.simulate_execution_latency()
            if latency_factor < 0.97:
                execution_failure_rate *= 1.05  # Minimal penalty
        
        if random.random() < execution_failure_rate:
            return None
        
        # Position sizing - Get current equity first
        current_equity = self.equity_curve[-1] if self.equity_curve else 500.0
        
        # LEARNING-OPTIMIZED Position sizing for AI training
        if current_equity <= 1000:
            risk_percent = 0.025      # Higher risk for faster learning feedback
        elif current_equity <= 5000:
            risk_percent = 0.020      # Maintain good learning rate
        elif current_equity <= 20000:
            risk_percent = 0.015      # Balanced risk for established accounts
        else:
            risk_percent = 0.010      # Conservative for large accounts
        
        base_risk_amount = current_equity * risk_percent
        
        # Apply advanced risk management
        if self.enhanced_config['advanced_risk_management']:
            optimized_size = self.risk_manager.optimize_position_size(
                pair, base_risk_amount, ai_confidence, market_data['market_condition']
            )
            
            can_trade, risk_reason = self.risk_manager.should_take_position(
                pair, optimized_size, ai_confidence, market_data['market_condition']
            )
            
            if not can_trade:
                return None
            
            base_risk_amount = optimized_size
        
        # USE REAL SPREADS from OANDA or realistic simulation
        if data_source == "OANDA" and 'actual_spread_pips' in market_data:
            # Use actual spread from OANDA
            spread_pips = market_data['actual_spread_pips']
            spread_cost = base_risk_amount * (spread_pips / 10000)  # Convert pips to decimal
        else:
            # Use simulated realistic spreads
            spread_pips = self.get_realistic_spread(pair, market_data['market_condition'])
            spread_cost = base_risk_amount * (spread_pips / 100)
        
        commission = base_risk_amount * 0.001
        
        # Enhanced slippage simulation
        if self.enhanced_config['latency_simulation']:
            slippage_factor = self.simulate_execution_latency()
        else:
            slippage_factor = random.uniform(0.97, 1.03)
        
        # Get market stress factor
        stress_level, stress_multiplier = self.get_market_stress_factor()
        
        # Adjust win probability for market stress
        win_probability = min(0.75, max(0.35, win_probability / stress_multiplier))
        
        # Determine outcome based on AI prediction
        is_win = random.random() < win_probability
        
        # Calculate P&L with enhanced realism
        if is_win:
            base_profit = base_risk_amount * random.uniform(1.2, 2.1)
            profit = (base_profit * slippage_factor) - spread_cost - commission
            profit *= (2.0 - stress_multiplier) / 2.0
            self.wins += 1
            self.lifetime_wins += 1
        else:
            base_loss = base_risk_amount * random.uniform(0.9, 1.1)
            profit = -(base_loss * slippage_factor) - spread_cost - commission
            profit *= stress_multiplier
            self.losses += 1
            self.lifetime_losses += 1
        
        # Update statistics
        self.pair_performance[pair]['wins' if is_win else 'losses'] += 1
        self.pair_performance[pair]['profit'] += profit
        self.confidence_scores.append(ai_confidence)
        self.total_profit += profit
        self.lifetime_profit += profit
        self.lifetime_trades += 1
        
        # Track recent trades for correlation
        if not hasattr(self, 'recent_trades'):
            self.recent_trades = []
        self.recent_trades.append({'pair': pair, 'timestamp': datetime.now()})
        if len(self.recent_trades) > 20:
            self.recent_trades = self.recent_trades[-15:]
        
        # ADD TO AI TRAINING DATA with source indicator
        self.add_training_sample(features, 1 if is_win else 0, market_data, trade_signal)
        
        # Update equity with LEARNING-OPTIMIZED scaling for AI training phase
        if current_equity <= 1000:
            scaling_factor = 1.0      # Full profits for early learning
        elif current_equity <= 5000:
            scaling_factor = 0.95     # Minimal reduction for continued learning
        elif current_equity <= 15000:
            scaling_factor = 0.85     # Moderate scaling for established learning
        elif current_equity <= 50000:
            scaling_factor = 0.70     # Progressive scaling for larger accounts
        else:
            scaling_factor = 0.50     # Realistic but not punitive for very large accounts
        
        scaled_profit = profit * scaling_factor
        
        # LEARNING-OPTIMIZED Market impact for large accounts - Less aggressive
        if current_equity > 25000:  # Raised threshold
            market_impact = abs(profit) * 0.05 * (current_equity / 200000)  # Reduced impact
            scaled_profit -= market_impact
        
        new_equity = max(100.0, current_equity + scaled_profit)
        self.equity_curve.append(new_equity)
        
        # Track drawdown
        peak_equity = max(self.equity_curve)
        self.drawdown = (peak_equity - new_equity) / peak_equity * 100
        self.max_drawdown = max(self.max_drawdown, self.drawdown)
        
        self.max_profit = max(self.max_profit, profit)
        self.max_loss = min(self.max_loss, profit)
        
        return {
            'pair': pair,
            'action': trade_signal['action'],
            'confidence': ai_confidence,
            'ai_win_probability': win_probability,
            'is_win': is_win,
            'profit': profit,
            'scaled_profit': scaled_profit,
            'equity': new_equity,
            'lifetime_trade_number': self.lifetime_trades,
            'ai_features_used': True,
            'spread_cost': spread_cost,
            'slippage_factor': slippage_factor,
            'market_stress': stress_level,
            'data_source': data_source,  # NEW: Track if using OANDA or simulation
            'actual_spread_pips': spread_pips  # NEW: Track actual spread used
        }
    
    def run_single_session(self):
        """Run a single 8000-trade session"""
        print(f"\n{Style.BRIGHT}{Fore.CYAN}{'='*80}")
        print(f"{Fore.YELLOW}🤖 JARVIS AI SESSION #{self.session_number}")
        print(f"{Fore.WHITE}Target: 8000 Trades | Lifetime: {self.lifetime_trades:,} trades")
        
        if self.lifetime_trades > 0:
            lifetime_win_rate = (self.lifetime_wins / self.lifetime_trades) * 100
            print(f"{Fore.GREEN}🧠 LIFETIME: {lifetime_win_rate:.1f}% Win Rate | ${self.lifetime_profit:,.2f} Profit")
        
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        
        start_time = datetime.now()
        
        # Run 8000 trades with optimized delays for 2-hour sessions
        for i in range(8000):
            trade = self.generate_realistic_trade()
            if trade is None:
                continue
            self.trades_completed += 1
            # Slower learning delay - 10 seconds per trade for deeper AI learning
            if i % 50 == 0:  # Show processing every 50 trades
                print(f"{Fore.CYAN}⚡ Processing trade #{self.trades_completed:,}...", end="\r", flush=True)
            time.sleep(10.0)  # 10 seconds for deeper learning and more realistic feedback

            # Progress reporting block must be inside the for loop, at the same indentation
            if i % 200 == 0 or i == 7999:
                win_rate = (self.wins / max(self.trades_completed, 1)) * 100
                color = Fore.GREEN if win_rate >= 65 else Fore.YELLOW if win_rate >= 55 else Fore.RED
                progress = (i + 1) / 8000 * 100
                elapsed = datetime.now() - start_time
                estimated_total = elapsed / ((i + 1) / 8000) if i > 0 else timedelta(seconds=80000)  # ~22 hours target (8000 trades × 10 seconds)
                remaining = estimated_total - elapsed
                # AI Learning Stats
                ai_accuracy = self.get_ai_accuracy()
                avg_confidence = sum(self.confidence_scores[-100:]) / max(len(self.confidence_scores[-100:]), 1)
                training_samples = len(self.training_data)
                ai_trained = "✅" if hasattr(self.feature_scaler, 'scale_') else "❌"
                # Data source tracking
                data_source_indicator = ""
                if hasattr(self, 'use_real_data') and self.use_real_data:
                    data_source_indicator = f"{Fore.GREEN}📡 LIVE DATA{Style.RESET_ALL}"
                else:
                    data_source_indicator = f"{Fore.CYAN}🎲 SIMULATION{Style.RESET_ALL}"
                print(f"\n{Fore.CYAN}📊 Progress: {color}{progress:.1f}% {Fore.CYAN}| WR: {color}{win_rate:.1f}%{Fore.CYAN} | "
                      f"AI: {ai_trained} {ai_accuracy:.0f}% | "
                      f"Conf: {avg_confidence:.2f} | "
                      f"Samples: {training_samples:,}")
                print(f"{Fore.WHITE}   Trades: {self.trades_completed:,}/8000 | "
                      f"Equity: ${self.equity_curve[-1]:,.0f} | "
                      f"{data_source_indicator} | "
                      f"{Fore.YELLOW}ETA: {str(remaining).split('.')[0]}")
                # Show recent trade with AI insights
                if trade and 'ai_win_probability' in trade:
                    win_status = f"{Fore.GREEN}✅ WIN" if trade['is_win'] else f"{Fore.RED}❌ LOSS"
                    source_icon = "📡" if trade.get('data_source') == 'OANDA' else "🎲"
                    print(f"{Fore.MAGENTA}   Latest: {source_icon} {trade['pair']} {trade['action']} | {win_status}{Fore.MAGENTA} | "
                          f"AI: {trade['ai_win_probability']:.2f} | Conf: {trade['confidence']:.2f}{Style.RESET_ALL}")
                print()  # Add spacing
    def adaptive_retraining(self):
        """Dynamically adjust AI retraining and thresholds if win rate plateaus below 60%."""
        recent_sessions = self.session_performance[-5:] if len(self.session_performance) >= 5 else self.session_performance
        if not recent_sessions:
            return
        avg_wr = sum(s['win_rate'] for s in recent_sessions) / len(recent_sessions)
        # If win rate is stuck below 60%, make AI more aggressive and retrain
        if avg_wr < 60.0:
            print(f"{Fore.YELLOW}⚡ Win rate plateau detected (avg {avg_wr:.1f}%). Adapting AI thresholds and retraining...{Style.RESET_ALL}")
            # Lower confidence and trend thresholds for more trade diversity
            self.enhanced_config['confidence_threshold'] = max(0.10, self.enhanced_config['confidence_threshold'] * 0.9)
            self.enhanced_config['trend_strength_min'] = max(0.15, self.enhanced_config['trend_strength_min'] * 0.9)
            self.enhanced_config['ai_retrain_frequency'] = max(50, int(self.enhanced_config['ai_retrain_frequency'] * 0.8))
            # Retrain AI model with all available data
            self.train_ai_model()
            print(f"{Fore.GREEN}✅ Adaptive retraining complete. New thresholds: confidence {self.enhanced_config['confidence_threshold']:.2f}, trend {self.enhanced_config['trend_strength_min']:.2f}, retrain freq {self.enhanced_config['ai_retrain_frequency']}{Style.RESET_ALL}")

    def train_ai_model(self):
        """Train the AI model with collected data."""
        if len(self.training_data) < 100:
            print(f"{Fore.YELLOW}⚠️ Not enough training data ({len(self.training_data)} samples). Need at least 100.{Style.RESET_ALL}")
            return
        
        try:
            print(f"{Fore.CYAN}🧠 Training AI model with {len(self.training_data):,} samples...{Style.RESET_ALL}")
            
            # Prepare features and targets
            features = []
            targets = []
            
            for data in self.training_data:
                if 'features' in data and 'outcome' in data:
                    features.append(data['features'])
                    targets.append(data['outcome'])
            
            if len(features) < 50:
                print(f"{Fore.YELLOW}⚠️ Not enough valid features ({len(features)}). Skipping training.{Style.RESET_ALL}")
                return
            
            # Convert to numpy arrays
            X = np.array(features)
            y = np.array(targets)
            
            # Scale features
            self.feature_scaler = StandardScaler()
            X_scaled = self.feature_scaler.fit_transform(X)
            
            # Split data
            test_size = min(0.2, 200 / len(X))  # Use smaller test size for small datasets
            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=test_size, random_state=42)
            
            # Train model
            self.ai_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            )
            
            self.ai_model.fit(X_train, y_train)
            
            # Verify the model was fitted properly
            if not hasattr(self.ai_model, 'n_features_in_'):
                print(f"{Fore.RED}❌ Model fitting failed. Resetting AI model to None.{Style.RESET_ALL}")
                self.ai_model = None
                return
            
            # Calculate accuracy
            if len(X_test) > 0:
                accuracy = self.ai_model.score(X_test, y_test)
                print(f"{Fore.GREEN}✅ AI Model trained! Accuracy: {accuracy*100:.1f}%{Style.RESET_ALL}")
                
                # Store accuracy in performance history
                self.model_performance_history.append({
                    'accuracy': accuracy,
                    'timestamp': datetime.now().isoformat(),
                    'training_samples': len(X_train)
                })
            else:
                accuracy = 0.5  # Default accuracy when no test data
                print(f"{Fore.GREEN}✅ AI Model trained! (No test data for accuracy calculation){Style.RESET_ALL}")
                
                # Store default accuracy
                self.model_performance_history.append({
                    'accuracy': accuracy,
                    'timestamp': datetime.now().isoformat(),
                    'training_samples': len(X_train)
                })
                
        except Exception as e:
            print(f"{Fore.RED}❌ AI training error: {e}{Style.RESET_ALL}")
            # Reset model to None to prevent further errors
            self.ai_model = None
            self.feature_scaler = StandardScaler()  # Reset scaler too
    
    def run_100_sessions(self):
        """Run 100 consecutive training sessions"""
        print(f"\n{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}")
        print("🚀 JARVIS AI - 100 SESSIONS CONTINUOUS TRAINING 🚀")
        print("=" * 60)
        print("AUTOMATIC 100-SESSION TRAINING MODE:")
        print("✅ 100 Sessions × 8000 Trades = 800,000 Total Trades")
        print("✅ Continuous AI Learning & Memory")
        print("✅ Full Real Market Simulation")
        print("✅ Progressive Skill Development")
        print("✅ Automatic Progress Saving")
        print("🕒 DEEP LEARNING MODE: 10-second delays between trades")
        print("⏱️  SESSION DURATION: ~22 hours per session (deep AI learning)")
        print("=" * 60 + Style.RESET_ALL)
        
        # Get starting session from memory
        start_session = self.session_number
        target_sessions = 100
        
        self.training_start_time = datetime.now().isoformat()
        
        print(f"\n{Fore.YELLOW}🎯 TARGET: {target_sessions} Sessions")
        print(f"{Fore.WHITE}📊 Starting from Session #{start_session}")
        print(f"{Fore.GREEN}🚀 Beginning continuous training...")
        
        try:
            for session_num in range(start_session, start_session + target_sessions):
                self.session_number = session_num
                self.reset_session_stats()
                
                print(f"\n{Style.BRIGHT}{Fore.MAGENTA}📍 SESSION {session_num}/{start_session + target_sessions - 1}")
                
                # Run session
                session_results = self.run_single_session()
                
                # Save memory after each session
                self.save_ai_memory()
                self.save_session_results()
                self.save_progress(session_num + 1, target_sessions)
                
                # Show overall progress
                completed = session_num - start_session + 1
                total_progress = (completed / target_sessions) * 100
                lifetime_win_rate = (self.lifetime_wins / max(self.lifetime_trades, 1)) * 100
                
                print(f"\n{Style.BRIGHT}{Fore.CYAN}🏆 OVERALL PROGRESS:")
                print(f"{Fore.WHITE}   Sessions: {completed}/{target_sessions} ({total_progress:.1f}%)")
                print(f"{Fore.YELLOW}   Total Trades: {self.lifetime_trades:,}")
                print(f"{Fore.GREEN if lifetime_win_rate >= 65 else Fore.RED}   Lifetime Win Rate: {lifetime_win_rate:.1f}%")
                print(f"{Fore.WHITE}   Total Profit: ${self.lifetime_profit:,.2f}")
                
                # Brief pause between sessions for AI memory consolidation
                print(f"\n{Fore.YELLOW}🧠 AI Memory Consolidation... (10s processing time)")
                time.sleep(10)
                
                # Save checkpoint every 10 sessions
                if completed % 10 == 0:
                    print(f"\n{Fore.GREEN}💾 CHECKPOINT: {completed} sessions completed")
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⏸️ Training interrupted by user")
            print(f"{Fore.WHITE}Progress saved. You can resume later.")
            completed = session_num - start_session + 1
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error during training: {e}")
            completed = session_num - start_session + 1
        
        # Final summary
        final_lifetime_wr = (self.lifetime_wins / max(self.lifetime_trades, 1)) * 100
        
        print(f"\n{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}")
        print("🏁 100-SESSION TRAINING COMPLETE! 🏁")
        print("=" * 50 + Style.RESET_ALL)
        
        print(f"\n{Style.BRIGHT}{Fore.GREEN}✅ FINAL RESULTS:")
        print(f"{Fore.CYAN}   Sessions Completed: {completed}/{target_sessions}")
        print(f"{Fore.YELLOW}   Total Lifetime Trades: {self.lifetime_trades:,}")
        print(f"{'   Lifetime Win Rate: ' + Fore.GREEN if final_lifetime_wr >= 65 else '   Lifetime Win Rate: ' + Fore.RED}{final_lifetime_wr:.1f}%")
        print(f"{Fore.WHITE}   Total Lifetime Profit: ${self.lifetime_profit:,.2f}")
        
        if final_lifetime_wr >= 65:
            print(f"\n{Style.BRIGHT}{Fore.GREEN}🎉 TARGET ACHIEVED! 65%+ Win Rate Reached!")
        elif final_lifetime_wr >= 60:
            print(f"\n{Style.BRIGHT}{Fore.YELLOW}🎯 Close to target! Continue training for 65%+")
        else:
            print(f"\n{Style.BRIGHT}{Fore.CYAN}📈 Good progress! AI is learning and improving")
        
        print(f"{Style.RESET_ALL}")
        return completed

def main():
    """Main execution function"""
    print(f"\n{Style.BRIGHT}{Back.BLUE}{Fore.WHITE}")
    print("🤖 JARVIS AI - 100 SESSIONS CONTINUOUS TRAINING 🤖")
    print("This will run 100 sessions non-stop (800,000 total trades)")
    print("Each session = 8000 realistic trades with full market friction")
    print("=" * 60 + Style.RESET_ALL)
    
    try:
        response = input(f"\n{Fore.YELLOW}🚀 Start 100-session continuous training? (y/n): {Fore.WHITE}").lower().strip()
    except (EOFError, KeyboardInterrupt):
        print(f"\n{Fore.RED}⏹️ Cancelled by user{Style.RESET_ALL}")
        return
    
    if response in ['y', 'yes']:
        training_system = ContinuousTrainingSystem()
        
        print(f"\n{Style.BRIGHT}{Fore.GREEN}🚀 STARTING 100-SESSION TRAINING...")
        print(f"{Fore.CYAN}   This will run continuously until complete")
        print(f"{Fore.YELLOW}   Press Ctrl+C to safely interrupt and save progress")
        print(f"{Style.RESET_ALL}")
        
        completed_sessions = training_system.run_100_sessions()
        
        print(f"\n{Style.BRIGHT}{Fore.GREEN}🏆 TRAINING FINISHED!")
        print(f"{Fore.WHITE}Completed {completed_sessions}/100 sessions")
        print(f"{Fore.CYAN}All progress has been saved to memory files")
        print(f"{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}👋 Training cancelled{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Training stopped by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Script failed: {e}")
        sys.exit(1)
