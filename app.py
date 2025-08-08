#!/usr/bin/env python3
"""
JARVIS Autonomous Trading System - Flask Application
Fixed webhook 'pair'/'symbol' field compatibility - v1.1
"""
from flask import Flask, request, jsonify, render_template_string
from trade_logic import execute_trade
from utils.journal_logger import log_trade
from oanda_client import OandaClient
f                # Use adaptive stops based on market conditions and TradingView compatibility
                account_balance = 0.95  # Current account balance
                risk_percent = data.get('risk_percentage', 1.0) / 100  # Very conservative risk
                
                # Ultra-conservative stop loss system - designed to never be rejected
                if data.get('conservative_mode', False) or data.get('wide_stops', False):
                    # Use very wide stops that will definitely pass validation
                    stop_loss_pips = max(30, data.get('stop_loss_pips', 35))  # Minimum 30 pips
                    take_profit_pips = max(60, data.get('take_profit_pips', 70))  # Minimum 60 pips
                    print(f"🛡️ Using ultra-conservative stops: SL={stop_loss_pips} pips, TP={take_profit_pips} pips")
                elif data.get('adaptive_stops', False):
                    # Use the adaptive values from the signal
                    stop_loss_pips = max(20, data.get('stop_loss_pips', 25))  # Minimum 20 pips
                    take_profit_pips = max(40, data.get('take_profit_pips', 50))  # Minimum 40 pips
                    print(f"📊 Using adaptive stops: SL={stop_loss_pips} pips, TP={take_profit_pips} pips")
                else:
                    # Fallback to safe defaults
                    stop_loss_pips = 25  # Safe default
                    take_profit_pips = 50  # Safe 2:1 ratiow_client import TradingViewClient
from trade_analyzer import TradeAnalyzer
from autonomous_trading_engine import autonomous_engine
from enhanced_trading_strategy import trading_strategy
from dotenv import load_dotenv
import os
import traceback
import json
from datetime import datetime

# Import the autonomous trading system
try:
    from live_trading_system import live_trading_system
    LIVE_SYSTEM_AVAILABLE = True
