"""Driver for Problem 4.

Reads directives from a file or standard input, one per line. Each directive is named
after a SortedDoublyLinkedList method:

    add <value>               delete <value>           exists <value>
    count <value>             total                    sum_middle_three
    median                    print_list

and prints the resulting list after all lines have been processed.

Set READ_FROM_FILE below to choose where the directives come from:

    True   read the lines from INPUT_FILE
               python3 problem4_driver.py
    False  read the lines from standard input
               python3 problem4_driver.py < problem4Tests/problem_test16.txt
"""
import os
import sys

from problem4 import SortedDoublyLinkedList

# Run toggle: True reads INPUT_FILE, False reads standard input.
READ_FROM_FILE = False
# Relative paths are taken from this script's folder, so the IDE's working
# directory doesn't matter.
INPUT_FILE = "problem4Tests/problem_test16.txt"

# directive -> the arguments it expects, in order
DIRECTIVES = {
    # Create
    "add":              ("value",),
    # Read
    "exists":           ("value",),
    "count":            ("value",),
    "total":            (),
    "sum_middle_three": (),
    "median":           (),
    # Delete
    "delete":           ("value",),
    # Print
    "print_list":       (),
}


def parse_value(text):
    # The list is sorted, so every value must be a number that can be compared.
    try:
        return int(text)
    except ValueError:
        return float(text)      # ValueError if not a number


def warn(line_number, message):
    print("line " + str(line_number) + ": " + message, file=sys.stderr)


def run_directive(my_list, directive, args):
    # Every directive has the same name as a SortedDoublyLinkedList method.
    result = getattr(my_list, directive)(*args)

    if directive in ("exists", "count"):
        print(directive + "(" + str(args[0]) + ") = " + str(result))
    elif directive in ("total", "sum_middle_three", "median"):
        print(directive + " = " + str(result))
    elif directive == "delete" and not result:
        raise LookupError(str(args[0]) + " not found, nothing deleted")
    elif directive != "print_list":
        print(directive + "(" + ", ".join([str(arg) for arg in args]) + ")")


def problem4_driver(lines):
    my_list = SortedDoublyLinkedList()

    for line_number, line in enumerate(lines, start=1):
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue

        directive = line.split(maxsplit=1)[0].lower()
        if directive not in DIRECTIVES:
            warn(line_number, "unknown directive '" + directive + "'")
            continue

        arg_names = DIRECTIVES[directive]
        arg_texts = line.split()[1:]
        if len(arg_texts) != len(arg_names):
            usage = " ".join([directive] + ["<" + name + ">" for name in arg_names])
            warn(line_number, "expected '" + usage + "', got '" + line + "'")
            continue

        try:
            args = [parse_value(text) for text in arg_texts]
        except ValueError:
            warn(line_number, "value must be a number, got '" + line + "'")
            continue

        try:
            run_directive(my_list, directive, args)
        except (ValueError, LookupError) as error:
            # ValueError: sum_middle_three or median on a list that is too short
            warn(line_number, str(error))

    print("Final list: ", end="")
    my_list.print_list()
    return my_list


if __name__ == "__main__":
    if READ_FROM_FILE:
        input_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), INPUT_FILE)
        with open(input_path) as input_file:
            lines = input_file.readlines()
        problem4_driver(lines)
    else:
        problem4_driver(sys.stdin)
