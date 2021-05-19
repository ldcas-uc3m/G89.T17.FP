"""Test module for testing store_access_log"""
import unittest

from secure_all import AccessManager, AccessManagementException, \
    JSON_FILES_PATH, KeysJsonStore, RequestJsonStore


class TestStoreAccessLog(unittest.TestCase):
    """Test class for testing store_access_log"""

    @classmethod
    def setUpClass(cls):
        """initialization of test environment"""
        requests_store = RequestJsonStore()
        requests_store.empty_store()

    # TODO: test cases

if __name__ == '__main__':
    unittest.main()
