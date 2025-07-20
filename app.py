from flask import Flask, request, jsonify
from trade_logic import execute_trade
from utils.journal_logger import log_trade
from oanda_client import OandaClient
from tradingview_client import TradingViewClient
from trade_analyzer import TradeAnalyzer
from dotenv import load_dotenv
import os
import traceback

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize clients with loaded configuration
oanda = OandaClient()
tradingview = TradingViewClient()
analyzer = TradeAnalyzer()

# Log startup configuration
print(f"\n🔐 OANDA Configuration:")
print(f"  - Account: {os.getenv('OANDA_ACCOUNT_ID')}")
print(f"  - Mode: {'LIVE' if os.getenv('OANDA_LIVE', 'false').lower() == 'true' else 'PRACTICE'}")
print(f"  - API URL: {os.getenv('OANDA_API_URL')}")

@app.route('/')
def home():
    is_live = os.getenv('OANDA_LIVE', 'false').lower() == 'true'
    mode = "LIVE" if is_live else "PRACTICE"
    return f"<h1>Welcome to Jarvis Dashboard</h1><p>Running in {mode} mode</p>"

@app.route('/test_connection')
def test_connection():
    """Test all system components"""
    try:
        results = {
            'status': 'success',
            'components': {},
            'environment': {
                'mode': 'LIVE' if os.getenv('OANDA_LIVE', 'false').lower() == 'true' else 'PRACTICE',
                'api_url': os.getenv('OANDA_API_URL'),
                'account_id': os.getenv('OANDA_ACCOUNT_ID')
            }
        }

        # Test OANDA connection
        price_data = None
        try:
            price_data = oanda.get_current_price('EUR_USD')
            results['components']['oanda'] = {
                'status': 'ok',
                'price_data': price_data
            }
        except Exception as e:
            results['components']['oanda'] = {
                'status': 'error',
                'error': str(e),
                'traceback': traceback.format_exc()
            }
            return jsonify(results)  # Return early if OANDA connection fails

        # Test analyzer with basic market check
        try:
            # First check if market is open
            analysis = analyzer.analyze_trade('EUR_USD', None)
            
            if analysis.get('status') == 'market_closed':
                # Market is closed, report status
                results['components']['analyzer'] = {
                    'status': 'ok',
                    'market_status': 'closed',
                    'details': analysis
                }
            else:
                # Market is open, do full analysis
                test_data = {
                    'pair': 'EUR_USD',
                    'action': 'buy',
                    'entry': price_data['ask'],
                    'stop_loss': price_data['ask'] - 0.0050,
                    'take_profit': price_data['ask'] + 0.0100,
                    'units': 1000,
                    'confidence': 0.8
                }
                analysis = analyzer.analyze_trade(test_data['pair'], test_data)
                results['components']['analyzer'] = {
                    'status': 'ok',
                    'market_status': 'open',
                    'analysis': analysis
                }
        except Exception as e:
            results['components']['analyzer'] = {
                'status': 'error',
                'error': str(e)
            }

        # Test TradingView configuration
        tv_status = tradingview.webhook_url is not None
        results['components']['tradingview'] = {
            'status': 'ok' if tv_status else 'not_configured',
            'webhook_url': tradingview.webhook_url if tv_status else None
        }

        return jsonify(results)

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        try:
            # First check market status
            market_check = analyzer.analyze_trade(data['pair'], None)
            if market_check.get('status') == 'market_closed':
                return jsonify({
                    'status': 'rejected',
                    'reason': 'market_closed',
                    'details': market_check
                }), 200

            # If market is open, analyze the trade setup
            analysis = analyzer.analyze_trade(data['pair'], data)
            
            # Check if analysis recommends the trade
            if analysis.get('prediction', {}).get('recommended', False):
                # Execute trade on OANDA
                trade_result = oanda.place_trade(data)
                
                # Update TradingView
                tradingview.send_trade_alert(data)
                tradingview.update_chart_annotation(data)
                
                # Log the trade
                log_data = {
                    **trade_result,
                    **data,
                    'analysis': analysis
                }
                log_trade(log_data)
                
                # Track trade performance for model improvement
                analyzer.track_trade_performance({
                    'pair': data['pair'],
                    'profit': trade_result.get('profit', 0),
                    'entry_price': trade_result.get('filled_price'),
                    'exit_price': None,  # Will be updated when trade is closed
                    'duration': 0,  # Will be updated when trade is closed
                    'market_conditions': analysis.get('market_conditions', {}),
                    'trade_setup': data
                })
                
                return jsonify({
                    'status': 'executed',
                    'details': trade_result,
                    'analysis': analysis
                }), 200
            else:
                return jsonify({
                    'status': 'rejected',
                    'reason': 'unfavorable_analysis',
                    'analysis': analysis
                }), 200
                
        except Exception as e:
            import traceback
            print(f"❌ Error in webhook: {str(e)}")
            print(traceback.format_exc())
            return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500
    
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