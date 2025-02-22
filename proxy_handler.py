import requests
import logging
import time
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ProxyRotator:
    def __init__(self, logger=None):
        # Load from .env
        self.api_key = os.getenv("API_KEY")
        self.proxy_host = os.getenv("PROXY_HOST")
        self.proxy_port = os.getenv("PROXY_PORT")
        self.proxy_username = os.getenv("PROXY_USERNAME")
        self.proxy_password = os.getenv("PROXY_PASSWORD")
        self.logger = logger or logging.getLogger(__name__)

        # Validate environment variables
        self._validate_config()

    def _validate_config(self):
        """Validate required environment variables"""
        required_vars = [
            'API_KEY', 'PROXY_HOST', 'PROXY_PORT',
            'PROXY_USERNAME', 'PROXY_PASSWORD'
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

    def change_ip(self):
        try:
            url = f"https://proxyxoay.net/api/rotating-proxy/change-key-ip/{self.api_key}"
            response = requests.get(url)
            data = response.json()
            
            if data.get('status') == 500 and "giây" in data.get('message', ''):
                try:
                    wait_time = int(''.join(filter(str.isdigit, data['message'])))
                    self.logger.info(f"Waiting {wait_time} seconds before next IP change...")
                    time.sleep(wait_time + 1)
                    return self.change_ip()
                except ValueError:
                    wait_time = 40
                    self.logger.info(f"Could not parse wait time, waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    return self.change_ip()
            
            if data.get('status') == 200:
                self.logger.info("IP changed successfully")
                new_ip = self.get_current_ip()
                if new_ip:
                    self.logger.info(f"New IP: {new_ip}")
                time.sleep(2)
                return True
            
            self.logger.error(f"Failed to change IP: {json.dumps(data)}")
            return False
            
        except Exception as e:
            self.logger.error(f"Error changing IP: {str(e)}")
            return False

    def get_current_ip(self):
        try:
            proxies = {
                'http': f'http://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}',
                'https': f'http://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}'
            }
            
            response = requests.get('https://api.ipify.org?format=json', proxies=proxies, timeout=10)
            if response.status_code == 200:
                return response.json().get('ip')
            return None
        except Exception as e:
            self.logger.error(f"Error getting current IP: {str(e)}")
            return None

    def get_proxy_url(self):
        return f"http://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}"

    def wait_for_ip_change(self, wait_time):
        self.logger.info(f"Waiting {wait_time} seconds for IP change cooldown...")
        interval = 5
        elapsed = 0
        while elapsed < wait_time:
            time.sleep(min(interval, wait_time - elapsed))
            elapsed += interval
            remaining = wait_time - elapsed
            if remaining > 0:
                self.logger.info(f"Still waiting... {remaining} seconds remaining")
        self.logger.info("Wait complete, attempting IP change...")
