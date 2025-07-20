import os
import shutil
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def backup_data():
    """Backup all system data and models"""
    try:
        # Create backup directory with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = f'backups/backup_{timestamp}'
        os.makedirs(backup_dir, exist_ok=True)
        
        # Backup data directory
        if os.path.exists('data'):
            shutil.copytree('data', f'{backup_dir}/data')
            logger.info(f"Data directory backed up to {backup_dir}/data")
            
        # Backup models
        if os.path.exists('models'):
            shutil.copytree('models', f'{backup_dir}/models')
            logger.info(f"Models backed up to {backup_dir}/models")
            
        # Backup logs
        if os.path.exists('logs'):
            shutil.copytree('logs', f'{backup_dir}/logs')
            logger.info(f"Logs backed up to {backup_dir}/logs")
            
        logger.info(f"Backup completed successfully: {backup_dir}")
        return True
        
    except Exception as e:
        logger.error(f"Error during backup: {str(e)}")
        return False

if __name__ == '__main__':
    backup_data()
