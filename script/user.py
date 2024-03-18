"""
Module to work with User data
"""

import pandas as pd

from script.loggers import LibraryLogger
from script.storage import Storage
from script.utils import UserValidator, clear_screen

logger = LibraryLogger()


class UserManagement:
    """Class to handle operations on User data"""

    def __init__(self, storage: Storage):
        self.storage = storage
        # validate once if all required data are present
        storage.validate_storage()

    def user_management_menu(self) -> None:
        """Display User management menu"""
        print()
        print("*** User Management ***")
        print("1. Create User")
        print("2. Update User")
        print("3. List Users")
        print("4. Delete User")
        print("5. Search User")
        print("6. Back")

    def search_user_menu(self):
        """Prints search options and executes the search"""
        while True:
            print()
            print("\nChoose search method")
            print("1. User ID")
            print("2. Name")
            print("3. Email")
            print("4. Back")
            choice = input("\nEnter Choice: ").strip()
            logger.debug(f"User chose option {choice} from Search Menu")

            if choice == "1":
                how = "uid"
                val = str(input("\nEnter user id: "))
                logger.info(f"User chose to search by {how}")

            elif choice == "2":
                how = "name"
                val = str(input("\nEnter user name: "))
                logger.info(f"User chose to search by {how}")

            elif choice == "3":
                how = "email"
                val = str(input("\nEnter user email: "))
                logger.info(f"User chose to search by {how}")

            elif choice == "4":
                logger.info("Exit Search Menu")
                break

            else:
                clear_screen()
                print(f"\nInvalid Choice {choice}, please choose again.")
                logger.info(f"Invalid choice {choice}. Retry.")
                continue

            # Call the search with collected info
            self.find_user(value=val, how=how)
            # Wait till user presses enter and then clear screen
            input("\nPress Enter to continue..")
            clear_screen()

    def main(self):
        """Main method for executing the User Management subsystem"""
        while True:
            clear_screen()
            # Display Menu
            self.user_management_menu()
            user_choice = input("\nEnter choice: ").strip()
            logger.info(f"User chose option {user_choice} from Menu")

            # Execute Choice
            if user_choice == "1":  # Create User
                logger.info("Create User: Start")
                name = input("\nEnter Name: ")
                email = input("\nEnter Email: ")
                self.create_user(name=name, email=email)
                input("\nPress Enter to continue")
                clear_screen()

            elif user_choice == "2":  # Update User
                logger.info("Update User: Start")
                print(
                    "\nEnter value to update OR just press 'Enter' with empty value to not update that."
                )
                user_id = name = input(
                    "\nEnter User ID to update (compulsory): "
                ).strip()
                name = input(
                    "\nEnter Name to Update or leave it empty: "
                ).strip()
                email = input(
                    "\nEnter Email to Update or leave it empty: "
                ).strip()
                self.update_user(user_id=user_id, name=name, email=email)
                input("\nPress Enter to continue")
                clear_screen()

            elif user_choice == "3":  # List Users
                logger.info("List User: Start")
                self.list_users()
                input("\nPress Enter to continue")
                clear_screen()

            elif user_choice == "4":  # Delete User
                logger.info("Delete User: Start")
                uid = input("\nEnter ID of User to Delete: ")
                self.delete_user(user_id=uid)
                input("\nPress Enter to continue")
                clear_screen()

            elif user_choice == "5":  # Search User
                clear_screen()
                logger.info("Search User: Start")
                self.search_user_menu()
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

    def create_user(self, name: str, email: str) -> None:
        """
        creates a user if doesn't already exists.
        User id is auto-incremented.

        Args:
            name (str): name of user
            email (str): email address of user
        """
        # get users_data for ease of readability
        users_data = self.storage.data["users"]

        # clean input data
        name = name.lower().strip()
        email = email.lower().strip()

        # validate user input and if fails then return None
        if not UserValidator.validate_user_data(
            name=name, email=email, users_data=users_data
        ):
            return None
        # Get available user id and Add data to storage instance
        new_uid = self._get_available_uid()
        users_data[new_uid] = {"name": name, "email": email}

        # Save all the data back to files
        self.storage.save_data()
        print(
            f"New user added with ID: {new_uid} - Name: {name} - Email: {email}"
        )
        logger.info(
            f"New user added with ID: {new_uid} - Name: {name} - Email: {email}"
        )

    def update_user(
        self, user_id: str, name: str = None, email: str = None
    ) -> None:
        """Update user's data of given ID

        Args:
            user_id (str): ID of user to update the data
            name (str, optional): New name. Defaults to None.
            email (str, optional): new email. Defaults to None.
        """
        users_data = self.storage.data["users"]
        # if user doesn't exist, return None
        if user_id not in users_data:
            print(f"User with ID {user_id} does not exist")
            logger.info(f"User with ID {user_id} does not exist")
            return None

        # clean, validate and assign
        if name:
            name = name.lower().strip()
            if not UserValidator.validate_name(name):
                return None
        if email:
            email = email.lower().strip()
            if UserValidator.validate_email(email):
                return None

        # update if all provided data passed validation
        if name:
            users_data[user_id]["name"] = name
        if email:
            users_data[user_id]["email"] = email
        # Save the data to files
        self.storage.save_data()
        print(f"User data with ID: {user_id}, updated")
        logger.info(f"User data with ID: {user_id}, updated")

    def delete_user(self, user_id: str) -> None:
        """Delete a user data

        Args:
            user_id (str): ID of user to be deleted
        """
        users_data = self.storage.data["users"]
        # clean input
        user_id = user_id.lower().strip()

        # if user doesnt exist, return None
        if user_id not in users_data:
            print(f"User with ID {user_id} does not exist")
            logger.info(f"User with ID {user_id} does not exist")
            return None

        # delete the data and save data back to all the files
        del users_data[user_id]
        self.storage.save_data()
        print(f"User data with ID: {user_id}, deleted")
        logger.info(f"User data with ID: {user_id}, deleted")

    def list_users(self) -> None:
        """
        Lists all the users with their data in tabular form

        """
        users_data = self.storage.data["users"]
        # using pandas to provide tabular structure to the data
        data_frame = pd.DataFrame(users_data.values(), index=users_data.keys())
        data_frame.index.name = "id"
        print()
        print(data_frame.to_string(), end="\n\n")
        logger.info("Users Listed")
        logger.debug(f"\n{data_frame.to_string()}")

    def find_user(self, value: str, how: str = "uid"):
        """Find a user by passing value and set how = 'uid' or 'name' or 'email'

        Args:
            value (str): Value passed to search
            how (str, optional): Field on which to search. Defaults to "uid".

        Raises:
            ValueError: Raises error if 'how' doesn't match any available fields
        """
        # clean the searched value
        value = value.lower().strip()

        # Get users data for readability
        users = self.storage.data["users"]

        # Check which field has been selected to search upon
        if how == "uid":
            user_info = users.get(value, None)
            if user_info is None:
                user = None
            else:
                user = (value, user_info)

        elif how in ["name", "email"]:
            # Loop over the users to search
            for user_id, user_info in users.items():
                # matching
                if how in user_info and user_info[how].lower() == value:
                    user = (user_id, user_info)
                    break
                else:
                    user = None
        # if how didn't match with any then it is an error
        else:
            raise ValueError("Invalid 'how' parameter found.")

        # If user was found then print data, else notify
        if user is None:
            print(f"User with {how}: {value} not found")
            logger.info(f"User with {how}: {value} not found")
        else:
            print(f"\nUser Found: \n")
            df = pd.DataFrame(
                user[1],  # user data
                index=[
                    user[0],  # uid
                ],
            )
            df.index.name = "id"  # rename index column
            logger.info(f"User Found with {how}: {value}")
            logger.debug(f"\n{df.to_string()}")
            print(df.to_string())

    def _get_available_uid(self) -> str:
        """Find an available(max of all + 1) uid to assign to new user

        Returns:
            str: available uid
        """
        user_ids = [
            int(user_id)
            for user_id in self.storage.data["users"].keys()
            if user_id.isdigit()
        ]
        new_user_id = str(max(user_ids) + 1) if user_ids else "1"
        return new_user_id


if __name__ == "__main__":
    storage = Storage()
    um = UserManagement(storage=storage)
    um.main()
