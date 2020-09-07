import logging
import sqlite3
from sqlite3 import Error
from utils.constants import NameConstants

WORK_TABLE = NameConstants.work_table_name.value
CREATE_TABLE = """CREATE TABLE IF NOT EXISTS {}
(time TEXT NOT NULL, action TEXT NOT NULL, name TEXT NOT NULL, type TEXT NOT NULL);""".format(WORK_TABLE)
DELETE_TABLE = """DELETE FROM {};""".format(WORK_TABLE)
SELECT_DATA = """SELECT {} from """ + WORK_TABLE + """ WHERE name='{}';"""
SELECT_DISTINCT_DATA = """SELECT DISTINCT name from """ + WORK_TABLE + """ WHERE type='{}';"""
INSERT_LOG_DATA = """INSERT INTO {} VALUES (?,?,?,?);""".format(WORK_TABLE)


def executemany_query(connection, query, values):
    """Execute query with multiple rows at once"""
    cursor = connection.cursor()
    try:
        cursor.executemany(query, values)
        connection.commit()
        logging.debug(f"Query executed successfully: {query}")
    except Error as e:
        logging.error(f"The error '{e}' occurred")


def execute_query(connection, query):
    """Execute query with one rows at once"""
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        logging.debug(f"Query executed successfully: {query}")
    except Error as e:
        logging.error(f"The error '{e}' occurred")


def create_connection(path=NameConstants.data_base_name.value):
    """Create DataBase connection"""
    connection = None
    try:
        connection = sqlite3.connect(path)
        logging.debug("\nConnection to SQLite DB successful")
    except Error as e:
        logging.error(f"The error '{e}' occurred")
    return connection


def execute_read_query(connection, query):
    """Fetches all rows of a query result, returning a list"""
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        logging.debug(f"Query executed successfully: {query}")
        return result
    except Error as e:
        logging.error(f"The error '{e}' occurred")


def __format_results(incoming_data, serial_number=0):
    """Retrives elements from incoming data by serial number"""
    result_list = []
    for i in incoming_data:
        result_list.append(i[serial_number])
    return result_list


def get_unique_files_by_type(file_type):
    """Gets unique file"""
    connection = create_connection()
    query = SELECT_DISTINCT_DATA.format(file_type)
    result = execute_read_query(connection, query)
    connection.close()
    records = __format_results(result)
    return records


def clear_table():
    """Clear work table"""
    connection = create_connection()
    execute_query(connection, DELETE_TABLE)
    connection.close()

