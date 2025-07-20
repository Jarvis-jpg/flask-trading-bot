import os
import requests
import logging
from typing import Dict, List
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradingViewClient:
    def __init__(self):
        self.webhook_url = os.getenv('TRADINGVIEW_WEBHOOK_URL')
        if not self.webhook_url:
            logger.warning("TRADINGVIEW_WEBHOOK_URL not set - analytics updates will be disabled")

    def send_trade_alert(self, trade_data: Dict) -> bool:
        """Send trade alert to TradingView webhook"""
        if not self.webhook_url:
            logger.warning("Cannot send alert: TradingView webhook URL not configured")
            return False

        try:
            # Format the alert data
            alert_data = {
                "timestamp": datetime.now().isoformat(),
                "pair": trade_data['pair'],
                "action": trade_data['action'],
                "entry": trade_data['entry'],
                "stop_loss": trade_data['stop_loss'],
                "take_profit": trade_data['take_profit'],
                "risk_reward": trade_data.get('risk_reward', None),
                "strategy": trade_data.get('strategy', 'custom'),
                "confidence": trade_data.get('confidence', None)
            }

            # Send the alert to TradingView
            response = requests.post(
                self.webhook_url,
                json=alert_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            if response.status_code == 200:
                logger.info(f"Trade alert sent successfully to TradingView")
                return True
            else:
                logger.error(f"Failed to send trade alert: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"Error sending trade alert: {str(e)}")
            return False

    def update_chart_annotation(self, trade_data: Dict) -> bool:
        """Update chart annotations on TradingView"""
        if not self.webhook_url:
            return False

        try:
            # Format the annotation data
            annotation_data = {
                "type": "chart_annotation",
                "timestamp": datetime.now().isoformat(),
                "pair": trade_data['pair'],
                "annotations": [
                    {
                        "type": "trade_entry",
                        "price": trade_data['entry'],
                        "text": f"{trade_data['action'].upper()} Entry"
                    },
                    {
                        "type": "stop_loss",
                        "price": trade_data['stop_loss'],
                        "text": "SL"
                    },
                    {
                        "type": "take_profit",
                        "price": trade_data['take_profit'],
                        "text": "TP"
                    }
                ]
            }

            # Send the annotation update
            response = requests.post(
                f"{self.webhook_url}/annotations",
                json=annotation_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            if response.status_code == 200:
                logger.info("Chart annotations updated successfully")
                return True
            else:
                logger.error(f"Failed to update chart annotations: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"Error updating chart annotations: {str(e)}")
            return False
