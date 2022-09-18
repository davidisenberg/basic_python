import pytest
import sys

sys.path.insert(0, '../src')
from structures import capital_case, valid_parens


@pytest.mark.parametrize("input,expected", [
    ("[()]", True),
    ("}{", False),
    ("())", False),
    ("[]{}()", True),
    ("()[", False)
])

def test_parens(input, expected):
    assert  valid_parens(input) == expected  


def test_capital_case():
    assert capital_case('semaphore') == 'Semaphore'
