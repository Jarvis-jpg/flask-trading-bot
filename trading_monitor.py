#!/usr/bin/env python3
"""
Basic Trading Monitoring System
Ensures proper logging and monitoring capabilities
"""
import logging
import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_safety.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def log_trade(trade_info):
    """Log trade information"""
    logger.info(f"Trade: {trade_info}")

def log_error(error_info):
    """Log error information"""  
    logger.error(f"Error: {error_info}")

def log_warning(warning_info):
    """Log warning information"""
    logger.warning(f"Warning: {warning_info}")

def log_system_status(status_info):
    """Log system status information"""
    logger.info(f"System Status: {status_info}")

# Create initial log entry
if __name__ == "__main__":
    log_system_status("Trading monitoring system initialized")
    print("✅ Basic monitoring system created and active")
