from dataclasses import dataclass


@dataclass
class Interval:
    """An interval indicated by start and end indices."""

    start: int
    end: int
    # post init spr czy start < end i >= 0


@dataclass
class Line:
    """A line of text."""

    text: str
    matching_intervals: list[Interval]
    index: int
