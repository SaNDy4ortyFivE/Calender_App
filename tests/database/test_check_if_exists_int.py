import pytest

from services.meeting_service import check_if_exists_int

def test_check_if_exists_int_when_value_exists(mocker):
    # Setup - pretending the fetch_from_db function returns a result indicating the value exists
    mock_fetch_from_db = mocker.MagicMock()
    mock_fetch_from_db.return_value=[(1003, "Room 103", 103)]
    mocker.patch('services.meeting_service.fetch_from_db', return_value=[(1003, "Room 103", 103)])

    assert check_if_exists_int('room_number', 103, 'MeetingRoom') is True

def test_check_if_exists_int_when_value_does_not_exist(mocker):
    # Setup - pretending the fetch_from_db function returns an empty list indicating the value does not exist
    mocker.patch('services.meeting_service.fetch_from_db', return_value=[])

    assert check_if_exists_int('room_number', 103, 'MeetingRoom') is False
