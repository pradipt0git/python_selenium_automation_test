from selenium import webdriver


class WebDriverManager:
    """
    Manages the creation and quitting of WebDriver objects for different browsers.
    """

    def __init__(self, browser="chrome"):
        """
        Initializes the WebDriverManager object.

        Args:
            browser (str, optional): The desired browser. Defaults to "chrome".
        """
        self.browser = browser.lower()
        self.driver = None

    def get_driver(self, webdriver_path=None):
        """
        Gets a WebDriver object for the specified browser.

        Args:
            webdriver_path (str, optional): The path to the WebDriver executable (optional).

        Returns:
            webdriver.Chrome | webdriver.Firefox: The initialized WebDriver object.

        Raises:
            ValueError: If the requested browser is not supported.
        """
        if self.browser == "chrome":
            if webdriver_path:
                self.driver = webdriver.Chrome(webdriver_path)
            else:
                self.driver = webdriver.Chrome()
        elif self.browser == "firefox":
            if webdriver_path:
                from selenium.webdriver.firefox.service import Service
                self.driver = webdriver.Firefox(service=Service(webdriver_path))
            else:
                # Add logic to handle missing geckodriver path (error or prompt for path)
                raise ValueError("Firefox support requires geckodriver. Please install and specify its path.")
        else:
            raise ValueError("Unsupported browser: {}".format(self.browser))

        return self.driver

    def quit_driver(self):
        """
        Quits the WebDriver object if it's been initialized.

        Prints a message if the driver was not initialized.
        """
        if self.driver:
            self.driver.quit()
        else:
            print("Driver not initialized")
