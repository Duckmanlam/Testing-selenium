from config.browser_config import BrowserConfig
from config.search_config import SearchConfig
from core.browser_manager import BrowserManager
from core.search_manager import SearchManager
from utils.logger import Logger
from utils.helpers import BrowserActions
from proxy_handler import ProxyRotator
import random
import time

class Worker:
    def __init__(self):
        self.logger = Logger.setup()
        self.browser_manager = BrowserManager(self.logger)
        self.search_manager = SearchManager(self.logger)
        self.proxy_rotator = ProxyRotator(self.logger)
        self.session_count = 0
        
    def run_session(self, browser_type, target_url):
        driver = None
        self.session_count += 1
        
        try:
            self.logger.info(f"Running session {self.session_count}")
            
            # Change IP before creating driver
            self.logger.info("Changing IP...")
            if not self.proxy_rotator.change_ip():
                raise Exception("Failed to change IP")
            
            driver = self.browser_manager.create_driver(browser_type)
            if not driver:
                raise Exception(f"Failed to create {browser_type} driver")
            
            # Verify IP after creating driver
            driver.get("https://api.ipify.org?format=json")
            time.sleep(3)
            self.logger.info(f"Browser IP check: {driver.page_source}")
            
            search_engine = random.choice(SearchConfig.SEARCH_ENGINES)
            search_query = random.choice(SearchConfig.SEARCH_QUERIES)
            
            self.logger.info(f"Using search engine: {search_engine['name']}")
            self.logger.info(f"Search query: {search_query}")
            
            if self.search_manager.perform_search(
                driver, search_engine, search_query, target_url
            ):
                self.logger.info("Target found and clicked")
                time.sleep(random.uniform(10, 15))
                BrowserActions.natural_scroll(driver)
                time.sleep(random.uniform(5, 10))
                
        except Exception as e:
            self.logger.error(f"Session error: {str(e)}")
            
        finally:
            if driver:
                driver.quit()
            delay = random.uniform(30, 60)
            self.logger.info(f"Waiting {delay:.2f} seconds before next session")
            time.sleep(delay)

    def run_multiple_sessions(self, target_url, total_sessions):
        browsers = [BrowserConfig.CHROME, BrowserConfig.FIREFOX, BrowserConfig.EDGE]
        
        try:
            # Initial IP check
            current_ip = self.proxy_rotator.get_current_ip()
            self.logger.info(f"Starting IP: {current_ip}")
            
            for session in range(total_sessions):
                browser_type = random.choice(browsers)
                self.logger.info(f"\n{'='*50}")
                self.logger.info(f"Starting session {session + 1}/{total_sessions} with {browser_type}")
                self.logger.info(f"{'='*50}\n")
                
                self.run_session(browser_type, target_url)
                
                if session < total_sessions - 1:
                    delay = random.uniform(60, 120)
                    self.logger.info(f"Waiting {delay:.2f} seconds before next session")
                    time.sleep(delay)
                
            self.logger.info(f"\n{'='*50}")
            self.logger.info(f"All {total_sessions} sessions completed!")
            self.logger.info(f"{'='*50}\n")
                
        except KeyboardInterrupt:
            self.logger.info("\nWorker stopped by user")
            self.logger.info(f"Completed sessions: {self.session_count}/{total_sessions}")
        except Exception as e:
            self.logger.error(f"Worker error: {str(e)}")
        finally:
            self.logger.info("Worker shutdown complete")

def main():
    worker = Worker()
    target_url = "kways.vn"
    total_sessions = 6
    
    worker.run_multiple_sessions(target_url, total_sessions)

if __name__ == "__main__":
    main()
