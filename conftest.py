import os
import re
import logging
import utils.db_utils as db
from utils.constants import FrameConstants, NameConstants


def pytest_sessionstart():
    """Pytest hook to do actions before starting test session"""
    parse_load_data()


def pytest_sessionfinish():
    """Pytest hook to do actions before finishing tests session"""
    logging.info('Clear database')
    db.clear_table()


def parse_load_data():
    """Extracts test data from work log"""
    logging.info('Extraction of data from log file')
    root_path = os.path.dirname(__file__)
    log_file = os.path.join(root_path, 'data', 'test_source', NameConstants.work_log_file.value)
    if os.path.exists(log_file):
        connection = db.create_connection()
        db.execute_query(connection, db.CREATE_TABLE)
        with open(log_file) as log:
            parsed_log_file = []
            for i in log:
                data = re.findall(FrameConstants.parsing_expression.value, i)
                parsed_log_file.append((data[0][0], data[0][2], data[0][3], data[0][5]))
        logging.info('Load data to database')
        db.executemany_query(connection, db.INSERT_LOG_DATA, parsed_log_file)
        connection.close()
