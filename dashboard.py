from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__, template_folder="templates")

@app.route('/')
def show_dashboard():
    if os.path.exists("trade_journal.csv"):
        try:
            df = pd.read_csv("trade_journal.csv")
            trades = df.to_dict(orient="records")
        except Exception:
            trades = []
    else:
        trades = []
    return render_template("dashboard.html", trades=trades)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
