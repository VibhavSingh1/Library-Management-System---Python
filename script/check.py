"""
Module to work with Transactions Or Checkin/Checkout data
"""

from datetime import datetime

import pandas as pd

from script.loggers import LibraryLogger
from script.storage import Storage
from script.utils import clear_screen

logger = LibraryLogger()


class TransactionManagement:
    """Class to handle operations on Transaction data"""

    def __init__(self, storage: Storage):
        self.storage = storage
        # validate once if all required data are present
        storage.validate_storage()
        self.CHECK_OUT = "checkout"
        self.CHECK_IN = "checkin"

    def transaction_management_menu(self) -> None:
        """Display Transaction management menu"""
        print()
        print("*** Transaction Management ***")
        print("1. Checkout Book")
        print("2. Checkin Book")
        print("3. List Checkins and checkouts")
        print("4. List Available Books")
        print("5. Back")

    def main(self) -> None:
        """Main method for executing the Transaction Management subsystem"""
        while True:
            clear_screen()
            # Display Menu
            self.transaction_management_menu()
            user_choice = input("\nEnter choice: ")
            logger.info(f"User chose option {user_choice} from Menu")

            # Execute Choice
            if user_choice == "1":  # Checkout Book
                logger.info("Checkout Book: Start")
                user_id = input("\nInput user id: ")
                isbn = input("\nEnter the isbn of book: ")
                # Calling checkout method
                self.check_out(
                    user_id=user_id,
                    isbn=isbn,
                )
                input("\nPress Enter to continue")
                clear_screen()

            elif user_choice == "2":  # Checkin Book
                logger.info("Checkin Book: Start")
                user_id = input("\nInput user id: ")
                isbn = input("\nEnter the isbn of book: ")
                # Calling checkout method
                self.check_in(
                    user_id=user_id,
                    isbn=isbn,
                )
                input("\nPress Enter to continue")
                clear_screen()

            elif user_choice == "3":  # List Checkins and Checkouts
                logger.info("List checkins and checkouts: Start")
                user_id = input("\nInput user id: ")
                # call list method
                self.list_transactions(user_id=user_id)
                input("\nPress Enter to continue")
                clear_screen()

            elif user_choice == "4":  # List Available Books
                logger.info("List Available Books: Start")
                # call the method
                self.check_available_books()
                input("\nPress Enter to continue")
                clear_screen()

            elif user_choice == "5":  # Go to previous Menu
                logger.info("Move Back")
                clear_screen()
                break
            else:
                input(
                    "\nInvalid choice, please try again. Press Enter to continue."
                )
                logger.info("Invalid choice made. Retry")
                clear_screen()

    def check_out(self, user_id: str, isbn: str) -> None:
        """Checkout book, update availability and save the data

        Args:
            user_id (str): user id of the user who checked out the book
            isbn (str): isbn of book which was checked out
        """
        # Get data separated for ease of readability
        # All of these are already checked for availability
        transac_data = self.storage.data.get("transactions", None)
        users_data = self.storage.data.get("users", None)
        books_data = self.storage.data.get("books", None)

        # Clean the input data
        user_id = user_id.strip().lower()
        isbn = isbn.strip().lower()

        # Check if user and book exists:
        user = users_data.get(user_id, None)
        if user is None:
            print(f"No User with user id: {user_id}")
            logger.info(f"No User with user id: {user_id}")
            return None

        book = books_data.get(isbn, None)
        if book is None:
            print(f"No Book with isbn: {isbn}")
            logger.info(f"No Book with isbn: {isbn}")
            return None
        # check if book is available
        if book.get("available", False) is False:
            print(f"Book with isbn: {isbn} is not available")
            logger.info(f"Book with isbn: {isbn} is not available")
            return None

        # Now both book and user is available
        # create checkout transaction data
        checkout_data = {
            "user_id": user_id,
            "isbn": isbn,
            "action": self.CHECK_OUT,
            "timestamp": datetime.now().isoformat(),
        }

        # Assign data to transactions
        transac_data.append(checkout_data)

        # update book availability
        book["available"] = False
        # update borrowed books list of user
        if user.get("borrowed", None) is None:
            user["borrowed"] = []
        user["borrowed"].append(isbn)

        logger.debug(f"Transaction data added: {checkout_data} to storage")
        # save the data
        self.storage.save_data()
        print(f"User: {user_id} checked out Book: {isbn}")
        logger.info(f"User: {user_id} checked out Book: {isbn}")

    def check_in(self, user_id: str, isbn: str) -> None:
        """Checkout book, update availability and save the data

        Args:
            user_id (str): user id of the user who checked out the book
            isbn (str): isbn of book which was checked out
        """
        # Get data separated for ease of readability
        # All of these are already checked for availability
        transac_data = self.storage.data.get("transactions", None)
        users_data = self.storage.data.get("users", None)
        books_data = self.storage.data.get("books", None)

        # Clean the input data
        user_id = user_id.strip().lower()
        isbn = isbn.strip().lower()

        # # Check if user and book exists:
        user = users_data.get(user_id, None)
        if user is None:
            print(f"No User with user id: {user_id}")
            logger.info(f"No User with user id: {user_id}")
            return None

        book = books_data.get(isbn, None)
        if book is None:
            print(f"No Book with isbn: {isbn}")
            logger.info(f"No Book with isbn: {isbn}")
            return None

        # validate checkout
        borrowed = user.get("borrowed", None)
        if borrowed is None or isbn not in borrowed:
            print(f"User {user_id} has not borrowed book {isbn} at the moment")
            logger.info(
                f"User {user_id} has not borrowed book {isbn} at the moment"
            )
            return None

        # create checkout transaction data
        checkin_data = {
            "user_id": user_id,
            "isbn": isbn,
            "action": self.CHECK_IN,
            "timestamp": datetime.now().isoformat(),
        }

        # Assign data to transactions
        transac_data.append(checkin_data)

        # update book availability and remove book from user's borrowed list
        book["available"] = True
        borrowed.remove(isbn)

        logger.debug(f"Transaction data added: {checkin_data} to storage")

        # save the data
        self.storage.save_data()
        print(f"User: {user_id} checked in Book: {isbn}")
        logger.info(f"User: {user_id} checked in Book: {isbn}")

    def list_transactions(self, user_id: str) -> None:
        """Method to list transactions for given user

        Args:
            user_id (str): id of user
        """
        # Get required data
        users_data = self.storage.data["users"]
        trans_data = self.storage.data["transactions"]

        # Clean input data
        user_id = user_id.strip().lower()

        # if user doesnt exist, return None
        if user_id not in users_data:
            print(f"User with ID {user_id} does not exist")
            logger.info(f"User with ID {user_id} does not exist")
            return None

        # filter data for current user
        tdf = pd.DataFrame(trans_data)
        req_df = tdf[tdf["user_id"] == user_id]
        # print the data frame
        print(f"All checkins and checkouts of User {user_id}:\n")
        print(req_df.to_string(index=False), end="\n\n")
        logger.info(f"Listed all the checkins and checkout of User: {user_id}")
        logger.debug(f"\n{req_df.to_string(index=False)}")

    def check_available_books(self) -> None:
        """prints all available books"""
        # Get the books data
        books_data = self.storage.data["books"]
        # Make a dataframe from books data
        df = pd.DataFrame(books_data.values(), index=books_data.keys())
        df.index.name = "isbn"
        # Filter available books and print it
        fil_df = df[df["available"] == True]
        print("Following are the currently available books:")
        print(fil_df.to_string(), end="\n\n")
        logger.info("Listed all the available books")
        logger.debug(f"\n{fil_df.to_string()}")


if __name__ == "__main__":
    storage = Storage()
    tm = TransactionManagement(storage)
    tm.main()
