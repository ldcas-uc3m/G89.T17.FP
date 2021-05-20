"""Test module for testing store_access_log"""
import json
import os
import stat
import unittest

from secure_all import (JSON_FILES_PATH, AccessLog, AccessLogStore,
                        AccessManagementException, AccessManager,
                        KeysJsonStore, RequestJsonStore)



class TestStoreAccessLog(unittest.TestCase):
    """Test class for testing store_access_log"""
 
    @classmethod
    def setUpClass(cls):
        """initialization of test environment"""
        requests_store = RequestJsonStore()
        keys_store = KeysJsonStore()
        requests_store.empty_store()
        keys_store.empty_store()

        # introduce a valid key
        my_manager = AccessManager()
        my_manager.request_access_code("53935158C", "Marta Lopez",
                                       "Resident", "uc3m@gmail.com", 0)
        # access_code: a18a1128ba61da4216c086b710f10237
        cls.key = my_manager.get_access_key(JSON_FILES_PATH + "valid_key_1.json")
        # key: f4368d997bf77980f12ee673d998c19c2c65397d7e2e7aee87759709776cd66c

    def setUp(self):
        """
        Ensures that the Access log file exists and is empty before each test.
        """
        log_store = AccessLogStore()
        log_store.empty_store()

    def test_store_access_log_not_exists_write_error(self):
        """
        Forces an os error when writing to the access log file
        by changing the permissions to the file.
        """
        am = AccessManager()
        # Save original permissions to access log file:
        access_log_fp = AccessLogStore.get_file_path()
        original_status = os.stat(access_log_fp).st_mode
        try:
            # Remove write permissions to access log file:
            os.chmod(access_log_fp, stat.S_IREAD)
            with self.assertRaises(AccessManagementException) as c_m:
                am.open_door(self.key)
            self.assertEqual(c_m.exception.message, AccessLog.WRITE_FILE_ERROR)
        finally:
            # Ensure the original file permissions are restored:
            os.chmod(access_log_fp, original_status)


    def test_store_access_log_not_exists_create_error(self):
        """
        Checks that there's a JSON Decode Error when reading the
        access log JSON file that has been edited with a wrong format.
        """
        am = AccessManager()
        # Edit storeAccessLogs so it does not have any JSON contents:
        with open((AccessLogStore.get_file_path()),"w") as f:
            f.write(":D I'm not Json Encoded HAHA :D !!")

        with self.assertRaises(AccessManagementException) as c_m:
            am.open_door(self.key)

        self.assertEqual(c_m.exception.message, "JSON Decode Error - Wrong JSON Format")

    def test_store_access_log_not_exists_ok(self):
        """
        Checks that creates the JSON log file since it does
        not exist and adds a new record to the logs
        """
        am = AccessManager()
        # Ensure that Access Log does not exist:
        if os.path.exists(AccessLogStore.get_file_path()):
            os.remove(AccessLogStore.get_file_path())
        am.open_door(self.key)
        # Check that Access Log exists and key was inserted:
        with open(AccessLogStore.get_file_path(), "r") as f:
            access_log = json.load(f)
        self.assertEqual(len(access_log), 1)
        # Check that the key contains the key and the timestamp:
        for item in access_log:
            if not isinstance(item, dict):
                self.fail(
                    "Items in access log are supposed to be objects "
                    "that resolve to python dictionaries."
                )
            if not set(["key","timestamp"]).issubset(item.keys()):
                self.fail("Items in the access logs should contain a 'key' and a 'timestamp'")
        # Check that the key value is correct:
        self.assertEqual(access_log[0]["key"], self.key)

    def test_store_access_log_exists_ok(self):
        """
        Checks that reads JSON log file that already exists
        and adds the new log record to it.
        """
        am = AccessManager()
        # Check that Access Log file exists and is empty:
        log_store = AccessLogStore()
        log_store.empty_store()
        am.open_door(self.key)
        # Check that Access Log file exists and read it:
        with open(AccessLogStore.get_file_path(), "r") as f:
            access_log = json.load(f)
        # Check that the key was inserted:
        self.assertEqual(len(access_log), 1)
        # Check that the key contains the key and the timestamp:
        for item in access_log:
            if not isinstance(item, dict):
                self.fail(
                    "Items in access log are supposed to be objects "
                    "that resolve to python dictionaries."
                )
            if not set(["key","timestamp"]).issubset(item.keys()):
                self.fail("Items in the access logs should contain a 'key' and a 'timestamp'")
        # Check that the key value is correct:
        self.assertEqual(access_log[0]["key"], self.key)


if __name__ == '__main__':
    unittest.main()
