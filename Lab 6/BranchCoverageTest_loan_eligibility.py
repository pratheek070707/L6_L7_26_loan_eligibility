
import pytest
from loan_eligibility import credit_band, is_eligible, interest_rate


# Credit band: test every decision outcome
@pytest.mark.parametrize("score, expected", [
    (299, None),
    (300, "poor"),
    (549, "poor"),
    (550, "fair"),
    (649, "fair"),
    (650, "good"),
    (749, "good"),
    (750, "excellent"),
    (900, "excellent"),
    (901, None),
])
def test_credit_band_branches(score, expected):
    if expected is None:
        with pytest.raises(ValueError):
            credit_band(score)
    else:
        assert credit_band(score) == expected


# Employment validation
def test_unknown_employment_branch():
    with pytest.raises(ValueError):
        is_eligible(30, 50000, "unemployed", 800)


# Age decision branches
@pytest.mark.parametrize("age, expected", [
    (20, False),
    (21, True),
    (30, True),
    (60, True),
    (61, False),
])
def test_age_branches(age, expected):
    assert is_eligible(age, 50000, "salaried", 800) is expected


# Income decision branches
def test_salaried_income_below_minimum():
    assert is_eligible(30, 24999, "salaried", 800) is False


def test_salaried_income_at_minimum():
    assert is_eligible(30, 25000, "salaried", 800) is True


def test_self_employed_income_below_minimum():
    assert is_eligible(30, 39999, "self_employed", 800) is False


def test_self_employed_income_at_minimum():
    assert is_eligible(30, 40000, "self_employed", 800) is True


# Credit eligibility branches
def test_poor_credit_branch():
    assert is_eligible(30, 50000, "salaried", 500) is False


def test_good_credit_branch():
    assert is_eligible(30, 50000, "salaried", 700) is True


# Interest rate branches
@pytest.mark.parametrize("score, expected", [
    (800, 8),
    (700, 10),
    (600, 13),
    (500, 13),
])
def test_interest_rate_credit_branches(score, expected):
    assert interest_rate(score, "salaried", False) == expected


# Employment adjustment branches
def test_salaried_rate_branch():
    assert interest_rate(800, "salaried", False) == 8


def test_self_employed_rate_branch():
    assert interest_rate(800, "self_employed", False) == 9


# Collateral adjustment branches
def test_without_collateral():
    assert interest_rate(800, "salaried", False) == 8


def test_with_collateral():
    assert interest_rate(800, "salaried", True) == 6


def test_self_employed_with_collateral():
    assert interest_rate(700, "self_employed", True) == 9
