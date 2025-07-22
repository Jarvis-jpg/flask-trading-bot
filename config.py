# config.py

# 🔐 Your personal OANDA API key
OANDA_API_KEY = "e9e9a03662b21ebbb03b965301f0182-ea0448d5fc88dd622b361855758d7f3e"

# 📊 Your OANDA account ID
OANDA_ACCOUNT_ID = "001-001-12623605-001"

# Optional: Set the base URL for OANDA API (practice or live)
OANDA_URL = "https://api-fxpractice.oanda.com/v3"

# ENHANCED RISK MANAGEMENT CONFIGURATION FOR 65%+ WIN RATE (REAL MARKET OPTIMIZED)
RISK_CONFIG = {
    'max_risk_per_trade': 0.015,       # 1.5% maximum risk per trade (reduced for better entries)
    'max_account_risk': 0.08,          # 8% maximum total account risk (tighter control)
    'max_daily_loss': 0.04,            # 4% maximum daily loss (more conservative)
    'max_drawdown': 0.12,              # 12% maximum drawdown (stricter limits)
    'position_sizing_method': 'atr',    # ATR-based position sizing
    'risk_reward_min': 3.0,            # Minimum 3:1 risk:reward (INCREASED FOR REAL MARKET)
    'confidence_threshold': 0.70       # 70% minimum confidence (INCREASED FOR REAL MARKET)
}

# ACTIVE TRADING PAIRS - OPTIMIZED FOR HIGH WIN RATES
ACTIVE_PAIRS = [
    'EUR_USD',  # Euro/US Dollar - Most liquid
    'GBP_USD',  # British Pound/US Dollar - High volatility
    'USD_JPY',  # US Dollar/Japanese Yen - Trending pair
    'AUD_USD',  # Australian Dollar/US Dollar - Commodity correlation
    'USD_CAD',  # US Dollar/Canadian Dollar - Oil correlation
    'USD_CHF',  # US Dollar/Swiss Franc - Safe haven
    'NZD_USD',  # New Zealand Dollar/US Dollar - Risk-on sentiment
    'EUR_GBP'   # Euro/British Pound - Cross pair opportunities
]

# ENHANCED SIGNAL QUALITY FILTERS
SIGNAL_QUALITY_CONFIG = {
    'min_trend_strength': 0.75,        # Stronger trend requirement (was 0.60)
    'rsi_sweet_spot_range': (45, 55),  # Tighter RSI range for entries
    'volume_surge_multiplier': 1.8,    # Higher volume requirement (was 1.5)
    'session_overlap_bonus': 0.15,     # Extra points for London/NY overlap
    'pullback_depth_max': 0.382,       # Maximum 38.2% Fibonacci pullback
    'breakout_confirmation': 3,         # 3-candle breakout confirmation
    'news_blackout_minutes': 30,       # No trades 30min before/after major news
    'correlation_filter': 0.7,         # Block highly correlated trades
    'market_structure_filter': True,   # Only trade with clear market structure
}

# HIGH-PERFORMANCE TIME WINDOWS (Only trade during PREMIUM periods for 65%+ win rate)
PREMIUM_TRADING_HOURS = {
    'monday': [(13, 16)],               # London/NY overlap ONLY (highest quality)
    'tuesday': [(8, 10), (13, 16)],     # London open + overlap (premium only)
    'wednesday': [(8, 10), (13, 16)],   # London open + overlap (best day)
    'thursday': [(13, 16)],             # London/NY overlap ONLY
    'friday': [(8, 10)],                # London open ONLY (avoid Friday afternoon)
    'weekend': []                       # No weekend trading
}

# TRADING SESSIONS WITH QUALITY SCORES
TRADING_SESSIONS = {
    'london': {'start': 8, 'end': 17, 'quality_score': 0.85},      # GMT hours
    'newyork': {'start': 13, 'end': 22, 'quality_score': 0.90},    # GMT hours
    'tokyo': {'start': 0, 'end': 9, 'quality_score': 0.70},        # GMT hours - Lower quality
    'overlap_london_ny': {'start': 13, 'end': 17, 'quality_score': 1.0},  # BEST session
    'quiet_hours': {'start': 22, 'end': 6, 'trading_allowed': False}  # No trading
}

