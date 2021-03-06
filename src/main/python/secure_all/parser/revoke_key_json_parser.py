"""parser for input key files according to FC3"""
import re

from secure_all.parser.json_parser import JsonParser
from secure_all.exception.access_management_exception import AccessManagementException


class RevokeKeyJsonParser(JsonParser):
    """parser for input key files containing a AccessKey request"""
    ERROR_MESSAGE = "JSON Decode Error - Wrong JSON Format"
    _key_error_message = ERROR_MESSAGE
    KEY = "Key"
    REVOCATION = "Revocation"
    REASON = "Reason"
    key_regex = r'[0-9a-f]{64}'
    revocation_regex = r'Temporal|Final'
    reason_regex = r'.{0,100}'
    _key_list = [KEY, REVOCATION, REASON]
    _contents_list = [key_regex, revocation_regex, reason_regex]

    def _validate_json(self):
        super()._validate_json()
        i = 0
        for _, content in self.json_content.items():
            if not re.fullmatch(self._contents_list[i], content):
                raise AccessManagementException(self._key_error_message)
            i += 1
