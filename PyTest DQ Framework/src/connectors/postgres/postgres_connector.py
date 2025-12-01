
import psycopg2
import psycopg2.extras
import pandas as pd

class PostgresConnectorContextManager:
    def __init__(self, db_host: str, db_name: str, db_port: int, db_user:str, db_password: str ):
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.db_port = db_port
        self.db_host = db_host

    def __enter__(self):
        # create connection
        try:
            self.connection = psycopg2.connect(user=self.db_user,
                                               password = self.db_password,
                                               host = self.db_host,
                                               database = self.db_name,
                                               port = self.db_port
                                               )
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            return self
        except Exception as e:
            raise Exception (f"Unable to connect to PostreSQL: {e}")

    def __exit__(self, exc_type, exc_value, exc_tb):
        # close conn
        """Closing the connection """
        try:
            if self.cursor:
                self.cursor.close()
            if self.cursor.connection:
                self.connection.close()
        except Exception as e:
            print(f"DB connection failed to close: {e}")

    def get_data_sql(self, sql):
        # exec query, result = pandas df
        """Execute SQL query to get pandas dataframe"""
        if not self.cursor:
            raise Exception("Unable to established connection with the DB ")

        try:
            self.cursor.execute(sql)
            #getting the column names
            columns = [desc[0] for desc in self.cursor.description]

            results = self.cursor.fetchall()

            #convert to pandas df
            df = pd.DataFrame(results,columns=columns)
            return df
        except Exception as e:
            raise Exception(f"Failed to execute SQL query {e}")

