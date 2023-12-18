from pathlib import Path

import pytest

from grep import grep
from printer import Printer


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
        f"{Printer.FILENAME_COLOR}{temp_file1.absolute()}{Printer.SEPARATOR_COLOR}:{Printer.DEFAULT_COLOR}"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
        f"{Printer.SEPARATOR_COLOR}--{Printer.DEFAULT_COLOR}\n"
        f"{Printer.FILENAME_COLOR}{temp_file1.absolute()}{Printer.SEPARATOR_COLOR}:{Printer.DEFAULT_COLOR}"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
        f"{Printer.SEPARATOR_COLOR}--{Printer.DEFAULT_COLOR}\n"
        f"{Printer.FILENAME_COLOR}{temp_file2.absolute()}{Printer.SEPARATOR_COLOR}:{Printer.DEFAULT_COLOR}"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
    )


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
        f"{Printer.FILENAME_COLOR}{temp_file2.absolute()}{Printer.SEPARATOR_COLOR}:{Printer.DEFAULT_COLOR}"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}2\n"
        f"{Printer.SEPARATOR_COLOR}--{Printer.DEFAULT_COLOR}\n"
        f"{Printer.FILENAME_COLOR}{temp_file1.absolute()}{Printer.SEPARATOR_COLOR}:{Printer.DEFAULT_COLOR}"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
        f"{Printer.SEPARATOR_COLOR}--{Printer.DEFAULT_COLOR}\n"
        f"{Printer.FILENAME_COLOR}{temp_file1.absolute()}{Printer.SEPARATOR_COLOR}:{Printer.DEFAULT_COLOR}"
        f"{Printer.MATCHED_TEXT_COLOR}test{Printer.DEFAULT_COLOR}\n"
    )