# AI MODEL CONFIGURATION - ENHANCED FOR BETTER PERFORMANCE
AI_CONFIG = {
    'model_type': 'GradientBoostingClassifier',  # Changed from RandomForest
    'n_estimators': 200,                         # Increased from 100
    'max_depth': 8,                              # Reduced from 10 (prevent overfitting)
    'min_samples_split': 10,                     # Increased from 5
    'learning_rate': 0.05,                       # More conservative learning
    'retrain_frequency': 500,                    # More frequent retraining (was 1000)
    'feature_importance_threshold': 0.08,        # Higher threshold (was 0.05)
    'cross_validation_folds': 8,                 # More rigorous validation (was 5)
    'ensemble_voting': 'soft',                   # Probability-based voting
    'prediction_confidence_min': 0.75,          # Only act on high-confidence predictions
}

# ENHANCED FEATURE ENGINEERING
FEATURES = [
    # Core Technical Indicators (Higher Weight)
    'ema_12_26_cross_strength', 'rsi_14_normalized', 'macd_signal_strength',
    'bb_position_relative', 'atr_volatility_ratio',
    
    # Market Structure Features (New - Critical for 65%+)
    'support_resistance_proximity', 'trend_strength_multi_tf',
    'volume_profile_analysis', 'market_sentiment_score',
    
    # Session & Time Features
    'session_quality_score', 'time_of_day_performance',
    'day_of_week_bias', 'news_proximity_score',
    
    # Risk & Position Features
    'risk_reward_optimization', 'correlation_with_open_trades',
    'recent_performance_momentum', 'drawdown_proximity'
]


# PHASE 2 ULTRA-ENHANCED CONFIGURATION FOR 65%+ WIN RATE
ULTRA_ENHANCED_CONFIG = {
    # CRITICAL: Ultra-high confidence threshold
    'confidence_threshold': 0.85,  # 85% minimum (up from 82%)
    
    # ADVANCED RISK MANAGEMENT
    'risk_reward_min': 3.0,  # 3:1 minimum (up from 2.5:1)
    'max_daily_trades': 2,   # Only 2 trades per day (ultra selective)
    'max_risk_per_trade': 0.01,  # 1% risk only (ultra conservative)
    
    # MARKET STRUCTURE REQUIREMENTS
    'trend_strength_min': 0.85,  # 85% trend strength (up from 75%)
    'volume_surge_min': 2.5,     # 2.5x volume requirement (up from 1.8x)
    'market_structure_score_min': 0.9,  # 90% market structure quality
    
    # MULTI-TIMEFRAME CONFIRMATION
    'require_multi_tf_confirmation': True,
    'timeframes_required': ['1H', '4H', 'D'],  # All 3 timeframes must agree
    
    # SESSION QUALITY ENFORCEMENT  
    'premium_sessions_only': True,
    'min_session_quality': 0.95,  # Only trade during 95%+ quality sessions
    
    # ADVANCED TECHNICAL FILTERS
    'rsi_range': (47, 53),        # Ultra-tight RSI range
    'macd_histogram_required': True,  # MACD histogram must confirm
    'bollinger_position_filter': True,  # BB position filtering
    'volume_profile_required': True,    # Volume profile analysis
    
    # CORRELATION AND NEWS PROTECTION
    'max_correlation': 0.5,       # Ultra-low correlation tolerance
    'news_blackout_hours': 2,     # 2-hour news blackout (up from 30min)
    'weekend_gap_protection': True,  # No trades before weekends
    
    # AI MODEL ENHANCEMENTS
    'ensemble_models': True,      # Use multiple AI models
    'confidence_weighting': True, # Weight predictions by confidence
    'dynamic_thresholds': True,   # Adjust thresholds based on performance
}

# ULTRA-PREMIUM TRADING WINDOWS (Even more restrictive)
ULTRA_PREMIUM_HOURS = {
    'tuesday': [(13, 16)],    # Only London/NY overlap on Tuesday
    'wednesday': [(13, 16)],  # Only London/NY overlap on Wednesday  
    'thursday': [(13, 16)],   # Only London/NY overlap on Thursday
    # No Monday (unpredictable) or Friday (low volume) trading
}

# ADVANCED TECHNICAL SCORING SYSTEM
TECHNICAL_SCORING = {
    'trend_alignment_weight': 0.3,    # 30% weight
    'momentum_confirmation_weight': 0.25,  # 25% weight  
    'volume_analysis_weight': 0.2,    # 20% weight
    'market_structure_weight': 0.15,  # 15% weight
    'session_quality_weight': 0.1,    # 10% weight
    'minimum_total_score': 0.85       # 85% minimum total score
}
