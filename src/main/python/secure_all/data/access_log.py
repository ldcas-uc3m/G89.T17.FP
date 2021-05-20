from datetime import datetime

from secure_all import AccessKey
from secure_all.exception.access_management_exception import \
    AccessManagementException
from secure_all.storage.access_log_store import AccessLogStore


class AccessLog:
    """Class representing an access log to the building"""

    WRITE_FILE_ERROR = f"Unable to write to file '{AccessLogStore.get_file_path()}'"

    def __init__(self, access_key:AccessKey):
        self.key = access_key.key
        self.timestamp = datetime.utcnow().timestamp()

    def store_access_log(self):
        """Stores the data of the current item in the log file."""
        access_log_store = AccessLogStore()
        try:
            access_log_store.add_item(self)
        except OSError as e:
            raise AccessManagementException(
                self.WRITE_FILE_ERROR
            ) from e
