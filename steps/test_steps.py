import logging

import allure
from delayed_assert import delayed_assert
import utils.db_utils as db


class TestSteps:

    @allure.step('Extract data for file')
    def get_data_for_file(self, file_name):
        connection = db.create_connection()
        records = db.execute_read_query(connection, db.SELECT_DATA.format("*", file_name))
        connection.close()
        return records

    def _find_record_with_action(self, results, action):
        for i in results:
            if i[1] == action:
                return True
        return False

    @allure.step('Verify clean file')
    def verify_clean_files(self, results):
        file_name = results[0][2]
        logging.info(f"List of validation for 'Clean' files:")

        message_1 = f"Validate there is at least 2 records for the file"
        with allure.step(message_1):
            logging.info(message_1)
            delayed_assert.expect(len(results) >= 2, f"There is not less than 2 records for Clean the file {file_name}")

        message_2 = f"Validate the first action for file is ADDED"
        with allure.step(message_2):
            logging.info(message_2)
            delayed_assert.expect(results[0][1] == 'ADDED', f"First action is not ADDED for the file {file_name}")

        message_3 = f"Validate the second action for file is CLEAN"
        with allure.step(message_3):
            logging.info(message_3)
            delayed_assert.expect(results[1][1] == 'CLEAN', f"Second action is not CLEAN for the file {file_name}")

        message_4 = f"Validate the file is not removed"
        with allure.step(message_4):
            logging.info(message_4)
            find_removed_action = self._find_record_with_action(results, 'REMOVED')
            delayed_assert.expect(find_removed_action is False, f"Clean file {file_name} should not be removed")

        message_5 = f"Validate the file does not have error action\n"
        with allure.step(message_5):
            logging.info(message_5)
            find_error_action = self._find_record_with_action(results, 'ERROR')
            delayed_assert.expect(find_error_action is False, f"Clean file {file_name} should not have ERROR action")

        delayed_assert.assert_expectations()

    @allure.step('Verify dirty file')
    def verify_dirty_files(self, results):
        file_name = results[0][2]
        logging.info(f"List of validation for 'Dirty' files:")

        message_1 = f"Validate there is at least 3 records for the file"
        with allure.step(message_1):
            logging.info(message_1)
            delayed_assert.expect(len(results) >= 3, f"There not less 3 records for the file {file_name}")

        message_2 = f"Validate the first action for file is ADDED"
        with allure.step(message_2):
            logging.info(message_2)
            delayed_assert.expect(results[0][1] == 'ADDED', f"First action is not ADDED for file {file_name}")

        message_3 = f"Validate the second action for file is DIRTY"
        with allure.step(message_3):
            logging.info(message_3)
            delayed_assert.expect(results[1][1] == 'DIRTY', f"Second action is not DIRTY for file {file_name}")

        message_4 = f"Validate the file is removed"
        with allure.step(message_4):
            logging.info(message_4)
            find_removed_action = self._find_record_with_action(results, 'REMOVED')
            delayed_assert.expect(find_removed_action is True, f"Dirty file {file_name} should be removed")

        message_5 = f"Validate the file does not have error action\n"
        with allure.step(message_5):
            logging.info(message_5)
            find_error_action = self._find_record_with_action(results, 'ERROR')
            delayed_assert.expect(find_error_action is False, f"Dirty file {file_name} should not have ERROR action")

        delayed_assert.assert_expectations()
