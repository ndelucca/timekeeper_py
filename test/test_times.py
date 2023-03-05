import pytest

from timekeeper.times import round_minutes


@pytest.mark.parametrize(
    "minutes,interval,expected",
    [
        (5, 15, 0),
        (25, 15, 15),
        (35, 10, 30),
    ],
)
def test_round_minutes(minutes: int, interval: int, expected: int) -> None:
    """Positive round minutes tests"""
    assert round_minutes(minutes, interval) == expected
