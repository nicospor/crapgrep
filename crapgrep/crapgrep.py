import exceptions
import re
import os
import sys


def find_line(line: str, pattern: str, i_case: bool, is_regexp=False) -> bool:
    """
    Check if line contains matches for pattern, with case and regexp flags.
    Returns True if pattern is found in line.
    """
    found = False

    if i_case:
        line = line.lower()
        pattern = pattern.lower()

    if is_regexp:
        matches = re.findall(pattern, line)
        FIND_COND = len(matches) > 0
    else:
        FIND_COND = line.find(pattern) != -1

    if FIND_COND:
        line = line.strip()
        found = True

    return found


def print_usage():
    usage = """
Usage: crapgrep.py [OPTIONS]... PATTERN [FILE]...

Example:

    crapgrep.py -i 'searching' target1.txt target2.txt

OPTIONS:

    -E : PATTERN is a (Python) regexp
    -i : case-insensitive search for PATTERN
    -n : print line numbers
    -r : search recursively in files in the given path

    --help: print this help message
    """
    print(usage)


def check_args(args: list) -> bool:
    """
    The arguments passed to crapgrep.py
    """
    if len(args) < 2 or args[0] == '--help':
        return False
    return True


def check_pattern(pattern: str) -> bool:
    """
    Compile pattern and return false if invalid
    """
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False


def parse_args(args: list) -> dict:
    """
    Parse cli arguments and return the tree as a dict
    """
    # TODO move to class
    OPTS = (
        'i',  # Case-insensitive search
        'E',  # Pattern is a full regexp
        'r',  # Search recursively in dir
        'n',  # Print line numbers
    )
    # TODO Handle extended options? (e.g. --ignore-case)
    LONG_OPTS = [
        '--ignore-case',
        '--regexp',
        '--recursive',
        '--line-numbers',
    ]

    args_tree = dict()
    # Filter short options
    options = [arg[1:] for arg in args if arg[0] == '-']

    # Remove invalid options and throw exception
    # TODO does it make sense?
    for opt in options:
        if opt not in OPTS:
            raise exceptions.InvalidOptionError(opt)

    args_tree["options"] = options

    # Filter options from args
    remaining_args = [a for a in args if a.lstrip('-') not in options]

    pattern = remaining_args[0]

    if pattern[0] == "'" and pattern[-1] == "'":
        pattern = pattern.strip("'")
    elif pattern[0] == '"' and pattern[-1] == '"':
        pattern = pattern.strip('"')

    args_tree["pattern"] = rf"{pattern}"
    args_tree["files"] = remaining_args[1:]

    return args_tree


def process_grep(args_tree: dict) -> list:
    lines = []
    found_lines = []
    options = args_tree["options"]
    pattern = args_tree["pattern"]
    files = args_tree["files"]
    i_case = False

    try:
        for f in files:
            with open(f, 'r') as fp:
                lines = fp.readlines()

            f = f + ':' if len(files) > 1 else ''

            n = 0

            for line in lines:
                n = n + 1
                # Check if case insensitive
                if 'i' in options:
                    i_case = True
                # Check if regexp flag
                if 'E' in options:
                    # pattern is regexp
                    if not check_pattern(pattern):
                        raise exceptions.InvalidPatternError(pattern)
                    found = find_line(line, pattern, i_case, True)
                else:
                    found = find_line(line, pattern, i_case)

                lnum = str(n) + ':' if 'n' in options else ''

                if found:
                    found_lines.append(f + lnum + line.strip())

    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    return found_lines


# When the script is executed directly...
if __name__ == "__main__":
    args = sys.argv[1:]

    if not check_args(args):
        print_usage()
        sys.exit(1)

    try:
        args_tree = parse_args(args)
    except exceptions.InvalidOptionError as e:
        print(e.get_message())
        print_usage()
        sys.exit(1)

    try:
        for line in process_grep(args_tree):
            print(line)
    except exceptions.InvalidPatternError as e:
        print(e.get_message())
        sys.exit(1)
