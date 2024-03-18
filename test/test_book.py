"""
Test Script for BookManagement Subsystem:
`sample only due to development time constraints`
"""

import pytest
from script.book import BookManagement


@pytest.fixture
def mock_storage():
    """Fixture for creating a mock Storage class."""

    class MockStorage:
        def __init__(self):
            self.data = {"books": {}}

        def save_data(self):
            pass

        def validate_storage(self):
            pass

        def load_data(self):
            pass

    return MockStorage()


def test_add_book(mock_storage) -> None:
    """Test for adding a new book."""
    bm = BookManagement(mock_storage)
    # Execute method
    bm.add_book("Book Title", "Author Name", "a1234567890")
    # Validate
    assert len(mock_storage.data["books"]) == 1
    assert "a1234567890" in mock_storage.data["books"]


def test_update_book(mock_storage) -> None:
    """Test for updating an existing book."""
    bm = BookManagement(mock_storage)
    # Mock data
    mock_storage.data["books"]["a1234567890"] = {
        "title": "Book Title",
        "author": "Author Name",
        "available": True,
    }
    # Execute method
    bm.update_book("a1234567890", title="New Title")
    # Validate
    assert mock_storage.data["books"]["a1234567890"]["title"] == "new title"


def test_delete_book(mock_storage) -> None:
    """Test for deleting an existing book."""
    bm = BookManagement(mock_storage)
    # Mock data
    mock_storage.data["books"]["a1234567890"] = {
        "title": "Book Title",
        "author": "Author Name",
        "available": True,
    }
    # Execute method
    bm.delete_book("a1234567890")
    # Validate
    assert "a1234567890" not in mock_storage.data["books"]


def test_list_books(mock_storage, capsys) -> None:
    """Test for listing all books."""
    bm = BookManagement(mock_storage)
    # Mock Data
    mock_storage.data["books"]["a1234567890"] = {
        "title": "Book Title",
        "author": "Author Name",
        "available": True,
    }
    # Execute method
    bm.list_books()
    # Validate
    captured = capsys.readouterr()
    assert "book title" in captured.out.lower()


def test_find_book(mock_storage, capsys) -> None:
    """Test for finding a book."""
    bm = BookManagement(mock_storage)
    # Mock Data
    mock_storage.data["books"]["a1234567890"] = {
        "title": "Book Title",
        "author": "Author Name",
        "available": True,
    }
    # Execute method
    bm.find_book("a1234567890", how="isbn")
    # Validate 
    captured = capsys.readouterr()
    assert "book title" in captured.out.lower()


if __name__ == "__main__":
    pass