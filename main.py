import pyodbc
import os

# Get database credentials from environment variables
db_name = os.environ.get("DB_NAME", "test_imis")
db_user = os.environ.get("DB_USER", "sa")
db_password = os.environ.get("DB_PASSWORD", "Centric@11")
# Replace with your SQL server
db_server = os.environ.get("DB_SERVER", "localhost")

# SQL scripts Base
full_demo_databases = "./sql/fullDemoDatabases.sql"
demo_online_sql = "./sql/1_demo_online.sql"


class SQLScriptRunner:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.conn = None
        self.cursor = None

    def connect(self):
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
        self.conn = pyodbc.connect(conn_str)
        self.cursor = self.conn.cursor()

    def execute_script(self, script_path):
        with open(script_path, 'r') as file:
            sql_script = file.read()
            sql_commands = sql_script.split("GO")  # Split script at "GO"
            for command in sql_commands:
                try:
                    self.cursor.execute(command)
                except pyodbc.DatabaseError as e:
                    print(
                        f"Error executing SQL command: {command}\nError: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
                else:
                    self.conn.commit()

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


class Main:
    def __init__(self):
        self.runner = SQLScriptRunner(
            server=db_server, database=db_name, username=db_user, password=db_password)

        self.execute_demo_database_scripts()
        self.execute_demo_online_scripts()

    def execute_demo_database_scripts(self):
        try:
            print("Executing demo database scripts...")
            self.runner.connect()
            self.runner.execute_script(full_demo_databases)
        except Exception as e:
            print("Error executing demo database scripts", e)
        finally:
            print("Closing connection...")
            self.runner.close_connection()

    def execute_demo_online_scripts(self):
        try:
            print("Executing demo database online scripts...")
            self.runner.connect()
            self.runner.execute_script(demo_online_sql)
        except Exception as e:
            print("Error executing demo database online scripts", e)
        finally:
            print("Closing connection...")
            self.runner.close_connection()


def __main__():
    main = Main()


if __name__ == "__main__":
    __main__()
