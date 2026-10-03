import sys


def read_and_print_file():
    for line in sys.stdin:
        print(line, end="")


def read_datafile_as_an_argument():
   with open(sys.argv[1]) as f:
        for line in f:
            print(line, end="")


def main():
    if len(sys.argv) >= 2:
        read_datafile_as_an_argument()
    elif sys.stdin.isatty():
        print("Error: no input file supplied on standard in. Usage: python3 homework1.py < file.txt")
    else:
        read_and_print_file()


if __name__ == "__main__":
    main()
