from flask import Blueprint, render_template_string
import pandas as pd
import os

# ✅ Use unique blueprint name: 'jarvis'
jarvis = Blueprint("jarvis", __name__, url_prefix="/")

DASHBOARD_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Jarvis - Trade Dashboard</title>
  <style>
    body {
      background: #0d1117;
      color: #c9d1d9;
      font-family: 'Segoe UI', sans-serif;
      padding: 2rem;
    }
    h1 {
      color: #58a6ff;
      text-align: center;
      margin-bottom: 2rem;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      background-color: #161b22;
    }
    th, td {
      padding: 12px;
      border: 1px solid #30363d;
      text-align: center;
    }
    th {
      background-color: #21262d;
      color: #58a6ff;
    }
    tr:nth-child(even) {
      background-color: #0d1117;
    }
    tr:hover {
      background-color: #21262d;
    }
  </style>
</head>
<body>
  <h1>Jarvis Real-Time Trade Dashboard</h1>
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
    <p>No trades found.</p>
  {% endif %}
</body>
</html>
"""

@jarvis.route("/")
def dashboard():
    trades = []
    if os.path.exists("trade_history.csv"):
        try:
            df = pd.read_csv("trade_history.csv")
            trades = df.to_dict(orient="records")
        except Exception as e:
            trades = [{"Error": f"Could not load trades: {str(e)}"}]
    return render_template_string(DASHBOARD_TEMPLATE, trades=trades)
