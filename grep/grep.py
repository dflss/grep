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


def _is_binary(file: Path):
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


def grep(
    pattern: str,
    files: list[str],
    recursive: bool,
    ignore_case: bool,
    invert_match: bool,
    word: bool,
    print_line_number: bool,
    number_of_lines_before_match: int,
    number_of_lines_after_match: int,
) -> None:
    printer = Printer(
        print_line_number=print_line_number,
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
        if not directory_path.is_dir():
            print(f"{directory}: directory does not exist")
            return
        files = _get_all_files_in_directory(directory_path)

    if recursive or len(files) > 0:
        for file in files:
            file = Path(file)
            if len(files) > 1 or recursive:
                printer.set_current_file(file)
            if not file.is_file():
                printer.print_warning(f"{file}: file does not exist")
                continue
            if _is_binary(file):
                printer.print_warning(f"{file}: file is binary")
                continue

            line_iterator = _read_file_by_line(file)
            matching_lines_iterator = find_matching_lines(
                pattern,
                line_iterator,
                number_of_lines_before_match,
                number_of_lines_after_match,
            )
            for line in matching_lines_iterator:
                printer.print_line(line)

    else:
        matching_lines_iterator = find_matching_lines(
            pattern,
            sys.stdin,
            number_of_lines_before_match,
            number_of_lines_after_match,
        )
        for line in matching_lines_iterator:
            printer.print_line(line)
