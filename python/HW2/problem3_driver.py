"""Driver for Problem 3.

Reads directives from a file or standard input, one per line. Each directive is named
after a function in problem3.py:

    ways <n>                  ways_1_or_2 <n>          print_ways <n>

and prints each result, e.g. "ways(4) = 7". print_ways also prints every climb,
one per line, before its result.

Set READ_FROM_FILE below to choose where the directives come from:

    True   read the lines from INPUT_FILE
               python3 problem3_driver.py
    False  read the lines from standard input
               python3 problem3_driver.py < problem3Resources/problem3_input1.txt
"""
import os
import sys

from problem3 import print_ways, ways, ways_1_or_2

# Run toggle: True reads INPUT_FILE, False reads standard input.
READ_FROM_FILE = True
# Relative paths are taken from this script's folder, so the IDE's working
# directory doesn't matter.
INPUT_FILE = "problem3Resources/problem3_input1.txt"

# directive -> the function it calls
DIRECTIVES = {
    "ways":        ways,
    "ways_1_or_2": ways_1_or_2,
    "print_ways":  print_ways,
}


def warn(line_number, message):
    print("line " + str(line_number) + ": " + message, file=sys.stderr)


def parse_n(text):
    # A negative n would never reach a base case, so reject it here.
    n = int(text)       # ValueError if not a whole number
    if n < 0:
        raise ValueError
    return n


def problem3_driver(lines):
    results = []

    for line_number, line in enumerate(lines, start=1):
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue

        parts = line.split()
        directive = parts[0].lower()
        if directive not in DIRECTIVES:
            warn(line_number, "unknown directive '" + directive + "'")
            continue

        if len(parts) != 2:
            warn(line_number, "expected '" + directive + " <n>', got '" + line + "'")
            continue

        try:
            n = parse_n(parts[1])
        except ValueError:
            warn(line_number, "n must be a whole number 0 or greater, got '" + line + "'")
            continue

        result = DIRECTIVES[directive](n)
        print(directive + "(" + str(n) + ") = " + str(result))
        results.append(result)

    return results


if __name__ == "__main__":
    if READ_FROM_FILE:
        input_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), INPUT_FILE)
        with open(input_path) as input_file:
            lines = input_file.readlines()
        problem3_driver(lines)
    else:
        problem3_driver(sys.stdin)
