import argparse
import csv
import os
import queue  # Use queue instead of Queue for Python 3 compatibility
from datetime import datetime
from threading import Thread

from core import DBProvider  # Import DBProvider from core
from core.utils import (
    read_config,  # Uncomment if needed for additional logic
    replace_placeholders,
    generate_output_filename,
    save_csv_data,
    create_day_log_file,
    get_logger,
)

# Configure logging
logger = get_logger(create_day_log_file())


class Worker(Thread):
    """
    Worker thread class that processes tasks from the task queue.
    """

    def __init__(self, task_queue, error_queue):
        super().__init__()
        self.task_queue = task_queue
        self.error_queue = error_queue
        self.daemon = True  # Set as daemon for proper program termination

    def run(self):
        while True:
            try:
                row = self.task_queue.get()
                if row['do_execute'].lower() == 'true':  # Check for execution flag
                    execute_and_save(row)
                self.task_queue.task_done()
            except Exception as e:
                self.error_queue.put(e)
            finally:
                self.task_queue.task_done()


def execute_and_save(row):
    """
    Executes SQL queries from logic and database paths, saves results to separate CSV files,
    and handles logging for a single row, considering argument-wise execution logic.

    Args:
        row (dict): A dictionary containing configuration data (may include placeholders).

    Raises:
        Exception: Re-raises any exceptions encountered during processing.
    """

    try:
        # Build a dictionary of all placeholders and their values (including command-line arguments)
        replacements = {
            '<DATE>': datetime.today().strftime('%Y-%m-%d'),
        }
        replacements.update(vars(args))  # Add command-line arguments to replacements

        # Extract arguments from additional columns (args_* format)
        for col_name, col_value in row.items():
            if col_name.startswith('args_'):
                placeholder_key = col_name[5:]  # Remove 'args_' prefix
                replacements[f"<{placeholder_key}>"] = col_value

        # Execute logic SQL (query1) only if 'do_logic_sql' flag is set (argument-wise execution)
        if row.get('do_logic_sql', 'false').lower() == 'true':
            logic_sql_file_path = replace_placeholders(row['logic_sql_file_path'], replacements)
            with open(logic_sql_file_path, 'r') as f:
                logic_sql_content = f.read()
            db_provider = DBProvider()
            logic_results = db_provider.execute_query(logic_sql_content)

            logic_output_filename = generate_output_filename(
                f"{row['application']}_{row['identifier_name']}_logic_generated"
            )
            logic_output_path = os.path.join("output", logic_output_filename)
            save_csv_data(logic_results, logic_output_path)

            logger.info(f"Successfully generated CSV: {logic_output_filename}")

        # Execute database SQL (query2) only if 'do_execute' flag is set (argument-wise execution)
        if row.get('do_execute', 'false').lower() == 'true':
            db_sql_file_path = replace_placeholders(row['db_sql_file_path'], replacements)
            with open(db_sql_file_path, 'r') as f:
                db_sql_content = f.read()
            db_results = db_provider.execute_query(db_sql_content)

            db_output_filename = generate_output_filename(
                f"{row['application']}_{row['identifier_name']}_db_generated"
            )
            db_output_path = os.path.join("output", db_output_filename)
            save_csv_data(db_results, db_output_path)

            logger.info(f"Successfully generated CSV: {db_output_filename}")

    except Exception as e:
        logger.error(f"Error processing row: {e}")
        raise e  # Re-raise to signal an error


def main():
    """
    Main function that parses command-line arguments, reads configuration (optional), executes SQL files
    in multithreading mode using a task queue and worker threads, and generates output CSV files.

    Handles potential errors using an error queue.

    - Introduces argument-wise execution logic based on 'do_logic_sql' and 'do_db_sql' flags.
    """

    # Define command-line arguments using argparse
    parser = argparse.ArgumentParser(description="Generate CSV files using SQL queries.")
    parser.add_argument(
        "-a", "--application", type=str, required=True, help="Application name"
    )
    parser.add_argument(
        "-i", "--identifier", type=str, required=True, help="Identifier name"
    )
    parser.add_argument("-d", "--date", type=str, default=datetime.today().strftime('%Y-%m-%d'), help="Date (YYYY-MM-DD)")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Additional arguments (key=value)")
    args = parser.parse_args()

    # Create a dictionary from remaining arguments (excluding application, identifier, date)
    arg_dict = {}
    for arg in args.args:
        key, value = arg.split("=")
        arg_dict[key] = value

    # Build a configuration row with parsed arguments
    row = {
        "application": args.application,
        "identifier_name": args.identifier,
        **arg_dict,  # Unpack arguments dictionary
    }

    # Read configuration data (optional, if needed for additional logic)
    # config_data = read_config()  # Uncomment if required

    # Create task queue and error queue
    task_queue = queue.Queue()
    error_queue = queue.Queue()

    # Create a pool of worker threads
    num_workers = 4  # Adjust the number of workers as needed
    workers = [Worker(task_queue, error_queue) for _ in range(num_workers)]
    for worker in workers:
        worker.start()

    # Add tasks to the queue (only rows with 'do_execute'='true')
    # config_data = ...  # If using configuration data

    # for row in config_data:  # Uncomment if using configuration data
    task_queue.put(row)

    # Wait for all tasks to finish
    task_queue.join()

    # Check for errors during processing
    while not error_queue.empty():
        try:
            error = error_queue.get_nowait()
            logger.error(f"An error occurred: {error}")
        except Exception as e:
            logger.error(f"Error retrieving error from queue: {e}")

    # Terminate worker threads (optional, since daemon=True)
    # for worker in workers:
    #     worker.join()


if __name__ == "__main__":
    main()

#python main.py -a my_application -i identifier123 -d 2023-08-15 arg1=value1 do_logic_sql=true
