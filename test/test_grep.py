from pathlib import Path

import pytest

from src.grep import grep
from src.printer import Printer


def test_grep_single_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    temp_dir = tmp_path / "temp_dir"
    temp_dir.mkdir()

    temp_file = temp_dir / "test_file.txt"
    temp_file.write_text("test\nnot a match\ntest")

    grep(
        pattern="test",
        files=[str(temp_file)],
        recursive=False,
        print_line_number=False,
        number_of_lines_before_match=0,
        number_of_lines_after_match=0,
    )

    captured = capsys.readouterr()
    assert captured.out == (
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
        f"{Printer.SEPARATOR_COLOR}--{Printer.DEFAULT_COLOR}\n"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
    )


def test_grep_multiple_files(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    temp_dir = tmp_path / "temp_dir"
    temp_dir.mkdir()

    temp_file1 = temp_dir / "test_file1.txt"
    temp_file1.write_text("test\nnot a match\ntest")
    temp_file2 = temp_dir / "test_file2.txt"
    temp_file2.write_text("test")

    grep(
        pattern="test",
        files=[str(temp_file1), str(temp_file2)],
        recursive=False,
        print_line_number=False,
        number_of_lines_before_match=0,
        number_of_lines_after_match=0,
    )

    captured = capsys.readouterr()
    assert captured.out == (
        f"{Printer.FILENAME_COLOR}{temp_file1}{Printer.SEPARATOR_COLOR}:{Printer.DEFAULT_COLOR}"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
        f"{Printer.SEPARATOR_COLOR}--{Printer.DEFAULT_COLOR}\n"
        f"{Printer.FILENAME_COLOR}{temp_file1}{Printer.SEPARATOR_COLOR}:{Printer.DEFAULT_COLOR}"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
        f"{Printer.SEPARATOR_COLOR}--{Printer.DEFAULT_COLOR}\n"
        f"{Printer.FILENAME_COLOR}{temp_file2}{Printer.SEPARATOR_COLOR}:{Printer.DEFAULT_COLOR}"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
    )


def test_grep_binary_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    temp_dir = tmp_path / "temp_dir"
    temp_dir.mkdir()

    temp_file1 = temp_dir / "test_file1.txt"
    temp_file1.write_bytes(b"\xff\xd8\xff\xe1")

    grep(
        pattern="test",
        files=[str(temp_file1)],
        recursive=False,
        print_line_number=False,
        number_of_lines_before_match=0,
        number_of_lines_after_match=0,
    )

    captured = capsys.readouterr()
    assert captured.out == (f"{temp_file1}: file is binary\n")


def test_grep_nonexistent_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    grep(
        pattern="test",
        files=["nonexistent_file"],
        recursive=False,
        print_line_number=False,
        number_of_lines_before_match=0,
        number_of_lines_after_match=0,
    )

    captured = capsys.readouterr()
    assert captured.out == ("nonexistent_file: file does not exist\n")


def test_grep_recursive(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    temp_dir = tmp_path / "temp_dir"
    temp_dir.mkdir()

    temp_file1 = temp_dir / "test_file1.txt"
    temp_file1.write_text("test\nnot a match\ntest")
    temp_file2 = temp_dir / "test_file2.txt"
    temp_file2.write_text("test2")

    grep(
        pattern="test",
        files=[str(temp_dir)],
        recursive=True,
        print_line_number=False,
        number_of_lines_before_match=0,
        number_of_lines_after_match=0,
    )

    captured = capsys.readouterr()
    assert captured.out == (
        f"{Printer.FILENAME_COLOR}{temp_file2}{Printer.SEPARATOR_COLOR}:{Printer.DEFAULT_COLOR}"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}2\n"
        f"{Printer.SEPARATOR_COLOR}--{Printer.DEFAULT_COLOR}\n"
        f"{Printer.FILENAME_COLOR}{temp_file1}{Printer.SEPARATOR_COLOR}:{Printer.DEFAULT_COLOR}"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
        f"{Printer.SEPARATOR_COLOR}--{Printer.DEFAULT_COLOR}\n"
        f"{Printer.FILENAME_COLOR}{temp_file1}{Printer.SEPARATOR_COLOR}:{Printer.DEFAULT_COLOR}"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
    )


def test_grep_recursive_multiple_files(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
):
    grep(
        pattern="test",
        files=["dir1", "dir2"],
        recursive=True,
        print_line_number=False,
        number_of_lines_before_match=0,
        number_of_lines_after_match=0,
    )

    captured = capsys.readouterr()
    assert captured.out == ("Only one directory can be searched in recursive mode!\n")


def test_grep_nonexistent_directory(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    grep(
        pattern="test",
        files=["nonexistent_dir"],
        recursive=True,
        print_line_number=False,
        number_of_lines_before_match=0,
        number_of_lines_after_match=0,
    )

    captured = capsys.readouterr()
    assert captured.out == (
        "nonexistent_dir: directory does not exist or is not a directory\n"
    )


def test_grep_stdin(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    pass


def test_grep_print_line_number(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    temp_dir = tmp_path / "temp_dir"
    temp_dir.mkdir()

    temp_file = temp_dir / "test_file.txt"
    temp_file.write_text("test\nnot a match\ntest")

    grep(
        pattern="test",
        files=[str(temp_file)],
        recursive=False,
        print_line_number=True,
        number_of_lines_before_match=0,
        number_of_lines_after_match=0,
    )

    captured = capsys.readouterr()
    assert captured.out == (
        f"{Printer.LINE_NUMBER_COLOR}1{Printer.SEPARATOR_COLOR}:{Printer.DEFAULT_COLOR}"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
        f"{Printer.SEPARATOR_COLOR}--{Printer.DEFAULT_COLOR}\n"
        f"{Printer.LINE_NUMBER_COLOR}3{Printer.SEPARATOR_COLOR}:{Printer.DEFAULT_COLOR}"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
    )


def test_grep_print_lines_before_and_after_match(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
):
    temp_dir = tmp_path / "temp_dir"
    temp_dir.mkdir()

    temp_file = temp_dir / "test_file.txt"
    temp_file.write_text(
        "not a match 1\nnot a match 2\ntest\nnot a match 3\ntest\nnot a match 4\nnot a match 5\nnot a match 6\n"
    )

    grep(
        pattern="test",
        files=[str(temp_file)],
        recursive=False,
        print_line_number=False,
        number_of_lines_before_match=1,
        number_of_lines_after_match=2,
    )

    captured = capsys.readouterr()
    assert captured.out == (
        f"not a match 2\n"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
        f"not a match 3\n"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
        f"not a match 4\n"
        f"not a match 5\n"
    )
