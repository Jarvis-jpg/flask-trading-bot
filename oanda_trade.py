# oanda_trade.py
import requests
from oanda_config import OANDA_API_KEY, OANDA_ACCOUNT_ID, OANDA_URL

def place_order(pair, side, units, entry_price, stop_loss, take_profit):
    headers = {
        "Authorization": f"Bearer {OANDA_API_KEY}",
        "Content-Type": "application/json"
    }

    order_type = "MARKET"
    data = {
        "order": {
            "instrument": pair,
            "units": str(units if side == "buy" else -units),
            "type": order_type,
            "positionFill": "DEFAULT",
            "stopLossOnFill": {"price": str(stop_loss)},
            "takeProfitOnFill": {"price": str(take_profit)}
        }
    }

    url = f"{OANDA_URL}/accounts/{OANDA_ACCOUNT_ID}/orders"
    response = requests.post(url, headers=headers, json=data)
    return response.json()
