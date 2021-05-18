"""Test module for testing revoke_key"""
import unittest
import os

from secure_all import AccessManager, AccessManagementException, \
    JSON_FILES_PATH, KeysJsonStore, RequestJsonStore


class TestRevokeKey(unittest.TestCase):
    """Test class for testing revoke_key"""

    def test_syntax_analysis_tests(self):
        """syntax analysis for json files"""
        # TODO: add files
        # TODO: create keys (setup class?)
        test_cases = JSON_FILES_PATH + "tests_revoke_key/"
        am = AccessManager()
        for json_file in os.listdir(test_cases):
            if json_file[:3] == "ok_" and json_file[-5:] == ".json":
                # json is valid
                self.assertEqual(am.revoke_key(test_cases + json_file), '["mail1@uc3m.es","mail2@uc3m.es"]')
            elif json_file[-5:] == ".json":
                # json is invalid
                with self.assertRaises(AccessManagementException) as c_m:
                    am.revoke_key(test_cases + json_file)
                self.assertEqual(c_m.exception.message, "Incorrect JSON Syntax")

    def test_io_tests(self):
        """input/output tests for json files (equivalent classes)"""
        # TODO
        pass


if __name__ == '__main__':
    unittest.main()
