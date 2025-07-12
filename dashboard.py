from flask import Blueprint, render_template, jsonify
import json
import os

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def index():
    journal_path = 'trade_journal.json'
    if os.path.exists(journal_path):
        with open(journal_path) as f:
            trades = json.load(f)
    else:
        trades = []

    return render_template('dashboard.html', trades=trades)
