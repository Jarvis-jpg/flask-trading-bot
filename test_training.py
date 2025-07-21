#!/usr/bin/env python3
"""Test the enhanced training system"""
try:
    print("Testing Enhanced Training System...")
    from enhanced_training_system import EnhancedTrainingSystem
    
    training = EnhancedTrainingSystem()
    print("✅ Training system initialized")
    print(f"📊 Target trades: {training.training_config['total_trades']:,}")
    print(f"🎯 Target win rate: {training.training_config['target_win_rate']:.1%}")
    print(f"📈 Active pairs: {len(training.currency_pairs)}")
    print("🚀 Enhanced training system ready!")
    
    print("\n🧠 Testing adaptive learning from 8000 trade system...")
    learning_factor = training.simulator.calculate_learning_factor()
    print(f"📈 Current learning factor: {learning_factor:.1%}")
    
    print("\n✅ All systems operational!")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
