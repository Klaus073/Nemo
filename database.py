import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv


class PostgreSQLConnector:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Get database connection parameters from environment variables
        self.db_host = os.getenv("HOST")
        self.db_port = os.getenv("PORT")
        self.db_name = os.getenv("DBNAME")
        self.db_master_user = os.getenv("MASTER_USERNAME")
        self.db_master_password = os.getenv("MASTER_PASSWORD")

        # Initialize connection
        self.conn = self._create_connection()

    def _create_connection(self):
        # Create a connection to the database
        try:
            conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_master_user,
                password=self.db_master_password,
                host=self.db_host,
                port=self.db_port
            )
            print("Connected to PostgreSQL database")
            return conn
        except psycopg2.Error as e:
            print("Error connecting to PostgreSQL database:", e)
            return None

    def is_connected(self):

        return self.conn is not None

    def execute_query(self, query):
        if not self.is_connected():
            print("Not connected to the database.")
            return None

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                print("Query executed successfully")
                return cursor.fetchall()
        # except psycopg2.Error as e:
        #     print("Error executing query:", e)
        #     return None
        # except Exception as e:
        #     raise e
        except psycopg2.Error as e:
            # Get the error message as a string
            error_message = str(e)
            # Print the error message for logging or debugging
            print("Error executing query:", error_message)
            # Return the error message instead of None
            return error_message
        
    async def execute_query1(self, query):
        if not self.is_connected():
            await self.connect()

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                print("Query executed successfully")
                rows = cursor.fetchall()
                return cursor, rows
        except psycopg2.Error as e:
            error_message = str(e)
            print("Error executing query:", error_message)
            return None, error_message

    def list_tables(self):

        if not self.is_connected():
            print("Not connected to the database.")
            return None

        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
                return [table[0] for table in cursor.fetchall()]
        except psycopg2.Error as e:
            print("Error listing tables:", e)
            return None

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("PostgreSQL connection closed")

    def get_user_related_tables(self):
   
        if not self.is_connected():
            print("Not connected to the database.")
            return None

        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT table_name FROM information_schema.columns WHERE column_name = 'UserId';")
                return [table[0] for table in cursor.fetchall()]
        except psycopg2.Error as e:
            print("Error getting user-related tables:", e)
            return None

def table_schemas(file_path):
    

    try:
        with open(file_path, "r") as file:
            db_schema = file.read()
            # print(file_content)
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", e)

    return db_schema

# db =PostgreSQLConnector()
# res = db.execute_query("""SELECT * FROM "AspNetUsers" WHERE "Id" = '52700585-5642-4366-aded-a9896af705b9';""")

# first_name = res[0][1]
# last_name = res[0][2]

# print("First Name:", first_name)
# print("Last Name:", last_name)