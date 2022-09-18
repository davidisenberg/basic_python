import pytest
import sys

sys.path.insert(0, '../src')
from structures import capital_case, valid_parens, canAttendMeetings


@pytest.mark.parametrize("input,expected", [
    ("[()]", True),
    ("}{", False),
    ("())", False),
    ("[]{}()", True),
    ("()[", False)
])

def test_parens(input, expected):
    assert  valid_parens(input) == expected  

@pytest.mark.parametrize("intervals_start_end,expected", [
    ([[1,3],[2,4]], False),
    ([[3,5],[1,3]], True)
])

def test_meeting_rooms(intervals_start_end, expected):
    assert  canAttendMeetings(intervals_start_end) == expected  


def test_capital_case():
    assert capital_case('semaphore') == 'Semaphore'
