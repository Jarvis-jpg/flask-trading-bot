#!/usr/bin/env python3
"""
Test the Live Trading Memory System
Simulate webhook alerts and trade cancellations to understand what happened
"""
from live_trading_memory import live_memory
import json

def simulate_your_trade_scenario():
    """Simulate what happened when your trade was cancelled"""
    
    print("🧪 SIMULATING YOUR TRADE SCENARIO")
    print("="*50)
    
    # Simulate TradingView webhook alert (example of what might have come in)
    webhook_data = {
        "pair": "EURUSD",
        "action": "buy", 
        "entry": 1.0856,
        "stop_loss": 1.0806,
        "take_profit": 1.0956,
        "confidence": 0.75,
        "strategy": "JARVIS",
        "timestamp": "2025-09-07T14:30:00Z"
    }
    
    print("📡 STEP 1: TradingView sends webhook alert")
    print(json.dumps(webhook_data, indent=2))
    
    # Log the webhook alert
    live_memory.log_webhook_alert(webhook_data)
    
    # Simulate trade attempt with analysis
    analysis_result = {
        "prediction": {
            "recommended": True,
            "confidence": 0.72
        },
        "market_conditions": {
            "trend_strength": 0.65,
            "session": "london",
            "volatility": "normal"
        }
    }
    
    oanda_trade_data = {
        "pair": "EUR_USD",
        "units": 10000,
        "stop_loss": 1.0806,
        "take_profit": 1.0956
    }
    
    print("\n🎯 STEP 2: System analyzes trade")
    live_memory.log_trade_attempt(oanda_trade_data, analysis_result)
    
    # Simulate cancellation (this is probably what happened to your trade)
    possible_cancellation_reasons = [
        {
            "reason": "execution_failed",
            "details": {
                "error": "Insufficient margin",
                "available_margin": 45.0,
                "required_margin": 100.0
            }
        },
        {
            "reason": "oanda_api_error", 
            "details": {
                "error": "Invalid price",
                "stop_loss_precision": "too many decimal places"
            }
        },
        {
            "reason": "market_closed",
            "details": {
                "current_time": "2025-09-07T22:00:00Z",
                "market_status": "closed for weekend"
            }
        },
        {
            "reason": "unfavorable_analysis",
            "details": {
                "ai_confidence": 0.72,
                "required_confidence": 0.75,
                "message": "Below minimum confidence threshold"
            }
        }
    ]
    
    # Test each possible scenario
    for i, scenario in enumerate(possible_cancellation_reasons, 1):
        print(f"\n❌ SCENARIO {i}: Trade cancelled - {scenario['reason']}")
        print(f"   Details: {scenario['details']}")
        
        # This would log the actual cancellation
        # live_memory.log_trade_cancellation(oanda_trade_data, scenario['reason'], scenario['details'])
    
    print(f"\n📊 Current Memory Status:")
    live_memory.display_status()
    
    print(f"\n💡 TO FIND OUT WHAT REALLY HAPPENED:")
    print(f"   1. Check live_trading_memory.json for real cancellation reasons")
    print(f"   2. Look at Flask terminal output during trade attempt")
    print(f"   3. Check OANDA web platform for rejected orders")
    print(f"   4. Monitor webhook alerts vs actual executions")

if __name__ == "__main__":
    simulate_your_trade_scenario()
