import utils.db_utils as db


class BaseTest:
    """Base class for test classes"""

    @staticmethod
    def get_workfiles(file_type):
        """Gets testing data for parameterization tests"""
        records = db.get_unique_files_by_type(file_type)
        return records
