from flask import Blueprint, render_template_string
import csv
import os

dashboard = Blueprint('dashboard', __name__)

@dashboard.route("/")
def index():
    trades = []
    csv_path = 'trade_history.csv'
    if os.path.exists(csv_path):
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            trades = list(reader)

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🧠 JARVIS AI Trade Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                background-color: #0f1115;
                color: #e0e0e0;
                font-family: 'Segoe UI', Tahoma, sans-serif;
                padding: 20px;
                margin: 0;
            }
            h1 {
                color: #00c7b7;
                text-align: center;
                margin-bottom: 30px;
                text-shadow: 0 0 10px #00c7b770;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                background-color: #1a1f27;
                box-shadow: 0 0 12px rgba(0, 255, 255, 0.1);
            }
            th, td {
                padding: 10px;
                border: 1px solid #2b2f3a;
                text-align: center;
            }
            th {
                background-color: #202833;
                color: #63f5d6;
            }
            tr:nth-child(even) {
                background-color: #161b22;
            }
            tr:hover {
                background-color: #2a2f3a;
                transition: 0.2s;
            }
            .empty {
                text-align: center;
                font-size: 18px;
                margin-top: 40px;
                color: #aaa;
            }
        </style>
    </head>
    <body>
        <h1>📊 JARVIS Quant Trading Dashboard</h1>
        {% if trades %}
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
        {% else %}
        <div class="empty">No trade data found yet. Send trades to populate the dashboard.</div>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html, trades=trades)

