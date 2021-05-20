"""Module AccessManager with AccessManager Class """

from secure_all.data.access_key import AccessKey
from secure_all.data.access_request import AccessRequest
from secure_all.data.access_log import AccessLog
from secure_all.storage.keys_json_store import KeysJsonStore
from secure_all.parser.revoke_key_json_parser import RevokeKeyJsonParser
from secure_all.exception.access_management_exception import AccessManagementException


class AccessManager:
    """AccessManager class, manages the access to a building implementing singleton """

    class __AccessManager:
        """Class for providing the methods for managing the access to a building"""

        @staticmethod
        def request_access_code(id_card, name_surname, access_type, email_address, days):
            """ this method give access to the building"""
            my_request = AccessRequest(id_card, name_surname, access_type, email_address, days)
            my_request.store_request()
            return my_request.access_code

        @staticmethod
        def get_access_key(keyfile):
            """Returns the access key for the access code received in a json file"""
            my_key = AccessKey.create_key_from_file(keyfile)
            my_key.store_keys()
            return my_key.key

        @staticmethod
        def open_door(key):
            """Opens the door if the key is valid an it is not expired"""
            access_key = AccessKey.create_key_from_id(key)
            key_valid = access_key.is_valid()
            if key_valid:
                log = AccessLog(access_key)
                log.store_access_log()
            return key_valid

        @staticmethod
        def revoke_key(file_path):
            """Revokes a key given a json file doc"""
            if not isinstance(file_path, str):
                raise AccessManagementException("Incorrect JSON path")

            parser = RevokeKeyJsonParser(file_path)
            key_store = KeysJsonStore()
            key = key_store.find_item(parser.json_content["Key"])

            if key is None:
                raise AccessManagementException("JSON Decode Error - Wrong JSON Format")
            emails = key["_AccessKey__notification_emails"]
            key_store.remove_item(parser.json_content["Key"])

            return emails

    __instance = None

    def __new__(cls):
        if not AccessManager.__instance:
            AccessManager.__instance = AccessManager.__AccessManager()
        return AccessManager.__instance
