from core.logger import Logger
from core.driver import WebDriverManager
from test_cases import test_login                       
from configparser import ConfigParser
import pytest
import allure
from allure_commons.types import Severity

class Initiate:
    def __init__(self):
        self.driver_manager = WebDriverManager()
        self.driver = self.driver_manager.get_driver()
        self.logger = Logger()
        # self.readConfig()

    # def readConfig(self):
    #     # Specify the path to your configuration file
    #     config_file = "config/config.properties"

    #     # Create a ConfigParser object
    #     config = ConfigParser()

    #     # Read the configuration file
    #     config.read(config_file)

    #     # Access the properties using section and key names
    #     self.selenium_driver = config['selenium']['driver']
    #     self.test_case_url = config['test_case']['url']  

    @allure.step("Login to the application")  
    def test_login_functionality(self): 
        allure.step("Step 1: Open the application")       
        tc = test_login.test_login("https://www.saucedemo.com/", self.driver,self.logger)       
        assert tc.test_1()


if __name__ =="__main__":
    main_obj = Initiate()
    main_obj.test_login_functionality()




   