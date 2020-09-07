from enum import Enum


class FrameConstants(Enum):
    """Stores the value for common project definitions"""
    parsing_expression = r'(\d{13})(::!(.+)!::/.*)((\w{8}-\w{4}-\w{4}-\w{4}-\w{12,}.)(dirty$|clean$))'


class NameConstants(Enum):
    """Stores the names for project entities"""
    data_base_name = "work_base.db"
    work_table_name = "work_table"
    work_log_file = "work.log"
