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
    """Find matching lines in a given iterable of lines.

    Parameters
    ----------
    regex : Regex pattern to search for.
    lines : Iterable of lines to search.
    before_context : Number of lines to include before a match.
    after_context : Number of lines to include after a match.

    Returns
    -------
    Generator of matching lines.
    """
    previous_lines = deque(maxlen=before_context)
    last_matched_line_index = -1

    for i, current_line in enumerate(lines):
        matching_intervals = _get_matching_intervals(regex, current_line)
        current_line = current_line.rstrip("\r\n")

        if len(matching_intervals) > 0:
            while len(previous_lines) > 0:
                yield previous_lines.pop()
            yield Line(current_line, matching_intervals, i)
            last_matched_line_index = i
        else:
            if before_context > 0 and before_context == len(previous_lines):
                previous_lines.popleft()
            if len(previous_lines) < before_context:
                previous_lines.append(Line(current_line, [], i))
            if (
                last_matched_line_index >= 0
                and i - last_matched_line_index <= after_context
            ):
                yield Line(current_line, [], i)
