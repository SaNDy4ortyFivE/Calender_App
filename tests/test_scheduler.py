import pytest

from services.scheduler_service import has_conflict

def test_no_conflict():
    """Test that no conflict is found for non-overlapping time windows."""
    time_windows = [("01:00", "02:00"), ("02:00", "03:00"), ("03:00", "04:00")]
    assert has_conflict(time_windows) is None

def test_conflict_found():
    """Test that a conflict is correctly identified."""
    time_windows = [("01:00", "03:00"), ("02:00", "04:00")]
    expected_conflict = (("02:00", "04:00"), ("01:00", "03:00"))
    assert has_conflict(time_windows) == expected_conflict

def test_conflict_at_end():
    """Test conflict detection when the conflict is at the end of the list."""
    time_windows = [("01:00", "02:00"), ("02:00", "04:00"), ("03:00", "05:00")]
    expected_conflict = (("03:00", "05:00"), ("02:00", "04:00"))
    assert has_conflict(time_windows) == expected_conflict

def test_no_conflict_single_window():
    """Test with only a single time window (no possible conflict)."""
    time_windows = [("01:00", "02:00")]
    assert has_conflict(time_windows) is None

def test_conflict_with_identical_start_times():
    """Test conflict detection when two windows have identical start times."""
    time_windows = [("01:00", "02:00"), ("01:00", "03:00")]
    expected_conflict = (("01:00", "03:00"), ("01:00", "02:00"))
    assert has_conflict(time_windows) == expected_conflict

def test_empty_input():
    """Test the function with an empty input."""
    time_windows = []
    assert has_conflict(time_windows) is None

def test_conflict_with_exact_overlap():
    """Test when one time window exactly overlaps another."""
    time_windows = [("01:00", "03:00"), ("01:00", "03:00")]
    expected_conflict = (("01:00", "03:00"), ("01:00", "03:00"))
    assert has_conflict(time_windows) == expected_conflict