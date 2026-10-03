"""
Palindrome solution for HW3, split out of HW3.py.

Reads lines of space separated characters from stdin, prints True/False for each line
depending on whether it is a palindrome, then prints the number of palindromes found.

Example:
    python palendrome.py < palendrome_resources/palendrome_0S.txt
"""
import sys


def isPalendrome(palendrome_input):
    #print("start is palendrome")
    if len(palendrome_input) == 1:
        return True
    else:
        if len(palendrome_input) == 2:
            if palendrome_input[0] == palendrome_input[1]:
                return True
        else:
            first_char = palendrome_input[0]
            last_char = palendrome_input[len(palendrome_input)-1]
            if palendrome_input[0] == palendrome_input[len(palendrome_input)-1]:
                #remove the first and last characters
                temp = palendrome_input[1:]
                temp1 = temp[:-1]
                return isPalendrome(temp1)
            else:
                return False

def solve_palendrome_test(palendrome_test_input):
    print("start test")

def test_true_palendrome():
    input = ['a','g','e','v','m','d','d','m','v','e','g','a']
    input_str = " ".join(input)
    print("input_str: ", input_str)
    print("Is Palendrome: ", isPalendrome(input_str))

def test_false_palendrome():
    input = ['q','i','l','n','k','s','r','v','c','z','z','c','v','r','o','k','n','l','i','q']

    input_str = " ".join(input)
    print("input_str: ", input_str)
    print("Is Palendrome: ", isPalendrome(input_str))

def run_palendrome_homework():
    palendrome_count = 0
    for line in sys.stdin:
        input_line = line.strip()
        #print("input line: ", input_line)
        if len(input_line) == 0:
            return
        else:
            is_palendrome = isPalendrome(input_line)
            print(is_palendrome)
            if is_palendrome:
                palendrome_count += 1

    print(palendrome_count)

if __name__ == "__main__":
    run_palendrome_homework()
