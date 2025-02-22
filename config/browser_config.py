from fake_useragent import UserAgent

class BrowserConfig:
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
    
    @staticmethod
    def get_browser_options(browser_type):
        ua = UserAgent()
        
        if browser_type == BrowserConfig.CHROME:
            from selenium.webdriver.chrome.options import Options
            options = Options()
        elif browser_type == BrowserConfig.FIREFOX:
            from selenium.webdriver.firefox.options import Options
            options = Options()
        elif browser_type == BrowserConfig.EDGE:
            from selenium.webdriver.edge.options import Options
            options = Options()
            
        # Common options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument(f'user-agent={ua.random}')
        options.add_argument('--start-maximized')
        
        return options