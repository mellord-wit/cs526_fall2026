# lais1.py
# Marie Mellor
# cs 665

import sys


def compute_longest_sequence(list_a, list_b, start_offset, starting_list, longest_lengths_of_a, longest_lengths_of_b):
    longest_sequence = 0

    if starting_list == "A":
        test_value = list_a[start_offset]
        for b_offset in range(start_offset+1, len(list_b)):
            if list_b[b_offset] > test_value:
                if longest_lengths_of_b[b_offset] == -1:
                    longest_length = compute_longest_sequence(list_a, list_b, b_offset, "B", longest_lengths_of_a, longest_lengths_of_b)
                    longest_lengths_of_b[b_offset] = longest_length
                else:
                    longest_length = longest_lengths_of_b[b_offset]

                if longest_length > longest_sequence:
                    longest_sequence = longest_length

    else:
        test_value = list_b[start_offset]
        for a_offset in range(start_offset+1, len(list_a)):
            if list_a[a_offset] > test_value:
                if longest_lengths_of_a[a_offset] == -1:
                    longest_length = compute_longest_sequence(list_a, list_b, a_offset, "A", longest_lengths_of_a, longest_lengths_of_b)
                    longest_lengths_of_a[a_offset] = longest_length
                else:
                    longest_length = longest_lengths_of_a[a_offset]

                if longest_length > longest_sequence:
                    longest_sequence = longest_length

    return longest_sequence + 1


def main():

    # read input data and put into a list
    i = 0
    for line in sys.stdin:
        if i == 2:
            list_a_string = line.split()
        if i == 3:
            list_b_string = line.split()
            break
        i+=1

    list_a_ints = []
    for a in list_a_string:
        list_a_ints.append(int(a))

    list_b_ints = []
    for b in list_b_string:
        list_b_ints.append(int(b))

    '''print("list a:", list_a_ints)
    print("list b:", list_b_ints)'''

    longest_lengths_of_a = [-1] * len(list_a_ints)
    longest_lengths_of_b = [-1] * len(list_b_ints)
    overall_longest = -1

    for a_offset in range(len(list_a_ints)):
        if longest_lengths_of_a[a_offset] == -1:
            longest_length = compute_longest_sequence(list_a_ints, list_b_ints, a_offset, "A", longest_lengths_of_a, longest_lengths_of_b)
            longest_lengths_of_a[a_offset] = longest_length
        else:
            longest_length = longest_lengths_of_a[a_offset]

        if longest_length > overall_longest:
            overall_longest = longest_length


    for b_offset in range(len(list_b_ints)):
        if longest_lengths_of_b[b_offset] == -1:
            longest_length = compute_longest_sequence(list_a_ints, list_b_ints, b_offset, "B", longest_lengths_of_a, longest_lengths_of_b)
            longest_lengths_of_b[b_offset] = longest_length
        else:
            longest_length = longest_lengths_of_b[b_offset]

        if longest_length > overall_longest:
            overall_longest = longest_length


    print("Longest Sequence:", overall_longest)

main()
