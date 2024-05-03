from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class locator:
    def __init__(self,driver):
        self.driver = driver

    def get_user_name(self):
        """
        Returns the WebElement representing the username element.
        """
        found_element= self.driver.find_element(By.XPATH, "//*[@id='user-name']")  # Replace with your XPath
        return found_element
