from collections.abc import Iterable

from line import Line
from colorama import Fore, Style


class Printer:
    def __init__(
        self, print_filename: bool, print_line_number: bool, only_text_files: bool
    ):
        self.is_first_file = True
        self.print_filename = print_filename
        self.print_line_number = print_line_number
        self.only_text_files = only_text_files

    def format_line(self, line: Line):
        output = ""
        previous_interval_end = 0
        for interval in line.matching_intervals:
            if interval.start > 0:
                output += line.text[previous_interval_end : interval.start]
            output += (
                Fore.RED + line.text[interval.start : interval.end] + Style.RESET_ALL
            )
            previous_interval_end = interval.end
        if previous_interval_end < len(line.text):
            output += line.text[previous_interval_end:]
        return output

    def format_separator(self):
        return Fore.LIGHTBLUE_EX + "--" + Style.RESET_ALL

    def print_output(self, lines_iterator: Iterable[Line], file):
        try:
            previous_line_index = -1
            for line in lines_iterator:
                if (line.index > previous_line_index + 1) or (
                    line.index == 0 and not self.is_first_file
                ):
                    print(self.format_separator())
                    self.is_first_file = False
                previous_line_index = line.index
                output = ""
                if self.print_filename:
                    output += f"{Fore.LIGHTMAGENTA_EX}{file}{Fore.LIGHTBLUE_EX}:{Style.RESET_ALL}"
                if self.print_line_number:
                    output += f"{Fore.LIGHTCYAN_EX}{line.index + 1}{Fore.LIGHTBLUE_EX}:{Style.RESET_ALL}"
                output += self.format_line(line)
                print(output)
        except UnicodeDecodeError:
            if not self.only_text_files:
                if not self.is_first_file:
                    print(self.format_separator())
                else:
                    print(f"{file}: not a text file")
                    self.is_first_file = False
