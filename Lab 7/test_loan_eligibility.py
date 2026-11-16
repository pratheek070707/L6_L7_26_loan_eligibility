
from hypothesis import given, strategies as st

from loan_eligibility import (
    parse_income,
    monthly_emi,
    pan_category
)


# Test 1: Income parsing
@given(st.text() | st.none())
def test_parse_income_no_crash(s):
    try:
        parse_income(s)
    except Exception as e:
        assert False, f"parse_income crashed with input {s!r}: {e}"


# Test 2: Monthly EMI calculation
@given(st.text() | st.none())
def test_monthly_emi_no_crash(s):
    try:
        monthly_emi(s)
    except Exception as e:
        assert False, f"monthly_emi crashed with input {s!r}: {e}"


# Test 3: PAN category identification
@given(st.text() | st.none())
def test_pan_category_no_crash(s):
    try:
        pan_category(s)
    except Exception as e:
        assert False, f"pan_category crashed with input {s!r}: {e}"
