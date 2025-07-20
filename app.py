from flask import Flask, request, jsonify
from trade_logic import execute_trade
from utils.journal_logger import log_trade

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to Jarvis Dashboard</h1>"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        try:
            result = execute_trade(data)
            return jsonify({'status': 'Trade executed', 'details': result}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid request method'}), 405

if __name__ == '__main__':
    try:
        print("\n🚀 Starting Jarvis Trading Bot...")
        print("📡 Routes configured:")
        print("  - GET  /")
        print("  - POST /webhook")
        print("\n⚙️ Configuration:")
        print("  - Host: 0.0.0.0")
        print("  - Port: 5000")
        print("  - Debug: True")
        print("\n🔄 Starting server...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"\n❌ Error starting server: {str(e)}")
        import traceback
        print(traceback.format_exc())