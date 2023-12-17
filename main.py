import argparse

from grep import grep


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Search for PATTERN in each FILE.\n\n"
        "Example: grep -i 'hello world' menu.h main.c",
        epilog="When FILE is not given, read standard input OR current directory if searching recursively.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Positional arguments
    parser.add_argument("pattern", help="pattern to search")
    parser.add_argument(
        "file",
        nargs="*",
        default=None,
        help="(optional) file to search in (can be multiple) OR directory to search in if searching recursively",
    )

    # Options
    parser.add_argument(
        "-r", "--recursive", action="store_true", help="search recursively"
    )
    parser.add_argument(
        "-i",
        "--ignore-case",
        action="store_true",
        help="ignore case distinctions in patterns and data",
    )
    parser.add_argument(
        "-v", "--invert-match", action="store_true", help="select non-matching lines"
    )
    parser.add_argument(
        "-w", "--word", action="store_true", help="match only whole words"
    )
    parser.add_argument(
        "-n",
        "--line-number",
        action="store_true",
        help="print line number with output lines",
    )
    parser.add_argument(
        "-b",
        "--ignore-binary-files",
        action="store_true",
        help="supress output for non-text files",
    )
    parser.add_argument(
        "-B",
        "--before-context",
        type=int,
        default=0,
        metavar="NUM",
        help="print NUM lines of leading context",
    )
    parser.add_argument(
        "-A",
        "--after-context",
        type=int,
        default=0,
        metavar="NUM",
        help="print NUM lines of trailing context",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    grep(
        pattern=args.pattern,
        files=args.file,
        recursive=args.recursive,
        ignore_case=args.ignore_case,
        invert_match=args.invert_match,
        word=args.word,
        print_line_number=args.line_number,
        ignore_binary_files=args.ignore_binary_files,
        before_context=args.before_context,
        after_context=args.after_context,
    )
