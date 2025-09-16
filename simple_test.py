import requests

print("Testing Render deployment...")

# Test home
try:
    r = requests.get('https://jarvis-quant-sys.onrender.com/', timeout=10)
    print(f"Home: {r.status_code} - {r.text[:100]}")
except Exception as e:
    print(f"Home error: {e}")

# Test webhook
try:
    data = {"ticker": "EUR_USD", "strategy.order.action": "buy", "close": 1.0850, "strategy": "SevenSYS"}
    r = requests.post('https://jarvis-quant-sys.onrender.com/webhook', json=data, timeout=10)
    print(f"Webhook: {r.status_code} - {r.text[:200]}")
except Exception as e:
    print(f"Webhook error: {e}")
