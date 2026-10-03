"""
This program is a simple Hello World program.

Author: Katherine Rein
Date: September 10, 2024

Description:
This program accepts from standard input a file with n number of lines.
It then print the lines to standard output.
"""

# Import Modules
import os

# Set filename
import sys

#Notice in your submission, you are reading the entire file into a single text variable called text_str
#this will work if you want to operate on the entire file as a single string note that the string you read
#is a file with new line characters at the end of each line ... the strip function removes them
#to make your submission more in line with what you will need going forward, I modified your code below
#in a function called dm_submission
def original_submission():
    FILENAME = 'KRein_input.txt'

    if not os.path.exists(FILENAME):
        print(f"The file {FILENAME} does not exist.")
        sys.exit()

    # Read in text file
    text_file = open(FILENAME, 'r', encoding='latin-1')
    text_str = text_file.read()

    # Print the text file
    print(text_str)

def dm_submission():
    FILENAME = 'KRein_input.txt'

    if not os.path.exists(FILENAME):
        print(f"The file {FILENAME} does not exist.")
        sys.exit()

    # Read in text file
    text_file = open(FILENAME, 'r', encoding='latin-1')
    lines = text_file.readlines()
    for line in lines:
        # Print the text file
        print(line.strip())

def example_read_from_standard_in():

    line_number = 1
    for line in sys.stdin:
        print("line number ", line_number, " content: ", line.strip())
        line_number += 1

print("Notice in your submission, you are reading the entire file into a single text variable called text_str")
print("this will work if you want to operate on the entire file as a single string note that the string you read")
print("is a file with new line characters at the end of each line ... the strip function removes them")
print("to make your submission more in line with what you will need going forward, I modified your code below")
print("in a function called dm_submission")

print("Read from standard in ... the command from the terminal would be python K.Rein_Homework1.py < KRein_input.txt")
example_read_from_standard_in()
print("\nYour submission")
original_submission()
print("\nDM submission")
dm_submission()
