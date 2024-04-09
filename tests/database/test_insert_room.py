import pytest
from services.meeting_service import insert_room
from unittest.mock import MagicMock


@pytest.fixture
def mock_utilities(mocker):
    """Fixture to mock the utilities module."""
    mock = mocker.patch('services.meeting_service.utilities.get_value')
    mock.side_effect = lambda key: {
        "custom_meeting_room": "meeting_rooms",
        "custom_meeting_details": "meeting_details"
    }[key]
    return mock

@pytest.fixture
def mock_fetch_from_db(mocker):
    """Fixture to mock the fetch_from_db function."""
    return mocker.patch('services.meeting_service.fetch_from_db')

@pytest.fixture
def mock_insert_new_record(mocker):
    """Fixture to mock the insert_new_record function."""
    return mocker.patch('services.meeting_service.insert_new_record', return_value=True)

@pytest.fixture
def mock_logger(mocker):
    """Fixture to mock custom_logger."""
    return mocker.patch('services.meeting_service.custom_logger.logger')

def test_insert_room_success(mock_utilities, mock_fetch_from_db, mock_insert_new_record, mock_logger):
    # Setup - Mocking the room number existing in the database
    mock_fetch_from_db.return_value = [(1,)]  # Simulate the room exists in the database

    # Call the function under test
    meeting_room_inserted = insert_room(1, 103)

    # Assertions
    assert meeting_room_inserted is True  # Expecting room to be inserted
    mock_fetch_from_db.assert_called_once_with(
        "SELECT id FROM meeting_rooms WHERE room_number=?", (103,)
    )
    mock_insert_new_record.assert_called_once_with(
        "INSERT INTO meeting_details(id, room_id) VALUES(?,?)", (1, 1)
    )
    mock_logger.debug.assert_called_once_with("Meeting Room Booked")
    mock_logger.error.assert_not_called()  # No error should be logged

def test_insert_room_room_not_found(mock_utilities, mock_fetch_from_db, mock_insert_new_record, mock_logger):
    # Setup - Mocking the room number not existing in the database
    mock_fetch_from_db.return_value = []  # Simulate the room doesn't exist in the database

    # Call the function under test
    meeting_room_inserted = insert_room(1, 103)

    # Assertions
    assert meeting_room_inserted is False  # Expecting room not to be inserted
    mock_fetch_from_db.assert_called_once_with(
        "SELECT id FROM meeting_rooms WHERE room_number=?", (103,)
    )
    mock_insert_new_record.assert_not_called()  # No insertion should be attempted
    mock_logger.debug.assert_not_called()  # No debug log should be created
    mock_logger.error.assert_called_once_with("No Meeting Room found with number 103")
