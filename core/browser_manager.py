from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from config.browser_config import BrowserConfig

class BrowserManager:
    def __init__(self, logger):
        self.logger = logger
        
    def create_driver(self, browser_type):
        try:
            options = BrowserConfig.get_browser_options(browser_type)
            
            if browser_type == BrowserConfig.CHROME:
                driver = webdriver.Chrome(options=options)
                self._apply_stealth(driver)
            elif browser_type == BrowserConfig.FIREFOX:
                driver = webdriver.Firefox(options=options)
            elif browser_type == BrowserConfig.EDGE:
                driver = webdriver.Edge(options=options)
            
            return driver
            
        except Exception as e:
            self.logger.error(f"Failed to create {browser_type} driver: {str(e)}")
            return None
            
    def _apply_stealth(self, driver):
        stealth(driver,
            languages=["en-US", "en", "vi-VN"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )