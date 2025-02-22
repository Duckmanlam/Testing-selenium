import logging
import os
from datetime import datetime

class Logger:
    @staticmethod
    def setup():
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(
                    f'logs/worker_{datetime.now().strftime("%Y%m%d")}.log',
                    encoding='utf-8'
                ),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)