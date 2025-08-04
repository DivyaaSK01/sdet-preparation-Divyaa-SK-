from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class WebElementHelper:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find_element(self, by_type, identifier):
        try:
            return self.wait.until(EC.presence_of_element_located((by_type, identifier)))
        except TimeoutException:
            print(f"[Error] Element not found: {identifier}")
            return None

    def click_element(self, by_type, identifier):
        try:
            element = self.wait.until(EC.element_to_be_clickable((by_type, identifier)))
            element.click()
        except TimeoutException:
            print(f"[Error] Click failed: {identifier}")

    def enter_text(self, by_type, identifier, text):
        element = self.find_element(by_type, identifier)
        if element:
            element.clear()
            element.send_keys(text)
