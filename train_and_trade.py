#!/usr/bin/env python3
"""
Training Integration Script
This script runs the enhanced 8000 trade training and then starts the autonomous engine
"""
import logging
import sys
import time
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_training_and_start_bot():
    """Run training first, then start the autonomous trading bot"""
    
    print("🎯 JARVIS TRADING BOT - ENHANCED TRAINING MODE")
    print("=" * 60)
    print("This will:")
    print("1. Run 8000 simulated trades for rapid learning")
    print("2. Apply learning to the autonomous engine") 
    print("3. Start the enhanced trading bot")
    print("=" * 60)
    
    # Ask user if they want to run training
    try:
        response = input("\n🤖 Run enhanced training first? (y/n): ").lower().strip()
    except (EOFError, KeyboardInterrupt):
        print("\n⏹️ Operation cancelled by user")
        return
    
    if response in ['y', 'yes']:
        print("\n🚀 Starting Enhanced Training...")
        
        try:
            # Import and run training
            from enhanced_training_system import EnhancedTrainingSystem
            
            training_system = EnhancedTrainingSystem()
            
            # Run accelerated training
            logger.info("🎯 Running 8000 trade simulation for rapid learning...")
            results = training_system.run_accelerated_training()
            
            # Apply training to autonomous engine
            training_system.apply_training_to_autonomous_engine()
            
            print("\n✅ Training completed successfully!")
            print(f"📊 Trained on: {results['total_trades']:,} simulated trades")
            print(f"🎯 Win Rate: {results['wins'] / max(results['total_trades'], 1):.1%}")
            print(f"💰 Simulated Profit: ${results['total_profit']:.2f}")
            
        except Exception as e:
            logger.error(f"❌ Training failed: {e}")
            print("⚠️ Training failed, but you can still run the bot without enhanced training")
    else:
        print("\n⏩ Skipping training - using default configuration")
    
    # Ask if user wants to start the autonomous engine
    print("\n" + "=" * 60)
    try:
        start_response = input("🚀 Start the autonomous trading engine now? (y/n): ").lower().strip()
    except (EOFError, KeyboardInterrupt):
        print("\n⏹️ Operation cancelled by user")
        return
    
    if start_response in ['y', 'yes']:
        print("\n🤖 Starting Jarvis Autonomous Trading Engine...")
        
        try:
            from autonomous_trading_engine import autonomous_engine
            
            # Start the autonomous engine
            success = autonomous_engine.start_trading()
            
            if success:
                print("✅ Autonomous trading engine started successfully!")
                print("\n📊 Engine Status:")
                status = autonomous_engine.get_status()
                print(f"   Running: {status['is_running']}")
                print(f"   Max Concurrent Trades: {status['config']['max_concurrent_trades']}")
                print(f"   Active Currency Pairs: {len(status['config']['active_pairs'])}")
                print(f"   Scan Interval: {status['config']['scan_interval']}s")
                
                print("\n🌐 Web Dashboard:")
                print("   URL: http://localhost:5000")
                print("   You can monitor and control the bot from there")
                
                # Keep the engine running
                try:
                    print("\n⏰ Bot is now running autonomously...")
                    print("   Press Ctrl+C to stop")
                    
                    while True:
                        time.sleep(10)
                        # Show brief status every 60 seconds
                        if int(time.time()) % 60 == 0:
                            status = autonomous_engine.get_status()
                            print(f"📊 Status: {status['daily_stats']['trades_count']} trades, "
                                  f"${status['daily_stats']['profit_loss']:.2f} P&L")
                
                except KeyboardInterrupt:
                    print("\n🛑 Stopping autonomous trading engine...")
                    autonomous_engine.stop_trading()
                    print("✅ Engine stopped safely")
            
            else:
                print("❌ Failed to start autonomous trading engine")
                print("   Check logs for details")
        
        except Exception as e:
            logger.error(f"❌ Failed to start engine: {e}")
            print("❌ Could not start autonomous engine")
    
    else:
        print("\n📱 You can start the web dashboard manually:")
        print("   Run: python start_trading_bot.py")
        print("   Then visit: http://localhost:5000")

if __name__ == "__main__":
    try:
        run_training_and_start_bot()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Script failed: {e}")
        sys.exit(1)
