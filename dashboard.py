from flask import Blueprint, render_template_string
import csv
import os

dashboard_app_ui = Blueprint("dashboard_ui", __name__)

@dashboard_app_ui.route("/")
def dashboard():
    trades = []
    file_path = "trade_history.csv"
    if os.path.exists(file_path):
        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                trades.append(row)

    # Reverse to show latest first
    trades = trades[::-1]

    html = """
    <html>
    <head>
        <title>Trading Dashboard</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #111; color: #eee; padding: 20px; }
            h1 { text-align: center; color: #4ef; }
            table { width: 100%; border-collapse: collapse; margin-top: 30px; }
            th, td { padding: 10px; border: 1px solid #555; text-align: center; }
            th { background-color: #222; color: #4ef; }
            tr:nth-child(even) { background-color: #1a1a1a; }
            tr:hover { background-color: #333; }
        </style>
    </head>
    <body>
        <h1>📊 Real-Time Trade Dashboard</h1>
        <table>
            <tr>
                {% for key in trades[0].keys() %}
                <th>{{ key }}</th>
                {% endfor %}
            </tr>
            {% for trade in trades %}
            <tr>
                {% for value in trade.values() %}
                <td>{{ value }}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, trades=trades)
