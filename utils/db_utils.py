import logging
import sqlite3
from sqlite3 import Error
from utils.constants import data_base_name

CREATE_TABLE = """CREATE TABLE IF NOT EXISTS work_log
(time TEXT NOT NULL, action TEXT NOT NULL, name TEXT NOT NULL, type TEXT NOT NULL);"""
DELETE_TABLE = """DELETE FROM work_log;"""
SELECT_DATA = """SELECT {} from work_log WHERE name='{}';"""
SELECT_DISTINCT_DATA = """SELECT DISTINCT name from work_log WHERE type='{}';"""
INSERT_LOG_DATA = """INSERT INTO `work_log` VALUES (?,?,?,?);"""


def executemany_query(connection, query, values):
    cursor = connection.cursor()
    try:
        cursor.executemany(query, values)
        connection.commit()
        logging.debug(f"Query executed successfully: {query}")
    except Error as e:
        logging.error(f"The error '{e}' occurred")


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        logging.debug(f"Query executed successfully: {query}")
    except Error as e:
        logging.error(f"The error '{e}' occurred")


def create_connection(path=data_base_name):
    connection = None
    try:
        connection = sqlite3.connect(path)
        logging.debug("\nConnection to SQLite DB successful")
    except Error as e:
        logging.error(f"The error '{e}' occurred")
    return connection


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        logging.debug(f"Query executed successfully: {query}")
        return result
    except Error as e:
        logging.error(f"The error '{e}' occurred")


def __format_results(incoming_data):
    result_list = []
    for i in incoming_data:
        result_list.append(i[0])
    return result_list


def get_unique_files_by_type(file_type):
    connection = create_connection()
    query = SELECT_DISTINCT_DATA.format(file_type)
    result = execute_read_query(connection, query)
    connection.close()
    records = __format_results(result)
    return records


def clear_table():
    connection = create_connection()
    execute_query(connection, DELETE_TABLE)
    connection.close()

