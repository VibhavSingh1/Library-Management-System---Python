"""
Test Script for UserManagement Subsystem:

"""

import pytest

from script.user import UserManagement


@pytest.fixture
def mock_storage():
    """Fixture for creating a mock Storage class."""

    class MockStorage:
        def __init__(self):
            self.data = {"users": {}}

        def save_data(self):
            pass

        def validate_storage(self):
            pass

        def load_data(self):
            pass

    return MockStorage()


def test_create_user(mock_storage, capsys) -> None:
    """Test for creating a new user."""

    um = UserManagement(mock_storage)
    um.create_user("John Doe", "john.doe@example.com")
    # Check if user got added
    assert len(mock_storage.data["users"]) == 1
    # Check expected message upon user creation
    captured = capsys.readouterr()
    assert "new user added" in captured.out.lower()


def test_update_user(mock_storage) -> None:
    """Test for updating an existing user."""
    um = UserManagement(mock_storage)
    # Data for mocking
    mock_storage.data["users"]["1"] = {
        "name": "alice",
        "email": "alice@example.com",
    }
    # Call update to mock data
    um.update_user("1", name="Alice Smith")
    # Check if it updated
    assert mock_storage.data["users"]["1"]["name"] == "alice smith"


def test_delete_user(mock_storage) -> None:
    """Test for deleting an existing user."""
    um = UserManagement(mock_storage)
    # Mock data
    mock_storage.data["users"]["1"] = {
        "name": "alice",
        "email": "alice@example.com",
    }
    # Call method
    um.delete_user("1")
    # Check if user id remains in storage
    assert "1" not in mock_storage.data["users"]


def test_list_users(mock_storage, capsys):
    """Test for listing all users."""
    um = UserManagement(mock_storage)
    # Mock Data
    mock_storage.data["users"]["1"] = {
        "name": "alice",
        "email": "alice@example.com",
    }
    # Call method
    um.list_users()
    # Check if mock data user in printed data
    captured = capsys.readouterr()
    assert "alice" in captured.out.lower()


def test_find_user(mock_storage, capsys):
    """Test for finding a user."""
    um = UserManagement(mock_storage)
    # Mock Data
    mock_storage.data["users"]["1"] = {
        "name": "alice",
        "email": "alice@example.com",
    }
    # Call method
    um.find_user("1", how="uid")
    # Check if user searched is present in printed data
    captured = capsys.readouterr()
    assert "alice".lower() in captured.out.lower()


if __name__ == "__main__":
    pass