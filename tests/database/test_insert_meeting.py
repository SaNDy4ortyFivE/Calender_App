import pytest
from services.meeting_service import insert_meeting
from models.meeting import SinglePersonMeeting
from models.person import Person
from unittest.mock import MagicMock



@pytest.fixture
def mock_utilities(mocker):
    """Fixture to mock the utilities module."""
    mock = mocker.patch('services.meeting_service.utilities.get_value')
    mock.return_value = 'meetings'
    return mock

@pytest.fixture
def mock_insert_new_record(mocker):
    """Fixture to mock the insert_new_record function."""
    return mocker.patch('services.meeting_service.insert_new_record', return_value=True)

@pytest.fixture
def mock_insert_meeting_member(mocker):
    """Fixture to mock the insert_meeting_member function."""
    return mocker.patch('services.meeting_service.insert_meeting_member', return_value=True)

@pytest.fixture
def mock_logger(mocker):
    """Fixture to mock custom_logger."""
    return mocker.patch('services.meeting_service.custom_logger.logger')

def test_insert_meeting_success(mock_utilities, mock_insert_new_record, mock_insert_meeting_member, mock_logger):
    # Setup - Creating a mock Meeting instance
    person_instance = Person(101)
    # meeting_instance = SinglePersonMeeting(meeting_id=1, date='2024-04-09', start_time='10:00', end_time='11:00', person_instance)
    meeting_instance = SinglePersonMeeting(1, '2024-04-09', '10:00', '11:00', person_instance)

    # Call the function under test
    is_meeting_inserted = insert_meeting(meeting_instance)

    # Assertions
    assert is_meeting_inserted is True  # Expecting meeting to be inserted
    mock_insert_new_record.assert_called_once_with(
        "INSERT INTO meetings (id, date, from_time, to_time) VALUES(?,?,?,?)",
        (1, '2024-04-09', '10:00', '11:00')
    )
    mock_insert_meeting_member.assert_called_once_with(1, 101)  # Expecting meeting member to be inserted


def test_insert_meeting_failure(mock_utilities, mock_insert_new_record, mock_insert_meeting_member, mock_logger):
    # Setup - Mocking insertion failure
    mock_insert_new_record.return_value = False

    # Call the function under test
    is_meeting_inserted = insert_meeting(SinglePersonMeeting(1,'2024-04-09', '10:00', '11:00', Person(person_id=101)))

    # Assertions
    assert is_meeting_inserted is False  # Expecting meeting not to be inserted
    mock_insert_new_record.assert_called_once()  # Ensure insert_new_record was called
    mock_insert_meeting_member.assert_not_called()  # No member insertion should be attempted
    mock_logger.error.assert_called_once_with("Meeting not inserted")
