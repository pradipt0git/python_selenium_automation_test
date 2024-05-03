from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class utility:
    def __init__(self, driver):
        self.driver = driver

    def text_entry(element, value_to_set):
        element.send_keys(value_to_set)