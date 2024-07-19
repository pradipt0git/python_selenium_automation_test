import csv
import logging
import os

def create_day_log_file(log_dir="logs"):
    """
    Creates a day-wise log file path within the specified directory.

    Args:
        log_dir (str, optional): Directory to store the log file. Defaults to "logs".

    Returns:
        str: The absolute path of the created log file.
    """

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)  # Create the logs directory if it doesn't exist

    today_str = os.path.strftime("%Y-%m-%d")
    log_file_path = os.path.join(log_dir, f"{today_str}.log")
    return log_file_path

def get_logger(log_file_path):
    """
    Creates and configures a logger instance for day-wise logging.

    Args:
        log_file_path (str): Path to the log file.

    Returns:
        logging.Logger: The configured logger instance.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Adjust log level as needed

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger

def read_config(config_file="config.csv"):
    """
    Reads configuration data from the specified CSV file.

    Args:
        config_file (str, optional): Path to the configuration file. Defaults to "config.csv".

    Returns:
        list: List of dictionaries representing each configuration row.
    """

    config_data = []
    with open(config_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            config_data.append(row)
    return config_data

def replace_placeholders(template_path, replacements):
    """
    Replaces placeholders in a template file with provided values.

    Args:
        template_path (str): Path to the template file (e.g., SQL file).
        replacements (dict): Dictionary containing key-value pairs for replacement.

    Returns:
        str: The modified content with placeholders replaced.
    """

    with open(template_path, 'r') as f:
        template_content = f.read()

    for key, value in replacements.items():
        template_content = template_content.replace(f"<{key}>", str(value))
    return template_content

def generate_output_filename(identifier_name, suffix=".csv"):
    """
    Generates a filename for the output CSV file.

    Args:
        identifier_name (str): Name of the identifier from the config file.
        suffix (str, optional): Suffix for the filename. Defaults to ".csv".

    Returns:
        str: The generated filename (e.g., EFTR_RMT-logic_generated.csv).
    """

    return f"{identifier_name}{suffix}"

def save_csv_data(data, output_path,overwrite=True):
    """
    Saves data to a CSV file at the specified path.

    Args:
        data (list): List of lists representing CSV data.
        output_path (str): Path to the output CSV file.
    """

    if not overwrite and os.path.exists(output_path):
        raise FileExistsError(f"File '{output_path}' already exists. Set 'overwrite=True' to replace.")

    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)