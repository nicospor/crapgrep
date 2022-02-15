import exceptions
import re
import os
import sys
import sty


# TODO Avoid extra fname argument??
def find_lines(lines: list, pattern: str, fname: str, is_regexp=False) -> list:
    """
    Distinguish between regexp or not (default is False)
    """
    found_lines = []

    for line in lines:
        if is_regexp:
            matches = re.findall(pattern, line)
            FIND_COND = len(matches) > 0
        else:
            FIND_COND = line.find(pattern) != -1

        if FIND_COND:
            line = line.strip()
            found_lines.append(fname + line)

    return found_lines


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
    OPTS = [
        'i',  # Case-insensitive search
        'E',  # Pattern is a full regexp
        'r',  # Search recursively in dir
        'n',  # Print line numbers
    ]
    # TODO Handle extended options? (e.g. --ignore-case)
    LONG_OPTS = [
        '--ignore-case',
        '--regexp',
        '--recursive',
        '--line-numbers',
    ]

    args_tree = dict()
    options = []
    # Get options
    for arg in args:
        # Parse short options
        if arg[0] == '-':
            if arg[1:] not in OPTS:
                raise exceptions.InvalidOption(arg[1:])

            options.append(arg[1:])

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

    """
    print(args_tree)
    sys.exit(1)
    """
    return args_tree


def match_regexp(pattern: str, line: str) -> object:
    """
    Search for pattern in the given line and return
    a match object or None if no match found.

    Flags??
    """
    return re.search(pattern, line)


def process_grep(args_tree: dict) -> list:
    lines = []
    found_lines = []
    options = args_tree["options"]
    pattern = args_tree["pattern"]
    files = args_tree["files"]

    try:
        for f in files:
            with open(f, 'r') as fp:
                lines = fp.readlines()

            f = f + ':' if len(files) > 1 else ''

            # Check if case insensitive
            if 'i' in options:
                pattern = pattern.lower()
            # Check if regexp flag
            if 'E' in options:
                # pattern is regexp
                if not check_pattern(pattern):
                    raise exceptions.InvalidPattern(pattern)
                found_lines.extend(find_lines(lines, pattern, f, True))
            else:
                found_lines.extend(find_lines(lines, pattern, f))

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
    except exceptions.InvalidOption as e:
        print(e.get_message())
        print_usage()
        sys.exit(1)

    try:
        for line in process_grep(args_tree):
            print(line)
    except exceptions.InvalidPattern as e:
        print(e.get_message())
        sys.exit(1)
