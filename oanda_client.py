import os
import oandapyV20
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.pricing as pricing
from oandapyV20.exceptions import V20Error
import logging
from typing import Dict, Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OandaClient:
    def __init__(self):
        self.api_key = os.getenv('OANDA_API_KEY')
        self.account_id = os.getenv('OANDA_ACCOUNT_ID')
        self.is_live = os.getenv('OANDA_LIVE', 'false').lower() == 'true'
        
        if not self.api_key or not self.account_id:
            raise ValueError("OANDA_API_KEY and OANDA_ACCOUNT_ID environment variables must be set")
        
        try:
            # Determine environment based on account ID format
            if self.account_id.startswith('001-001-'):
                self.environment = "live"
                self.api_url = "api-fxtrade.oanda.com"
                self.is_live = True
            else:
                self.environment = "practice"
                self.api_url = "api-fxpractice.oanda.com"
                self.is_live = False
            
            # Clean and validate API key
            if not self.api_key:
                raise ValueError("OANDA API key is not set")
            
            # Remove 'Bearer ' prefix if present as oandapyV20 doesn't need it
            self.api_key = self.api_key.replace('Bearer ', '')
            
            # Initialize API client
            self.client = oandapyV20.API(
                access_token=self.api_key,
                environment=self.environment
            )
            
            # Log configuration details (safely)
            logger.info(f"OANDA client configuration:")
            logger.info(f"- Environment: {self.environment.upper()} mode")
            logger.info(f"- API URL: {self.api_url}")
            logger.info(f"- Account ID: {self.account_id}")
            logger.info(f"- API Key Status: {'Set (starts with Bearer)' if self.api_key.startswith('Bearer') else 'Set (missing Bearer)'}")
            logger.info(f"- API Key Length: {len(self.api_key)} characters")
            
        except Exception as e:
            logger.error(f"Error initializing OANDA client: {str(e)}")
            raise

    def get_account_details(self) -> Dict:
        """Get account details and balance"""
        try:
            import oandapyV20.endpoints.accounts as accounts
            
            # Get account details
            r = accounts.AccountDetails(accountID=self.account_id)
            response = self.client.request(r)
            
            account_data = response.get('account', {})
            
            return {
                'balance': float(account_data.get('balance', 0)),
                'currency': account_data.get('currency', 'USD'),
                'margin_used': float(account_data.get('marginUsed', 0)),
                'margin_available': float(account_data.get('marginAvailable', 0)),
                'open_positions': len(account_data.get('positions', [])),
                'open_trades': len(account_data.get('trades', [])),
                'unrealized_pl': float(account_data.get('unrealizedPL', 0))
            }
            
        except V20Error as e:
            logger.error(f"OANDA API error getting account details: {str(e)}")
            raise Exception(f"Failed to get account details: {str(e)}")
        except Exception as e:
            logger.error(f"Error getting account details: {str(e)}")
            raise

    def place_trade(self, trade_data: Dict) -> Dict:
        """Place a trade on OANDA"""
        try:
            # Get current market price first
            current_price = self.get_current_price(trade_data['symbol'])
            logger.info(f"Current market price for {trade_data['symbol']}: {current_price.get('bid', 'N/A')}/{current_price.get('ask', 'N/A')}")
            
            # Place market order WITHOUT TP/SL first (to avoid direction issues)
            order_data = {
                "order": {
                    "type": "MARKET",
                    "instrument": trade_data['symbol'].replace('/', '_').upper(),
                    "units": str(trade_data['units']),  # Positive for buy, negative for sell
                    "timeInForce": "FOK",
                    "positionFill": "DEFAULT"
                }
            }
            
            logger.info(f"Placing trade: {trade_data['units']} units of {trade_data['symbol']}")
            
            # Create and process the order request
            r = orders.OrderCreate(self.account_id, data=order_data)
            response = self.client.request(r)
            
            logger.info(f"Trade placed successfully: {response}")
            return {
                'status': 'success',
                'order_id': response['orderFillTransaction']['id'],
                'filled_price': response['orderFillTransaction']['price'],
                'timestamp': datetime.now().isoformat()
            }
            
        except V20Error as e:
            logger.error(f"OANDA API error: {str(e)}")
            raise Exception(f"OANDA trade execution failed: {str(e)}")
        except Exception as e:
            logger.error(f"Error placing trade: {str(e)}")
            raise

    def get_current_price(self, pair: str) -> Dict:
        """Get current price for a currency pair"""
        try:
            # Ensure the pair is properly formatted
            formatted_pair = pair.replace('/', '_').upper()
            logger.info(f"Fetching price for {formatted_pair}")
            
            # Create the pricing request
            params = {"instruments": formatted_pair}
            r = pricing.PricingInfo(accountID=self.account_id, params=params)
            
            # Make the request with full debugging
            logger.info(f"Making pricing request for {formatted_pair}")
            logger.debug(f"Request parameters: {params}")
            
            try:
                logger.info(f"Sending request to OANDA for {formatted_pair}")
                logger.info(f"Environment: {self.environment} (detected from account ID), Account ID: {self.account_id}")
                response = self.client.request(r)
                logger.debug(f"Raw response: {response}")
            except oandapyV20.exceptions.V20Error as v20_error:
                error_msg = str(v20_error)
                logger.error("OANDA API error details:")
                logger.error(f"- Error message: {error_msg}")
                logger.error(f"- Environment: {self.environment} (detected from account ID)")
                logger.error(f"- API URL: {self.api_url}")
                logger.error(f"- Account ID: {self.account_id}")
                logger.error("Common solutions:")
                logger.error("1. Verify API key matches the detected environment (LIVE)")
                logger.error("2. Ensure API key has proper permissions for live trading")
                logger.error("3. Check if the API key is valid and not expired")
                raise Exception(f"OANDA API error: {error_msg}")
            except Exception as req_error:
                logger.error(f"Request failed: {str(req_error)}")
                logger.error("Please verify your network connection and API endpoint")
                raise
            
            # Process response
            if response and 'prices' in response and len(response['prices']) > 0:
                price_data = response['prices'][0]
                result = {
                    'bid': float(price_data['bids'][0]['price']),
                    'ask': float(price_data['asks'][0]['price']),
                    'timestamp': price_data['time']
                }
                logger.info(f"Price data received for {pair}: Bid={result['bid']}, Ask={result['ask']}")
                return result
            else:
                error_msg = f"No price data available for {pair}"
                logger.error(error_msg)
                if response:
                    logger.error(f"Unexpected response format: {response}")
                raise Exception(error_msg)
                
        except Exception as e:
            logger.error(f"Error getting price for {pair}: {str(e)}")
            raise

    def close_trade(self, trade_id: str) -> Dict:
        """Close a specific trade"""
        try:
            r = trades.TradeClose(self.account_id, trade_id)
            response = self.client.request(r)
            
            logger.info(f"Trade closed successfully: {response}")
            return {
                'status': 'success',
                'close_price': response['orderFillTransaction']['price'],
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error closing trade: {str(e)}")
            raise

    def modify_trade(self, trade_id: str, stop_loss: Optional[float] = None, 
                    take_profit: Optional[float] = None) -> Dict:
        """Modify an existing trade's stop loss or take profit"""
        try:
            data = {}
            if stop_loss is not None:
                data["stopLoss"] = {"price": str(stop_loss)}
            if take_profit is not None:
                data["takeProfit"] = {"price": str(take_profit)}
                
            if data:
                r = trades.TradeCRCDO(self.account_id, trade_id, data)
                response = self.client.request(r)
                
                logger.info(f"Trade modified successfully: {response}")
                return {
                    'status': 'success',
                    'trade_id': trade_id,
                    'timestamp': datetime.now().isoformat()
                }
            
            return {'status': 'no_changes_requested'}
            
        except Exception as e:
            logger.error(f"Error modifying trade: {str(e)}")
            raise
