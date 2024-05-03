import logging
import os
import datetime


class Logger:
    """
    Custom logger class that creates log files with timestamps and supports different logging levels.
    """

    def __init__(self, log_file="automation.log", log_level=logging.INFO):
        """
        Initializes the logger object.

        Args:
            log_file (str, optional): The filename for the log file. Defaults to "automation.log".
            log_level (int, optional): The logging level. Defaults to logging.INFO.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        logs_folder = "logs"
        if not os.path.exists(logs_folder):
            os.makedirs(logs_folder)

        today = datetime.date.today().strftime("%Y-%m-%d")
        log_file_name = os.path.join(logs_folder, f"{today}.log")

        file_handler = logging.FileHandler(log_file_name)
        file_handler.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def info(self, message):
        """
        Logs a message at the INFO level.

        Args:
            message (str): The message to log.
        """
        self.logger.info(message)

    def debug(self, message):
        """
        Logs a message at the DEBUG level.

        Args:
            message (str): The message to log.
        """
        self.logger.debug(message)

    def warning(self, message):
        """
        Logs a message at the WARNING level.

        Args:
            message (str): The message to log.
        """
        self.logger.warning(message)

    def error(self, message):
        """
        Logs a message at the ERROR level.

        Args:
            message (str): The message to log.
        """
        self.logger.error(message)

    def close(self):
        """
        Closes the file handler associated with the logger.
        """
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)
