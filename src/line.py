from dataclasses import dataclass


@dataclass
class Interval:
    """An interval indicated by start and end indices.

    Attributes
    ----------
    start : Start index (inclusive).
    end : End index (exclusive).
    """

    start: int
    end: int

    def __post_init__(self):
        if self.start >= self.end:
            raise ValueError("Start index must be before end index!")
        if self.start < 0:
            raise ValueError("Start index must be non-negative!")


@dataclass
class Line:
    """A line of text.

    Attributes
    ----------
    text : Text of the line.
    matching_intervals : List of intervals in the line that match the given pattern.
    index : Index of the line in the file or input stream.
    """

    text: str
    matching_intervals: list[Interval]
    index: int

    def __post_init__(self):
        for interval in self.matching_intervals:
            if interval.end > len(self.text):
                raise ValueError("Interval index is out of bounds!")
        if self.index < 0:
            raise ValueError("Index must be non-negative!")
