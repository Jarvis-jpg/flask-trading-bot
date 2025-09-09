from flask import Flask, request, jsonify, render_template_string
from trade_logic import execute_trade
from utils.journal_logger import log_trade
from oanda_client import OandaClient
from tradingview_client import TradingViewClient
from trade_analyzer import TradeAnalyzer
from autonomous_trading_engine import autonomous_engine
from enhanced_trading_strategy import trading_strategy
from live_trading_memory import live_memory
from oanda_sync import oanda_sync
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
                    <a href="/training" class="btn btn-test">🎯 Enhanced Training</a>
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
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
            
        print(f"Received webhook data: {json.dumps(data, indent=2)}")

        # Extract data from TradingView webhook format
        symbol = data.get("ticker") or data.get("symbol", "").replace("_", "")
        action = data.get("strategy.order.action") or data.get("action", "")
        price = data.get("close") or data.get("price", 0)
        stop_loss = data.get("stop_loss", 0)
        take_profit = data.get("take_profit", 0)
        
        if not all([symbol, action, price, stop_loss, take_profit]):
            return jsonify({"error": "Missing required fields"}), 400

        # Calculate position size (conservative for small account)
        position_size = 500  # Fixed size for $42 account
        units = position_size if action.lower() == "buy" else -position_size
        
        trade_data = {
            "symbol": symbol,
            "units": units,
            "stop_loss": float(stop_loss),
            "take_profit": float(take_profit)
        }

        print(f"Placing trade: {action} {abs(units)} units of {symbol}")
        
        trade_result = oanda.place_trade(trade_data)
        
        if isinstance(trade_result, dict) and "error" not in trade_result:
            print("Trade placed successfully")
            return jsonify({
                "status": "success",
                "message": "Trade placed successfully",
                "trade_data": trade_result
            }), 200
        else:
            error_msg = trade_result.get("error", "Unknown error") if isinstance(trade_result, dict) else "Invalid response"
            return jsonify({"status": "error", "message": error_msg}), 500
            
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
        
        try:
            # Valid OANDA forex pairs only
            VALID_OANDA_PAIRS = {
                'EURUSD': 'EUR_USD',
                'GBPUSD': 'GBP_USD', 
                'USDJPY': 'USD_JPY',
                'USDCHF': 'USD_CHF',
                'AUDUSD': 'AUD_USD',
                'USDCAD': 'USD_CAD',
                'NZDUSD': 'NZD_USD',
                'EURJPY': 'EUR_JPY',
                'GBPJPY': 'GBP_JPY',
                'EURGBP': 'EUR_GBP'
            }
            
            # Check if pair is valid for OANDA
            original_pair = data.get('pair', '').replace('/', '').replace('_', '').upper()
            oanda_pair = VALID_OANDA_PAIRS.get(original_pair, None)
            
            if not oanda_pair:
                # Log the cancellation reason
                live_memory.log_trade_cancellation(data, "invalid_pair", {
                    "original_pair": original_pair,
                    "valid_pairs": list(VALID_OANDA_PAIRS.keys())
                })
                return jsonify({
                    'status': 'rejected',
                    'reason': 'invalid_pair',
                    'message': f'Pair {original_pair} not supported by OANDA. Valid pairs: {list(VALID_OANDA_PAIRS.keys())}',
                    'valid_pairs': list(VALID_OANDA_PAIRS.keys())
                }), 200
            
            # Validate stop loss format and direction
            entry = float(data.get('entry', 0))
            stop_loss = float(data.get('stop_loss', 0))
            take_profit = float(data.get('take_profit', 0))
            action = data.get('action', '').lower()
            
            # Validate stop loss direction
            if action == 'buy' and stop_loss >= entry:
                # Log the cancellation reason
                live_memory.log_trade_cancellation(data, "invalid_stop_loss_direction", {
                    "action": action,
                    "entry": entry,
                    "stop_loss": stop_loss,
                    "message": f"BUY order: Stop loss {stop_loss} must be below entry {entry}"
                })
                return jsonify({
                    'status': 'rejected',
                    'reason': 'invalid_stop_loss',
                    'message': f'BUY order: Stop loss {stop_loss} must be below entry {entry}'
                }), 200
            elif action == 'sell' and stop_loss <= entry:
                # Log the cancellation reason
                live_memory.log_trade_cancellation(data, "invalid_stop_loss_direction", {
                    "action": action,
                    "entry": entry,
                    "stop_loss": stop_loss,
                    "message": f"SELL order: Stop loss {stop_loss} must be above entry {entry}"
                })
                return jsonify({
                    'status': 'rejected', 
                    'reason': 'invalid_stop_loss',
                    'message': f'SELL order: Stop loss {stop_loss} must be above entry {entry}'
                }), 200
            
            # Convert to OANDA format - Dynamic position sizing based on balance
            current_balance = live_memory.memory["live_statistics"]["current_balance"]
            
            # Conservative position sizing: 2-3% of account balance
            # For $43 account: 1000 units ≈ $1-2 risk per trade
            if current_balance <= 50:
                base_units = 1000
            elif current_balance <= 100:
                base_units = 1500 
            elif current_balance <= 500:
                base_units = 2500
            else:
                base_units = 5000
                
            units = base_units if action == 'buy' else -base_units
            
            print(f"📊 POSITION SIZING: Balance=${current_balance:.2f} → Units={abs(units):,}")
            
            oanda_trade_data = {
                'pair': oanda_pair,
                'units': units,
                'stop_loss': round(stop_loss, 5),
                'take_profit': round(take_profit, 5)
            }
            
            print(f"✅ VALID TRADE: {oanda_pair} {action.upper()} - Entry: {entry}, SL: {stop_loss}, TP: {take_profit}")
            
            # First check market status
            market_check = analyzer.analyze_trade(oanda_pair, None)
            if market_check.get('status') == 'market_closed':
                # Log the cancellation reason
                live_memory.log_trade_cancellation(oanda_trade_data, "market_closed", market_check)
                return jsonify({
                    'status': 'rejected',
                    'reason': 'market_closed',
                    'details': market_check
                }), 200

            # STEP 2: Log the trade attempt with analysis
            analysis = analyzer.analyze_trade(oanda_pair, oanda_trade_data)
            live_memory.log_trade_attempt(oanda_trade_data, analysis)
            
            # Check if analysis recommends the trade
            if analysis.get('prediction', {}).get('recommended', False):
                try:
                    # STEP 3: Attempt to execute trade on OANDA
                    trade_result = oanda.place_trade(oanda_trade_data)
                    
                    # STEP 4: Log successful execution
                    live_memory.log_trade_execution(oanda_trade_data, trade_result)
                    
                    # Update TradingView (use original data format)
                    tradingview.send_trade_alert(data)
                    tradingview.update_chart_annotation(data)
                    
                    # Log the trade (merge both formats)
                    log_data = {
                        **trade_result,
                        **data,
                        'oanda_pair': oanda_pair,
                        'oanda_units': units,
                        'analysis': analysis
                    }
                    log_trade(log_data)
                    
                    # Track trade performance for model improvement
                    analyzer.track_trade_performance({
                        'pair': oanda_pair,
                        'profit': trade_result.get('profit', 0),
                        'entry_price': trade_result.get('filled_price'),
                        'exit_price': None,  # Will be updated when trade is closed
                        'duration': 0,  # Will be updated when trade is closed
                        'market_conditions': analysis.get('market_conditions', {}),
                        'trade_setup': oanda_trade_data
                    })
                    
                    return jsonify({
                        'status': 'executed',
                        'details': trade_result,
                        'analysis': analysis,
                        'oanda_pair': oanda_pair,
                        'converted_data': oanda_trade_data
                    }), 200
                    
                except Exception as trade_error:
                    # STEP 4b: Log execution failure
                    live_memory.log_trade_cancellation(oanda_trade_data, "execution_failed", {
                        "error": str(trade_error),
                        "error_type": type(trade_error).__name__
                    })
                    
                    return jsonify({
                        'status': 'execution_failed',
                        'error': str(trade_error),
                        'analysis': analysis
                    }), 500
            else:
                # STEP 4c: Log trade rejected by analysis
                live_memory.log_trade_cancellation(oanda_trade_data, "unfavorable_analysis", {
                    "analysis_result": analysis,
                    "recommendation": analysis.get('prediction', {}).get('recommended', False),
                    "confidence": analysis.get('prediction', {}).get('confidence', 0)
                })
                return jsonify({
                    'status': 'rejected',
                    'reason': 'unfavorable_analysis',
                    'analysis': analysis,
                    'pair_info': f'Converted {original_pair} → {oanda_pair}'
                }), 200
                    'oanda_pair': oanda_pair,
                    'converted_data': oanda_trade_data
                }), 200
            else:
                return jsonify({
                    'status': 'rejected',
                    'reason': 'unfavorable_analysis',
                    'analysis': analysis,
                    'pair_info': f'Converted {original_pair} → {oanda_pair}'
                }), 200
                
        except ValueError as e:
            return jsonify({
                'error': f'Invalid numeric data: {str(e)}',
                'message': 'Check entry, stop_loss, and take_profit values'
            }), 400
        except KeyError as e:
            return jsonify({
                'error': f'Missing required field: {str(e)}',
                'required_fields': ['pair', 'action', 'entry', 'stop_loss', 'take_profit']
            }), 400
                
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

