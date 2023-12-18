import pytest

from src.line import Interval, Line


@pytest.mark.parametrize(
    "start,end,error_message",
    [
        pytest.param(
            -1,
            1,
            "Start index must be non-negative!",
            id="start_smaller_than_zero",
        ),
        pytest.param(
            0,
            -1,
            "Start index must be before end index!",
            id="end_smaller_than_zero",
        ),
        pytest.param(
            -1,
            -2,
            "Start index must be before end index!",
            id="start_and_end_smaller_than_zero",
        ),
        pytest.param(
            1,
            1,
            "Start index must be before end index!",
            id="start_and_end_equal",
        ),
        pytest.param(
            2,
            1,
            "Start index must be before end index!",
            id="start_greater_than_end",
        ),
    ],
)
def test_interval_validation_fail(start: int, end: int, error_message: str):
    with pytest.raises(ValueError, match=error_message):
        Interval(start, end)


def test_interval_validation_success():
    interval = Interval(0, 1)

    assert interval.start == 0 and interval.end == 1


@pytest.mark.parametrize(
    "text,matching_intervals,index,error_message",
    [
        pytest.param(
            "test",
            [Interval(0, 5)],
            0,
            "Interval index is out of bounds!",
            id="interval_out_of_bounds",
        ),
        pytest.param(
            "test",
            [Interval(0, 4)],
            -1,
            "Index must be non-negative!",
            id="index_smaller_than_zero",
        ),
    ],
)
def test_line_validation_fail(
    text: str, matching_intervals: list[Interval], index: int, error_message: str
):
    with pytest.raises(ValueError, match=error_message):
        Line(text, matching_intervals, index)


def test_line_validation_success():
    line = Line("test", [Interval(0, 1)], 0)

    assert line.text == "test"
    assert line.matching_intervals == [Interval(0, 1)]
    assert line.index == 0
