# Marie Mellor
# CSCI 665 hw3
# fewest.py

import sys
import datetime


def quicksort(input_array):
    input_array.sort()

    return input_array


def calculate_median(input_list):

    sorted_input = quicksort(input_list)
    if len(sorted_input) % 2 == 0:
        return sorted_input[(len(sorted_input) // 2)-1]
    else:
        return sorted_input[len(sorted_input) // 2]


def calculate_median_of_medians(median_array):


    # split incoming list into lists of 5
    slice_val = 5
    input_length = len(median_array)

    if input_length > slice_val:
        list_of_lists = []

        for i in range(input_length//slice_val):
            temp_list = median_array[i*slice_val:(i+1) * slice_val]
            list_of_lists.append(temp_list)

        if input_length % 5 != 0:
            temp_list = median_array[(input_length//slice_val) * slice_val:]
            list_of_lists.append(temp_list)

        median_list = []

        for current_list in list_of_lists:
            median = calculate_median(current_list)
            median_list.append(median)

        return calculate_median_of_medians(median_list)

    else:

        return calculate_median(median_array)




def median_k_select(list_of_vals, k, c):

    n = len(list_of_vals)
    sum_ = 0
    smallest = -1
    smallest_index = 0
    for x in range(len(list_of_vals)):
        sum_ += list_of_vals[x]
        if list_of_vals[x] < smallest or smallest == -1:
            smallest = list_of_vals[x]
            smallest_index = x
    if sum_ > c and sum_ - smallest <= c:
        return len(list_of_vals)

    if n <= 5 and n > 1:
        return_list = []
        for i in range(len(list_of_vals)):
            if i != smallest_index:
                return_list.append(list_of_vals[i])
        #return median_k_select([list_of_vals[element] for element in range(len(list_of_vals)) if element != smallest_index], 0,c)
        return median_k_select(return_list, 0, c)
    elif n == 1:
        return list_of_vals[0]
    else:

        pivot = calculate_median_of_medians(list_of_vals)

        less = []
        equal = []
        greater = []
        less_sum = 0
        equal_sum = 0
        greater_sum = 0
        for current_value in list_of_vals:
            if current_value < pivot:
                less.append(current_value)
                less_sum += current_value
            if current_value == pivot:
                equal.append(current_value)
                equal_sum += current_value
            if current_value > pivot:
                greater.append(current_value)
                greater_sum += current_value

        if greater_sum > c:
            # apply function to list of greater values
            return median_k_select(greater, (len(greater)-1)//2, c)
        elif equal_sum + greater_sum > c:
             return median_k_select(greater + equal, ((len(greater) + len(equal))-1)//2, c)
        else:
            return_list = []
            for i in range(len(list_of_vals)):
                if i != smallest_index:
                    return_list.append(list_of_vals[i])
            #return median_k_select(greater + equal + [less[element] for element in range(len(less)) if element != smallest_index], (n-2)//2, c)
            return median_k_select(return_list, (n-2)//2, c)




def main():
    # read input data and put into a list
    i = 0
    for line in sys.stdin:
        if i == 0:
            n = int(line.strip())
        elif i == 1:
            target_val = int(line.strip())
        elif i == 3:
            break
        else:
            input_list = line.strip().split()
        i += 1

    #print(n)
    #print(target_val)

    # convert input list from strings to ints
    list_of_vals = []
    for i in input_list:
        list_of_vals.append(int(i))

    #print(list_of_vals)

    k = 0
    start = datetime.datetime.now()
    num_values = median_k_select(list_of_vals, k, target_val)
    #check_median = calculate_median_of_medians(list_of_vals)
    end = datetime.datetime.now()
    #print("time to run:", end-start)
    print(num_values)


main()
