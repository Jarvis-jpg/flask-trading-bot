import requests

def test_connection():
    try:
        # Test root endpoint
        root_response = requests.get("http://localhost:5000/")
        print(f"Root endpoint status: {root_response.status_code}")
        print(f"Root response: {root_response.text}\n")
        
        # Test webhook endpoint
        test_data = {
            "pair": "BTCUSDT",
            "action": "buy",
            "entry": 45000,
            "stop_loss": 44500,
            "take_profit": 46000,
            "confidence": 0.75,
            "strategy": "TEST",
            "timestamp": "2025-07-16T12:00:00Z"
        }
        
        webhook_response = requests.post("http://localhost:5000/webhook", json=test_data)
        print(f"Webhook endpoint status: {webhook_response.status_code}")
        print(f"Webhook response: {webhook_response.text}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Is the Flask server running?")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_connection()