
import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate


# Credit band tests
def test_credit_band_excellent():
    assert credit_band(800) == "excellent"


def test_credit_band_good():
    assert credit_band(700) == "good"


def test_credit_band_fair():
    assert credit_band(600) == "fair"


def test_credit_band_poor():
    assert credit_band(500) == "poor"


def test_credit_band_minimum_valid():
    assert credit_band(300) == "poor"


def test_credit_band_maximum_valid():
    assert credit_band(900) == "excellent"


def test_credit_band_below_range():
    with pytest.raises(ValueError):
        credit_band(299)


def test_credit_band_above_range():
    with pytest.raises(ValueError):
        credit_band(901)


# Loan eligibility tests
def test_unknown_employment():
    with pytest.raises(ValueError):
        is_eligible(30, 50000, "unemployed", 800)


def test_age_below_limit():
    assert is_eligible(20, 50000, "salaried", 800) is False


def test_age_above_limit():
    assert is_eligible(61, 50000, "salaried", 800) is False


def test_minimum_age_eligible():
    assert is_eligible(21, 50000, "salaried", 800) is True


def test_maximum_age_eligible():
    assert is_eligible(60, 50000, "salaried", 800) is True


def test_low_salaried_income():
    assert is_eligible(30, 24999, "salaried", 800) is False


def test_low_self_employed_income():
    assert is_eligible(30, 39999, "self_employed", 800) is False


def test_poor_credit_not_eligible():
    assert is_eligible(30, 50000, "salaried", 500) is False


def test_salaried_eligible():
    assert is_eligible(30, 50000, "salaried", 800) is True


def test_self_employed_eligible():
    assert is_eligible(30, 50000, "self_employed", 700) is True


# Interest rate tests
def test_excellent_interest_rate():
    assert interest_rate(800, "salaried", False) == 8


def test_good_interest_rate():
    assert interest_rate(700, "salaried", False) == 10


def test_fair_interest_rate():
    assert interest_rate(600, "salaried", False) == 13


def test_self_employed_interest_rate():
    assert interest_rate(800, "self_employed", False) == 9


def test_collateral_discount():
    assert interest_rate(800, "salaried", True) == 6


def test_both_adjustments():
    assert interest_rate(700, "self_employed", True) == 9
