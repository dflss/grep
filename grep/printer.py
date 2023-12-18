from pathlib import Path

from colorama import Fore, Style

from line import Line


class Printer:
    """A class used to print matching lines."""

    MATCHED_TEXT_COLOR = Fore.RED
    FILENAME_COLOR = Fore.LIGHTMAGENTA_EX
    SEPARATOR_COLOR = Fore.LIGHTBLUE_EX
    LINE_NUMBER_COLOR = Fore.LIGHTCYAN_EX
    DEFAULT_COLOR = Style.RESET_ALL

    def __init__(self, print_line_number: bool) -> None:
        """Create a new Printer instance.

        Parameters
        ----------
        print_line_number : Indicates whether the line number should be printed for each line.
        """
        self.print_line_number: bool = print_line_number

        self._is_first_print: bool = True  # Used to correctly print the separator.
        self._file: Path | None = None
        self._previous_line_index: int = -1

    def _get_formatted_separator(self) -> str:
        return self.SEPARATOR_COLOR + "--" + self.DEFAULT_COLOR

    def _get_formatted_line(self, line: Line) -> str:
        output = ""
        previous_interval_end = 0
        for interval in line.matching_intervals:
            if interval.start > 0:
                output += line.text[previous_interval_end : interval.start]
            output += (
                self.MATCHED_TEXT_COLOR
                + line.text[interval.start : interval.end]
                + self.DEFAULT_COLOR
            )
            previous_interval_end = interval.end
        if previous_interval_end < len(line.text):
            output += line.text[previous_interval_end:]
        return output

    def set_file(self, file: Path) -> None:
        """Set the file to be printed.

        Parameters
        ----------
        file : Path of the file to be printed.
        """
        self._file = file

    def print_message(self, message: str) -> None:
        if not self._is_first_print:
            print(self._get_formatted_separator())
        else:
            self._is_first_print = False
        print(message)

    def print_line(self, line: Line) -> None:
        """Print the given line.

        Parameters
        ----------
        line : Line to be printed.
        """
        if (line.index > self._previous_line_index + 1) or (
            line.index == 0 and not self._is_first_print
        ):
            print(self._get_formatted_separator())

        self._is_first_print = False
        self._previous_line_index = line.index

        output_line = ""
        if self._file is not None:
            output_line += f"{self.FILENAME_COLOR}{self._file}{self.SEPARATOR_COLOR}:{self.DEFAULT_COLOR}"
        if self.print_line_number:
            output_line += f"{self.LINE_NUMBER_COLOR}{line.index + 1}{self.SEPARATOR_COLOR}:{self.DEFAULT_COLOR}"
        output_line += self._get_formatted_line(line)

        print(output_line)
