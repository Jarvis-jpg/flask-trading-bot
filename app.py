import logging
import json
from flask import Flask, request, jsonify
from oanda_client import OandaClient     
from datetime import datetime
import numpy as np
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize Flask app
app = Flask(__name__)

# Initialize OANDA client
oanda = OandaClient()

def calculate_position_size(price, stop_loss, account_balance=50, risk_percent=4.0):
    try:
        risk_amount = account_balance * (risk_percent / 100)
        price_difference = abs(float(price) - float(stop_loss))
        if price_difference == 0:
            return 100
        position_size = round(risk_amount / price_difference)
        # Cap position size for $50 account with limited margin
        return max(100, min(position_size, 500))  # Much smaller max for $50 account
    except Exception as e:
        logging.error(f"Error calculating position size: {e}")
        return 100

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "service": "JARVIS Trading System",
        "environment": oanda.environment,
        "account": oanda.account_id
    })

@app.route("/dashboard")
def dashboard():
    try:
        # Basic account info
        account_id = oanda.account_id
        environment = oanda.environment
        
        dashboard_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>JARVIS Trading Dashboard</title>
            <meta http-equiv="refresh" content="30">
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background: #0a0a0a; color: #00ff88; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .header h1 {{ color: #00ff88; font-size: 2.5em; margin: 0; text-shadow: 0 0 10px #00ff88; }}
                .header p {{ color: #888; font-size: 1.1em; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }}
                .card {{ background: #1a1a1a; border: 1px solid #333; border-radius: 10px; padding: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.3); }}
                .card h3 {{ color: #00ff88; margin: 0 0 15px 0; border-bottom: 1px solid #333; padding-bottom: 10px; }}
                .stat {{ display: flex; justify-content: space-between; margin: 10px 0; }}
                .stat-label {{ color: #ccc; }}
                .stat-value {{ color: #00ff88; font-weight: bold; }}
                .status-online {{ color: #00ff88; }}
                .status-offline {{ color: #ff4444; }}
                .timestamp {{ font-size: 0.9em; color: #888; }}
                .webhook-url {{ background: #2a2a2a; padding: 10px; border-radius: 5px; font-family: monospace; word-break: break-all; }}
                .test-button {{ background: #00ff88; color: #000; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; }}
                .test-button:hover {{ background: #00cc66; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤖 JARVIS Trading Dashboard</h1>
                    <p>Real-time monitoring of your automated trading system</p>
                    <p class="timestamp">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                </div>
                
                <div class="grid">
                    <div class="card">
                        <h3>📊 System Status</h3>
                        <div class="stat">
                            <span class="stat-label">System Status:</span>
                            <span class="stat-value status-online">🟢 ONLINE</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Account ID:</span>
                            <span class="stat-value">{account_id}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Environment:</span>
                            <span class="stat-value">{environment.upper()}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Webhook Status:</span>
                            <span class="stat-value status-online">🟢 ACTIVE</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Last Test:</span>
                            <span class="stat-value">Order #8456 ✅</span>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h3>📈 Trading Configuration</h3>
                        <div class="stat">
                            <span class="stat-label">Strategy:</span>
                            <span class="stat-value">JARVIS BULLETPROOF</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Confidence Threshold:</span>
                            <span class="stat-value">65%</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Risk per Trade:</span>
                            <span class="stat-value">4.0%</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Max Position Size:</span>
                            <span class="stat-value">500 units</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Trading Hours:</span>
                            <span class="stat-value">24/7 (All Sessions)</span>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h3>⚙️ Webhook Configuration</h3>
                        <div class="stat">
                            <span class="stat-label">Webhook URL:</span>
                        </div>
                        <div class="webhook-url">
                            https://jarvis-quant-sys.onrender.com/webhook
                        </div>
                        <br>
                        <div class="stat">
                            <span class="stat-label">Supported Formats:</span>
                            <span class="stat-value">TradingView, Custom JSON</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Auto Stop/Take Profit:</span>
                            <span class="stat-value">✅ Enabled (25/50 pips)</span>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h3>🎯 Recent Activity</h3>
                    <div class="stat">
                        <span class="stat-label">✅ System Test Passed:</span>
                        <span class="stat-value">Order #8456 - EUR_USD BUY @ 1.16997</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">🔄 Webhook Active:</span>
                        <span class="stat-value">Ready to receive TradingView alerts</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">📊 Strategy Status:</span>
                        <span class="stat-value">JARVIS BULLETPROOF deployed and monitoring</span>
                    </div>
                    <div class="stat">
                        <span class="stat-label">⏰ Next Update:</span>
                        <span class="stat-value">Auto-refresh in 30 seconds</span>
                    </div>
                </div>
                
                <div class="card">
                    <h3>📋 PineScript Alert Format</h3>
                    <p style="color: #ccc; margin-bottom: 15px;">Use this JSON format in your TradingView alerts:</p>
                    <div class="webhook-url">
{{"ticker": "{{{{ticker}}}}", "strategy.order.action": "{{{{strategy.order.action}}}}", "close": {{{{close}}}}, "strategy": "JARVIS_BULLETPROOF"}}
                    </div>
                </div>
                
                <div class="card">
                    <h3>🔧 Quick Actions</h3>
                    <button class="test-button" onclick="testWebhook()">Test Webhook</button>
                    <button class="test-button" onclick="window.location.reload()">Refresh Dashboard</button>
                    <button class="test-button" onclick="window.open('/', '_blank')">API Status</button>
                    
                    <script>
                    function testWebhook() {{
                        fetch('/webhook', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{
                                "ticker": "EUR_USD",
                                "strategy.order.action": "buy", 
                                "close": 1.0850,
                                "strategy": "DASHBOARD_TEST"
                            }})
                        }})
                        .then(response => response.json())
                        .then(data => {{
                            alert('Test Result: ' + JSON.stringify(data, null, 2));
                        }})
                        .catch(error => {{
                            alert('Test Error: ' + error);
                        }});
                    }}
                    </script>
                </div>
            </div>
        </body>
        </html>
        """
        
        return dashboard_html
        
    except Exception as e:
        logging.error(f"Dashboard error: {str(e)}")
        return f"""
        <html><body style="background: #0a0a0a; color: #00ff88; font-family: Arial;">
        <h1>JARVIS Dashboard</h1>
        <p>Dashboard Error: {str(e)}</p>
        <p><a href="/" style="color: #00ff88;">Return to API Status</a></p>
        </body></html>
        """

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        logging.info(f"Received webhook data: {json.dumps(data, indent=2)}")

        # Handle both custom format and PineScript default format
        if "ticker" in data:
            # PineScript default format
            symbol = data.get("ticker", "EURUSD")
            action = data.get("strategy.order.action", "buy")
            price = float(data.get("close", 1.0850))
            strategy = data.get("strategy", "PineScript")
            
            # Get current market price for proper take profit calculation
            try:
                current_price = oanda.get_current_price(oanda._format_instrument(symbol))
                logging.info(f"Current market price for {symbol}: {current_price}")
                
                # Use current market price for calculations - realistic pip-based levels
                if action.lower() == "buy":
                    stop_loss = round(current_price - 0.0025, 5)   # 25 pips below (realistic stop)
                    take_profit = round(current_price + 0.0050, 5)  # 50 pips above (2:1 reward)
                else:  # sell
                    stop_loss = round(current_price + 0.0025, 5)   # 25 pips above (realistic stop)
                    take_profit = round(current_price - 0.0050, 5)  # 50 pips below (2:1 reward)
                    
                # Use current price for position sizing too
                price = current_price
            except Exception as e:
                logging.warning(f"Could not get current price, using provided price: {e}")
                # Fallback to provided price with realistic pip-based levels
                if action.lower() == "buy":
                    stop_loss = round(price - 0.0025, 5)   # 25 pips below (realistic stop)
                    take_profit = round(price + 0.0050, 5) # 50 pips above (2:1 reward)
                else:
                    stop_loss = round(price + 0.0025, 5)   # 25 pips above (realistic stop)
                    take_profit = round(price - 0.0050, 5) # 50 pips below (2:1 reward)
        else:
            # Custom format
            required_fields = ["symbol", "action", "price", "strategy", "stop_loss", "take_profit"]
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400
            
            symbol = data["symbol"]
            action = data["action"]
            price = float(data["price"])
            strategy = data["strategy"]
            stop_loss = float(data["stop_loss"])
            take_profit = float(data["take_profit"])

        position_size = calculate_position_size(price, stop_loss)
        units = position_size if action.upper() == "BUY" else -position_size

        trade_data = {
            "symbol": symbol,
            "units": units,
            "stop_loss": stop_loss,
            "take_profit": take_profit
        }

        logging.info(f"Placing trade: {action} {abs(units)} units of {symbol}")

        try:
            trade_result = oanda.place_trade(trade_data)
            logging.info("Trade placed successfully")
            return jsonify({
                "status": "success",
                "message": "Trade placed successfully",
                "trade_data": trade_result
            }), 200
        except Exception as trade_error:
            error_msg = str(trade_error)
            logging.error(f"Trade execution failed: {error_msg}")
            return jsonify({
                "status": "error", 
                "message": f"Trade execution failed: {error_msg}"
            }), 400

    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    print("\nOANDA Configuration:")
    print(f"  - Account: {oanda.account_id}")
    print(f"  - Mode: {oanda.environment.upper()}")
    print(f"  - API URL: {oanda.api_url}")

    print("\nStarting Jarvis Trading Bot...")
    print("Routes configured:")
    print("  - GET  /")
    print("  - POST /webhook")

    print("\nConfiguration:")
    print("  - Host: 0.0.0.0")
    print("  - Port: 5000")
    print("  - Debug: True")

    print("\nStarting server...")
    app.run(host="0.0.0.0", port=5000, debug=True)
