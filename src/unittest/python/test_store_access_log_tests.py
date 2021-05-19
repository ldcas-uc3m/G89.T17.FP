"""Test module for testing store_access_log"""
import unittest

from secure_all import AccessManager, AccessManagementException, \
    JSON_FILES_PATH, KeysJsonStore, RequestJsonStore, AccessLogStore

import os
import json

class TestStoreAccessLog(unittest.TestCase):
    """Test class for testing store_access_log"""

    @classmethod
    def setUpClass(cls):
        """initialization of test environment"""
        requests_store = RequestJsonStore()
        keys_store = KeysJsonStore()
        requests_store.empty_store()
        keys_store.empty_store()
        cls.log_store = AccessLogStore()
        cls.log_store.empty_store()

        # introduce a valid key
        my_manager = AccessManager()
        my_manager.request_access_code("53935158C", "Marta Lopez",
                                       "Resident", "uc3m@gmail.com", 0)
        # access_code: a18a1128ba61da4216c086b710f10237
        cls.key = my_manager.get_access_key(JSON_FILES_PATH + "valid_key_1.json")
        # key: f4368d997bf77980f12ee673d998c19c2c65397d7e2e7aee87759709776cd66c

    # TODO: test cases
    def test_store_access_log_not_exists_create_error(self):
        # Skip test since can't force a create error:
        self.SkipTest()
        """
        am = AccessManager()
        with self.assertRaises(AccessManagementException) as c_m:
            am.open_door(self.key)
        
        self.assertEqual(c_m.exception.message, "Unable to create file storeAccessLogs.json")
        """

    def test_store_access_log_not_exists_write_error(self):
        
        # Skip test since can't force a write error:
        self.SkipTest()
        """
        am = AccessManager()
        with self.assertRaises(AccessManagementException) as c_m:
            am.open_door(self.key)
        
        self.assertEqual(c_m.exception.message, "Unable to write to file storeAccessLogs.json")
        """

    def test_store_access_log_not_exists_create_error(self):
        """
        Checks that there's a JSON Decode Error when reading the
        access log JSON file that has been edited with a wrong format.
        """
        am = AccessManager()
        # Edit storeAccessLogs so it does not have any JSON contents:
        with open((JSON_FILES_PATH + "storeAccessLogs.json"),"w") as f:
            f.write(":D I'm not Json Encoded HAHA :D !!")

        with self.assertRaises(AccessManagementException) as c_m:
            am.open_door(self.key)
        
        self.assertEqual(c_m.exception.message, "Unable to read file storeAccessLogs.json, is not JSON encoded")
    
    def test_store_access_log_not_exists_ok(self):
        am = AccessManager()
        # Check that Access Log does not exist:
        if os.path.exists(JSON_FILES_PATH + "storeAccessLogs.json"):
            os.remove(JSON_FILES_PATH + "storeAccessLogs.json")
        am.open_door(self.key)
        # Check that Access Log exists and key was inserted:
        with open(JSON_FILES_PATH + "storeAccessLogs.json", "r") as f:
            access_log = json.load(f)
            self.assertEqual(len(access_log), 1)
    
    def test_store_access_log_exists_ok(self):
        am = AccessManager()
        # Check that Access Log file exists and is empty:
        self.log_store.empty_store()
        am.open_door(self.key)
        # Check that Access Log exists and key was inserted:
        with open(JSON_FILES_PATH + "storeAccessLogs.json", "r") as f:
            access_log = json.load(f)
            self.assertEqual(len(access_log), 1)


if __name__ == '__main__':
    unittest.main()
