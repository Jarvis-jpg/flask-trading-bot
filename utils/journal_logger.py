# utils/journal_logger.py
import os
import csv
from datetime import datetime

JOURNAL_PATH = 'journal/trade_journal.csv'

# Ensure folder exists
os.makedirs(os.path.dirname(JOURNAL_PATH), exist_ok=True)

# Write header if file doesn't exist
if not os.path.exists(JOURNAL_PATH):
    with open(JOURNAL_PATH, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'timestamp', 'pair', 'action', 'entry_price', 'sl', 'tp',
            'result', 'profit_usd', 'rr', 'strategy'
        ])

def log_trade(pair, action, entry_price, sl, tp, result, profit, rr, strategy):
    with open(JOURNAL_PATH, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.utcnow().isoformat(),
            pair, action, entry_price, sl, tp,
            result, profit, rr, strategy
        ])
