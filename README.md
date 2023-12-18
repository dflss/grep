# Grep

## Table of contents
* [General info](#general-info)
* [Getting started](#getting-started)
* [Testing](#testing)

## General info

This is a simplified version of the grep command-line utility to search for matching patterns in a file.

Currently implemented features:
- searching a list of one or more files provided
- recursively searching a single directory provided
- searching STDIN
- printing the line number
- printing leading and trailing context

## Getting started

The project is built with Python 3. To get started, first create a virtualenv and install requirements:

```commandline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then, you can run the program like this:
```commandline
python -m src.main test_pattern test_file  -A 2 -B 0 -n
```

To see all the options, run:
```commandline
python -m src.main --help
```

## Testing

You can run the tests using:

```commandline
python -m pytest
```
