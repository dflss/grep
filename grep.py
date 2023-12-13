import re
import sys
from collections import deque
from collections.abc import Generator, Iterable
from dataclasses import dataclass
from typing import Optional

from colorama import Fore, Style


@dataclass
class Interval:
    """An interval indicated by start and end indices."""
    start: int
    end: int


@dataclass
class MatchingLine:
    """A line that matches the pattern."""
    text: str
    intervals_matched: list[Interval]
    before_context: list[str]
    after_context: list[str]


def _raise_if_not_text_file(path: str) -> None:
    pass


def _read_files_by_line(paths: Iterable[str]) -> Generator[str, None, None]:
    yield "test line"


def _get_subpaths(path: str) -> Generator[str, None, None]:
    yield "test_path"


def _process_line(regex: str, line: str) -> Optional[MatchingLine]:
    matches = re.finditer(regex, line)
    intervals = []
    for match in matches:
        intervals.append(Interval(match.start(), match.end()))
    if len(intervals) > 0:
        return MatchingLine(line, intervals, before_context=[], after_context=[])
    return None

def _find_matching_lines(
    regex: str, lines: Iterable[str], before_context: int, after_context: int
) -> Generator[MatchingLine, None, None]:
    window_size = before_context + after_context + 1
    window_before = deque(maxlen=before_context)
    window_after = deque(maxlen=after_context)
    current_line = None

    for i, line in enumerate(lines):
        if i == 0:
            current_line = line
        elif i <= after_context:
            window_after.append(line)
            if i == after_context:
                # process line
                matching_line = _process_line(regex, current_line)
                if matching_line is not None:
                    # Add before context and after context if needed
                    yield matching_line
        else:
            if len(window_before) == before_context:
                window_before.popleft()
            window_before.append(current_line)
            current_line = window_after.popleft()
            window_after.append(line)
        print("i", i)
        print("before", window_before)
        print("current", current_line)
        print("after", window_after)
        print("*******")

    # process lines in window_after




def _print_matching_lines(lines: Iterable[MatchingLine]) -> None:
    for line in lines:
        output = ""
        previous_interval_end = 0
        for interval in line.intervals_matched:
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
