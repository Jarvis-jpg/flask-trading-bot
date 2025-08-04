#!/usr/bin/env python3
"""
Analyze Million Trade Training Results and Deploy
"""

import json
import os
from datetime import datetime

def analyze_training_data():
    """Analyze the completed training data"""
    
    print("ANALYZING MILLION TRADE TRAINING RESULTS")
    print("=" * 50)
    
    # Check if training file exists
    if not os.path.exists("temp_million_trades.json"):
        print("❌ Training file not found!")
        return False
    
    file_size = os.path.getsize("temp_million_trades.json") / (1024 * 1024)
    print(f"📁 Training file: {file_size:.1f}MB")
    
    try:
        with open("temp_million_trades.json", 'r') as f:
            data = json.load(f)
        
        trades = data.get("trades", [])
        total_trades = len(trades)
        
        if total_trades == 0:
            print("❌ No trades found in file!")
            return False
        
        # Calculate win rate
        wins = sum(1 for trade in trades if trade.get("outcome") == 1)
        win_rate = (wins / total_trades) * 100
        
        # Calculate other statistics
        avg_confidence = sum(trade.get("confidence", 0) for trade in trades) / total_trades
        avg_risk_reward = sum(trade.get("risk_reward", 0) for trade in trades) / total_trades
        avg_trend_strength = sum(trade.get("trend_strength", 0) for trade in trades) / total_trades
        
        # Analyze by pairs
        pair_stats = {}
        for trade in trades:
            pair = trade.get("pair", "Unknown")
            if pair not in pair_stats:
                pair_stats[pair] = {"total": 0, "wins": 0}
            pair_stats[pair]["total"] += 1
            if trade.get("outcome") == 1:
                pair_stats[pair]["wins"] += 1
        
        # Results
        print(f"✅ TRAINING ANALYSIS COMPLETE!")
        print(f"📊 Total Trades: {total_trades:,}")
        print(f"🎯 Win Rate: {win_rate:.2f}%")
        print(f"🔥 Total Wins: {wins:,}")
        print(f"📈 Total Losses: {total_trades - wins:,}")
        print(f"⚡ Avg Confidence: {avg_confidence:.3f}")
        print(f"💰 Avg Risk/Reward: {avg_risk_reward:.2f}")
        print(f"📊 Avg Trend Strength: {avg_trend_strength:.3f}")
        print()
        
        print("🌍 PAIR PERFORMANCE:")
        for pair, stats in pair_stats.items():
            pair_wr = (stats["wins"] / stats["total"]) * 100 if stats["total"] > 0 else 0
            print(f"   {pair}: {pair_wr:.1f}% WR ({stats['wins']:,}/{stats['total']:,})")
        
        # Assessment
        print()
        print("🎯 WIN RATE ASSESSMENT:")
        if win_rate >= 68:
            print("🚀 EXCELLENT: 68%+ win rate - Perfect for live trading!")
        elif win_rate >= 65:
            print("✅ VERY GOOD: 65%+ win rate - Ready for live trading!")
        elif win_rate >= 62:
            print("📈 GOOD: 62%+ win rate - Solid performance, ready to trade!")
        elif win_rate >= 58:
            print("📊 DECENT: 58%+ win rate - Acceptable, can trade with caution")
        else:
            print("⚠️ NEEDS WORK: <58% win rate - Needs improvement")
        
        # Create final deployment file
        final_data = {
            "session_number": 1000,
            "lifetime_trades": total_trades,
            "lifetime_wins": wins,
            "lifetime_losses": total_trades - wins,
            "lifetime_win_rate": round(win_rate, 2),
            "last_session_date": datetime.now().isoformat(),
            "avg_confidence": round(avg_confidence, 3),
            "avg_risk_reward": round(avg_risk_reward, 2),
            "avg_trend_strength": round(avg_trend_strength, 3),
            "pair_performance": {},
            "training_complete": True,
            "deployment_ready": win_rate >= 58
        }
        
        # Add pair performance
        for pair, stats in pair_stats.items():
            pair_wr = (stats["wins"] / stats["total"]) * 100 if stats["total"] > 0 else 0
            final_data["pair_performance"][pair] = {
                "wins": stats["wins"],
                "losses": stats["total"] - stats["wins"],
                "total_trades": stats["total"],
                "win_rate": round(pair_wr, 2)
            }
        
        # Save final AI memory file
        with open("jarvis_ai_memory.json", 'w') as f:
            json.dump(final_data, f, indent=2)
        
        final_size = os.path.getsize("jarvis_ai_memory.json") / 1024
        print()
        print(f"💾 FINAL AI MEMORY CREATED: {final_size:.1f}KB")
        print("🚀 READY FOR DEPLOYMENT TO RENDER!")
        
        return win_rate >= 58
        
    except Exception as e:
        print(f"❌ Error analyzing data: {e}")
        return False

def deploy_final_system():
    """Deploy the final system to git"""
    
    print()
    print("🚀 DEPLOYING FINAL SYSTEM")
    print("=" * 30)
    
    try:
        import subprocess
        
        # Add files
        subprocess.run(["git", "add", "jarvis_ai_memory.json"], check=True)
        subprocess.run(["git", "add", "TRADINGVIEW_SETUP_GUIDE.md"], check=True)
        subprocess.run(["git", "add", "smart_git_manager.py"], check=True)
        subprocess.run(["git", "add", "windows_million_trade_trainer.py"], check=True)
        
        # Commit
        subprocess.run(["git", "commit", "-m", "FINAL: Million trade AI training complete - System ready for live trading"], check=True)
        
        # Push
        subprocess.run(["git", "push"], check=True)
        
        print("✅ DEPLOYMENT SUCCESSFUL!")
        print()
        print("🎯 LIVE TRADING SYSTEM STATUS: READY!")
        print("📖 Next: Configure TradingView using TRADINGVIEW_SETUP_GUIDE.md")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment error: {e}")
        return False

if __name__ == "__main__":
    success = analyze_training_data()
    if success:
        deploy_final_system()
    else:
        print("❌ Analysis failed - check training data")
