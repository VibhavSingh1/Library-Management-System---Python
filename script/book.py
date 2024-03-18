"""
Module to work with Book data
"""

import pandas as pd

from script.loggers import LibraryLogger
from script.storage import Storage
from script.utils import BookValidator, clear_screen

logger = LibraryLogger()


class BookManagement:
    """Class to handle operations on Book data"""

    def __init__(self, storage: Storage):
        self.storage = storage
        # validate once if all required data are present
        storage.validate_storage()

    def book_management_menu(self):
        """Book management menu to be displayed"""
        print()
        print("*** Book Management ***")
        print("1. Add Book")
        print("2. Update Book")
        print("3. List Book")
        print("4. Delete Book")
        print("5. Search Book")
        print("6. Back")

    def search_book_menu(self):
        """Prints search options and executes the search"""
        while True:
            print()
            print("\nChoose search method:-")
            print("1. Title")
            print("2. Author")
            print("3. ISBN")
            print("4. Back")
            choice = input("\nEnter Choice: ").strip()
            logger.debug(f"User chose option {choice} from Search Menu")

            if choice == "1":
                how = "title"
                val = str(input("\nEnter book title: "))
                logger.info(f"User chose to search by {how}")

            elif choice == "2":
                how = "author"
                val = str(input("\nEnter book author: "))
                logger.info(f"User chose to search by {how}")

            elif choice == "3":
                how = "isbn"
                val = str(input("\nEnter book isbn: "))
                logger.info(f"User chose to search by {how}")

            elif choice == "4":
                logger.info("Exit Search Menu")
                break

            else:
                clear_screen()
                print(f"Invalid choice {choice}, please choose again.")
                logger.info(f"Invalid choice {choice}. Retry.")
                continue

            # Call the search with collected info
            self.find_book(value=val, how=how)
            # Wait till user presses enter and then clear screen
            input("\nPress Enter to continue.")
            clear_screen()

    def main(self):
        """Main method for executing the Book Management subsystem"""
        while True:
            clear_screen()
            # Display Menu
            self.book_management_menu()
            user_choice = input("\nEnter choice: ").strip()
            logger.info(f"User chose option {user_choice} from Menu")

            # Execute choice
            if user_choice == "1":  # Create Book
                logger.info("Create Book: Start")
                # taking user inputs
                title = input("\nEnter Book Title: ")
                author = input("\nEnter Book Author: ")
                isbn = input("\nEnter Book ISBN: ")
                # call the method to create
                self.add_book(
                    title=title,
                    author=author,
                    isbn=isbn,
                )
                input("\nPress Enter to continue")
                clear_screen()

            elif user_choice == "2":  # Update Book
                logger.info("Update Book: Start")

                print(
                    "\nEnter value to update OR just press 'Enter' with empty value to not update that."
                )
                isbn = input("\nEnter ISBN to update (compulsory): ").strip()
                title = input(
                    "\nEnter Title to Update or leave it empty: "
                ).strip()
                author = input(
                    "\nEnter Author to Update or leave it empty: "
                ).strip()

                # Call the method to udpate
                self.update_book(
                    isbn=isbn,
                    title=title,
                    author=author,
                )
                input("\nPress Enter to continue")
                clear_screen()

            elif user_choice == "3":  # List Books
                logger.info("List Book: Start")
                self.list_books()
                input("\nPress Enter to continue")
                clear_screen()

            elif user_choice == "4":  # Delete Book
                logger.info("Delete Book: Start")
                isbn = input("\nEnter isbn of Book to Delete: ").strip()
                # Call method to delete
                self.delete_book(isbn=isbn)
                input("\nPress Enter to continue")
                clear_screen()

            elif user_choice == "5":  # Search Book
                clear_screen()
                logger.info("Search Book: Start")
                self.search_book_menu()
                clear_screen()

            elif user_choice == "6":
                logger.info("Move Back")
                clear_screen()
                # break current loop and go back to main menu of LMS
                break
            else:
                input(
                    "\nInvalid choice, please try again. Press Enter to continue."
                )
                logger.info("Invalid choice made. Retry")
                clear_screen()

    def add_book(self, title: str, author: str, isbn: str) -> None:
        """creates a book if doesn't already exists.

        Args:
            title (str): title of book
            author (str): author of book
            isbn (str): isbn of book

        """
        # get books data for ease of readability
        books_data = self.storage.data["books"]

        # clean input data
        title = title.lower().strip()
        author = author.lower().strip()
        isbn = isbn.lower().strip()

        # validate user input and if fails then return None
        if not BookValidator.validate_book_data(
            title=title,
            author=author,
            isbn=isbn,
            books_data=books_data,
        ):
            return None

        # Add the data with isbn as key
        books_data[isbn] = {
            "title": title,
            "author": author,
            "available": True,
        }

        # Save all the data back to files
        self.storage.save_data()
        print(
            f"New Book added with ISBN: {isbn} - Title: {title} - Author: {author}"
        )
        logger.info(
            f"New Book added with ISBN: {isbn} - Title: {title} - Author: {author}"
        )

    def update_book(
        self, isbn: str, title: str = None, author: str = None
    ) -> None:
        """Updates the book data whose isbn is provided

        Args:
            title (str): title of book
            author (str, Optional): author of book. Defauts to None
            isbn (str, Optional): isbn of book. Defaults to None

        """
        books_data = self.storage.data["books"]
        # if book doesn't exist, return None
        if isbn not in books_data:
            print(f"Book with ISBN {isbn} does not exist")
            logger.info(f"Book with ISBN {isbn} does not exist")
            return None

        # clean, validate and assign
        if title:
            title = title.lower().strip()
            if not BookValidator.validate_title(title=title):
                return None

        if author:
            author = author.lower().strip()
            if not BookValidator.validate_author_name(author):
                return None

        # update if all provided data passed validation
        if title:
            books_data[isbn]["title"] = title
        if author:
            books_data[isbn]["author"] = author

        # Save the data to files
        self.storage.save_data()
        print(f"Book data with ISBN: {isbn}, updated")
        logger.info(f"Book data with ISBN: {isbn}, updated")

    def delete_book(self, isbn: str) -> None:
        """Delete a Book data

        Args:
            isbn (str): isbn of the book to be deleted
        """
        books_data = self.storage.data["books"]
        # clean input
        isbn = isbn.lower().strip()

        # if book doesn't exist, return None
        if isbn not in books_data:
            print(f"Book with ISBN {isbn} does not exist")
            logger.info(f"Book with ISBN {isbn} does not exist")
            return None

        # delete the data and save data back to all the files
        del books_data[isbn]
        self.storage.save_data()
        print(f"Book data with ID: {isbn}, deleted")
        logger.info(f"Book data with ID: {isbn}, deleted")

    def list_books(self) -> None:
        """List down all the books"""
        books_data = self.storage.data["books"]
        df = pd.DataFrame(books_data.values(), index=books_data.keys())
        df.index.name = "isbn"
        print()
        print(df.to_string(), end="\n\n")
        logger.info("Books Listed")
        logger.debug(f"\n{df.to_string()}")

    def find_book(self, value: str, how: str = "isbn") -> None:
        """Find a book by passing value and set [how = 'isbn' or 'title' or 'author']

        Args:
            value (str): Value passed to search
            how (str, optional): Field on which to search. Defaults to 'isbn'.
        """
        # Clean the data to search
        value = value.strip().lower()
        # Get books data
        books_data = self.storage.data["books"]
        # To store books found
        found_books = {}

        # Check the field chosen to search upon
        if how == "isbn":
            # Get book based on isbn and store in found books
            book_info = books_data.get(value, None)
            if book_info is not None:
                found_books[value] = book_info

        elif how in ["author", "title"]:
            # loop over the books to search
            for isbn, book_info in books_data.items():
                # compare
                if how in book_info and book_info[how].lower() == value:
                    found_books[isbn] = book_info

        # Case when 'how' don't match any availble options then it is an error
        else:
            raise ValueError("Invalid 'how' parameter found.")

        # If book is found then print data, else notify not found
        if len(found_books) == 0:
            print(f"Book with {how}: {value} not found")
            logger.info(f"Book with {how}: {value} not found")
        else:
            print("\nBook Found:\n")
            df = pd.DataFrame(
                found_books.values(),
                index=found_books.keys(),
            )
            df.index.name = "isbn"

            logger.info(f"Book Found with {how}: {value}")
            logger.debug(f"\n{df.to_string()}")
            print(df.to_string())


if __name__ == "__main__":
    storage = Storage()
    bm = BookManagement(storage=storage)
    bm.main()
