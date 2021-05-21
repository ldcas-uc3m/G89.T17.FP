"""Test module for testing revoke_key"""

import unittest
import os

from secure_all import AccessManager, AccessManagementException, \
    JSON_FILES_PATH, KeysJsonStore, RequestJsonStore
from secure_all.parser.revoke_key_json_parser import RevokeKeyJsonParser


class TestRevokeKey(unittest.TestCase):
    """Test class for testing revoke_key"""

    @classmethod
    def setUpClass(cls):
        """initialization of test environment"""
        cls.initialize_keys()

    @classmethod
    def initialize_keys(cls):
        """
        Removes the old stored keys and creates a new one to use
        for the test cases.
        """
        # remove the old storeKeys
        requests_store = RequestJsonStore()
        keys_store = KeysJsonStore()
        requests_store.empty_store()
        keys_store.empty_store()
        # introduce a valid key for test_io_tests
        my_manager = AccessManager()
        my_manager.request_access_code("53935158C", "Marta Lopez",
                                       "Resident", "uc3m@gmail.com", 0)
        # access_code: a18a1128ba61da4216c086b710f10237
        my_manager.get_access_key(JSON_FILES_PATH + "valid_key_1.json")
        # key: f4368d997bf77980f12ee673d998c19c2c65397d7e2e7aee87759709776cd66c

    def test_syntax_analysis_tests(self):
        """syntax analysis for json files"""
        test_cases = JSON_FILES_PATH + "tests_revoke_key/"
        am = AccessManager()
        for json_file in os.listdir(test_cases):
            if not json_file.startswith("ok_") and json_file.endswith(".json"):
                # json is invalid
                with self.assertRaises(AccessManagementException) as c_m:
                    am.revoke_key(test_cases + json_file)
                    self.assertEqual(RevokeKeyJsonParser.ERROR_MESSAGE, c_m.exception.message)
            elif json_file.endswith(".json"):
                # Empty the old stored keys and create new ones to ensure the test runs correctly:
                self.initialize_keys()
                email = am.revoke_key(test_cases + json_file)
                self.assertEqual(email, ["mail1@uc3m.es", "mail2@uc3m.es"])


    def test_revoke_key_all_ok_tests(self):
        """i/o test"""
        am = AccessManager()
        self.assertEqual(am.revoke_key(JSON_FILES_PATH + "revoke_key_all_ok.json"),
                         ['mail1@uc3m.es', 'mail2@uc3m.es'])

    def test_revoke_key_wrong_path_tests(self):
        """i/o test"""
        am = AccessManager()
        with self.assertRaises(AccessManagementException) as c_m:
            am.revoke_key(JSON_FILES_PATH + "revoke_key_wrong_path.json")
        self.assertEqual(c_m.exception.message, "Wrong file or file path")

    def test_revoke_key_boolean_path_tests(self):
        """i/o test"""
        am = AccessManager()
        with self.assertRaises(AccessManagementException) as c_m:
            am.revoke_key(True)
        self.assertEqual(c_m.exception.message, "Incorrect JSON path")

    def test_revoke_key_null_path_tests(self):
        """i/o test"""
        am = AccessManager()
        with self.assertRaises(AccessManagementException) as c_m:
            am.revoke_key(None)
        self.assertEqual(c_m.exception.message, "Incorrect JSON path")

    def test_revoke_key_empty_path_tests(self):
        """i/o test"""
        am = AccessManager()
        with self.assertRaises(AccessManagementException) as c_m:
            am.revoke_key("")
        self.assertEqual(c_m.exception.message, "Wrong file or file path")

    def test_revoke_key_integer_path_tests(self):
        """i/o test"""
        am = AccessManager()
        with self.assertRaises(AccessManagementException) as c_m:
            am.revoke_key(420)
        self.assertEqual(c_m.exception.message, "Incorrect JSON path")


if __name__ == '__main__':
    unittest.main()
