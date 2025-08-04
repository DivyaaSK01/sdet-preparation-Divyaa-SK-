from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException

class BrowserManager:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(30)
        except WebDriverException as e:
            print(f"[Error] WebDriver Initialization Failed: {e}")
            self.driver = None

    def open_url(self, url: str):
        try:
            self.driver.get(url)
        except TimeoutException:
            print(f"[Error] Page load timed out: {url}")
        except Exception as e:
            print(f"[Error] Could not open URL: {e}")

    def close_browser(self):
        if self.driver:
            self.driver.quit()
