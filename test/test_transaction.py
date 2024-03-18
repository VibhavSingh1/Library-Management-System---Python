"""
Test Script for TransactionManagement Subsystem:
`sample only due to development time constraints`
"""

import pytest
from datetime import datetime
from script.check import TransactionManagement

@pytest.fixture
def mock_storage():
    """Fixture for creating a mock Storage class."""
    class MockStorage:
        def __init__(self):
            self.data = {"transactions": [], "users": {}, "books": {}}

        def save_data(self):
            pass

        def validate_storage(self):
            pass

        def load_data(self):
            pass

    return MockStorage()

def test_check_out(mock_storage) -> None:
    """Test for checking out a book."""
    tm = TransactionManagement(mock_storage)
    # Prepare mock data
    mock_storage.data["users"]["1"] = {"name": "alice", "email": "alice@example.com"}
    mock_storage.data["books"]["b1000"] = {"title": "book 1", "available": True}
    # Execute method
    tm.check_out("1", "b1000")
    # Validate
    assert len(mock_storage.data["transactions"]) == 1
    # Availibility should be False now
    assert not mock_storage.data["books"]["b1000"]["available"]

def test_check_in(mock_storage) -> None:
    """Test for checking in a book."""
    tm = TransactionManagement(mock_storage)
    # Prepare mock data
    mock_storage.data["users"]["1"] = {"name": "alice", "email": "alice@example.com", "borrowed": ["b1000"]}
    mock_storage.data["books"]["b1000"] = {"title": "book 1", "available": False}
    # Execute method
    tm.check_in("1", "b1000")
    # Validate
    assert len(mock_storage.data["transactions"]) == 1
    # Availability should be True now
    assert mock_storage.data["books"]["b1000"]["available"]

def test_list_transactions(mock_storage, capsys) -> None:
    """Test for listing transactions for a user."""
    tm = TransactionManagement(mock_storage)
    # Prepare mock data
    mock_storage.data["users"]["1"] = {"name": "alice", "email": "alice@example.com"}
    mock_storage.data["transactions"].append({
        "user_id": "1",
        "isbn": "b1000",
        "action": "checkout",
        "timestamp": datetime.now().isoformat()
    })
    # Execute method
    tm.list_transactions("1")
    # Validate
    captured = capsys.readouterr()
    assert "all checkins and checkouts" in captured.out.lower()

def test_check_available_books(mock_storage, capsys) -> None:
    """Test for listing available books."""
    tm = TransactionManagement(mock_storage)
    # Prepare mock data
    mock_storage.data["books"]["b1000"] = {"title": "book 1", "available": True}
    # Execute method
    tm.check_available_books()
    # Validate
    captured = capsys.readouterr()
    assert "book 1" in captured.out.lower()

if __name__ == "__main__":
    pass