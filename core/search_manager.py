from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
from utils.helpers import BrowserActions

class SearchManager:
    def __init__(self, logger):
        self.logger = logger
        
    def perform_search(self, driver, search_engine, search_query, target_url):
        try:
            self.logger.info(f"Searching on {search_engine['name']}")
            
            driver.get(search_engine['url'])
            time.sleep(random.uniform(2, 4))
            
            # Find and fill search box
            search_box = driver.find_element(
                by=getattr(By, search_engine['search_box']['type'].upper()),
                value=search_engine['search_box']['value']
            )
            
            BrowserActions.natural_type(search_box, search_query)
            time.sleep(random.uniform(0.5, 1.5))
            search_box.send_keys(Keys.RETURN)
            
            time.sleep(random.uniform(3, 5))
            return self.find_and_click_target(driver, target_url)
            
        except Exception as e:
            self.logger.error(f"Search error: {str(e)}")
            return False
            
    def find_and_click_target(self, driver, target_url):
        try:
            links = driver.find_elements(By.TAG_NAME, "a")
            target_links = [
                link for link in links 
                if target_url.lower() in str(link.get_attribute("href")).lower()
                and link.is_displayed()
            ]
            
            if target_links:
                target_link = target_links[0]
                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                    target_link
                )
                time.sleep(random.uniform(1, 2))
                
                try:
                    target_link.click()
                except:
                    driver.execute_script("arguments[0].click();", target_link)
                return True
                
            return False
            
        except Exception as e:
            self.logger.error(f"Error finding/clicking target: {str(e)}")
            return False