from core.driver import WebDriverManager

# Create an instance of WebDriverManager
driver_manager = WebDriverManager()

# Get the WebDriver object
driver = driver_manager.get_driver()

# Use the driver object for your test script logic...

# Quit the driver after use
driver_manager.quit_driver()
