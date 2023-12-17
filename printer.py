from pathlib import Path

from colorama import Fore, Style

from line import Line


def is_binary(file: Path):
    """Return true if the given filename is binary.

    Parameters
    ----------
    file :

    Returns
    -------
    True if the given filename is binary, False otherwise.
    """

    file = open(file, "rb")
    try:
        chunk_size = 1024
        while 1:
            chunk = file.read(chunk_size)
            if b"\0" in chunk:
                return True
            if len(chunk) < chunk_size:
                break
    finally:
        file.close()

    return False


class Printer:
    """A class used to print matching lines."""

    def __init__(self, print_filename: bool, print_line_number: bool) -> None:
        """Create a new Printer instance.

        Parameters
        ----------
        print_filename : Indicates whether the filename should be printed for each line.
        print_line_number : Indicates whether the line number should be printed for each line.
        """
        # Configurable settings
        self.print_filename = print_filename
        self.print_line_number = print_line_number

        # Color settings
        self.matched_text_color = Fore.RED
        self.filename_color = Fore.LIGHTMAGENTA_EX
        self.separator_color = Fore.LIGHTBLUE_EX
        self.line_number_color = Fore.LIGHTCYAN_EX
        self.default_color = Style.RESET_ALL

        self._is_first_file = True  # Used to correctly print the separator.
        self._current_file = None
        self._previous_line_index = -1

    def _print_file_warning(self, message: str) -> None:
        if not self._is_first_file:
            print(self._format_separator())
        else:
            print(f"{self._current_file}: {message}")
            self._is_first_file = False

    def _format_separator(self) -> str:
        return self.separator_color + "--" + self.default_color

    def _format_line(self, line: Line) -> str:
        output = ""
        previous_interval_end = 0
        for interval in line.matching_intervals:
            if interval.start > 0:
                output += line.text[previous_interval_end : interval.start]
            output += (
                self.matched_text_color
                + line.text[interval.start : interval.end]
                + self.default_color
            )
            previous_interval_end = interval.end
        if previous_interval_end < len(line.text):
            output += line.text[previous_interval_end:]
        return output

    def set_current_file(self, file: Path) -> bool:
        """Set the file to be printed.

        Parameters
        ----------
        file : Path of the file to be printed.

        Returns
        -------
        True if file was set successfully, False otherwise.
        """
        self._current_file = file
        if not file.is_file():
            self._print_file_warning("file does not exist")
            return False
        if is_binary(file):
            self._print_file_warning("file is binary")
            return False
        return True

    def print_line(self, line: Line) -> None:
        """

        Parameters
        ----------
        line : Line to be printed.

        Returns
        -------
        None
        """
        if (line.index > self._previous_line_index + 1) or (
            line.index == 0 and not self._is_first_file
        ):
            print(self._format_separator())
            self._is_first_file = False

        self._previous_line_index = line.index

        output_line = ""
        if self.print_filename:
            output_line += f"{self.filename_color}{self._current_file}{self.separator_color}:{self.default_color}"
        if self.print_line_number:
            output_line += f"{self.line_number_color}{line.index + 1}{self.separator_color}:{self.default_color}"
        output_line += self._format_line(line)

        print(output_line)
