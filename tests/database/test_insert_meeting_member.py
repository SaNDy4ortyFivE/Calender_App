import pytest
from services.meeting_service import insert_meeting_member
from unittest.mock import MagicMock

@pytest.fixture
def mock_utilities(mocker):
    """Fixture to mock the utilities module."""
    mock = mocker.patch('services.meeting_service.utilities.get_value')
    mock.return_value = 'meeting_members'
    return mock

@pytest.fixture
def mock_insert_new_record(mocker):
    """Fixture to mock the insert_new_record function."""
    return mocker.patch('services.meeting_service.insert_new_record', return_value=True)

@pytest.fixture
def mock_logger(mocker):
    """Fixture to mock custom_logger."""
    return mocker.patch('services.meeting_service.custom_logger.logger')

def test_insert_meeting_member_success(mock_utilities, mock_insert_new_record, mock_logger):
    # Call the function under test
    is_member_inserted = insert_meeting_member(1, 101)

    # Assertions
    assert is_member_inserted is True  # Expecting member to be inserted
    mock_insert_new_record.assert_called_once_with(
        "INSERT INTO meeting_members(meeting_id, person_id) VALUES(?,?)", (1, 101)
    )
    mock_logger.debug.assert_called_once_with("Meeting Member added")
    mock_logger.error.assert_not_called()  # No error should be logged

def test_insert_meeting_member_failure(mock_utilities, mock_insert_new_record, mock_logger):
    # Setup - Mocking insertion failure
    mock_insert_new_record.return_value = False

    # Call the function under test
    is_member_inserted = insert_meeting_member(1, 101)

    # Assertions
    assert is_member_inserted is False  # Expecting member not to be inserted
    mock_insert_new_record.assert_called_once_with(
        "INSERT INTO meeting_members(meeting_id, person_id) VALUES(?,?)", (1, 101)
    )
    mock_logger.debug.assert_not_called()  # No debug log should be created
    mock_logger.error.assert_called_once_with("Meeting Member not added")
