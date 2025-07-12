from flask import Blueprint, render_template_string
import csv

dashboard_app = Blueprint("dashboard_app", __name__)  # Make sure this name matches your import in app.py

@dashboard_app.route("/")
def dashboard():
    trades = []
    try:
        with open("trade_history.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            trades = list(reader)
    except FileNotFoundError:
        trades = []

    trades.reverse()  # newest first

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Trade Dashboard</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background-color: #0d1117;
                color: #c9d1d9;
                padding: 40px;
            }
            h1 {
                text-align: center;
                color: #58a6ff;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 30px;
                background-color: #161b22;
            }
            th, td {
                padding: 12px;
                border: 1px solid #30363d;
                text-align: center;
            }
            th {
                background-color: #21262d;
            }
            tr:hover {
                background-color: #1f6feb33;
            }
        </style>
    </head>
    <body>
        <h1>📊 AI Trade Dashboard</h1>
        <table>
            <tr>
                <th>Timestamp</th>
                <th>Pair</th>
                <th>Action</th>
                <th>Entry</th>
                <th>Stop Loss</th>
                <th>Take Profit</th>
                <th>Confidence</th>
                <th>Result</th>
            </tr>
            {% for trade in trades %}
            <tr>
                <td>{{ trade.timestamp }}</td>
                <td>{{ trade.pair }}</td>
                <td>{{ trade.action }}</td>
                <td>{{ trade.entry }}</td>
                <td>{{ trade.stop_loss }}</td>
                <td>{{ trade.take_profit }}</td>
                <td>{{ trade.ai_confidence }}</td>
                <td>{{ trade.result or "Pending" }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, trades=trades)
