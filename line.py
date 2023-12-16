from dataclasses import dataclass
from colorama import Fore, Style


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

    def __str__(self):
        output = ""
        previous_interval_end = 0
        for interval in self.matching_intervals:
            if interval.start > 0:
                output += self.text[previous_interval_end : interval.start]
            output += (
                Fore.RED + self.text[interval.start : interval.end] + Style.RESET_ALL
            )
            previous_interval_end = interval.end
        if previous_interval_end < len(self.text):
            output += self.text[previous_interval_end:]
        return output
