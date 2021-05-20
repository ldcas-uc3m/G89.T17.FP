"""Global constants for finding the path"""
import os

# Dynamically build path to json files folder:
JSON_FILES_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../..", "JsonFiles")
) + os.sep
