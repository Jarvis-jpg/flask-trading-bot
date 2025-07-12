from flask import Blueprint, render_template_string, jsonify
import json
import os

dashboard_app = Blueprint("dashboard_app", __name__)

@dashboard_app.route("/dashboard")
def dashboard():
    trades = []
    if os.path.exists("trades.json"):
        with open("trades.json", "r") as f:
            trades = json.load(f)
    return render_template_string("""
        <h1>📊 Trade Dashboard</h1>
        <table border="1">
            <tr>
                <th>Pair</th><th>Action</th><th>Entry</th><th>SL</th><th>TP</th><th>Result</th><th>Confidence</th>
            </tr>
            {% for trade in trades %}
            <tr>
                <td>{{ trade.pair }}</td>
                <td>{{ trade.action }}</td>
                <td>{{ trade.entry }}</td>
                <td>{{ trade.stop_loss }}</td>
                <td>{{ trade.take_profit }}</td>
                <td>{{ trade.result }}</td>
                <td>{{ trade.get('ai_confidence', 'N/A') }}</td>
            </tr>
            {% endfor %}
        </table>
    """, trades=trades)

@dashboard_app.route("/api/trades")
def trades_api():
    if os.path.exists("trades.json"):
        with open("trades.json", "r") as f:
            trades = json.load(f)
        return jsonify(trades)
    return jsonify([])
