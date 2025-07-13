# ai/train.py

import pandas as pd
import os

def run_ai_training():
    try:
        # Load trade journal
        df = pd.read_csv("journal/trade_journal.csv")

        # Example learning logic (you can expand this)
        total_trades = len(df)
        win_rate = (df['result'] == 'win').sum() / total_trades
        avg_rr = df['rr'].mean()

        # Save performance stats (or train model here)
        with open("ai/last_ai_summary.txt", "w") as f:
            f.write(f"Trades: {total_trades}\n")
            f.write(f"Win Rate: {win_rate:.2f}\n")
            f.write(f"Avg R:R: {avg_rr:.2f}\n")

        return "AI model retrained successfully"

    except Exception as e:
        return f"AI training failed: {str(e)}"
