"""Test module for testing revoke_key"""
import json
import unittest
import os

from secure_all import AccessManager, AccessManagementException, \
    JSON_FILES_PATH, KeysJsonStore, RequestJsonStore


class TestRevokeKey(unittest.TestCase):
    """Test class for testing revoke_key"""

    @classmethod
    def setUpClass(cls):
        """initialization of test environment"""
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
       #my_manager.get_access_key(JSON_FILES_PATH + "valid_key_1.json")
        # key: f4368d997bf77980f12ee673d998c19c2c65397d7e2e7aee87759709776cd66c

    def test_syntax_analysis_tests(self):
        """syntax analysis for json files"""
        test_cases = JSON_FILES_PATH + "tests_revoke_key/"
        am = AccessManager()
        for json_file in os.listdir(test_cases):
            if not json_file[:3] == "ok_" and json_file[-5:] == ".json":
                # json is invalid
                with self.assertRaises(AccessManagementException) as c_m:
                    am.revoke_key(test_cases + json_file)
                self.assertEqual(c_m.exception.message, "Incorrect JSON Syntax")
            if json_file[:3] == "ok_" and json_file[-5:] == ".json":
                with open(test_cases + json_file, "r") as f:
                    contents = f.read()
                    input_data = json.loads(contents)
                with self.assertRaises(AccessManagementException) as c_m:
                    self.assertEqual(am.revoke_key(test_cases + json_file), input_data["NotificationMail"])


    # i/o tests

    # i/o tests

    def test_revoke_key_all_ok_tests(self):
        test_cases = JSON_FILES_PATH
        am = AccessManager()
        self.assertEqual(am.revoke_key(JSON_FILES_PATH + "valid_key_1.json"),
                         ['mail1@uc3m.es', 'mail2@uc3m.es'])

    def test_revoke_key_wrong_path_tests(self):
        am = AccessManager()
        with self.assertRaises(AccessManagementException) as c_m:
            am.revoke_key(JSON_FILES_PATH + "revoke_key_wrong_path.json")
        self.assertEqual(c_m.exception.message, "Incorrect JSON path")
        pass

    def test_revoke_key_boolean_path_tests(self):
        am = AccessManager()
        with self.assertRaises(AccessManagementException) as c_m:
            am.revoke_key(True)
        self.assertEqual(c_m.exception.message, "Incorrect JSON path")

    def test_revoke_key_null_path_tests(self):
        am = AccessManager()
        with self.assertRaises(AccessManagementException) as c_m:
            am.revoke_key(None)
        self.assertEqual(c_m.exception.message, "Incorrect JSON path")

    def test_revoke_key_empty_path_tests(self):
        am = AccessManager()
        with self.assertRaises(AccessManagementException) as c_m:
            am.revoke_key("")
        self.assertEqual(c_m.exception.message, "Incorrect JSON path")

    def test_revoke_key_integer_path_tests(self):
        am = AccessManager()
        with self.assertRaises(AccessManagementException) as c_m:
            am.revoke_key(420)
        self.assertEqual(c_m.exception.message, "Incorrect JSON path")

    def test_revoke_key_save_request_duplicate_tests(self):
        am = AccessManager()
        with self.assertRaises(AccessManagementException) as c_m:
            am.revoke_key(JSON_FILES_PATH + "valid_key_1.json")
        self.assertEqual(c_m.exception.message, "Key already revoked")


if __name__ == '__main__':
    unittest.main()
