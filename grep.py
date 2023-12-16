import sys
from collections import deque
from collections.abc import Generator
from pathlib import Path
from colorama import Fore, Style

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
    line_number: bool,
    only_text_files: bool,
    before_context: int,
    after_context: int,
) -> None:
    multiple_files = len(files) > 1 or recursive
    printer = Printer(
        print_filename=multiple_files,
        print_line_number=line_number,
        only_text_files=only_text_files,
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

    if len(files) > 0:
        for file_index, file in enumerate(files):
            line_iterator = _read_file_by_line(file)
            matching_lines_iterator = find_matching_lines(
                pattern, line_iterator, before_context, after_context
            )
            printer.print_output(matching_lines_iterator, file)
    else:
        matching_lines_iterator = find_matching_lines(
            pattern, sys.stdin, before_context, after_context
        )
        printer.print_output(matching_lines_iterator, None)
