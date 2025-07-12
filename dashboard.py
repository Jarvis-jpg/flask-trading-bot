from flask import Blueprint, render_template_string
import pandas as pd
import os

dashboard_app_ui_v2 = Blueprint("dashboard_ui_v2", __name__)

DASHBOARD_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>📊 Trade Dashboard</title>
  <style>
    body {
      background: #0f0f0f; color: #f0f0f0;
      font-family: 'Segoe UI', sans-serif; padding: 2rem;
    }
    h1 { color: #00ffcc; text-align: center; }
    table {
      border-collapse: collapse; width: 100%;
      background: #1a1a1a;
    }
    th, td {
      border: 1px solid #333; padding: 10px; text-align: center;
    }
    th {
      background: #00ffcc; color: #000;
    }
    tr:nth-child(even) { background-color: #2a2a2a; }
    tr:hover { background-color: #444; }
  </style>
</head>
<body>
  <h1>Real-Time Trade Dashboard</h1>
  {% if trades %}
  <table>
    <tr>
      {% for col in trades[0].keys() %}
        <th>{{ col }}</th>
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
    <p>No trade data found.</p>
  {% endif %}
</body>
</html>
"""

@dashboard_app_ui_v2.route("/")
def dashboard():
    trades = []
    if os.path.exists("trade_history.csv"):
        try:
            df = pd.read_csv("trade_history.csv")
            trades = df.to_dict(orient="records")
        except Exception as e:
            trades = [{"Error": f"Could not load trades: {str(e)}"}]
    return render_template_string(DASHBOARD_TEMPLATE, trades=trades)
