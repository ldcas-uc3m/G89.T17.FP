"""Implements the RequestsJSON Store"""
from secure_all.storage.json_store import JsonStore
from secure_all.exception.access_management_exception import AccessManagementException
from secure_all.cfg.access_manager_config import JSON_FILES_PATH


class AccessLogStore:
    """Extends JsonStore """
    class __AccessLogStore(JsonStore):

        ID_FIELD = "_AccessLog__log"
        _FILE_PATH = JSON_FILES_PATH + "storeAccessLogs.json"
        _ID_FIELD = ID_FIELD

    __instance = None

    def __new__(cls):
        if not AccessLogStore.__instance:
            AccessLogStore.__instance = AccessLogStore.__AccessLogStore()
        return AccessLogStore.__instance

    def __getattr__(self, name):
        return getattr(self.__instance, name)

    def __setattr__ (self, name, value):
        return setattr(self.__instance, name, value)
