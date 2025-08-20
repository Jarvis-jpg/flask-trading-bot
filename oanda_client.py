import logging
import os
from datetime import datetime
from typing import Dict, Optional
import oandapyV20
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.accounts as accounts
from oandapyV20 import V20Error

# Configure logging
logger = logging.getLogger(__name__)

class OandaClient:
    def __init__(self):
        # Get credentials from environment variables
        self.api_key = os.getenv('OANDA_API_KEY')
        self.account_id = os.getenv('OANDA_ACCOUNT_ID')
        self.environment = os.getenv('OANDA_ENVIRONMENT', 'live')
        
        # Set API URL based on environment
        if self.environment.lower() == 'live':
            self.api_url = 'api-fxtrade.oanda.com'
            self.stream_url = 'stream-fxtrade.oanda.com'
        else:
            self.api_url = 'api-fxpractice.oanda.com'
            self.stream_url = 'stream-fxpractice.oanda.com'
        
        # Initialize OANDA client
        self.client = oandapyV20.API(
            access_token=self.api_key,
            environment=self.environment.lower()
        )
        
        # Log configuration
        logger.info("OANDA client configuration:")
        logger.info(f"- Environment: {self.environment.upper()} mode")
        logger.info(f"- API URL: {self.api_url}")
        logger.info(f"- Account ID: {self.account_id}")
        api_key_status = "Set" if self.api_key else "Missing"
        if self.api_key and not self.api_key.startswith('Bearer '):
            api_key_status += " (missing Bearer)"
        logger.info(f"- API Key Status: {api_key_status}")
    def _format_instrument(self, symbol: str) -> str:
        """Convert symbol from EURUSD format to EUR_USD format for OANDA"""
        if '_' in symbol:
            return symbol  # Already in correct format
        
        # Common currency pairs mapping
        if len(symbol) == 6:
            return f"{symbol[:3]}_{symbol[3:]}"
        
        # Default fallback
        return symbol

        if self.api_key:
            logger.info(f"- API Key Length: {len(self.api_key)} characters")

    def place_trade(self, trade_data: Dict) -> Dict:
        try:
            trading_pair = self._format_instrument(trade_data.get('pair') or trade_data.get('symbol') or 'EURUSD')
            order_data = {
                "order": {
                    "type": "MARKET",
                    "instrument": trading_pair,
                    "units": str(trade_data['units']),
                    "timeInForce": "FOK",
                    "positionFill": "DEFAULT",
                    "stopLossOnFill": {"price": str(trade_data['stop_loss'])},
                    "takeProfitOnFill": {"price": str(trade_data['take_profit'])}
                }
            }

            r = orders.OrderCreate(self.account_id, data=order_data)
            response = self.client.request(r)
            logger.info(f"Trade response: {response}")
            
            if 'orderFillTransaction' in response:
                return {
                    'status': 'success',
                    'order_id': response['orderFillTransaction']['id'],
                    'filled_price': response['orderFillTransaction']['price'],
                    'timestamp': datetime.now().isoformat()
                }
            elif 'orderCancelTransaction' in response:
                cancel_reason = response['orderCancelTransaction'].get('reason', 'Unknown')
                raise Exception(f"Trade cancelled: {cancel_reason}")
            else:
                raise Exception("Unexpected response format")
        except Exception as e:
            logger.error(f"Error placing trade: {str(e)}")
            raise

    def get_current_price(self, instrument: str) -> float:
        try:
            from oandapyV20.endpoints import pricing
            params = {"instruments": instrument}
            r = pricing.PricingInfo(accountID=self.account_id, params=params)
            response = self.client.request(r)
            
            if 'prices' in response and len(response['prices']) > 0:
                price_data = response['prices'][0]
                bid = float(price_data['bids'][0]['price'])
                ask = float(price_data['asks'][0]['price'])
                return (bid + ask) / 2
            else:
                raise Exception(f"No price data available for {instrument}")
        except Exception as e:
            logger.error(f"Error getting current price: {str(e)}")
            raise
