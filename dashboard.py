from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route("/")
@app.route("/dashboard")
def dashboard():
    trades = []
    journal_path = os.path.join(os.getcwd(), "trade_journal.json")

    if os.path.exists(journal_path):
        try:
            with open(journal_path, "r") as f:
                trades = json.load(f)
        except Exception as e:
            print("Error loading journal:", e)
    return render_template("dashboard.html", trades=trades)

if __name__ == "__main__":
    app.run(debug=True)


