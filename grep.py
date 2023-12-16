import re
import sys
from collections import deque
from collections.abc import Generator, Iterable
from dataclasses import dataclass

from colorama import Fore, Style


@dataclass
class Interval:
    """An interval indicated by start and end indices."""
    start: int
    end: int


@dataclass
class Line:
    """A line of text."""
    text: str
    matching_intervals: list[Interval]


def _raise_if_not_text_file(path: str) -> None:
    pass


def _read_files_by_line(paths: Iterable[str]) -> Generator[str, None, None]:
    yield "test line"


def _get_subpaths(path: str) -> Generator[str, None, None]:
    yield "test_path"


def _get_matching_intervals(regex: str, line: str) -> list[Interval]:
    matches = re.finditer(regex, line)
    return [Interval(match.start(), match.end()) for match in matches]


def _find_matching_lines(
    regex: str, lines: Iterable[str], before_context: int, after_context: int
) -> Generator[Line, None, None]:
    previous_lines = deque(maxlen=before_context)
    last_matched_line_index = -1

    for i, current_line in enumerate(lines):
        matching_intervals = _get_matching_intervals(regex, current_line)
        current_line = current_line.rstrip("\r\n")
        # Line is a match
        if len(matching_intervals) > 0:
            while len(previous_lines) > 0:
                # Yield all lines that are part of before context for this line
                yield previous_lines.pop()
            yield Line(current_line, matching_intervals)
            last_matched_line_index = i
        # Line is not a match
        else:
            # Remove oldest previous line
            if 0 < before_context == len(previous_lines):
                previous_lines.popleft()
            # Add current line to previous lines
            if len(previous_lines) < before_context:
                previous_lines.append(Line(current_line, []))
            # Yield current line if it's a part of after context for the previously matched line
            if last_matched_line_index >= 0 and i - last_matched_line_index <= after_context:
                yield Line(current_line, [])


def _print_matching_lines(lines: Iterable[Line]) -> None:
    for line in lines:
        output = ""
        previous_interval_end = 0
        for interval in line.matching_intervals:
            if interval.start > 0:
                output += line.text[previous_interval_end:interval.start]
            output += Fore.RED + line.text[interval.start:interval.end] + Style.RESET_ALL
            previous_interval_end = interval.end
        if previous_interval_end < len(line.text):
            output += line.text[previous_interval_end:]
        print(output)


def grep(
    pattern: str,
    files: list[str],
    recursive: bool,
    ignore_case: bool,
    invert_match: bool,
    word: bool,
    before_context: int,
    after_context: int,
) -> None:
    if recursive:
        subpaths = _get_subpaths(files[0])
        file_iterator = _read_files_by_line(subpaths)
    elif files is not None:
        file_iterator = _read_files_by_line(files)
    else:
        file_iterator = sys.stdin

    if ignore_case:
        pattern = fr"(?i){pattern}"
    if word:
        pattern = fr"\b{pattern}\b"
    if invert_match:
        pattern = fr"^((?!{pattern}).)*$"

    matching_lines_iterator = _find_matching_lines(pattern, file_iterator, before_context, after_context)
    _print_matching_lines(matching_lines_iterator)
