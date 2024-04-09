import pytest

from database.helpers import fetch_from_db

# pytest-mock uses the `mocker` fixture
def test_fetch_from_db_success_no_values(mocker):
    # Mock the cursor and its return value
    mock_cursor = mocker.MagicMock()
    mock_cursor.fetchall.return_value = [(123,145,156,167)]
    mocker.patch('database.helpers.get_cursor', return_value=mock_cursor)
    
    # Mock the logger
    mock_logger_debug = mocker.patch('services.helpers.custom_logger.logger.debug')
    
    sql_query = "SELECT id FROM Person"
    values = ()
    
    # Call the function
    results = fetch_from_db(sql_query, values)
    
    # Assertions
    assert results == [(123,145,156,167)]
    mock_cursor.execute.assert_called_once_with(sql_query)
    mock_logger_debug.assert_called()

def test_fetch_from_db_success_with_values(mocker):
    # Setup similar to the previous test but with values for the SQL query
    mock_cursor = mocker.MagicMock()
    mock_cursor.fetchall.return_value = [(1003,1004,1005)]
    mocker.patch('database.helpers.get_cursor', return_value=mock_cursor)
    mocker.patch('database.helpers.get_cursor', return_value=mock_cursor)
    
    # Mock the logger
    mock_logger_debug = mocker.patch('services.helpers.custom_logger.logger.debug')
    
    sql_query = "SELECT id FROM MeetinRoom WHERE room_number >= %d"
    values = (103,)
    
    # Call the function
    results = fetch_from_db(sql_query, values)
    
    # Assertions
    assert results == [(1003,1004,1005)]
    mock_cursor.execute.assert_called_once_with(sql_query, values)