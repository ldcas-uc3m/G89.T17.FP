"""Implements the RequestsJSON Store"""
from secure_all.storage.json_store import JsonStore
from secure_all.exception.access_management_exception import AccessManagementException
from secure_all.cfg.access_manager_config import JSON_FILES_PATH


class AccessLogStore:
    """
    Extends JsonStore to implement the storing of
    the access logs when the door is opened
    """
    class __AccessLogStore(JsonStore):

        INVALID_ITEM_ERROR = (
            "Invalid item to be stored as an access log, "
            "must be an access_log.AccessLog instance"
        )

        ITEM_ALREADY_STORED = (
            "An item with the same timestamp and key is already stored in the logs."
        )

        FILE_PATH = JSON_FILES_PATH + "storeAccessLogs.json"

        _FILE_PATH = FILE_PATH

        def add_item(self, item):
            """
            Adds an item to the access log storage.
            Implements the restrictions related to avoid duplicated access logs
            """
            from secure_all.data.access_log import AccessLog

            if not isinstance(item, AccessLog):
                raise AccessManagementException(self.INVALID_ITEM_ERROR)

            if not self.find_item(item) is None:
                raise AccessManagementException(self.ITEM_ALREADY_STORED)

            return super().add_item(item)

        def find_item(self, key:dict):
            """
            Find an object in the access logs storage
            that is equal to the dictionary given.
            """
            self.load_store()
            for list_item in self._data_list:
                if list_item == key:
                    return list_item
            return None

    @classmethod
    def get_file_path(cls):
        """
        Returns the file path used format_control the AccessLogStore
        """
        return AccessLogStore.__AccessLogStore.FILE_PATH

    __instance = None

    def __new__(cls):
        if not AccessLogStore.__instance:
            AccessLogStore.__instance = AccessLogStore.__AccessLogStore()
        # Add file path class attribute from inner class:
        return AccessLogStore.__instance

    def __getattr__(self, name):
        return getattr(self.__instance, name)

    def __setattr__ (self, name, value):
        return setattr(self.__instance, name, value)
