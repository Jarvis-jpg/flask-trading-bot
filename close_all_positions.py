import os
import logging
from oanda_client import OandaClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def close_all_positions():
    """Emergency function to close all open positions"""
    try:
        logger.info("Initiating emergency position closure...")
        
        # Initialize OANDA client
        oanda = OandaClient()
        
        # Get all open positions
        positions = oanda.get_open_positions()
        
        closed_positions = 0
        for position in positions:
            try:
                # Close position
                result = oanda.close_position(position['id'])
                if result.get('status') == 'closed':
                    closed_positions += 1
                    logger.info(f"Closed position {position['id']}")
                else:
                    logger.warning(f"Failed to close position {position['id']}: {result}")
            except Exception as e:
                logger.error(f"Error closing position {position['id']}: {str(e)}")
        
        logger.info(f"Emergency closure completed. Closed {closed_positions} positions")
        return True
        
    except Exception as e:
        logger.error(f"Emergency closure failed: {str(e)}")
        return False

if __name__ == '__main__':
    close_all_positions()
