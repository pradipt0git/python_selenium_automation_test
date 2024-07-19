import nzpy
import configparser
from core.utils import create_day_log_file, get_logger


class DBProvider:
    """
    Abstract base class for database providers, enabling easy switching between databases.
    """

    def __init__(self, config_file='config.ini', config_section='netezza'):
        """
        Initializes the database connection using configuration details.

        Args:
            config_file (str, optional): Path to the configuration file. Defaults to 'config.ini'.
            config_section (str, optional): Configuration section within the file. Defaults to 'netezza'.
        """

        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.connection = None
        self.logger = get_logger(create_day_log_file())  # Create logger for this instance


        self._connect()

    def _connect(self):
        """
        Establishes a connection to the database using configuration details.

        Raises:
            ConnectionError: If connection fails.
        """

        try:
            credentials = self.config[self.config_section]
            self.connection = nzpy.connect(
                host=credentials['host'],
                port=int(credentials['port']),
                user=credentials['user'],
                password=credentials['password'],
                database=credentials['database']
            )
        except (configparser.NoOptionError, configparser.NoSectionError) as e:
            self.logger.error(f"Error connecting to Netezza: Missing configuration: {e}")
            raise ConnectionError(f"Error connecting to Netezza: Missing configuration: {e}")
        except nzpy.Error as e:
            self.logger.error(f"Error connecting to Netezza: {e}")
            raise ConnectionError(f"Error connecting to Netezza: {e}") from e

    def close_connection(self):
        """
        Closes the database connection if open.
        """

        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, fetch_all=True):
        """
        Executes a SQL query against the database.

        Args:
            query (str): The SQL query to execute.
            fetch_all (bool, optional): Whether to fetch all results at once (True) or a cursor (False). Defaults to True.

        Returns:
            list or nzpy.Cursor: The query results or a cursor depending on the `fetch_all` parameter.
        """

        cursor = self.connection.cursor()
        cursor.execute(query)

        if fetch_all:
            return cursor.fetchall()
        else:
            return cursor

    def execute_dml(self, query):
        """
        Executes a data manipulation language (DML) statement against the database.

        Args:
            query (str): The DML statement to execute (e.g., INSERT, UPDATE, DELETE).

        Returns:
            None
        """

        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    # Add other database interaction functions as needed...

    def __enter__(self):
        """
        Context manager support for automatic connection acquisition.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager support for automatic connection closing on exit.
        """
        self.close_connection()
