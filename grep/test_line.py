import pytest

from line import Interval


@pytest.mark.parametrize(
    "start,end",
    [
        pytest.param(
            -1,
            1,
            id="start_smaller_than_zero",
        ),
        pytest.param(
            0,
            -1,
            id="end_smaller_than_zero",
        ),
        pytest.param(
            -1,
            -1,
            id="start_and_end_smaller_than_zero",
        ),
        pytest.param(
            1,
            1,
            id="start_and_end_equal",
        ),
        pytest.param(
            2,
            1,
            id="start_greater_than_end",
        ),
    ],
)
def test_interval_validation_fail(start: int, end: int):
    with pytest.raises(ValueError):
        Interval(start, end)


def test_interval_validation_success():
    interval = Interval(0, 1)

    assert interval.start == 0 and interval.end == 1
