from dataclasses import dataclass


@dataclass
class Interval:
    """An interval indicated by start and end indices."""

    start: int
    end: int

    def __post_init__(self):
        if self.start >= self.end:
            raise ValueError("Start index must be before end index!")
        if self.start < 0:
            raise ValueError("Start index must be non-negative!")
        if self.end < 0:
            raise ValueError("End index must be non-negative!")


@dataclass
class Line:
    """A line of text."""

    text: str
    matching_intervals: list[Interval]
    index: int
