#!/usr/bin/env python3
"""
Quick test to verify AI learning system works
"""
import os
import sys

print("Testing AI Learning System...")

try:
    # Import the training system
    from train_and_trade_100_sessions import ContinuousTrainingSystem
    print("✅ Successfully imported ContinuousTrainingSystem")
    
    # Create instance
    trainer = ContinuousTrainingSystem()
    print("✅ Successfully created trainer instance")
    
    # Test AI initialization
    if hasattr(trainer, 'ai_model') and trainer.ai_model is not None:
        print("✅ AI model is initialized")
    else:
        print("❌ AI model is NOT initialized")
    
    # Test generate features
    market_data = {
        'pair': 'EUR/USD',
        'market_condition': 'trending',
        'session': 'london',
        'trend_strength': 0.7,
        'rsi_normalized': 0.6,
        'macd_signal_strength': 0.8,
        'volume_surge_factor': 1.2,
        'support_resistance_clarity': 0.5,
        'market_structure_score': 0.9,
        'session_quality_score': 0.8,
        'volatility_score': 0.4,
        'time_quality_score': 0.9
    }
    
    trade_signal = {
        'pair': 'EUR/USD',
        'risk_reward_ratio': 2.0,
        'base_confidence': 0.7,
        'action': 'BUY'
    }
    
    features = trainer.generate_ai_features(market_data, trade_signal)
    print(f"✅ Generated AI features: {len(features)} dimensions")
    
    # Test AI prediction
    win_prob, confidence = trainer.ai_predict_outcome(market_data, trade_signal)
    print(f"✅ AI Prediction: Win Prob={win_prob:.3f}, Confidence={confidence:.3f}")
    
    # Test one trade generation
    trade = trainer.generate_realistic_trade()
    if trade and 'ai_win_probability' in trade:
        print(f"✅ Generated AI trade: {trade['pair']} | AI Prob: {trade['ai_win_probability']:.3f}")
        print("🎉 AI LEARNING SYSTEM IS WORKING!")
    else:
        print("❌ Trade generation failed or missing AI data")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
