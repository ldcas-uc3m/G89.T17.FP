"""Module AccessManager with AccessManager Class """
import secure_all
from secure_all.data.access_key import AccessKey
from secure_all.data.access_request import AccessRequest


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
            """Returns the access key for the access code & dni received in a json file"""
            my_key = AccessKey.create_key_from_file(keyfile)
            my_key.store_keys()
            return my_key.key

        @staticmethod
        def open_door(key):
            """Opens the door if the key is valid an it is not expired"""
            return AccessKey.create_key_from_id(key).is_valid()

        @staticmethod
        def validate_file_path(file_path):
            if file_path is None:
                raise secure_all.AccessManagementException("Incorrect JSON path")
            if not isinstance(file_path, str):
                raise secure_all.AccessManagementException("Incorrect JSON path")
            if not file_path:
                raise secure_all.AccessManagementException("Incorrect JSON path")

            return

        def revoke_key(self, file_path):
           self.validate_file_path(file_path)
           return
            # TODO

        def store_access_log(self):
            pass
            # TODO

    __instance = None

    def __new__(cls):
        if not AccessManager.__instance:
            AccessManager.__instance = AccessManager.__AccessManager()
        return AccessManager.__instance
