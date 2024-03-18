"""
Module for loggers

Using Singleton design for logger.
"""

import logging
from logging.handlers import TimedRotatingFileHandler

from script.settings import LOG_ERR_FILE_PATH, LOG_FILE_PATH, LOG_LEVEL


class LibraryLogger:
    """Singleton Implementation of Logger"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Get logger and configure it
            cls._instance.logger = logging.getLogger("Library_Logger")
            # Set the level for logs
            cls._instance.logger.setLevel(LOG_LEVEL)

            # Set the format for logger
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

            # File handler for normal logs with daily rotation
            file_handler = TimedRotatingFileHandler(
                LOG_FILE_PATH, when="midnight", interval=1, backupCount=5
            )
            file_handler.setFormatter(formatter)
            cls._instance.logger.addHandler(file_handler)

            # File handler for error logs with daily rotation
            error_handler = TimedRotatingFileHandler(
                LOG_ERR_FILE_PATH, when="midnight", interval=1, backupCount=5
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(formatter)
            cls._instance.logger.addHandler(error_handler)

            # Log the starting message
            cls._instance.logger.info(
                "~~~~~~~~~~~~~~~~~~ Logger Initialized ~~~~~~~~~~~~~~~~~~~"
            )

        return cls._instance

    def info(self, message: str):
        """Log INFO level message

        Args:
            message (str): message to log
        """
        self.logger.info(message)

    def debug(self, message: str):
        """Log DEBUG level message

        Args:
            message (str): message to log
        """
        self.logger.debug(message)

    def error(self, message: str):
        """Log ERROR level message

        Args:
            message (str): message to log
        """
        self.logger.error(message)

    def warn(self, message: str):
        """Log WARNING level message

        Args:
            message (str): message to log
        """
        self.logger.warning(message)

    def critical(self, message: str):
        """Log CRITICAL level message

        Args:
            message (str): message to log
        """
        self.logger.critical(message)
