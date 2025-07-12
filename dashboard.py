from flask import Blueprint, render_template_string
import json
import os

dashboard_app = Blueprint('dashboard_app', __name__, template_folder='templates')

@dashboard_app.route('/')
def dashboard():
    if os.path.exists('trade_history.csv'):
        with open('trade_history.csv', 'r') as f:
            lines = f.readlines()
        headers = lines[0].strip().split(',')
        trades = [line.strip().split(',') for line in lines[1:]]
    else:
        headers = []
        trades = []

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🧠 Jarvis Quant System Dashboard</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background-color: #0f0f0f;
                color: #00ffcc;
                margin: 0;
                padding: 20px;
            }
            h1 {
                text-align: center;
                color: #00ffff;
                font-size: 32px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 30px;
            }
            th, td {
                padding: 12px;
                text-align: center;
                border-bottom: 1px solid #333;
            }
            tr:nth-child(even) {
                background-color: #1a1a1a;
            }
            tr:hover {
                background-color: #222;
            }
            th {
                background-color: #1f1f1f;
                color: #00ffcc;
            }
            .container {
                max-width: 1000px;
                margin: auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Jarvis Quant Trading Dashboard</h1>
            {% if trades %}
                <table>
                    <thead>
                        <tr>
                            {% for header in headers %}
                                <th>{{ header }}</th>
                            {% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {% for trade in trades %}
                            <tr>
                                {% for value in trade %}
                                    <td>{{ value }}</td>
                                {% endfor %}
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            {% else %}
                <p>No trades found.</p>
            {% endif %}
        </div>
    </body>
    </html>
    """, headers=headers, trades=trades)

