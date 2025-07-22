#!/usr/bin/env python3
"""
Professional Trading Configuration for 65% Win Rate
Enhanced settings and parameters for institutional-grade performance
"""

import json
from datetime import datetime

def create_professional_config():
    """Create configuration targeting 65% win rate"""
    
    config = {
        "system_info": {
            "name": "JARVIS Professional Trading System",
            "target_win_rate": 0.65,
            "version": "2.0",
            "created": datetime.now().isoformat(),
            "description": "Enhanced configuration for professional forex trading"
        },
        
        "ai_learning": {
            "confidence_threshold": 0.40,  # Higher quality threshold
            "retrain_frequency": 150,       # More frequent retraining
            "min_samples": 100,             # Higher minimum for quality
            "feature_count": 24,            # Enhanced feature set
            "cross_validation_folds": 7,    # More rigorous validation
            "model_type": "GradientBoosting",
            "hyperparameters": {
                "n_estimators": 300,
                "max_depth": 8,
                "learning_rate": 0.03,
                "min_samples_split": 15,
                "min_samples_leaf": 7,
                "subsample": 0.85
            }
        },
        
        "market_analysis": {
            "news_awareness": True,
            "economic_calendar": True,
            "microstructure_analysis": True,
            "liquidity_threshold": 0.75,
            "volatility_adjustment": True,
            "correlation_monitoring": True,
            "session_quality_filter": True
        },
        
        "risk_management": {
            "max_portfolio_heat": 0.05,     # 5% maximum risk
            "max_correlation_exposure": 0.025, # 2.5% correlated risk
            "position_size_scaling": True,
            "var_95_limit": 0.03,           # 3% VaR limit
            "max_positions": 4,             # Reduced for quality
            "drawdown_limit": 0.15          # 15% max drawdown
        },
        
        "execution": {
            "smart_execution": True,
            "slippage_optimization": True,
            "market_impact_modeling": True,
            "latency_compensation": True,
            "order_book_analysis": True
        },
        
        "filters": {
            "trend_strength_min": 0.75,     # Strong trends only
            "session_quality_min": 0.85,    # High quality sessions
            "risk_reward_min": 2.8,         # Better R:R
            "liquidity_min": 0.75,          # Good liquidity
            "confidence_min": 0.40,         # Higher confidence
            "volatility_max": 0.12          # Avoid extreme volatility
        },
        
        "trading_hours": {
            "london_open": "08:00",
            "new_york_open": "13:00",
            "tokyo_open": "23:00",
            "overlap_trading": True,
            "off_hours_trading": False,
            "weekend_trading": False
        },
        
        "pairs": {
            "major_pairs": ["EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF"],
            "minor_pairs": ["AUD/USD", "USD/CAD"],
            "exotic_pairs": [],  # Disabled for now
            "max_correlation": 0.80,
            "min_liquidity": 0.70
        }
    }
    
    return config

def save_professional_config():
    """Save the professional configuration"""
    config = create_professional_config()
    
    with open('professional_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Professional configuration saved to professional_config.json")
    return config

if __name__ == "__main__":
    save_professional_config()
