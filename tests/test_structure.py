import pytest
import sys

sys.path.insert(0, '../src')
from structures import capital_case, movingAverage, valid_parens, canAttendMeetings, heap


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

@pytest.mark.parametrize("list, num, expected", [
    ([1,2,3,4,5,6],2, [1.5,2.5,3.5,4.5,5.5])
])

def test_moving_average(list, num, expected):
    assert movingAverage(list, num) == expected

def test_heap():
    assert heap() == [1,1,2,3,[5,7,8]]



def test_capital_case():
    assert capital_case('semaphore') == 'Semaphore'
