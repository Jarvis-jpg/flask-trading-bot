import os
import pandas as pd
import random
from datetime import datetime

class AdaptiveTradeLogic:
    journal_path = 'trade_journal.csv'

    @staticmethod
    def execute_trade(data):
        # Parse and validate incoming trade data
        pair = data.get('pair')
        action = data.get('action')  # 'buy' or 'sell'
        entry = float(data.get('entry'))
        sl = float(data.get('stop_loss'))
        tp = float(data.get('take_profit'))
        strategy_id = data.get('strategy_id')
        confidence = float(data.get('confidence', 0))
        timestamp = data.get('timestamp', datetime.utcnow().isoformat())

        # Simulated exit price (you can connect to real broker or price feed later)
        exit_price = tp if random.random() > 0.3 else sl  # simulate 70% win rate

        if action == "buy":
            profit = round(exit_price - entry, 5)
        else:
            profit = round(entry - exit_price, 5)

        result = "win" if profit > 0 else "loss"

        # Log the trade
        trade = {
            'timestamp': timestamp,
            'pair': pair,
            'action': action,
            'entry': entry,
            'exit': exit_price,
            'pnl': profit,
            'result': result,
            'strategy_id': strategy_id,
            'confidence': confidence
        }

        AdaptiveTradeLogic.log_trade(trade)

        return trade

    @staticmethod
    def log_trade(trade):
        df = pd.DataFrame([trade])
        file_exists = os.path.isfile(AdaptiveTradeLogic.journal_path)
        df.to_csv(AdaptiveTradeLogic.journal_path, mode='a', header=not file_exists, index=False)
