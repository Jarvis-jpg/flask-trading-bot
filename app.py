from flask import Flask, request, jsonify, render_template_string
from trade_logic import execute_trade
from utils.journal_logger import log_trade
from oanda_client import OandaClient
from tradingview_client import TradingViewClient
from trade_analyzer import TradeAnalyzer
from autonomous_trading_engine import autonomous_engine
from enhanced_trading_strategy import trading_strategy
from dotenv import load_dotenv
import os
import traceback
import json
from datetime import datetime

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
    """Enhanced dashboard with autonomous trading controls"""
    is_live = os.getenv('OANDA_LIVE', 'false').lower() == 'true'
    mode = "LIVE" if is_live else "PRACTICE"
    
    # Get engine status
    engine_status = autonomous_engine.get_status()
    
    dashboard_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Jarvis Autonomous Trading Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: #fff; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .header {{ text-align: center; padding: 20px; background: #2a2a2a; border-radius: 10px; margin-bottom: 20px; }}
            .status-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
            .status-card {{ background: #2a2a2a; padding: 20px; border-radius: 10px; border: 2px solid #444; }}
            .status-card.running {{ border-color: #4CAF50; }}
            .status-card.stopped {{ border-color: #f44336; }}
            .btn {{ padding: 10px 20px; margin: 5px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }}
            .btn-start {{ background: #4CAF50; color: white; }}
            .btn-stop {{ background: #f44336; color: white; }}
            .btn-test {{ background: #2196F3; color: white; }}
            .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; }}
            .stat-item {{ background: #333; padding: 10px; border-radius: 5px; text-align: center; }}
            .trades-list {{ max-height: 300px; overflow-y: auto; background: #333; padding: 10px; border-radius: 5px; }}
            .refresh {{ position: fixed; top: 20px; right: 20px; }}
        </style>
        <script>
            function refreshPage() {{ window.location.reload(); }}
            function startEngine() {{ fetch('/start_engine', {{method: 'POST'}}).then(() => refreshPage()); }}
            function stopEngine() {{ fetch('/stop_engine', {{method: 'POST'}}).then(() => refreshPage()); }}
            setInterval(refreshPage, 30000); // Auto-refresh every 30 seconds
        </script>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Jarvis Autonomous Trading Bot</h1>
                <h2>Mode: {mode} | Status: {'🟢 RUNNING' if engine_status['is_running'] else '🔴 STOPPED'}</h2>
                <button class="btn refresh btn-test" onclick="refreshPage()">🔄 Refresh</button>
            </div>
            
            <div class="status-grid">
                <div class="status-card {'running' if engine_status['is_running'] else 'stopped'}">
                    <h3>🎛️ Engine Controls</h3>
                    <p>Status: {'RUNNING' if engine_status['is_running'] else 'STOPPED'}</p>
                    <p>Trading Hours: {'✅ ACTIVE' if engine_status['trading_hours'] else '⏰ INACTIVE'}</p>
                    <button class="btn btn-start" onclick="startEngine()" {'disabled' if engine_status['is_running'] else ''}>
                        🚀 Start Engine
                    </button>
                    <button class="btn btn-stop" onclick="stopEngine()" {'disabled' if not engine_status['is_running'] else ''}>
                        🛑 Stop Engine
                    </button>
                    <br><br>
                    <a href="/test_connection" class="btn btn-test">🔧 Test Systems</a>
                </div>
                
                <div class="status-card">
                    <h3>📊 Daily Statistics</h3>
                    <div class="stats">
                        <div class="stat-item">
                            <strong>{engine_status['daily_stats']['trades_count']}</strong><br>
                            Total Trades
                        </div>
                        <div class="stat-item">
                            <strong>{engine_status['daily_stats']['wins']}</strong><br>
                            Wins
                        </div>
                        <div class="stat-item">
                            <strong>{engine_status['daily_stats']['losses']}</strong><br>
                            Losses
                        </div>
                        <div class="stat-item">
                            <strong>${engine_status['daily_stats']['profit_loss']:.2f}</strong><br>
                            P&L
                        </div>
                    </div>
                    <p>Win Rate: {(engine_status['daily_stats']['wins'] / max(engine_status['daily_stats']['trades_count'], 1) * 100):.1f}%</p>
                </div>
                
                <div class="status-card">
                    <h3>⚙️ Configuration</h3>
                    <p>Max Concurrent Trades: {engine_status['config']['max_concurrent_trades']}</p>
                    <p>Active Trades: {engine_status['active_trades']}</p>
                    <p>Max Daily Trades: {engine_status['config']['max_daily_trades']}</p>
                    <p>Max Daily Loss: ${engine_status['config']['max_daily_loss']}</p>
                    <p>Scan Interval: {engine_status['config']['scan_interval']}s</p>
                </div>
            </div>
            
            <div class="status-card" style="margin-top: 20px;">
                <h3>📈 Active Currency Pairs</h3>
                <p>{', '.join(engine_status['config']['active_pairs'])}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return dashboard_html

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

@app.route('/start_engine', methods=['POST'])
def start_engine():
    """Start the autonomous trading engine"""
    try:
        success = autonomous_engine.start_trading()
        if success:
            return jsonify({'status': 'success', 'message': 'Autonomous trading engine started'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to start engine'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/stop_engine', methods=['POST'])
def stop_engine():
    """Stop the autonomous trading engine"""
    try:
        autonomous_engine.stop_trading()
        return jsonify({'status': 'success', 'message': 'Autonomous trading engine stopped'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/engine_status')
def engine_status():
    """Get current engine status"""
    try:
        status = autonomous_engine.get_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/manual_trade', methods=['POST'])
def manual_trade():
    """Manual trade execution with enhanced strategy analysis"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        # Use enhanced strategy for analysis
        pair = data.get('pair', 'EUR_USD')
        
        # Get current market data (simplified)
        import pandas as pd
        import numpy as np
        from datetime import datetime, timedelta
        
        # Generate sample data for analysis
        dates = pd.date_range(end=datetime.now(), periods=100, freq='1H')
        prices = np.random.normal(1.0950, 0.01, 100).cumsum() * 0.001 + 1.0950
        
        market_data = pd.DataFrame({
            'datetime': dates,
            'open': prices * 0.9999,
            'high': prices * 1.0002,
            'low': prices * 0.9998,
            'close': prices,
            'volume': np.random.randint(1000, 5000, 100)
        }).set_index('datetime')
        
        # Generate signal using enhanced strategy
        signal = trading_strategy.generate_trade_signal(pair, market_data)
        
        if signal['signal'] != 'no_signal':
            # Execute the trade
            trade_data = {
                'pair': signal['pair'],
                'action': signal['signal'],
                'entry': signal['entry'],
                'stop_loss': signal['stop_loss'],
                'take_profit': signal['take_profit'],
                'units': signal['units'],
                'confidence': signal['confidence'],
                'strategy': signal['strategy'],
                'timestamp': signal['timestamp']
            }
            
            # Execute on OANDA
            trade_result = oanda.place_trade(trade_data)
            
            return jsonify({
                'status': 'executed',
                'signal': signal,
                'trade_result': trade_result
            })
        else:
            return jsonify({
                'status': 'no_signal',
                'signal': signal,
                'reason': signal.get('reason', 'No trading opportunity found')
            })
            
    except Exception as e:
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

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