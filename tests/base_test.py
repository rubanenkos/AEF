import utils.db_utils as db


class BaseTest:

    @staticmethod
    def get_workfiles(file_type):
        records = db.get_unique_files_by_type(file_type)
        return records
