import requests

URL = "https://jarvis-quant-sys.onrender.com/webhook"  # Your Render URL

trade = {
    "pair": "EURUSD",
    "action": "buy",
    "entry": 1.1234,
    "stop_loss": 1.1200,
    "take_profit": 1.1294,
    "confidence": 0.75,
    "strategy": "MACD+EMA",
    "timestamp": "2025-07-14T00:00:00Z"
}

response = requests.post(URL, json=trade)
print(f"Status: {response.status_code}")
print("Response:", response.text)
