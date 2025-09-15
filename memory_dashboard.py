"""
SevenSYS Memory Dashboard - Web interface for monitoring SevenSYS performance
Provides real-time insights into webhook activity and trading performance
"""

from flask import Flask, render_template, jsonify
import json
from datetime import datetime, timedelta
from memory_logger import SevenSYSMemoryLogger
import sqlite3

class SevenSYSMemoryDashboard:
    def __init__(self, memory_logger: SevenSYSMemoryLogger):
        self.app = Flask(__name__)
        self.memory_logger = memory_logger
        self.setup_routes()
    
    def setup_routes(self):
        """Setup Flask routes for the dashboard"""
        
        @self.app.route('/')
        def dashboard():
            """Main dashboard view"""
            return render_template('sevensys_dashboard.html')
        
        @self.app.route('/api/status')
        def api_status():
            """API endpoint for system status"""
            return jsonify(self.memory_logger.get_system_status())
        
        @self.app.route('/api/today')
        def api_today():
            """API endpoint for today's summary"""
            return jsonify(self.memory_logger.get_today_summary())
        
        @self.app.route('/api/recent-alerts/<int:limit>')
        def api_recent_alerts(limit=20):
            """API endpoint for recent alerts"""
            conn = sqlite3.connect(self.memory_logger.db_path)
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    SELECT timestamp, ticker, action, close_price, raw_data
                    FROM webhook_alerts
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
                
                alerts = []
                for row in cursor.fetchall():
                    alerts.append({
                        'timestamp': row[0],
                        'ticker': row[1],
                        'action': row[2],
                        'close_price': row[3],
                        'raw_data': json.loads(row[4]) if row[4] else {}
                    })
                
                return jsonify({'alerts': alerts})
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            finally:
                conn.close()
        
        @self.app.route('/api/recent-trades/<int:limit>')
        def api_recent_trades(limit=20):
            """API endpoint for recent trades"""
            conn = sqlite3.connect(self.memory_logger.db_path)
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    SELECT 
                        te.timestamp, te.ticker, te.action, te.entry_price,
                        te.position_size, te.stop_loss, te.take_profit,
                        te.execution_status, te.oanda_order_id
                    FROM trade_executions te
                    ORDER BY te.timestamp DESC
                    LIMIT ?
                ''', (limit,))
                
                trades = []
                for row in cursor.fetchall():
                    trades.append({
                        'timestamp': row[0],
                        'ticker': row[1],
                        'action': row[2],
                        'entry_price': row[3],
                        'position_size': row[4],
                        'stop_loss': row[5],
                        'take_profit': row[6],
                        'status': row[7],
                        'order_id': row[8]
                    })
                
                return jsonify({'trades': trades})
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            finally:
                conn.close()
        
        @self.app.route('/api/performance-chart/<int:days>')
        def api_performance_chart(days=7):
            """API endpoint for performance chart data"""
            conn = sqlite3.connect(self.memory_logger.db_path)
            cursor = conn.cursor()
            
            try:
                start_date = (datetime.now() - timedelta(days=days)).date()
                
                cursor.execute('''
                    SELECT 
                        date, total_alerts, successful_executions, failed_executions
                    FROM daily_performance
                    WHERE date >= ?
                    ORDER BY date
                ''', (start_date,))
                
                chart_data = []
                for row in cursor.fetchall():
                    chart_data.append({
                        'date': row[0],
                        'alerts': row[1] or 0,
                        'successful_trades': row[2] or 0,
                        'failed_trades': row[3] or 0,
                        'success_rate': (row[2] / row[1] * 100) if row[1] and row[1] > 0 else 0
                    })
                
                return jsonify({'performance_data': chart_data})
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            finally:
                conn.close()
        
        @self.app.route('/api/execution-analysis')
        def api_execution_analysis():
            """API endpoint for execution success/failure analysis"""
            conn = sqlite3.connect(self.memory_logger.db_path)
            cursor = conn.cursor()
            
            try:
                # Success vs failure counts
                cursor.execute('''
                    SELECT 
                        SUM(CASE WHEN execution_status NOT LIKE 'FAILED%' THEN 1 ELSE 0 END) as successful,
                        SUM(CASE WHEN execution_status LIKE 'FAILED%' THEN 1 ELSE 0 END) as failed
                    FROM trade_executions
                ''')
                result = cursor.fetchone()
                successful, failed = result[0] or 0, result[1] or 0
                
                # Failure reasons analysis
                cursor.execute('''
                    SELECT execution_status, COUNT(*) as count
                    FROM trade_executions
                    WHERE execution_status LIKE 'FAILED%'
                    GROUP BY execution_status
                    ORDER BY count DESC
                ''')
                failure_reasons = [{'reason': row[0], 'count': row[1]} for row in cursor.fetchall()]
                
                return jsonify({
                    'execution_summary': {
                        'successful': successful,
                        'failed': failed,
                        'success_rate': (successful / (successful + failed) * 100) if (successful + failed) > 0 else 0
                    },
                    'failure_reasons': failure_reasons
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            finally:
                conn.close()
    
    def run(self, host='127.0.0.1', port=5001, debug=True):
        """Run the dashboard server"""
        print(f"\n🚀 SevenSYS Memory Dashboard starting on http://{host}:{port}")
        print("📊 Monitoring SevenSYS webhook activity and trade executions")
        self.app.run(host=host, port=port, debug=debug)


def create_dashboard_template():
    """Create the HTML template for the dashboard"""
    template_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SevenSYS Memory Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .header h1 {
            color: white;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .header p {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.2em;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card h2 {
            color: white;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 2px solid rgba(255, 255, 255, 0.3);
            padding-bottom: 10px;
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #4CAF50;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .stat-label {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.1em;
            margin-top: 5px;
        }
        
        .alert-item, .trade-item {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #4CAF50;
        }
        
        .alert-item.sell, .trade-item.sell {
            border-left-color: #f44336;
        }
        
        .timestamp {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9em;
        }
        
        .ticker {
            color: #FFD700;
            font-weight: bold;
            font-size: 1.1em;
        }
        
        .action {
            color: white;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        .action.buy {
            color: #4CAF50;
        }
        
        .action.sell {
            color: #f44336;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-healthy {
            background-color: #4CAF50;
            animation: pulse 2s infinite;
        }
        
        .status-warning {
            background-color: #FF9800;
        }
        
        .status-error {
            background-color: #f44336;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .refresh-btn {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            margin: 10px 5px;
            transition: all 0.3s ease;
        }
        
        .refresh-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }
        
        .no-data {
            color: rgba(255, 255, 255, 0.7);
            font-style: italic;
            text-align: center;
            padding: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 SevenSYS Memory Dashboard</h1>
            <p>Real-time monitoring of SevenSYS webhook activity and trading performance</p>
            <div style="margin-top: 15px;">
                <button class="refresh-btn" onclick="refreshData()">🔄 Refresh Data</button>
                <button class="refresh-btn" onclick="clearLogs()" style="background: linear-gradient(45deg, #f44336, #d32f2f);">🗑️ Clear Logs</button>
            </div>
        </div>
        
        <div class="dashboard-grid">
            <div class="card">
                <h2>📊 Today's Summary</h2>
                <div id="today-summary">
                    <div class="no-data">Loading data...</div>
                </div>
            </div>
            
            <div class="card">
                <h2>🖥️ System Status</h2>
                <div id="system-status">
                    <div class="no-data">Loading status...</div>
                </div>
            </div>
            
            <div class="card">
                <h2>📢 Recent Alerts</h2>
                <div id="recent-alerts" style="max-height: 400px; overflow-y: auto;">
                    <div class="no-data">Loading alerts...</div>
                </div>
            </div>
            
            <div class="card">
                <h2>💼 Recent Trades</h2>
                <div id="recent-trades" style="max-height: 400px; overflow-y: auto;">
                    <div class="no-data">Loading trades...</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>📈 Execution Analysis</h2>
            <div id="execution-analysis">
                <div class="no-data">Loading analysis...</div>
            </div>
        </div>
    </div>

    <script>
        let refreshInterval;
        
        function formatTimestamp(timestamp) {
            return new Date(timestamp).toLocaleString();
        }
        
        function refreshData() {
            loadTodaySummary();
            loadSystemStatus();
            loadRecentAlerts();
            loadRecentTrades();
            loadExecutionAnalysis();
        }
        
        function loadTodaySummary() {
            fetch('/api/today')
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('today-summary');
                    if (data.total_alerts === 0 && data.successful_trades === 0) {
                        container.innerHTML = '<div class="no-data">No activity today</div>';
                    } else {
                        container.innerHTML = `
                            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;">
                                <div style="text-align: center;">
                                    <div class="stat-value">${data.total_alerts || 0}</div>
                                    <div class="stat-label">Webhook Alerts</div>
                                </div>
                                <div style="text-align: center;">
                                    <div class="stat-value">${data.successful_trades || 0}</div>
                                    <div class="stat-label">Successful Trades</div>
                                </div>
                                <div style="text-align: center;">
                                    <div class="stat-value">${data.failed_trades || 0}</div>
                                    <div class="stat-label">Failed Trades</div>
                                </div>
                                <div style="text-align: center;">
                                    <div class="stat-value">${data.success_rate?.toFixed(1) || 0}%</div>
                                    <div class="stat-label">Success Rate</div>
                                </div>
                            </div>
                        `;
                    }
                })
                .catch(error => {
                    console.error('Error loading today summary:', error);
                    document.getElementById('today-summary').innerHTML = '<div class="no-data">Error loading data</div>';
                });
        }
        
        function loadSystemStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    const statusClass = data.database_status === 'HEALTHY' ? 'status-healthy' : 'status-error';
                    document.getElementById('system-status').innerHTML = `
                        <div style="margin-bottom: 15px;">
                            <span class="status-indicator ${statusClass}"></span>
                            <strong>Database: ${data.database_status}</strong>
                        </div>
                        <div style="color: rgba(255, 255, 255, 0.9);">
                            <div>Total Alerts: <strong>${data.total_alerts || 0}</strong></div>
                            <div>Total Successful Trades: <strong>${data.total_successful_trades || 0}</strong></div>
                            <div>Overall Success Rate: <strong>${data.overall_success_rate?.toFixed(1) || 0}%</strong></div>
                            <div>Last Alert: <strong>${data.last_alert_time ? formatTimestamp(data.last_alert_time) : 'Never'}</strong></div>
                            <div>Last Execution: <strong>${data.last_execution_time ? formatTimestamp(data.last_execution_time) : 'Never'}</strong></div>
                        </div>
                    `;
                })
                .catch(error => {
                    console.error('Error loading system status:', error);
                    document.getElementById('system-status').innerHTML = '<div class="no-data">Error loading status</div>';
                });
        }
        
        function loadRecentAlerts() {
            fetch('/api/recent-alerts/10')
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('recent-alerts');
                    if (!data.alerts || data.alerts.length === 0) {
                        container.innerHTML = '<div class="no-data">No recent alerts</div>';
                        return;
                    }
                    
                    container.innerHTML = data.alerts.map(alert => `
                        <div class="alert-item ${alert.action.toLowerCase()}">
                            <div class="timestamp">${formatTimestamp(alert.timestamp)}</div>
                            <div style="margin: 5px 0;">
                                <span class="ticker">${alert.ticker}</span>
                                <span class="action ${alert.action.toLowerCase()}">${alert.action}</span>
                                @ <strong>$${alert.close_price.toFixed(5)}</strong>
                            </div>
                        </div>
                    `).join('');
                })
                .catch(error => {
                    console.error('Error loading alerts:', error);
                    document.getElementById('recent-alerts').innerHTML = '<div class="no-data">Error loading alerts</div>';
                });
        }
        
        function loadRecentTrades() {
            fetch('/api/recent-trades/10')
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('recent-trades');
                    if (!data.trades || data.trades.length === 0) {
                        container.innerHTML = '<div class="no-data">No recent trades</div>';
                        return;
                    }
                    
                    container.innerHTML = data.trades.map(trade => `
                        <div class="trade-item ${trade.action.toLowerCase()}">
                            <div class="timestamp">${formatTimestamp(trade.timestamp)}</div>
                            <div style="margin: 5px 0;">
                                <span class="ticker">${trade.ticker}</span>
                                <span class="action ${trade.action.toLowerCase()}">${trade.action}</span>
                                @ <strong>$${trade.entry_price.toFixed(5)}</strong>
                            </div>
                            <div style="font-size: 0.9em; color: rgba(255, 255, 255, 0.8);">
                                Size: ${trade.position_size} | SL: ${trade.stop_loss?.toFixed(5) || 'N/A'} | TP: ${trade.take_profit?.toFixed(5) || 'N/A'}
                            </div>
                            <div style="font-size: 0.9em; color: ${trade.status.includes('FAILED') ? '#f44336' : '#4CAF50'};">
                                ${trade.status}
                            </div>
                        </div>
                    `).join('');
                })
                .catch(error => {
                    console.error('Error loading trades:', error);
                    document.getElementById('recent-trades').innerHTML = '<div class="no-data">Error loading trades</div>';
                });
        }
        
        function loadExecutionAnalysis() {
            fetch('/api/execution-analysis')
                .then(response => response.json())
                .then(data => {
                    const summary = data.execution_summary;
                    let html = `
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 20px;">
                            <div style="text-align: center;">
                                <div class="stat-value" style="color: #4CAF50;">${summary.successful}</div>
                                <div class="stat-label">Successful</div>
                            </div>
                            <div style="text-align: center;">
                                <div class="stat-value" style="color: #f44336;">${summary.failed}</div>
                                <div class="stat-label">Failed</div>
                            </div>
                            <div style="text-align: center;">
                                <div class="stat-value">${summary.success_rate.toFixed(1)}%</div>
                                <div class="stat-label">Success Rate</div>
                            </div>
                        </div>
                    `;
                    
                    if (data.failure_reasons && data.failure_reasons.length > 0) {
                        html += '<h3 style="color: white; margin-bottom: 15px;">Failure Analysis:</h3>';
                        html += data.failure_reasons.map(reason => `
                            <div style="background: rgba(244, 67, 54, 0.1); padding: 10px; margin: 5px 0; border-radius: 8px; border-left: 4px solid #f44336;">
                                <strong style="color: #f44336;">${reason.reason}</strong> - ${reason.count} occurrences
                            </div>
                        `).join('');
                    }
                    
                    document.getElementById('execution-analysis').innerHTML = html;
                })
                .catch(error => {
                    console.error('Error loading execution analysis:', error);
                    document.getElementById('execution-analysis').innerHTML = '<div class="no-data">Error loading analysis</div>';
                });
        }
        
        function clearLogs() {
            if (confirm('Are you sure you want to clear all logs? This action cannot be undone.')) {
                // This would need a backend endpoint to clear logs
                alert('Clear logs functionality needs to be implemented in the backend.');
            }
        }
        
        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {
            refreshData();
            // Auto-refresh every 30 seconds
            refreshInterval = setInterval(refreshData, 30000);
        });
    </script>
</body>
</html>'''
    
    return template_content


if __name__ == '__main__':
    # Create dashboard with memory logger
    logger = SevenSYSMemoryLogger()
    dashboard = SevenSYSMemoryDashboard(logger)
    
    # Create templates directory and template file
    import os
    os.makedirs('templates', exist_ok=True)
    with open('templates/sevensys_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(create_dashboard_template())
    
    dashboard.run()
