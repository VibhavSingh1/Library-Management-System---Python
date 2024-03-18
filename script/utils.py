"""
Utilities for our LMS
"""

import os
import re
import sys

from script.loggers import LibraryLogger
from script.storage import Storage

# Get the logger instance
logger = LibraryLogger()


def clear_screen():
    """Clears the console screen"""
    os.system("cls" if os.name == "nt" else "clear")


# Error handler
def handle_error(func):
    """
    Error handler to be wrapped around methods to be handled\n
    `Use as a decorator: @handle_error
    `
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            # shutdown gracefully
            clear_screen()
            print(f"An error occurred. Please check error.log for details.")
            print("Shutting down the LMS gracefully.")
            sys.exit()

    return wrapper


# Data Validators
class UserValidator:
    """Validator class for User input data"""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validates format for email

        Args:
            email (str): user email

        Returns:
            bool: True if email is valid else False
        """

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("Invalid email format")
            logger.info("Invalid email format")
            return False

        return True

    @staticmethod
    def validate_name(name: str) -> bool:
        """Validates format for name

        Args:
            name (str): user name

        Returns:
            bool: True if name is valid else False
        """
        # Regular expression pattern to validate name (allows letters, digits, and whitespace
        pattern = r"^[a-zA-Z0-9\s]+$"
        if re.match(pattern, name):
            return True
        else:
            print("Invalid name format")
            logger.info("Invalid name format")
            return False

    @staticmethod
    def validate_unique(users_data: dict, email: str) -> bool:
        """Validates if email already exists or if user already exists
        with given email

        Args:
            email (str): user email
            users_data (dict): storage instance's users data

        Returns:
            bool: True if all email is unique else False
        """

        for user_id, user_info in users_data.items():
            if "email" in user_info and user_info["email"] == email:
                print("User with this email already exists")
                logger.info("User with this email already exists")
                return False

        return True

    @staticmethod
    def validate_user_data(name: str, email: str, users_data: dict) -> bool:
        """Validates the user input fields data

        Args:
            name (str): user name
            email (str): user email
            users_data (dict): Storage instance's users data

        Returns:
            bool: True if all inputs valid else False
        """
        return (
            UserValidator.validate_name(name)
            and UserValidator.validate_email(email)
            and UserValidator.validate_unique(users_data, email)
        )


class BookValidator:
    """Validator class for Book input data"""

    @staticmethod
    def validate_author_name(name: str) -> bool:
        """Validates format for author name

        Args:
            name (str): user name

        Returns:
            bool: True if name is valid else False
        """
        # Regular expression pattern to validate name (allows letters, digits, and whitespace)
        pattern = r"^[a-zA-Z0-9\s]+$"
        if re.match(pattern, name):
            return True
        else:
            print("Invalid Author Name")
            logger.info("Invalid Author Name")
            return False

    @staticmethod
    def validate_title(title: str) -> bool:
        """Validates format for author name

        Args:
            name (str): user name

        Returns:
            bool: True if name is valid else False
        """
        # Regular expression pattern to validate book title
        # Max length 100
        pattern = r"^[\w\s.,'!?:;-]{1,100}$"
        if re.match(pattern, title):
            return True
        else:
            print("Invalid or unsupported title format")
            logger.info("Invalid or unsupported title format")
            return False

    @staticmethod
    def validate_unique(books_data: dict, isbn: str) -> bool:
        """Validates if ISBN already exists i.e., book already exists
        with given ISBN

        Args:
            isbn (str): book isbn
            books_data (dict): storage instance's books data

        Returns:
            bool: True if all email is unique else False
        """
        if isbn in books_data.keys():
            print("Book already exists with provided ISBN")
            logger.info("Book already exists with provided ISBN")
            return False

        return True

    @staticmethod
    def validate_isbn(isbn: str) -> bool:
        """Validates if ISBN format

        Args:
            isbn (str): book isbn

        Returns:
            bool: True if all email is unique else False
        """
        # Check if the ISBN consists of exactly 5 lowercase alphanumeric characters
        if len(isbn) >= 5 and isbn.islower() and isbn.isalnum():
            return True
        else:
            print(
                "Invalid isbn. Minimum length 5 characters. All lower. No special characters. Atleast one alphabet should be there."
            )
            logger.info(
                "Invalid isbn. Minimum length 5 characters. All lower. No special characters. Atleast one alphabet should be there."
            )
            return False

    @staticmethod
    def validate_book_data(
        title: str, author: str, isbn: str, books_data: dict
    ) -> bool:
        """Executes all validations on provided book data

        Args:
            title (str): book title
            author (str): book author
            isbn (str): book isbn
            books_data (dict): storage instance's books data

        Returns:
            bool: True if all email is unique else False
        """
        return (
            BookValidator.validate_author_name(name=author)
            and BookValidator.validate_title(title=title)
            and BookValidator.validate_isbn(isbn=isbn)
            and BookValidator.validate_unique(books_data=books_data, isbn=isbn)
        )


if __name__ == "__main__":
    pass
