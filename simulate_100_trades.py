import requests
import random
from datetime import datetime, timedelta

URL = "https://jarvis-quant-sys.onrender.com"
PAIRS = ["EUR_USD", "GBP_USD", "USD_JPY", "AUD_USD", "USD_CAD"]
ACTIONS = ["buy", "sell"]

base_time = datetime(2025, 6, 1, 12, 0)

for i in range(100):
    entry = round(random.uniform(1.0500, 1.1000), 4)
    sl = round(entry - 0.0030 if random.choice(ACTIONS) == "buy" else entry + 0.0030, 4)
    tp = round(entry + 0.0060 if sl < entry else entry - 0.0060, 4)

    trade = {
        "pair": random.choice(PAIRS),
        "action": random.choice(ACTIONS),
        "entry": entry,
        "stop_loss": sl,
        "take_profit": tp,
        "confidence": round(random.uniform(0.6, 0.95), 2),
        "timestamp": (base_time + timedelta(minutes=i * 15)).isoformat() + "Z"
    }

    response = requests.post(URL, json=trade)
    print(f"{i+1}/100 => {response.status_code}: {response.text}")
