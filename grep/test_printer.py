from pathlib import Path

import pytest

from line import Interval, Line
from printer import Printer


@pytest.mark.parametrize(
    "lines,expected_output",
    [
        pytest.param(
            [Line("test", [Interval(0, 4)], 0)],
            f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n",
            id="match_entire_line",
        ),
        pytest.param(
            [Line("test", [], 0)],
            "test\n",
            id="no_match",
        ),
        pytest.param(
            [
                Line(
                    "test and !test! and some more test",
                    [Interval(0, 4), Interval(10, 14), Interval(30, 34)],
                    0,
                )
            ],
            f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR} and !{Printer.MATCHED_TEXT_COLOR}test"
            f"{Printer.DEFAULT_COLOR}! and some more {Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n",
            id="mutiple_matches_in_line",
        ),
        pytest.param(
            [
                Line("test", [Interval(0, 4)], 0),
                Line("test", [Interval(0, 4)], 1),
            ],
            f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
            f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n",
            id="matches_in_consecutive_lines",
        ),
        pytest.param(
            [
                Line("test", [Interval(0, 4)], 0),
                Line("test", [Interval(0, 4)], 2),
            ],
            f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
            f"{Printer.SEPARATOR_COLOR}--{Printer.DEFAULT_COLOR}\n"
            f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n",
            id="matches_in_non_consecutive_lines",
        ),
    ],
)
def test_print_line(
    capsys,
    lines,
    expected_output,
):
    printer = Printer(print_line_number=False)

    for line in lines:
        printer.print_line(line)

    captured = capsys.readouterr()
    assert captured.out == expected_output


def test_print_line_with_line_number(capsys):
    printer = Printer(print_line_number=True)
    line = Line("test", [Interval(0, 4)], 0)

    printer.print_line(line)

    captured = capsys.readouterr()
    assert captured.out == (
        f"{Printer.LINE_NUMBER_COLOR}1{Printer.SEPARATOR_COLOR}:{Printer.DEFAULT_COLOR}"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
    )


def test_print_line_with_filename(capsys):
    printer = Printer(print_line_number=False)
    printer.set_file(Path("test"))
    line = Line("test", [Interval(0, 4)], 0)

    printer.print_line(line)

    captured = capsys.readouterr()
    assert captured.out == (
        f"{Printer.FILENAME_COLOR}test{Printer.SEPARATOR_COLOR}:{Printer.DEFAULT_COLOR}"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
    )


def test_print_line_with_filename_and_line_number(capsys):
    printer = Printer(print_line_number=True)
    printer.set_file(Path("test"))
    line = Line("test", [Interval(0, 4)], 0)

    printer.print_line(line)

    captured = capsys.readouterr()
    assert captured.out == (
        f"{Printer.FILENAME_COLOR}test{Printer.SEPARATOR_COLOR}:{Printer.DEFAULT_COLOR}"
        f"{Printer.LINE_NUMBER_COLOR}1{Printer.SEPARATOR_COLOR}:{Printer.DEFAULT_COLOR}"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
    )


def test_print_message(capsys):
    printer = Printer(print_line_number=False)
    message = "test message"

    printer.print_message(message)
    printer.print_message(message)

    captured = capsys.readouterr()
    assert (
        captured.out
        == f"{message}\n{Printer.SEPARATOR_COLOR}--{Printer.DEFAULT_COLOR}\n{message}\n"
    )
