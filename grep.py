import sys
from collections import deque
from collections.abc import Generator
from pathlib import Path

from printer import Printer
from search import find_matching_lines


def _read_file_by_line(path: str) -> Generator[str, None, None]:
    with open(path, "r") as file:
        for line in file:
            yield line


def _get_all_files_in_directory(directory: Path) -> Generator[str, None, None]:
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
    ignore_case: bool,
    invert_match: bool,
    word: bool,
    print_line_number: bool,
    ignore_binary_files: bool,
    before_context: int,
    after_context: int,
) -> None:
    print_filename = len(files) > 1 or recursive
    printer = Printer(
        print_filename=print_filename,
        print_line_number=print_line_number,
        ignore_binary_files=ignore_binary_files,
    )

    if ignore_case:
        pattern = rf"(?i){pattern}"
    if word:
        pattern = rf"\b{pattern}\b"
    if invert_match:
        pattern = rf"^((?!{pattern}).)*$"

    if recursive:
        directory = files[0] if len(files) > 0 else "."
        directory_path = Path(directory)
        files = _get_all_files_in_directory(directory_path)

    if recursive or len(files) > 0:
        for file in files:
            try:
                printer.set_current_file(file)
            except ValueError:
                continue
            line_iterator = _read_file_by_line(file)
            matching_lines_iterator = find_matching_lines(
                pattern, line_iterator, before_context, after_context
            )
            for line in matching_lines_iterator:
                printer.print_line(line)

    else:
        matching_lines_iterator = find_matching_lines(
            pattern, sys.stdin, before_context, after_context
        )
        for line in matching_lines_iterator:
            printer.print_line(line)
