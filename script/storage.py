"""
This module consists of logics for data storage and retrieval related tasks.

Singleton Design to interact with the datasets.
Pandas to perform operations on them.

"""

import json
import os

from script.loggers import LibraryLogger
from script.settings import DATA_FILE_PATHS

logger = LibraryLogger()


class Storage:
    """
    Storage class to handle the data storage and retrieval

    `Following a Singleton Design: Only a single instance will be made and
    returned.`
    """

    _instance = None

    def __new__(cls):
        """
        Overriding the default, so it creates only one instance and returns
        the same one everytime.
        """
        # check if instance already exists, if not then create a new one
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            logger.info("Singleton Storage Instantiated")
            cls._instance.data = {}
            cls._instance.load_data()

        return cls._instance

    def load_data(self) -> None:
        """Loads the files data into instance.data as dict for each file"""
        for name, path in DATA_FILE_PATHS.items():
            # load data and save it in storage instance
            if os.path.exists(path):
                with open(path, "r") as file:
                    self.data[name] = json.load(file)
            else:
                # If file doesn't exist, create one with empty json data
                if name == "transactions":
                    self.data[name] = []
                else:
                    self.data[name] = {}

                with open(path, "w") as file:
                    json.dump({}, file)
            logger.debug(
                f"Loaded data into storage instance from File: {path}"
            )

    def save_data(self) -> None:
        """Saves the datasets into their respective files"""

        for name, path in DATA_FILE_PATHS.items():
            with open(path, "w") as file:
                json.dump(self.data[name], file, indent=4)
            logger.debug(f"Saved data into File: {path}")

        # Refresh storage instance data after every update to files
        self.refresh_data()

    def refresh_data(self) -> None:
        """Reloads the data from each file"""
        self.load_data()
        logger.debug("Refreshed/reloaded the fresh data from files")

    def validate_storage(self) -> None:
        """Validates if all important file data exists in
        storage instance data or not. Like if 'users', 'books', etc.,
        exists or not in instance.data

        Raises:
            Exception: If any is missing then raises exception
        """
        for name in DATA_FILE_PATHS.keys():
            if name not in self.data:
                raise Exception(
                    f"{name} file data is not available in storage instance"
                )


if __name__ == "__main__":

    instance = Storage()
    print(instance.data)
