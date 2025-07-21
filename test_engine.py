#!/usr/bin/env python3
"""Quick engine test"""
try:
    from autonomous_trading_engine import autonomous_engine
    status = autonomous_engine.get_status()
    
    print("🤖 Autonomous Engine Status:")
    print(f"   Running: {status['is_running']}")
    print(f"   Active Trades: {status['active_trades']}")
    print(f"   Max Concurrent: {status['config']['max_concurrent_trades']}")
    print(f"   Max Daily Loss: ${status['config']['max_daily_loss']}")
    print(f"   Active Pairs: {len(status['config']['active_pairs'])}")
    print("✅ Engine ready for operation!")
    
except Exception as e:
    print(f"❌ Engine test failed: {e}")
    import traceback
    traceback.print_exc()
