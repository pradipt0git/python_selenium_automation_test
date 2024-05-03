from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from core.logger import Logger
from utility import utility
from test_cases import locator

class tc01_login:
    def __init__(self,url: str, driver : webdriver.Chrome, logger: Logger):
        self.url = url
        self.driver = driver
        self.logger = logger
        self.locator = locator.locator(driver)

    def step1(self):
        try:
            self.logger.info(f"Opening URL: {self.url}")
            self.driver.get(self.url)
            username_element = self.locator.get_user_name()

            # Set the desired value in the username field
            username = "your_username"
            utility.text_entry(username_element, username)

            self.logger.info(f"set Username."+username+"")
            return True

        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            return None

        finally:
            # Consider adding logic to close the browser based on your workflow
            pass  # Placeholder for browser closure (if needed)