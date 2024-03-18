"""Script to contain configurations and settings"""

import os
from logging import DEBUG  # INFO,; WARNING,; ERROR

# Project Root Settings --
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Data Related Settings --
DATA_DIR = "data"
DATA_PATH = os.path.join(ROOT_PATH, DATA_DIR)
# Check if data dir exists, if not then make one
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH, exist_ok=True, mode=777)

# Data Files to be loaded and their paths
file_extension = ".json"
DATA_FILE_NAMES = ["users", "books", "transactions"]
DATA_FILE_PATHS = {
    file_name: os.path.join(DATA_PATH, file_name + file_extension)
    for file_name in DATA_FILE_NAMES
}


# LOG Related Settings --
LOG_LEVEL = DEBUG
LOG_DIR = "log"
LOG_FILE_NAME = "library.log"
LOG_ERR_FILE_NAME = "error.log"
# log dir and file paths
LOG_DIR_PATH = os.path.join(ROOT_PATH, LOG_DIR)
LOG_FILE_PATH = os.path.join(LOG_DIR_PATH, LOG_FILE_NAME)
LOG_ERR_FILE_PATH = os.path.join(LOG_DIR_PATH, LOG_ERR_FILE_NAME)

# Create required dir, if doesn't exist already
if not os.path.exists(LOG_DIR_PATH):
    os.makedirs(LOG_DIR_PATH, exist_ok=True, mode=777)


if __name__ == "__main__":
    print(ROOT_PATH)
    print(LOG_DIR_PATH)
    print(LOG_ERR_FILE_PATH)
    print(LOG_FILE_PATH)
