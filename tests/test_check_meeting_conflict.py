import pytest
from services.meeting_service import check_meeting_conflict
from unittest.mock import MagicMock


@pytest.fixture
def mock_utilities(mocker):
    """Fixture to mock the utilities module."""
    mock = mocker.patch('services.meeting_service.utilities.get_value')
    mock.side_effect = lambda key: {
        "custom_meeting_table": "meetings",
        "custom_meeting_member_table": "meeting_members"
    }[key]
    return mock

@pytest.fixture
def mock_fetch_from_db(mocker):
    """Fixture to mock the fetch_from_db function."""
    return mocker.patch('services.meeting_service.fetch_from_db', return_value=[(1, '2024-04-09', '08:00', '09:00')])

@pytest.fixture
def mock_logger(mocker):
    """Fixture to mock custom_logger."""
    return mocker.patch('services.meeting_service.custom_logger.logger')

def test_check_meeting_conflict_no_conflict(mock_utilities, mock_fetch_from_db, mock_logger):
    # Setup - Mocking no conflicts in the database
    mock_fetch_from_db.return_value = []

    # Call the function under test
    is_conflict = check_meeting_conflict('2024-04-09', 1, '10:00', '11:00')

    # Assertions
    assert is_conflict is False  # Expecting no conflicts


def test_check_meeting_conflict_with_conflict(mock_utilities, mock_fetch_from_db, mock_logger):
    # Setup - Mocking a conflict in the database
    mock_fetch_from_db.return_value = [(2, '2024-04-09', '08:30', '10:00')]  # A conflicting meeting

    # Call the function under test
    is_conflict = check_meeting_conflict('2024-04-09', 1, '09:30', '10:30')

    # Assertions
    assert is_conflict is True  # Expecting a conflict
