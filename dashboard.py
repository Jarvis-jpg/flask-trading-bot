from flask import Blueprint, render_template_string
import pandas as pd
import os

dashboard_app = Blueprint("dashboard_app", __name__, template_folder="templates")

@dashboard_app.route("/")
def dashboard():
    if not os.path.exists("trade_history.csv"):
        return "<h2>No trade history found.</h2>"

    df = pd.read_csv("trade_history.csv")
    total = len(df)
    wins = len(df[df["result"] == "win"])
    losses = len(df[df["result"] == "loss"])
    win_rate = round((wins / total) * 100, 2) if total > 0 else 0

    html = f"""
    <h1>Trading Bot Dashboard</h1>
    <p><strong>Total Trades:</strong> {total}</p>
    <p><strong>Wins:</strong> {wins}</p>
    <p><strong>Losses:</strong> {losses}</p>
    <p><strong>Win Rate:</strong> {win_rate}%</p>
    <h3>Last 5 Trades:</h3>
    {df.tail(5).to_html(index=False)}
    """
    return render_template_string(html)


@dashboard_app.route("/api/trades")
def trades_api():
    if os.path.exists("trades.json"):
        with open("trades.json", "r") as f:
            trades = json.load(f)
        return jsonify(trades)
    return jsonify([])
