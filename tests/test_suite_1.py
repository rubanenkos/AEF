import pytest
import logging

from steps.test_steps import TestSteps
from tests.base_test import BaseTest


@pytest.mark.suite1
class TestSuite1(BaseTest):
    """Test suite #1"""

    @pytest.mark.clean
    @pytest.mark.parametrize("file_name", [*BaseTest.get_workfiles('clean')])
    def test_validate_clean_files(self, file_name):
        """Test for express verification 'Clean' files"""
        logging.info(f"Start test for file: {file_name}")
        flow = TestSteps()
        results = flow.get_data_for_file(file_name)
        flow.verify_clean_files(results)

    @pytest.mark.dirty
    @pytest.mark.parametrize("file_name", [*BaseTest.get_workfiles('dirty')])
    def test_validate_dirty_files(self, file_name):
        """Test for express verification 'Dirty' files"""
        logging.info(f"Start test for file: {file_name}")
        flow = TestSteps()
        results = flow.get_data_for_file(file_name)
        flow.verify_dirty_files(results)
