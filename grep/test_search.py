from typing import Iterable

import pytest

from line import Interval, Line
from search import find_matching_lines


def compare_iterator_with_expected_output(
    iterator_to_test: Iterable[Line], expected_output: list[Line]
):
    range_index = 0
    for actual in iterator_to_test:
        assert range_index + 1 <= len(
            expected_output
        ), "Too many values returned from range"
        assert expected_output[range_index] == actual
        range_index += 1

    assert range_index == len(expected_output), "Too few values returned from range"


@pytest.mark.parametrize(
    "regex,lines,number_of_lines_before_match,number_of_lines_after_match,expected_result",
    [
        pytest.param(
            "test",
            ["test", "not a match"],
            0,
            0,
            [Line("test", [Interval(0, 4)], 0)],
            id="one_match",
        ),
        pytest.param(
            "test",
            ["test", "not a match", "test", "test"],
            0,
            0,
            [
                Line("test", [Interval(0, 4)], 0),
                Line("test", [Interval(0, 4)], 2),
                Line("test", [Interval(0, 4)], 3),
            ],
            id="multiple_matches",
        ),
        pytest.param(
            "test",
            ["test", "not a match", "test test", "test and !test! and some more test"],
            0,
            0,
            [
                Line("test", [Interval(0, 4)], 0),
                Line("test test", [Interval(0, 4), Interval(5, 9)], 2),
                Line(
                    "test and !test! and some more test",
                    [Interval(0, 4), Interval(10, 14), Interval(30, 34)],
                    3,
                ),
            ],
            id="multiple_matches_per_line",
        ),
        pytest.param(
            "test",
            ["not a match", "also not a match"],
            0,
            0,
            [],
            id="no_matches",
        ),
        pytest.param(
            "test",
            ["test", "not a match"],
            1,
            0,
            [Line("test", [Interval(0, 4)], 0)],
            id="match_on_first_line_with_before_lines",
        ),
        pytest.param(
            "test",
            ["not a match 1", "not a match 2", "test", "not a match 3"],
            1,
            0,
            [Line("not a match 2", [], 1), Line("test", [Interval(0, 4)], 2)],
            id="match_on_middle_line_with_before_lines",
        ),
        pytest.param(
            "test",
            ["not a match 1", "not a match 2", "test"],
            0,
            2,
            [Line("test", [Interval(0, 4)], 2)],
            id="match_on_last_line_with_after_lines",
        ),
        pytest.param(
            "test",
            [
                "not a match 1",
                "not a match 2",
                "test",
                "not a match 3",
                "not a match 4",
                "not a match 5",
            ],
            0,
            2,
            [
                Line("test", [Interval(0, 4)], 2),
                Line("not a match 3", [], 3),
                Line("not a match 4", [], 4),
            ],
            id="match_on_middle_line_with_after_lines",
        ),
        pytest.param(
            "test",
            [
                "not a match 1",
                "not a match 2",
                "test",
                "not a match 3",
                "not a match 4",
                "not a match 5",
            ],
            2,
            2,
            [
                Line("not a match 1", [], 0),
                Line("not a match 2", [], 1),
                Line("test", [Interval(0, 4)], 2),
                Line("not a match 3", [], 3),
                Line("not a match 4", [], 4),
            ],
            id="match_on_middle_line_with_before_and_after_lines",
        ),
        pytest.param(
            "test",
            [
                "not a match 1",
                "not a match 2",
                "test",
                "test2",
                "not a match 3",
                "not a match 4",
                "not a match 5",
            ],
            2,
            2,
            [
                Line("not a match 1", [], 0),
                Line("not a match 2", [], 1),
                Line("test", [Interval(0, 4)], 2),
                Line("test2", [Interval(0, 4)], 3),
                Line("not a match 3", [], 4),
                Line("not a match 4", [], 5),
            ],
            id="consecutive_matches_with_overlapping_before_and_after_lines",
        ),
        pytest.param(
            "test",
            [
                "not a match 1",
                "not a match 2",
                "test",
                "not a match 3",
                "not a match 4",
                "test2",
                "not a match 5",
            ],
            2,
            2,
            [
                Line("not a match 1", [], 0),
                Line("not a match 2", [], 1),
                Line("test", [Interval(0, 4)], 2),
                Line("not a match 3", [], 3),
                Line("not a match 4", [], 4),
                Line("test2", [Interval(0, 4)], 5),
                Line("not a match 5", [], 6),
            ],
            id="non_consecutive_matches_with_overlapping_before_and_after_lines",
        ),
        pytest.param(
            "test",
            [
                "not a match 1",
                "not a match 2",
                "test",
                "not a match 3",
                "not a match 4",
                "not a match 5",
                "test2",
                "not a match 6",
                "not a match 7",
            ],
            1,
            1,
            [
                Line("not a match 2", [], 1),
                Line("test", [Interval(0, 4)], 2),
                Line("not a match 3", [], 3),
                Line("not a match 5", [], 5),
                Line("test2", [Interval(0, 4)], 6),
                Line("not a match 6", [], 7),
            ],
            id="non_consecutive_matches_with_non_overlapping_before_and_after_lines",
        ),
    ],
)
def test_find_matching_lines(
    regex: str,
    lines: list[str],
    number_of_lines_before_match: int,
    number_of_lines_after_match: int,
    expected_result: list[Line],
):
    generator = find_matching_lines(
        regex=regex,
        lines=lines,
        number_of_lines_before_match=number_of_lines_before_match,
        number_of_lines_after_match=number_of_lines_after_match,
    )

    compare_iterator_with_expected_output(
        generator,
        expected_result,
    )
