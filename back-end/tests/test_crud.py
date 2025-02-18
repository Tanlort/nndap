import pytest
from unittest.mock import MagicMock
from datetime import datetime
from src import crud
from src.models import CowDB


# Create a mock database session fixture
@pytest.fixture
def mock_db():
    mock_db = MagicMock()
    yield mock_db
    mock_db.close()


@pytest.fixture
def new_cow():
    return CowDB(id="1", name="Sandra #1", birthdate=datetime(2020, 5, 10))


def test_get_cow(mock_db, new_cow):
    mock_db.query.return_value.filter.return_value.first.return_value = new_cow

    cow = crud.get_cow(mock_db, new_cow.id)
    
    assert cow is not None
    assert cow.id == new_cow.id
    assert cow.name == new_cow.name
    assert cow.birthdate == new_cow.birthdate