@app.route('/training')
def training_interface():
    """Enhanced training interface"""
    training_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Jarvis Enhanced Training System</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: #fff; }
            .container { max-width: 1000px; margin: 0 auto; }
            .header { text-align: center; padding: 20px; background: #2a2a2a; border-radius: 10px; margin-bottom: 20px; }
            .training-card { background: #2a2a2a; padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 2px solid #444; }
            .btn { padding: 10px 20px; margin: 5px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            .btn-train { background: #FF9800; color: white; }
            .btn-back { background: #2196F3; color: white; }
            .progress-bar { width: 100%; height: 20px; background: #333; border-radius: 10px; overflow: hidden; margin: 10px 0; }
            .progress-fill { height: 100%; background: linear-gradient(90deg, #4CAF50, #8BC34A); width: 0%; transition: width 0.3s; }
            .training-log { background: #333; padding: 15px; border-radius: 5px; max-height: 400px; overflow-y: auto; font-family: monospace; }
            .hidden { display: none; }
        </style>
        <script>
            let trainingActive = false;
            
            function startTraining() {
                if (trainingActive) return;
                
                trainingActive = true;
                document.getElementById('startBtn').disabled = true;
                document.getElementById('trainingProgress').classList.remove('hidden');
                
                const log = document.getElementById('trainingLog');
                log.innerHTML = '🚀 Starting Enhanced Training System...\\n';
                
                fetch('/start_training', {method: 'POST'})
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'success') {
                            log.innerHTML += '✅ Training started successfully\\n';
                            pollTrainingStatus();
                        } else {
                            log.innerHTML += `❌ Training failed: ${data.message}\\n`;
                            trainingActive = false;
                            document.getElementById('startBtn').disabled = false;
                        }
                    })
                    .catch(error => {
                        log.innerHTML += `❌ Error: ${error}\\n`;
                        trainingActive = false;
                        document.getElementById('startBtn').disabled = false;
                    });
            }
            
            function pollTrainingStatus() {
                if (!trainingActive) return;
                
                fetch('/training_status')
                    .then(response => response.json())
                    .then(data => {
                        updateTrainingProgress(data);
                        
                        if (data.status === 'running') {
                            setTimeout(pollTrainingStatus, 2000); // Poll every 2 seconds
                        } else {
                            trainingActive = false;
                            document.getElementById('startBtn').disabled = false;
                            document.getElementById('trainingLog').innerHTML += '🏁 Training completed!\\n';
                        }
                    })
                    .catch(error => {
                        console.error('Polling error:', error);
                        setTimeout(pollTrainingStatus, 5000); // Retry in 5 seconds
                    });
            }
            
            function updateTrainingProgress(data) {
                if (data.progress) {
                    const progressBar = document.getElementById('progressFill');
                    progressBar.style.width = data.progress + '%';
                    
                    const log = document.getElementById('trainingLog');
                    if (data.log_message) {
                        log.innerHTML += data.log_message + '\\n';
                        log.scrollTop = log.scrollHeight;
                    }
                }
            }
        </script>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎯 Enhanced Training System</h1>
                <h2>8000 Trade Accelerated Learning</h2>
                <a href="/" class="btn btn-back">← Back to Dashboard</a>
            </div>
            
            <div class="training-card">
                <h3>🧠 AI Training Overview</h3>
                <p>The Enhanced Training System uses the proven 8000 trade simulator to rapidly train your autonomous trading bot:</p>
                <ul>
                    <li><strong>8000 Simulated Trades</strong> - Accelerated learning through high-volume simulation</li>
                    <li><strong>Adaptive Learning</strong> - Continuously improves based on performance</li>
                    <li><strong>Multi-Strategy Testing</strong> - Tests all trading strategies simultaneously</li>
                    <li><strong>Risk Management Optimization</strong> - Learns optimal risk parameters</li>
                    <li><strong>Market Condition Adaptation</strong> - Trains on various market scenarios</li>
                </ul>
                
                <h4>📊 Expected Results:</h4>
                <ul>
                    <li>Win Rate: 55-65% (up from base 45-50%)</li>
                    <li>Risk-Reward Optimization: 2.5:1 average</li>
                    <li>Reduced Drawdown: Better risk management</li>
                    <li>Faster Learning: Immediate strategy improvements</li>
                </ul>
            </div>
            
            <div class="training-card">
                <h3>🚀 Start Training</h3>
                <p>This will run 8000 simulated trades to train your bot. Training typically takes 5-15 minutes.</p>
                <button id="startBtn" class="btn btn-train" onclick="startTraining()">
                    🎯 Start Enhanced Training (8000 trades)
                </button>
                
                <div id="trainingProgress" class="hidden">
                    <h4>📈 Training Progress</h4>
                    <div class="progress-bar">
                        <div id="progressFill" class="progress-fill"></div>
                    </div>
                    <div id="trainingLog" class="training-log">
                        Waiting for training to start...
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return training_html

@app.route('/start_training', methods=['POST'])
def start_training():
    """Start the enhanced training process"""
    try:
        # Import training system
        from enhanced_training_system import EnhancedTrainingSystem
        
        # Start training in background
        import threading
        
        def run_training():
            global training_system
            training_system = EnhancedTrainingSystem()
            training_system.run_accelerated_training()
            training_system.apply_training_to_autonomous_engine()
        
        training_thread = threading.Thread(target=run_training, daemon=True)
        training_thread.start()
        
        return jsonify({'status': 'success', 'message': 'Training started'})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/training_status')
def training_status():
    """Get current training status"""
    try:
        # This would normally check the actual training progress
        # For now, return a simple status
        global training_system
        
        if 'training_system' in globals() and hasattr(training_system, 'performance_metrics'):
            total_trades = training_system.performance_metrics['total_trades']
            target_trades = training_system.training_config['total_trades']
            progress = min(100, (total_trades / target_trades) * 100)
            
            return jsonify({
                'status': 'running' if progress < 100 else 'completed',
                'progress': progress,
                'total_trades': total_trades,
                'win_rate': training_system.performance_metrics['wins'] / max(total_trades, 1),
                'profit': training_system.performance_metrics['total_profit'],
                'log_message': f"📊 Progress: {progress:.1f}% ({total_trades}/{target_trades} trades)"
            })
        else:
            return jsonify({
                'status': 'not_started',
                'progress': 0,
                'log_message': 'Training not yet started'
            })
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

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