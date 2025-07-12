from flask import Blueprint, render_template_string
import csv

jarvis_ui = Blueprint("jarvis_ui", __name__)  # ✅ Unique name

@jarvis_ui.route("/")
def dashboard():
    trades = []
    try:
        with open("trade_history.csv", "r") as f:
            reader = csv.DictReader(f)
            trades = list(reader)
    except FileNotFoundError:
        trades = []

    trades = trades[::-1]  # Most recent first

    html = """
    <html>
        <head>
            <title>Jarvis Trading Dashboard</title>
            <style>
                body { font-family: Arial; background-color: #0f111a; color: #fff; padding: 20px; }
                h1 { color: #00ffcc; }
                table { width: 100%; border-collapse: collapse; background-color: #1e1f2f; }
                th, td { border: 1px solid #333; padding: 8px; text-align: center; }
                th { background-color: #2a2d40; color: #00ffcc; }
                tr:nth-child(even) { background-color: #15161e; }
            </style>
        </head>
        <body>
            <h1>🚀 Jarvis AI Trading Dashboard</h1>
            <table>
                <tr>
                    <th>Timestamp</th><th>Pair</th><th>Action</th><th>Entry</th>
                    <th>Stop Loss</th><th>Take Profit</th><th>Confidence</th><th>AI</th><th>Result</th>
                </tr>
                {% for trade in trades %}
                <tr>
                    <td>{{ trade.timestamp }}</td>
                    <td>{{ trade.pair }}</td>
                    <td>{{ trade.action }}</td>
                    <td>{{ trade.entry }}</td>
                    <td>{{ trade.stop_loss }}</td>
                    <td>{{ trade.take_profit }}</td>
                    <td>{{ trade.confidence }}</td>
                    <td>{{ trade.ai_confidence or 'N/A' }}</td>
                    <td>{{ trade.result or 'Pending' }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
    </html>
    """
    return render_template_string(html, trades=trades)