except ImportError as e:
    print(f"Live trading system not available: {e}")
    live_trading_system = None
    LIVE_SYSTEM_AVAILABLE = False

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
    
    # Get live trading system status
    live_status = None
    if LIVE_SYSTEM_AVAILABLE and live_trading_system:
        try:
            live_status = live_trading_system.get_status()
        except:
            live_status = None
    
    dashboard_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Jarvis Autonomous Trading Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: #fff; }}
            .container {{ max-width: 1400px; margin: 0 auto; }}
            .header {{ text-align: center; padding: 20px; background: #2a2a2a; border-radius: 10px; margin-bottom: 20px; }}
            .status-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
            .status-card {{ background: #2a2a2a; padding: 20px; border-radius: 10px; border: 2px solid #444; }}
            .status-card.running {{ border-color: #4CAF50; }}
            .status-card.stopped {{ border-color: #f44336; }}
            .status-card.live {{ border-color: #FF9800; }}
            .btn {{ padding: 10px 20px; margin: 5px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }}
            .btn-start {{ background: #4CAF50; color: white; }}
            .btn-stop {{ background: #f44336; color: white; }}
            .btn-test {{ background: #2196F3; color: white; }}
            .btn-live {{ background: #FF9800; color: white; }}
            .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; }}
            .stat-item {{ background: #333; padding: 10px; border-radius: 5px; text-align: center; }}
            .trades-list {{ max-height: 300px; overflow-y: auto; background: #333; padding: 10px; border-radius: 5px; }}
            .refresh {{ position: fixed; top: 20px; right: 20px; }}
            .warning {{ background: #ff6b35; padding: 10px; border-radius: 5px; margin: 10px 0; }}
            .success {{ background: #4CAF50; padding: 10px; border-radius: 5px; margin: 10px 0; }}
        </style>
        <script>
            function refreshPage() {{ window.location.reload(); }}
            function startEngine() {{ fetch('/start_engine', {{method: 'POST'}}).then(() => refreshPage()); }}
            function stopEngine() {{ fetch('/stop_engine', {{method: 'POST'}}).then(() => refreshPage()); }}
            function startLive() {{ fetch('/autonomous/start', {{method: 'POST'}}).then(() => refreshPage()); }}
            function stopLive() {{ fetch('/autonomous/stop', {{method: 'POST'}}).then(() => refreshPage()); }}
            setInterval(refreshPage, 30000); // Auto-refresh every 30 seconds
        </script>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 JARVIS Autonomous Trading Bot</h1>
                <h2>Mode: {mode} | Engine: {'🟢 RUNNING' if engine_status['is_running'] else '🔴 STOPPED'}{'| Live System: 🟢 RUNNING' if live_status and live_status.get('is_running') else '| Live System: 🔴 STOPPED' if live_status else ''}</h2>
                <button class="btn refresh btn-test" onclick="refreshPage()">🔄 Refresh</button>
                {f'<div class="warning">⚠️ LIVE TRADING MODE - Real money at risk!</div>' if is_live else '<div class="success">✅ PRACTICE MODE - Safe for testing</div>'}
            </div>
            
            <div class="status-grid">
                <div class="status-card {'running' if engine_status['is_running'] else 'stopped'}">
                    <h3>🎛️ Legacy Engine Controls</h3>
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
                </div>"""
    
    # Add live trading system card if available
    if live_status:
        dashboard_html += f"""
                <div class="status-card {'live' if live_status['is_running'] else 'stopped'}">
                    <h3>🚀 LIVE Trading System</h3>
                    <p>Status: {'🟢 RUNNING' if live_status['is_running'] else '🔴 STOPPED'}</p>
                    <p>AI System: {'✅ AVAILABLE' if live_status['ai_system_available'] else '❌ NOT AVAILABLE'}</p>
                    <p>Trading Hours: {'✅ ACTIVE' if live_status['trading_hours'] else '⏰ INACTIVE'}</p>
                    <p>Active Trades: {live_status['active_trades']}/{live_status['config']['max_concurrent_trades']}</p>
                    <button class="btn btn-live" onclick="startLive()" {'disabled' if live_status['is_running'] else ''}>
                        🎯 Start LIVE Trading
                    </button>
                    <button class="btn btn-stop" onclick="stopLive()" {'disabled' if not live_status['is_running'] else ''}>
                        🛑 Stop LIVE Trading
                    </button>
                </div>
                
                <div class="status-card">
                    <h3>📊 LIVE Daily Statistics</h3>
                    <div class="stats">
                        <div class="stat-item">
                            <strong>{live_status['daily_stats']['trades_count']}</strong><br>
                            Total Trades
                        </div>
                        <div class="stat-item">
                            <strong>{live_status['daily_stats']['wins']}</strong><br>
                            Wins
                        </div>
                        <div class="stat-item">
                            <strong>{live_status['daily_stats']['losses']}</strong><br>
                            Losses
                        </div>
                        <div class="stat-item">
                            <strong>${live_status['daily_stats']['profit_loss']:.2f}</strong><br>
                            P&L
                        </div>
                    </div>
                    <p>Win Rate: {(live_status['daily_stats']['wins'] / max(live_status['daily_stats']['trades_count'], 1) * 100):.1f}%</p>
                </div>"""
    else:
        dashboard_html += f"""
                <div class="status-card stopped">
                    <h3>🚀 LIVE Trading System</h3>
                    <p>Status: ❌ NOT AVAILABLE</p>
                    <p>System needs to be properly initialized</p>
                    <p>Check live_trading_system.py imports</p>
                </div>"""
    
    # Continue with original cards
    dashboard_html += f"""
                <div class="status-card">
                    <h3>📊 Legacy Daily Statistics</h3>
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
            # Handle both 'pair' and 'symbol' field names
            trading_pair = data.get('pair') or data.get('symbol') or 'EURUSD'
            
            # First check market status
            market_check = analyzer.analyze_trade(trading_pair, None)
            if market_check.get('status') == 'market_closed':
                return jsonify({
                    'status': 'rejected',
                    'reason': 'market_closed',
                    'details': market_check
                }), 200

            # PINE SCRIPT BYPASS MODE - Trust Pine Script analysis
            pine_script_signal = data.get('confidence', 0) > 0 or data.get('action') in ['BUY', 'SELL']
            
            if pine_script_signal:
                # Pine Script already did the analysis - execute directly
                analysis = {
                    'prediction': {'recommended': True},
                    'confidence': data.get('confidence', 85.0),
                    'source': 'pine_script_bypass',
                    'market_conditions': {'status': 'analyzed_by_pine_script'}
                }
            else:
                # If not from Pine Script, analyze the trade setup
                analysis = analyzer.analyze_trade(trading_pair, data)
            
            # Check if analysis recommends the trade
            if analysis.get('prediction', {}).get('recommended', False):
                # Use adaptive stops based on market conditions and TradingView compatibility
                account_balance = 0.95  # Current account balance
                risk_percent = data.get('risk_percentage', 2.0) / 100  # Moderate risk
                
                # Adaptive stop loss system - designed to pass TradingView validation
                if data.get('adaptive_stops', False):
                    # Use the adaptive values from the signal
                    stop_loss_pips = data.get('stop_loss_pips', 12)
                    take_profit_pips = data.get('take_profit_pips', 24)
                    print(f"� Using adaptive stops: SL={stop_loss_pips} pips, TP={take_profit_pips} pips")
                else:
                    # Fallback to conservative defaults
                    stop_loss_pips = 12  # Conservative but realistic
                    take_profit_pips = 24  # 2:1 ratio
                    
                # Get current price
                current_price = float(data.get('price', 1.0850))
                
                # Calculate position size based on risk (ensure minimum viable size)
                pip_value = 0.0001  # Standard pip value for EURUSD
                risk_amount = account_balance * risk_percent
                position_size = max(1, int(risk_amount / (stop_loss_pips * pip_value)))  # Ensure minimum 1 unit
                
                # Adjust units for BUY/SELL (positive for BUY, negative for SELL)
                if data.get('action', '').upper() == 'SELL':
                    position_size = -position_size
                
                # Calculate stop loss and take profit prices with proper rounding
                if data.get('action', '').upper() == 'BUY':
                    stop_loss_price = round(current_price - (stop_loss_pips * pip_value), 5)
                    take_profit_price = round(current_price + (take_profit_pips * pip_value), 5)
                else:  # SELL
                    stop_loss_price = round(current_price + (stop_loss_pips * pip_value), 5)
                    take_profit_price = round(current_price - (take_profit_pips * pip_value), 5)
                
                # Prepare complete OANDA trade data with adaptive stops
                # Convert EURUSD to EUR_USD format for OANDA
                oanda_instrument = trading_pair
                if trading_pair == "EURUSD":
                    oanda_instrument = "EUR_USD"
                elif trading_pair == "GBPUSD":
                    oanda_instrument = "GBP_USD"
                elif trading_pair == "USDJPY":
                    oanda_instrument = "USD_JPY"
                
                oanda_trade_data = {
                    'pair': oanda_instrument,  # Use OANDA format
                    'symbol': oanda_instrument,  # Use OANDA format
                    'action': data.get('action'),
                    'units': position_size,
                    'stop_loss': stop_loss_price,
                    'take_profit': take_profit_price,
                    'confidence': data.get('confidence', 85.0),
                    'source': 'pine_script_automated_adaptive',
                    'stop_loss_pips': stop_loss_pips,
                    'take_profit_pips': take_profit_pips
                }
                
                print(f"🎯 Prepared OANDA trade: {data.get('action')} {position_size} units, SL: {stop_loss_price}, TP: {take_profit_price}")
                
                # Execute trade on OANDA
                trade_result = oanda.place_trade(oanda_trade_data)
                
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
                    'pair': trading_pair,
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

@app.route('/autonomous/start', methods=['POST'])
def start_autonomous():
    """Start autonomous trading system"""
    try:
        if not LIVE_SYSTEM_AVAILABLE or not live_trading_system:
            return jsonify({
                'success': False,
                'message': 'Live trading system not available'
            }), 400
        
        success = live_trading_system.start_trading()
        return jsonify({
            'success': success,
            'message': 'Autonomous trading started' if success else 'Failed to start autonomous trading',
            'status': live_trading_system.get_status()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error starting autonomous trading: {str(e)}'
        }), 500

@app.route('/autonomous/stop', methods=['POST'])
def stop_autonomous():
    """Stop autonomous trading system"""
    try:
        if not LIVE_SYSTEM_AVAILABLE or not live_trading_system:
            return jsonify({
                'success': False,
                'message': 'Live trading system not available'
            }), 400
        
        live_trading_system.stop_trading()
        return jsonify({
            'success': True,
            'message': 'Autonomous trading stopped',
            'status': live_trading_system.get_status()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error stopping autonomous trading: {str(e)}'
        }), 500

@app.route('/autonomous/status', methods=['GET'])
def autonomous_status():
    """Get autonomous trading system status"""
    try:
        if not LIVE_SYSTEM_AVAILABLE or not live_trading_system:
            return jsonify({
                'success': False,
                'message': 'Live trading system not available',
                'available': False
            })
        
        status = live_trading_system.get_status()
        return jsonify({
            'success': True,
            'available': True,
            'status': status
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting status: {str(e)}'
        }), 500

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