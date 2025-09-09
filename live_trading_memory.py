#!/usr/bin/env python3
"""
Real-Time Trading Memory Journal
Tracks all live trades, webhook alerts, and system decisions in real-time
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any
import threading

class LiveTradingMemory:
    """Real-time memory system for live trading tracking"""
    
    def __init__(self, memory_file="live_trading_memory.json"):
        self.memory_file = memory_file
        self.lock = threading.Lock()
        self.memory = self.load_memory()
        
    def load_memory(self) -> Dict:
        """Load existing memory or create new structure"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "system_info": {
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "trading_mode": "live",
                "system_version": "2.0"
            },
            "live_statistics": {
                "total_webhook_alerts": 0,
                "total_trades_attempted": 0,
                "total_trades_executed": 0,
                "total_trades_cancelled": 0,
                "total_wins": 0,
                "total_losses": 0,
                "total_profit_loss": 0.0,
                "current_balance": 50.0,
                "live_win_rate": 0.0,
                "best_trade": 0.0,
                "worst_trade": 0.0
            },
            "webhook_alerts": [],
            "trade_attempts": [],
            "executed_trades": [],
            "cancelled_trades": [],
            "system_decisions": [],
            "daily_summaries": {}
        }
    
    def save_memory(self):
        """Thread-safe save to file"""
        with self.lock:
            self.memory["system_info"]["last_updated"] = datetime.now().isoformat()
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2, default=str)
    
    def log_webhook_alert(self, webhook_data: Dict, source="TradingView"):
        """Log incoming webhook alert"""
        alert_record = {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "pair": webhook_data.get("pair", "unknown"),
            "action": webhook_data.get("action", "unknown"),
            "entry": webhook_data.get("entry", 0),
            "stop_loss": webhook_data.get("stop_loss", 0),
            "take_profit": webhook_data.get("take_profit", 0),
            "confidence": webhook_data.get("confidence", 0),
            "raw_data": webhook_data
        }
        
        self.memory["webhook_alerts"].append(alert_record)
        self.memory["live_statistics"]["total_webhook_alerts"] += 1
        
        # Keep only last 1000 alerts
        if len(self.memory["webhook_alerts"]) > 1000:
            self.memory["webhook_alerts"] = self.memory["webhook_alerts"][-1000:]
        
        self.save_memory()
        print(f"📡 Webhook Alert Logged: {webhook_data.get('pair')} {webhook_data.get('action')}")
        
    def log_trade_attempt(self, trade_data: Dict, analysis_result: Dict):
        """Log when system attempts to place a trade"""
        attempt_record = {
            "timestamp": datetime.now().isoformat(),
            "pair": trade_data.get("pair", "unknown"),
            "action": trade_data.get("action", "unknown"),
            "entry": trade_data.get("entry", 0),
            "stop_loss": trade_data.get("stop_loss", 0),
            "take_profit": trade_data.get("take_profit", 0),
            "position_size": trade_data.get("units", 0),
            "analysis": analysis_result,
            "ai_confidence": analysis_result.get("prediction", {}).get("confidence", 0),
            "recommended": analysis_result.get("prediction", {}).get("recommended", False)
        }
        
        self.memory["trade_attempts"].append(attempt_record)
        self.memory["live_statistics"]["total_trades_attempted"] += 1
        
        # Keep only last 500 attempts
        if len(self.memory["trade_attempts"]) > 500:
            self.memory["trade_attempts"] = self.memory["trade_attempts"][-500:]
        
        self.save_memory()
        print(f"🎯 Trade Attempt Logged: {trade_data.get('pair')} analysis complete")
        
    def log_trade_execution(self, trade_data: Dict, execution_result: Dict):
        """Log successful trade execution"""
        execution_record = {
            "timestamp": datetime.now().isoformat(),
            "pair": trade_data.get("pair", "unknown"),
            "action": trade_data.get("action", "unknown"),
            "entry_requested": trade_data.get("entry", 0),
            "entry_filled": execution_result.get("filled_price", 0),
            "stop_loss": trade_data.get("stop_loss", 0),
            "take_profit": trade_data.get("take_profit", 0),
            "position_size": trade_data.get("units", 0),
            "order_id": execution_result.get("order_id", "unknown"),
            "execution_status": execution_result.get("status", "unknown"),
            "slippage": abs(float(execution_result.get("filled_price", 0)) - float(trade_data.get("entry", 0))),
            "is_live": True
        }
        
        self.memory["executed_trades"].append(execution_record)
        self.memory["live_statistics"]["total_trades_executed"] += 1
        
        # Keep only last 200 executions
        if len(self.memory["executed_trades"]) > 200:
            self.memory["executed_trades"] = self.memory["executed_trades"][-200:]
        
        self.save_memory()
        print(f"✅ Trade Execution Logged: {trade_data.get('pair')} order #{execution_result.get('order_id')}")
        
    def log_trade_cancellation(self, trade_data: Dict, reason: str, details: Dict = None):
        """Log when a trade is cancelled and why"""
        cancellation_record = {
            "timestamp": datetime.now().isoformat(),
            "pair": trade_data.get("pair", "unknown"),
            "action": trade_data.get("action", "unknown"),
            "entry": trade_data.get("entry", 0),
            "stop_loss": trade_data.get("stop_loss", 0),
            "cancellation_reason": reason,
            "details": details or {},
            "trade_data": trade_data
        }
        
        self.memory["cancelled_trades"].append(cancellation_record)
        self.memory["live_statistics"]["total_trades_cancelled"] += 1
        
        # Keep only last 200 cancellations
        if len(self.memory["cancelled_trades"]) > 200:
            self.memory["cancelled_trades"] = self.memory["cancelled_trades"][-200:]
        
        self.save_memory()
        print(f"❌ Trade Cancellation Logged: {trade_data.get('pair')} - {reason}")
        
    def log_system_decision(self, decision_type: str, details: Dict, context: Dict = None):
        """Log important system decisions for debugging"""
        decision_record = {
            "timestamp": datetime.now().isoformat(),
            "decision_type": decision_type,
            "details": details,
            "context": context or {}
        }
        
        self.memory["system_decisions"].append(decision_record)
        
        # Keep only last 100 decisions
        if len(self.memory["system_decisions"]) > 100:
            self.memory["system_decisions"] = self.memory["system_decisions"][-100:]
        
        self.save_memory()
        print(f"🧠 System Decision Logged: {decision_type}")
        
    def log_trade_result(self, order_id: str, result: str, profit_loss: float):
        """Log final trade result (win/loss)"""
        # Find the executed trade
        for trade in self.memory["executed_trades"]:
            if trade.get("order_id") == order_id:
                trade["result"] = result
                trade["profit_loss"] = profit_loss
                trade["closed_timestamp"] = datetime.now().isoformat()
                
                # Update statistics
                if result == "win":
                    self.memory["live_statistics"]["total_wins"] += 1
                else:
                    self.memory["live_statistics"]["total_losses"] += 1
                    
                self.memory["live_statistics"]["total_profit_loss"] += profit_loss
                
                # Update balance
                self.memory["live_statistics"]["current_balance"] += profit_loss
                
                # Update win rate
                total_closed = self.memory["live_statistics"]["total_wins"] + self.memory["live_statistics"]["total_losses"]
                if total_closed > 0:
                    self.memory["live_statistics"]["live_win_rate"] = (self.memory["live_statistics"]["total_wins"] / total_closed) * 100
                
                # Update best/worst trades
                if profit_loss > self.memory["live_statistics"]["best_trade"]:
                    self.memory["live_statistics"]["best_trade"] = profit_loss
                if profit_loss < self.memory["live_statistics"]["worst_trade"]:
                    self.memory["live_statistics"]["worst_trade"] = profit_loss
                
                break
        
        self.save_memory()
        print(f"📊 Trade Result Logged: {result} P/L: ${profit_loss:.2f}")
        
    def get_recent_activity(self, hours=24) -> Dict:
        """Get recent trading activity"""
        cutoff = datetime.now().timestamp() - (hours * 3600)
        
        recent = {
            "webhook_alerts": [],
            "trade_attempts": [],
            "executed_trades": [],
            "cancelled_trades": []
        }
        
        for alert in self.memory["webhook_alerts"]:
            if datetime.fromisoformat(alert["timestamp"]).timestamp() > cutoff:
                recent["webhook_alerts"].append(alert)
        
        for attempt in self.memory["trade_attempts"]:
            if datetime.fromisoformat(attempt["timestamp"]).timestamp() > cutoff:
                recent["trade_attempts"].append(attempt)
                
        for execution in self.memory["executed_trades"]:
            if datetime.fromisoformat(execution["timestamp"]).timestamp() > cutoff:
                recent["executed_trades"].append(execution)
                
        for cancellation in self.memory["cancelled_trades"]:
            if datetime.fromisoformat(cancellation["timestamp"]).timestamp() > cutoff:
                recent["cancelled_trades"].append(cancellation)
        
        return recent
    
    def get_live_statistics(self) -> Dict:
        """Get current live trading statistics"""
        return self.memory["live_statistics"].copy()
    
    def display_status(self):
        """Display current memory status"""
        stats = self.memory["live_statistics"]
        
        print("\n" + "="*60)
        print("📊 LIVE TRADING MEMORY STATUS")
        print("="*60)
        print(f"🔔 Webhook Alerts: {stats['total_webhook_alerts']}")
        print(f"🎯 Trade Attempts: {stats['total_trades_attempted']}")
        print(f"✅ Trades Executed: {stats['total_trades_executed']}")
        print(f"❌ Trades Cancelled: {stats['total_trades_cancelled']}")
        print(f"🏆 Wins: {stats['total_wins']} | 📉 Losses: {stats['total_losses']}")
        print(f"📈 Live Win Rate: {stats['live_win_rate']:.1f}%")
        print(f"💰 Current Balance: ${stats['current_balance']:.2f}")
        print(f"📊 Total P/L: ${stats['total_profit_loss']:.2f}")
        print(f"🎯 Best Trade: ${stats['best_trade']:.2f}")
        print(f"📉 Worst Trade: ${stats['worst_trade']:.2f}")

# Global instance for easy access
live_memory = LiveTradingMemory()

if __name__ == "__main__":
    # Display current status
    live_memory.display_status()
    
    # Show recent activity
    recent = live_memory.get_recent_activity(24)
    print(f"\n📈 Recent Activity (24 hours):")
    print(f"   Webhook alerts: {len(recent['webhook_alerts'])}")
    print(f"   Trade attempts: {len(recent['trade_attempts'])}")
    print(f"   Executions: {len(recent['executed_trades'])}")
    print(f"   Cancellations: {len(recent['cancelled_trades'])}")
