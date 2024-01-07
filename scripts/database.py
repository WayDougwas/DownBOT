import sqlite3
from sqlite3 import Error

DATABASE_FILE = "bot_database.db"

def create_connection():
    connection = None
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        print(f"Connected to SQLite database ({DATABASE_FILE})")
        return connection
    except Error as e:
        print(f"Error connecting to SQLite database: {e}")
        raise e

def execute_query(connection, query, data=None):
    try:
        cursor = connection.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        return cursor
    except Error as e:
        print(e)
        raise e

def create_table():
    connection = create_connection()
    if connection is not None:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS server_settings (
            server_id INTEGER PRIMARY KEY,
            prefix TEXT NOT NULL
        );
        """
        execute_query(connection, create_table_query)
        connection.close()

def get_prefix(server_id):
    connection = create_connection()
    create_table()  # Ensure the table is created
    if connection is not None:
        select_query = "SELECT prefix FROM server_settings WHERE server_id = ?;"
        data = (server_id,)
        cursor = execute_query(connection, select_query, data)
        if cursor:
            result = cursor.fetchone()
            if result:
                return str(result[0])
        connection.close()
    return "!"

def set_prefix(server_id, prefix):
    connection = create_connection()
    create_table()  # Ensure the table is created
    if connection is not None:
        insert_query = "INSERT OR REPLACE INTO server_settings (server_id, prefix) VALUES (?, ?);"
        data = (server_id, prefix)
        execute_query(connection, insert_query, data)
        connection.close()
