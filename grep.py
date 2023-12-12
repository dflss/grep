from collections.abc import Generator, Iterable


def _raise_if_not_text_file(path: str) -> None:
    pass


def _read_files_by_line(paths: Iterable[str]) -> Generator[str, None, None]:
    yield "test_line"


def _get_subpaths(path: str) -> Generator[str, None, None]:
    yield "test_path"


def _find_matching_lines(
    regex: str, lines: Iterable[str]
) -> Generator[str, None, None]:
    yield "test_matching_line"


def _print_highlighted(lines: Iterable[str]) -> None:
    for line in lines:
        print(line)


def grep(
    pattern: str,
    files: list[str],
    recursive: bool,
    ignore_case: bool,
    invert_match: bool,
    word: bool,
    before_context: int,
    after_context: int,
) -> None:
    if recursive:
        subpaths = _get_subpaths(files[0])
        file_iterator = _read_files_by_line(subpaths)
    else:
        file_iterator = _read_files_by_line(files)

    matching_lines_iterator = _find_matching_lines(pattern, file_iterator)
    _print_highlighted(matching_lines_iterator)
