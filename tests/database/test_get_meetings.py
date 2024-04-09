import pytest

from unittest.mock import MagicMock

from services.meeting_service import get_meetings


@pytest.fixture
def mock_utilities(mocker):
    """Fixture to mock the utilities module."""
    mock = mocker.patch('services.meeting_service.utilities.get_value')
    mock.return_value = 'meetings'
    return mock

@pytest.fixture
def mock_fetch_from_db(mocker):
    """Fixture to mock the fetch_from_db function."""
    return mocker.patch('services.meeting_service.fetch_from_db', return_value=[(1,), (2,), (3,)])

@pytest.fixture
def mock_logger(mocker):
    """Fixture to mock custom_logger."""
    return mocker.patch('services.meeting_service.custom_logger.logger')

def test_get_meetings_success(mock_utilities, mock_fetch_from_db, mock_logger):
    # Call the function under test
    results = get_meetings()

    # Check that the utilities.get_value was called correctly
    mock_utilities.assert_called_once_with("custom_meeting_table")

    # Check that the correct SQL query was used in fetch_from_db
    mock_fetch_from_db.assert_called_once()
    args, kwargs = mock_fetch_from_db.call_args
    assert "SELECT id FROM meetings" in args[0]  # Confirm the SQL query structure
    assert kwargs == {} or args[1] == ()  # Confirm no additional arguments were passed

    # Check that results are as expected
    assert len(results) == 3  # Confirm we got 3 meeting IDs as mocked

    # Confirm logging of the correct number of meetings fetched
    mock_logger.debug.assert_any_call("Getting all meetings...")
    mock_logger.debug.assert_any_call("Total Meetings Fetched:3")
