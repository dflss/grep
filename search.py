import re

from collections import deque
from collections.abc import Generator, Iterable

from line import Interval, Line


def _get_matching_intervals(regex: str, line: str) -> list[Interval]:
    matches = re.finditer(regex, line)
    return [Interval(match.start(), match.end()) for match in matches]


def find_matching_lines(
    regex: str, lines: Iterable[str], before_context: int, after_context: int
) -> Generator[Line, None, None]:
    previous_lines = deque(maxlen=before_context)
    last_matched_line_index = -1

    for i, current_line in enumerate(lines):
        matching_intervals = _get_matching_intervals(regex, current_line)
        current_line = current_line.rstrip("\r\n")
        # Current line is a match
        if len(matching_intervals) > 0:
            while len(previous_lines) > 0:
                # Yield all lines that are part of before context for this line
                yield previous_lines.pop()
            yield Line(current_line, matching_intervals, i)
            last_matched_line_index = i
        # Current line is not a match
        else:
            # Remove the oldest previous line if previous_lines is full
            if before_context > 0 and before_context == len(previous_lines):
                previous_lines.popleft()
            # Add current line to previous lines
            if len(previous_lines) < before_context:
                previous_lines.append(Line(current_line, [], i))
            # Yield current line if it's a part of after context for the previously matched line
            if (
                last_matched_line_index >= 0
                and i - last_matched_line_index <= after_context
            ):
                yield Line(current_line, [], i)
