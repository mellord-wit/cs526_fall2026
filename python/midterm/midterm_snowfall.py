import sys


def snowfall_main():
    print("starting snowfall main program")
    '''
    8
    1 4 10 14 15 17 17 23
    YES

    16
    44 127 166 231 238 320 363 429 500 511 577 642 689 764 812 886
    NO

    9
    3 8 14 19 21 24 25 25 32
    NO

    5
    1 2 3 4 5
    YES
    '''
    # initialize empty lists
    input_list = []
    snow_list = []

    number_of_days_input = 0
    snowfall_input = ''
    input_line_count = 0
    for line in sys.stdin:
        if input_line_count == 0:
            # read n number of nodes
            number_of_days_input = int(line.strip())
        elif input_line_count == 1:
            snowfall_input = line
        else:
            break
        input_line_count += 1

    print("Number of Snowfall days: ", number_of_days_input)
    print("Cumulative Snowfall input: ", snowfall_input)

    # split string of snowfall values as strings into list of snowfall values as strings
    snow_list_as_strings = snowfall_input.split()

    snow_list = []
    # convert snowfall list from strings to ints
    for i in range(0, number_of_days_input):
        num = int(snow_list_as_strings[i])
        snow_list.append(num)

    # get the sum of all the snow
    snow_sum = snow_list[number_of_days_input - 1]
    # get half of the sum of all the snow
    half = snow_sum / 2

    # initialize found to false
    found = False
    # loop over the length of the snowfall list -2
    for j in range(0, number_of_days_input - 2):
        if j != 0:
            # if this is not the first value in the list
            # subtract the previous cumulative snowfall to the
            # current cumulative snowfall to get the total snow for the first day
            # in this situation, first day refers to the first day of the three consecutive days
            first = (snow_list[j] - snow_list[j - 1])
        else:
            # otherwise, just use the snowfall at the current position in the list
            first = snow_list[j]

        # for both the second and third days in the three consecutive days
        # subtract the previous cumulative snowfall to the
        # current cumulative snowfall to get the total snow for that day
        second = (snow_list[j + 1] - snow_list[j])
        third = (snow_list[j + 2] - snow_list[j + 1])

        # add the values of fist, second and third together to get the sum of three consecutive days
        consecutive_sum = first + second + third

        if consecutive_sum > half:
            # if the sum is greater than half the total snowfall
            # set found to true, print YES and break out of the loop
            found = True
            print("YES")
            break

    # if we get through the entire list and found is still false
    # then print NO
    if not found:
        print("NO")

snowfall_main()