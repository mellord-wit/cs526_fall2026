# Marie Mellor
# CSCI 665
# hw3 morseVowel.py

import sys
import datetime


def vowel_at_position_with_len_1(offset, morse_code_list):
    E = '.'

    if morse_code_list[offset] == E:
        return True
    else:
        return False


def vowel_at_position_with_len_2(offset, morse_code_list):
    A = '.-'
    I = '..'

    if offset < len(morse_code_list)-1:
        current_two_char_value = morse_code_list[offset] + morse_code_list[offset+1]

        if current_two_char_value == A or current_two_char_value == I:
            return True

    return False


def vowel_at_position_with_len_3(offset, morse_code_list):
    O = '---'
    U = '..-'

    if offset < len(morse_code_list)-2:
        current_two_char_value = morse_code_list[offset] + morse_code_list[offset+1] + morse_code_list[offset+2]

        if current_two_char_value == O or current_two_char_value == U:
            return True

    return False


def reverse_vowel_at_diagonal_position(offset, num_vowels_matrix):

    return_value = 0

    if offset > 0:
        return_value += num_vowels_matrix[offset-1][0]
    if offset > 1:
        return_value += num_vowels_matrix[offset-2][1]
    if offset > 2:
        return_value += num_vowels_matrix[offset-3][2]

    return return_value


def vowel_combinations(morse_code_list, n):

    num_vowels_matrix = [None] * n
    for j in range(n):
        temp = [0] * 3
        num_vowels_matrix[j] = temp


    diagonal = 0
    for offset in range(len(morse_code_list)):
        check_1 = vowel_at_position_with_len_1(offset, morse_code_list)
        if check_1:
            if offset == 0:
                num_vowels_matrix[offset][0] = 1
            else:
                previous_vowel_num = reverse_vowel_at_diagonal_position(offset, num_vowels_matrix)
                num_vowels_matrix[offset][0] = previous_vowel_num

        check_2 = vowel_at_position_with_len_2(offset, morse_code_list)
        if check_2:
            if offset == 0:
                num_vowels_matrix[offset][1] = 1
            else:
                previous_vowel_num = reverse_vowel_at_diagonal_position(offset, num_vowels_matrix)
                num_vowels_matrix[offset][1] = previous_vowel_num

        check_3 = vowel_at_position_with_len_3(offset, morse_code_list)
        if check_3:
            if offset == 0:
                num_vowels_matrix[offset][2] = 1
            else:
                previous_vowel_num = reverse_vowel_at_diagonal_position(offset, num_vowels_matrix)
                num_vowels_matrix[offset][2] = previous_vowel_num

        #print(num_vowels_matrix)
    return num_vowels_matrix[n-1][0] + num_vowels_matrix[n-2][1] + num_vowels_matrix[n-3][2]


def main():
    # read input data and put into a list
    i = 0
    morse_input = ""
    for line in sys.stdin:
        if i == 0:
            n = int(line.strip())
        elif i == 1:
            morse_input = line.strip()
        else:
            break
        i += 1

    morse_code_list = []
    for x in range(len(morse_input)):
        morse_code_list.append(morse_input[x])

    #print(morse_code_list)

    start = datetime.datetime.now()
    number_of_vowel_combinations = vowel_combinations(morse_code_list, n)
    end = datetime.datetime.now()
    #print("time:", end - start)
    print("The Number of Vowel combinations is: ", number_of_vowel_combinations)

main()
