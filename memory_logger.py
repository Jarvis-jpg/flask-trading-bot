"""
SevenSYS Memory Logger - Core logging system for webhook tracking and trade analysis
Focuses exclusively on SevenSYS Pine script performance without altering trading logic
"""

import json
import sqlite3
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

class SevenSYSMemoryLogger:
    def __init__(self, db_path: str = "sevensys_memory.db"):
        self.db_path = db_path
        self.setup_logging()
        self.setup_database()
    
    def setup_logging(self):
        """Setup logging for the memory logger itself"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('memory_logger.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_database(self):
        """Initialize SQLite database with tables for SevenSYS tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Webhook alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS webhook_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                ticker TEXT NOT NULL,
                action TEXT NOT NULL,
                close_price REAL NOT NULL,
                strategy_name TEXT DEFAULT 'SevenSYS',
                raw_data TEXT,
                processed BOOLEAN DEFAULT FALSE,
                session_id TEXT
            )
        ''')
        
        # Trade executions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trade_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                webhook_id INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                ticker TEXT NOT NULL,
                action TEXT NOT NULL,
                entry_price REAL NOT NULL,
                position_size REAL NOT NULL,
                stop_loss REAL,
                take_profit REAL,
                execution_status TEXT DEFAULT 'PENDING',
                oanda_order_id TEXT,
                session_id TEXT,
                FOREIGN KEY (webhook_id) REFERENCES webhook_alerts (id)
            )
        ''')
        
        # Trade outcomes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trade_outcomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trade_id INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                exit_price REAL,
                pnl REAL,
                exit_reason TEXT,
                duration_minutes INTEGER,
                session_id TEXT,
                FOREIGN KEY (trade_id) REFERENCES trade_executions (id)
            )
        ''')
        
        # Daily performance summary table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE UNIQUE,
                total_alerts INTEGER DEFAULT 0,
                successful_executions INTEGER DEFAULT 0,
                failed_executions INTEGER DEFAULT 0,
                total_pnl REAL DEFAULT 0.0,
                win_trades INTEGER DEFAULT 0,
                loss_trades INTEGER DEFAULT 0,
                avg_win REAL DEFAULT 0.0,
                avg_loss REAL DEFAULT 0.0,
                largest_win REAL DEFAULT 0.0,
                largest_loss REAL DEFAULT 0.0,
                session_id TEXT
            )
        ''')
        
        # Session tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                end_time DATETIME,
                total_alerts INTEGER DEFAULT 0,
                total_trades INTEGER DEFAULT 0,
                net_pnl REAL DEFAULT 0.0,
                status TEXT DEFAULT 'ACTIVE'
            )
        ''')
        
        conn.commit()
        conn.close()
        self.logger.info("Database initialized successfully")
    
    def log_webhook_alert(self, webhook_data: Dict[str, Any], session_id: str = None) -> int:
        """Log incoming webhook alert from SevenSYS"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO webhook_alerts (ticker, action, close_price, raw_data, session_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                webhook_data.get('ticker', 'UNKNOWN'),
                webhook_data.get('strategy.order.action', 'UNKNOWN'),
                float(webhook_data.get('close', 0.0)),
                json.dumps(webhook_data),
                session_id
            ))
            
            webhook_id = cursor.lastrowid
            conn.commit()
            
            self.logger.info(f"Logged webhook alert: ID={webhook_id}, Ticker={webhook_data.get('ticker')}, Action={webhook_data.get('strategy.order.action')}")
            
            # Update daily performance
            self._update_daily_alerts_count()
            
            return webhook_id
            
        except Exception as e:
            self.logger.error(f"Error logging webhook alert: {e}")
            return -1
        finally:
            conn.close()
    
    def log_trade_execution(self, webhook_id: int, execution_data: Dict[str, Any], session_id: str = None) -> int:
        """Log successful trade execution"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO trade_executions (
                    webhook_id, ticker, action, entry_price, position_size, 
                    stop_loss, take_profit, execution_status, oanda_order_id, session_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                webhook_id,
                execution_data.get('ticker', 'UNKNOWN'),
                execution_data.get('action', 'UNKNOWN'),
                float(execution_data.get('entry_price', 0.0)),
                float(execution_data.get('position_size', 0.0)),
                float(execution_data.get('stop_loss', 0.0)) if execution_data.get('stop_loss') else None,
                float(execution_data.get('take_profit', 0.0)) if execution_data.get('take_profit') else None,
                execution_data.get('status', 'EXECUTED'),
                execution_data.get('order_id'),
                session_id
            ))
            
            trade_id = cursor.lastrowid
            conn.commit()
            
            self.logger.info(f"Logged trade execution: ID={trade_id}, Ticker={execution_data.get('ticker')}, Entry={execution_data.get('entry_price')}")
            
            # Update daily performance
            self._update_daily_executions_count(success=True)
            
            return trade_id
            
        except Exception as e:
            self.logger.error(f"Error logging trade execution: {e}")
            return -1
        finally:
            conn.close()
    
    def log_execution_failure(self, webhook_id: int, error_details: Dict[str, Any], session_id: str = None):
        """Log failed trade execution"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO trade_executions (
                    webhook_id, ticker, action, entry_price, position_size, 
                    execution_status, session_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                webhook_id,
                error_details.get('ticker', 'UNKNOWN'),
                error_details.get('action', 'UNKNOWN'),
                float(error_details.get('entry_price', 0.0)),
                0.0,  # No position size for failed execution
                f"FAILED: {error_details.get('error', 'Unknown error')}",
                session_id
            ))
            
            conn.commit()
            
            self.logger.warning(f"Logged execution failure: Webhook ID={webhook_id}, Error={error_details.get('error')}")
            
            # Update daily performance
            self._update_daily_executions_count(success=False)
            
        except Exception as e:
            self.logger.error(f"Error logging execution failure: {e}")
        finally:
            conn.close()
    
    def _update_daily_alerts_count(self):
        """Update daily alerts counter"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            today = datetime.date.today()
            cursor.execute('''
                INSERT OR REPLACE INTO daily_performance (date, total_alerts)
                VALUES (?, COALESCE((SELECT total_alerts FROM daily_performance WHERE date = ?), 0) + 1)
            ''', (today, today))
            
            conn.commit()
        except Exception as e:
            self.logger.error(f"Error updating daily alerts count: {e}")
        finally:
            conn.close()
    
    def _update_daily_executions_count(self, success: bool):
        """Update daily executions counter"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            today = datetime.date.today()
            
            if success:
                cursor.execute('''
                    INSERT OR REPLACE INTO daily_performance (date, successful_executions)
                    VALUES (?, COALESCE((SELECT successful_executions FROM daily_performance WHERE date = ?), 0) + 1)
                ''', (today, today))
            else:
                cursor.execute('''
                    INSERT OR REPLACE INTO daily_performance (date, failed_executions)
                    VALUES (?, COALESCE((SELECT failed_executions FROM daily_performance WHERE date = ?), 0) + 1)
                ''', (today, today))
            
            conn.commit()
        except Exception as e:
            self.logger.error(f"Error updating daily executions count: {e}")
        finally:
            conn.close()
    
    def get_today_summary(self) -> Dict[str, Any]:
        """Get today's performance summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            today = datetime.date.today()
            
            # Get webhook alerts count for today
            cursor.execute('''
                SELECT COUNT(*) FROM webhook_alerts 
                WHERE DATE(timestamp) = ?
            ''', (today,))
            alerts_today = cursor.fetchone()[0]
            
            # Get trade executions for today
            cursor.execute('''
                SELECT COUNT(*) FROM trade_executions 
                WHERE DATE(timestamp) = ? AND execution_status NOT LIKE 'FAILED%'
            ''', (today,))
            successful_trades = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT COUNT(*) FROM trade_executions 
                WHERE DATE(timestamp) = ? AND execution_status LIKE 'FAILED%'
            ''', (today,))
            failed_trades = cursor.fetchone()[0]
            
            # Get recent alerts
            cursor.execute('''
                SELECT timestamp, ticker, action, close_price 
                FROM webhook_alerts 
                WHERE DATE(timestamp) = ?
                ORDER BY timestamp DESC
                LIMIT 10
            ''', (today,))
            recent_alerts = cursor.fetchall()
            
            return {
                'date': str(today),
                'total_alerts': alerts_today,
                'successful_trades': successful_trades,
                'failed_trades': failed_trades,
                'success_rate': (successful_trades / alerts_today * 100) if alerts_today > 0 else 0.0,
                'recent_alerts': [
                    {
                        'timestamp': alert[0],
                        'ticker': alert[1],
                        'action': alert[2],
                        'price': alert[3]
                    } for alert in recent_alerts
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Error getting today's summary: {e}")
            return {}
        finally:
            conn.close()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status and recent activity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Total counts
            cursor.execute('SELECT COUNT(*) FROM webhook_alerts')
            total_alerts = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM trade_executions WHERE execution_status NOT LIKE "FAILED%"')
            total_successful_trades = cursor.fetchone()[0]
            
            # Last alert time
            cursor.execute('SELECT MAX(timestamp) FROM webhook_alerts')
            last_alert = cursor.fetchone()[0]
            
            # Last execution time
            cursor.execute('SELECT MAX(timestamp) FROM trade_executions')
            last_execution = cursor.fetchone()[0]
            
            return {
                'total_alerts': total_alerts,
                'total_successful_trades': total_successful_trades,
                'overall_success_rate': (total_successful_trades / total_alerts * 100) if total_alerts > 0 else 0.0,
                'last_alert_time': last_alert,
                'last_execution_time': last_execution,
                'database_status': 'HEALTHY'
            }
            
        except Exception as e:
            self.logger.error(f"Error getting system status: {e}")
            return {'database_status': 'ERROR', 'error': str(e)}
        finally:
            conn.close()
