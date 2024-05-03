from core.logger import Logger
from core.driver import WebDriverManager
from test_cases import tc01_login

class Initiate:
    def __init__(self):
        self.driver_manager = WebDriverManager()
        self.driver = self.driver_manager.get_driver()
        self.logger = Logger()
        
       

    def run_automation(self):        
        tc = tc01_login.tc01_login("https://www.saucedemo.com/", self.driver,self.logger)
        tc.step1()


if __name__ =="__main__":
    main_obj = Initiate()
    main_obj.run_automation()