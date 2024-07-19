import csv
import os
from datetime import datetime

from core.DB_Operation.db_provider import DBProvider  # Import DBProvider from core
from core.utils import (
    read_config,
    replace_placeholders,
    generate_output_filename,
    save_csv_data,
    create_day_log_file,
    get_logger,
)

# Configure logging
logger = get_logger(create_day_log_file())

def main():
    """
    Main function that reads configuration, executes SQL files, and generates output CSV files.
    """

    # Read configuration data from config.csv
    config_data = read_config()

    for row in config_data:
        if row['do_execute'].lower() == 'true':  # Handle case-insensitive comparison
            try:
                # Build replacements for placeholders
                replacements = {
                    '<DATE>': datetime.today().strftime('%Y-%m-%d')
                }

                # Extract arguments from additional columns (args_* format)
                for col_name, col_value in row.items():
                    if col_name.startswith('args_'):
                        placeholder_key = col_name[5:]  # Remove 'args_' prefix
                        replacements[f"<{placeholder_key}>"] = col_value

                # Replace placeholders in the SQL file path
                sql_file_path = replace_placeholders(row['sql_file_pth'], replacements)

                # Read the modified SQL content
                with open(sql_file_path, 'r') as f:
                    sql_content = f.read()

                # Execute SQL using DBProvider and capture results
                db_provider = DBProvider()
                results = db_provider.execute_query(sql_content)

                # Generate output filename
                output_filename = generate_output_filename(f"{row['application']}_{row['identifier_name']}")
                output_path = os.path.join("output", output_filename)

                # Save the query results to a CSV file
                save_csv_data(results, output_path, overwrite=True)  # Set overwrite=True

                logger.info(f"Successfully generated CSV: {output_filename}")
            except Exception as e:
                logger.error(f"Error processing row {row}: {e}")

if __name__ == "__main__":
    main()
