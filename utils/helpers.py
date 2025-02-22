import random
import time

class BrowserActions:
    @staticmethod
    def natural_type(element, text):
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

    @staticmethod
    def natural_scroll(driver):
        total_height = driver.execute_script("return document.body.scrollHeight")
        viewed_height = 0
        
        while viewed_height < total_height:
            scroll_step = random.randint(100, 300)
            viewed_height += scroll_step
            driver.execute_script(
                f"window.scrollTo({{top: {viewed_height}, behavior: 'smooth'}});"
            )
            time.sleep(random.uniform(0.5, 1.5))