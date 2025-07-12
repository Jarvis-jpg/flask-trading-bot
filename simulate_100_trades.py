import requests
import json
import time

url = "https://jarvis-quant-sys.onrender.com/webhook"

for i in range(100):
    trade = {
        "pair": "GBP_USD",
        "action": "buy" if i % 2 == 0 else "sell",
        "entry": 1.0850 + i * 0.0001,
        "stop_loss": 1.0820 + i * 0.0001,
        "take_profit": 1.0910 + i * 0.0001,
        "confidence": round(0.7 + 0.01 * (i % 3), 2),
        "timestamp": "2025-07-10T14:35:00Z"
    }

    response = requests.post(url, data=json.dumps(trade), headers={"Content-Type": "application/json"})
    print(f"{i+1}/100 => {response.status_code}: {response.text}")
    time.sleep(0.5)
