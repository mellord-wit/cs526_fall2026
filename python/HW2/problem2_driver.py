"""Driver for Problem 2.

Reads directives from a file or standard input, one per line. Each directive is named
after a SinglyLinkedList method:

    append <value>            prepend <value>          insert <index> <value>
    get <index>               find <value>             len
    update <index> <value>
    delete <value>            delete_at <index>
    print_list

and prints the resulting list after all lines have been processed.

Set READ_FROM_FILE below to choose where the directives come from:

    True   read the lines from INPUT_FILE
               python3 problem2_driver.py
    False  read the lines from standard input
               python3 problem2_driver.py < problem2Resources/problem2_basic.txt
"""
import os
import sys

from problem2 import SinglyLinkedList

# Run toggle: True reads INPUT_FILE, False reads standard input.
READ_FROM_FILE = False
# Relative paths are taken from this script's folder, so the IDE's working
# directory doesn't matter.
INPUT_FILE = "problem2Resources/problem2_basic.txt"

# directive -> the arguments it expects, in order
DIRECTIVES = {
    # Create
    "append":     ("value",),
    "prepend":    ("value",),
    "insert":     ("index", "value"),
    # Read
    "get":        ("index",),
    "find":       ("value",),
    "len":        (),
    # Update
    "update":     ("index", "value"),
    # Delete
    "delete":     ("value",),
    "delete_at":  ("index",),
    # Print
    "print_list": (),
}


def parse_value(text):
    # Store numbers as ints so "delete 5" matches a node added with "append 5".
    try:
        return int(text)
    except ValueError:
        return text


def warn(line_number, message):
    print("line " + str(line_number) + ": " + message, file=sys.stderr)


def parse_args(arg_names, arg_texts):
    args = []
    for name, text in zip(arg_names, arg_texts):
        if name == "index":
            args.append(int(text))      # ValueError if not a whole number
        else:
            args.append(parse_value(text))
    return args


def run_directive(my_list, directive, args):
    if directive == "len":
        print("len = " + str(len(my_list)))
        return

    # Every other directive has the same name as a SinglyLinkedList method.
    result = getattr(my_list, directive)(*args)

    if directive in ("get", "find", "delete_at"):
        print(directive + "(" + str(args[0]) + ") = " + str(result))
    elif directive == "delete" and not result:
        raise LookupError(str(args[0]) + " not found, nothing deleted")


def problem2_driver(lines):
    my_list = SinglyLinkedList()

    for line_number, line in enumerate(lines, start=1):
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue

        directive = line.split(maxsplit=1)[0].lower()
        if directive not in DIRECTIVES:
            warn(line_number, "unknown directive '" + directive + "'")
            continue

        arg_names = DIRECTIVES[directive]
        # The last argument takes the rest of the line, so values may contain spaces.
        # (maxsplit=0 would not split at all, so directives without arguments
        # split fully and any extra text is reported as an error.)
        parts = line.split(maxsplit=len(arg_names)) if arg_names else line.split()
        arg_texts = parts[1:]
        if len(arg_texts) != len(arg_names):
            usage = " ".join([directive] + ["<" + name + ">" for name in arg_names])
            warn(line_number, "expected '" + usage + "', got '" + line + "'")
            continue

        try:
            args = parse_args(arg_names, arg_texts)
            run_directive(my_list, directive, args)
        except ValueError:
            warn(line_number, "index must be a whole number, got '" + line + "'")
        except (IndexError, LookupError) as error:
            warn(line_number, str(error))

    print("Final list: ", end="")
    my_list.print_list()
    return my_list


if __name__ == "__main__":
    if READ_FROM_FILE:
        input_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), INPUT_FILE)
        with open(input_path) as input_file:
            lines = input_file.readlines()
        problem2_driver(lines)
    else:
        problem2_driver(sys.stdin)
