from fractions import Fraction as F
import pytest
from sketchcheck import evaluate, derivative, rational_roots, end_behaviour, turning_point_count, check_sketch


def test_evaluate():
    assert evaluate([1, -3, 2], 2) == 0
    assert evaluate([F(1, 2), 0, 1], 2) == 3


def test_derivative():
    assert derivative([1, -3, 2]) == [2, -3]
    assert derivative([5]) == [0]


def test_roots_quadratic():
    assert rational_roots([1, -3, 2]) == [1, 2]


def test_roots_with_zero_root_and_fractions():
    assert rational_roots([2, -1, 0]) == [0, F(1, 2)]


def test_roots_cubic():
    # (x - 1)(x + 2)(x - 3) = x^3 - 2x^2 - 5x + 6
    assert rational_roots([1, -2, -5, 6]) == [-2, 1, 3]


def test_no_rational_roots():
    assert rational_roots([1, 0, -2]) == []


def test_end_behaviour():
    assert end_behaviour([1, 0, 0]) == ("up", "up")
    assert end_behaviour([-1, 0, 0, 0]) == ("up", "down")
    assert end_behaviour([2, 1]) == ("down", "up")


def test_turning_points():
    assert turning_point_count([1, 1]) == 0
    assert turning_point_count([1, 0, 0]) == 1
    assert turning_point_count([1, 0, -3, 0]) == 2
    assert turning_point_count([1, 0, 3, 0]) == 0


def test_check_good_sketch():
    assert check_sketch([1, -3, 2], {"y_intercept": 2, "roots": [1, 2], "end": ("up", "up"), "points": [(3, 2)]}) == []


def test_check_bad_sketch():
    p = check_sketch([1, -3, 2], {"y_intercept": -2, "roots": [1], "end": ("down", "down"), "points": [(0, 0)]})
    assert len(p) == 4


def test_extra_claimed_root():
    assert any("not on the x-axis" in s for s in check_sketch([1, -3, 2], {"roots": [1, 2, 3]}))


def test_zero_polynomial():
    with pytest.raises(ValueError):
        evaluate([0, 0], 1)
