from flask import Blueprint, render_template
import json
import os

dashboard_app = Blueprint("dashboard_unique", __name__)

@dashboard_app.route("/")
def dashboard():
    journal_path = "trade_journal.json"
return "<h1>Trading Dashboard</h1>"
    trades = []

    if os.path.exists(journal_path):
        with open(journal_path, "r") as file:
            for line in file:
                try:
                    trades.append(json.loads(line.strip()))
                except:
                    continue

    return render_template("dashboard.html", trades=trades)

