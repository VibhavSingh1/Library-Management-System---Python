"""
Main module:
Runs the LMS / Entry Point to the program
"""

from script.book import BookManagement
from script.check import TransactionManagement
from script.loggers import LibraryLogger
from script.storage import Storage
from script.user import UserManagement
from script.utils import clear_screen, handle_error


# Instantiate singleton LibraryLogger
logger = LibraryLogger()
# Instantiate singleton Storage
storage = Storage()


class LMS:
    """Library Management System initiator and entry point"""

    def __init__(self, logger: LibraryLogger, storage: Storage) -> None:
        self.logger = logger
        self.storage = storage
        self.um = UserManagement(self.storage)
        self.bm = BookManagement(self.storage)
        self.tm = TransactionManagement(self.storage)

    def _main_menu(self) -> str:
        """Prints Main menu options and returns the user input

        Returns:
            str: User choice input
        """
        print("\n\n****** Library Management System *****")
        print("1. Book Management Menu")
        print("2. User Management Menu")
        print("3. Checkout/Checkin Book Menu")
        print("4. Exit\n")
        choice = input("Enter choice: ").strip()
        return choice

    def _main(self):
        """Main method to run the LMS"""

        clear_screen()
        # Loop over and stay on Menu till user exits
        while True:
            storage.refresh_data()
            logger.info("Enter LMS Main Menu")
            choice = self._main_menu()
            logger.info(f"User chose option {choice} from Main Menu")
            if choice == "1":
                logger.info("Enter Book Management Menu")
                clear_screen()
                # Enter Book Management Menu
                self.bm.main()
                logger.info("Exit Book Management Menu")

            elif choice == "2":
                logger.info("Enter User Management Menu")
                clear_screen()
                # Enter User Management Menu
                self.um.main()
                logger.info("Exit User Management Menu")

            elif choice == "3":
                logger.info("Enter Transaction Management Menu")
                clear_screen()
                # Enter Transaction Management Menu
                self.tm.main()
                logger.info("Exit Transaction Management Menu")

            elif choice == "4":
                clear_screen()
                print("Exiting. Thank you for using LMS.")
                logger.info("Exit LMS Main Menu")
                break
            else:
                clear_screen()
                print("Invalid choice, please try again.")
                logger.info(f"Invalid choice: {choice} for LMS main menu")

    # error handler at topmost level, will catch the error once it propagates till here
    @handle_error
    def execute_LMS(self) -> None:
        self._main()


if __name__ == "__main__":
    # Init LMS
    logger.debug("LMS initialized")
    lms = LMS(
        logger=logger,
        storage=storage,
    )
    # Start execution of LMS Main Menu
    logger.info("--LMS Start--")
    lms.execute_LMS()
    logger.info("--LMS Stopped--")
