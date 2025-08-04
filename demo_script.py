from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class BrowserManager:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def get_driver(self):
        return self.driver

    def close_browser(self):
        input("Press Enter to close browser...")
        self.driver.quit()

class WebElementHelper:
    def __init__(self, driver):
        self.driver = driver

    def find_and_click(self, by, value):
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((by, value)))
        element.click()

    def find_and_fill(self, by, value, text):
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((by, value)))
        element.clear()
        element.send_keys(text)

def login_to_saucedemo(driver, helper):
    driver.get("https://www.saucedemo.com/")
    helper.find_and_fill(By.ID, "user-name", "standard_user")
    helper.find_and_fill(By.ID, "password", "secret_sauce")
    helper.find_and_click(By.ID, "login-button")
    print("Login successful!")

def add_backpack_to_cart(helper):
    helper.find_and_click(By.ID, "add-to-cart-sauce-labs-backpack")
    print("Backpack added to cart")

if __name__ == "__main__":
    browser_manager = BrowserManager()
    driver = browser_manager.get_driver()
    helper = WebElementHelper(driver)

    try:
        login_to_saucedemo(driver, helper)
        add_backpack_to_cart(helper)
    except Exception as e:
        print("Error:", e)
    finally:
        browser_manager.close_browser()
