import sys
from collections import deque
from collections.abc import Generator
from pathlib import Path

from printer import Printer
from search import find_matching_lines


def _read_file_by_line(path: Path) -> Generator[str, None, None]:
    with open(path, "r") as file:
        for line in file:
            yield line


def _get_all_files_in_directory(directory: Path) -> Generator[Path, None, None]:
    if not directory.is_dir():
        raise ValueError(f"Directory {directory} does not exist")

    directory_queue = deque([directory])

    while len(directory_queue) > 0:
        current_dir = directory_queue.popleft()
        for path in current_dir.iterdir():
            if path.is_file():
                yield path
            elif path.is_dir():
                directory_queue.append(path)


def grep(
    pattern: str,
    files: list[str],
    recursive: bool,
    print_line_number: bool,
    number_of_lines_before_match: int,
    number_of_lines_after_match: int,
) -> None:
    printer = Printer(print_line_number=print_line_number)

    if recursive:
        if len(files) > 1:
            printer.print_message(
                "Only one directory can be searched in recursive mode!"
            )
            return
        directory = files[0] if len(files) > 0 else "."
        directory_path = Path(directory)
        if not directory_path.is_dir():
            printer.print_message(
                f"{directory}: directory does not exist or is not a directory"
            )
            return
        files = _get_all_files_in_directory(directory_path)

    if recursive or len(files) > 0:
        for file in files:
            file_path = Path(file)
            # No need to set file if there is only one file to be searched.
            if recursive or len(files) > 1:
                printer.set_file(file_path)
            if not file_path.is_file():
                printer.print_message(f"{file_path}: file does not exist")
                continue

            line_iterator = _read_file_by_line(file_path)
            matching_lines_iterator = find_matching_lines(
                pattern,
                line_iterator,
                number_of_lines_before_match,
                number_of_lines_after_match,
            )
            try:
                for line in matching_lines_iterator:
                    printer.print_line(line)
            except UnicodeDecodeError:
                printer.print_message(f"{file_path}: file is binary")

    else:
        matching_lines_iterator = find_matching_lines(
            pattern,
            sys.stdin,
            number_of_lines_before_match,
            number_of_lines_after_match,
        )
        for line in matching_lines_iterator:
            printer.print_line(line)
