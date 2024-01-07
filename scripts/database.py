import os
import sqlite3
from sqlite3 import Error

DATABASE_FOLDER = ".data"
DATABASE_FILE = "bot_database.db"
DATABASE_PATH = os.path.join(DATABASE_FOLDER, DATABASE_FILE)

def create_connection():
    try:
        os.makedirs(DATABASE_FOLDER, exist_ok=True)  # Cria a pasta se não existir
        connection = sqlite3.connect(DATABASE_PATH)
        print(f"Connected to SQLite database ({DATABASE_PATH})")
        return connection
    except Error as e:
        print(f"Error connecting to SQLite database: {e}")
        raise e

def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
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
        try:
            execute_query(connection, create_table_query)
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
            raise e
        finally:
            connection.close()

def get_prefix(bot, message):
    server_id = message.guild.id if message.guild else None
    connection = create_connection()
    create_table()  # Ensure the table is created
    if connection is not None and server_id is not None:
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
