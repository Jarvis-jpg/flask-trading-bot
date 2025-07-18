import requests
import json
from datetime import datetime, UTC, timedelta
import random
import time
import sys
from tqdm import tqdm

PAIRS = {
    "BTCUSDT": {"base": 45000, "volatility": 1000, "min_move": 0.5},
    "ETHUSDT": {"base": 2500, "volatility": 100, "min_move": 0.1},
    "SOLUSDT": {"base": 100, "volatility": 5, "min_move": 0.01},
    "MATICUSDT": {"base": 1.5, "volatility": 0.1, "min_move": 0.001},
    "DOGEUSDT": {"base": 0.1, "volatility": 0.01, "min_move": 0.00001}
}

def generate_trade(timestamp=None):
    """Generate realistic trade data with price action patterns"""
    pair = random.choice(list(PAIRS.keys()))
    pair_info = PAIRS[pair]
    
    # Generate price with minimal movement consideration
    price = round(pair_info["base"] + random.uniform(-pair_info["volatility"], pair_info["volatility"]), 6)
    price = round(price / pair_info["min_move"]) * pair_info["min_move"]
    
    action = random.choice(["buy", "sell"])
    confidence = round(random.uniform(0.65, 0.95), 2)
    
    # Risk management: 1-2% stop loss, 2-4% take profit
    sl_percent = random.uniform(0.01, 0.02)
    tp_percent = random.uniform(0.02, 0.04)
    
    if action == "buy":
        stop_loss = round(price * (1 - sl_percent), 6)
        take_profit = round(price * (1 + tp_percent), 6)
    else:
        stop_loss = round(price * (1 + sl_percent), 6)
        take_profit = round(price * (1 - tp_percent), 6)
    
    if timestamp is None:
        timestamp = datetime.now(UTC)
    
    return {
        "pair": pair,
        "action": action,
        "entry": price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "confidence": confidence,
        "strategy": "MACD+EMA",
        "timestamp": timestamp.isoformat().replace('+00:00', 'Z')
    }