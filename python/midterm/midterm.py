
'''
a healthy person switches from healthy to infected if 2 of their neighbors is infected
a neighbor is defined as up or down vertically or right or left horizontally
'''

def check_up(input_board, row_count, current_row, current_col):
    #return 0 if this check is out of bounds or neighbor is healthy
    retval = 0
    if current_row != 0:
        up_person = input_board[current_row-1][current_col]
        if up_person == "I":
            retval = 1

    return retval

def check_down(input_board, row_count, current_row, current_col):
    #return 0 if this check is out of bounds or neighbor is healthy
    retval = 0
    if current_row != row_count-1:
        up_person = input_board[current_row+1][current_col]
        if up_person == "I":
            retval = 1

    return retval

def check_right(input_board, col_count,current_row, current_col):
    #return 0 if this check is out of bounds or neighbor is healthy
    retval = 0
    if current_col != col_count-1:
        up_person = input_board[current_row][current_col+1]
        if up_person == "I":
            retval = 1

    return retval

def check_left (input_board, col_count, current_row, current_col):
    #return 0 if this check is out of bounds or neighbor is healthy
    retval = 0
    if current_col != 0:
        up_person = input_board[current_row][current_col-1]
        if up_person == "I":
            retval = 1

    return retval

def process_pandemic(input_board, row_count, col_count):

    new_infected = True
    day_count = 1
    while new_infected:
        new_infected_count = 0
        new_infected_people = []
        for row_num in range(row_count):
            for col_num in range(col_count):
                if input_board[row_num][col_num] == "H":
                    # determine if you should switch healthy to infected
                    infected_count = 0
                    infected_count += check_up(input_board, row_count, row_num, col_num)
                    infected_count += check_down(input_board, row_count, row_num, col_num)
                    infected_count += check_left(input_board, col_count, row_num, col_num)
                    infected_count += check_right(input_board, col_count, row_num, col_num)

                    if infected_count >= 2:
                        new_infected_count += 1
                        new_infected_people.append([row_num, col_num])
                        #input_board[row_num][col_num] = 'I'

        for newPerson in new_infected_people:
            input_board[newPerson[0]][newPerson[1]] = 'I'

        print("Day: ", day_count)
        day_count += 1
        print_pandemic(input_board, row_count, col_count)
        print("")
        if new_infected_count == 0:
            new_infected = False

    '''print("******************************************")
    print_pandemic(input_board, row_count, col_count)
    print("******************************************")'''


def print_pandemic(input_board, row_count, col_count):
    for row_num in range(row_count):
        print(input_board[row_num])

def pandemic_main():
    print("starting pandemic main program")
    row_count = 5
    col_count = 5
    input_board = []
    for i in range(row_count):
        row = []
        for j in range(col_count):
            row.append('H')
        input_board.append(row)

    input_board[1][3] = 'I'
    input_board[2][2] = 'I'
    input_board[3][4] = 'I'

    print("Initial State Test 1")
    print_pandemic(input_board, row_count, col_count)
    print("")

    process_pandemic(input_board, row_count, col_count)


    input_board = []
    for i in range(row_count):
        row = []
        for j in range(col_count):
            row.append('H')
        input_board.append(row)

    input_board[0][2] = 'I'
    input_board[0][4] = 'I'
    input_board[1][1] = 'I'
    input_board[1][4] = 'I'
    input_board[2][2] = 'I'
    input_board[3][0] = 'I'
    input_board[3][3] = 'I'
    input_board[4][2] = 'I'

    print("Initial State Test 2")
    print_pandemic(input_board, row_count, col_count)
    print("")

    process_pandemic(input_board, row_count, col_count)


def snowfall_main():
    print("starting pandemic main program")
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

    # read the data from standard in and add them to a list of inputs
    for i in range(0, 2):
        value = input()
        input_list.append(value)

    # separate input data between n and the snowfall
    n = int(input_list[0])
    input_string = input_list[1]

    # split string of snowfall values as strings into list of snowfall values as strings
    snow_list_as_strings = input_string.split()

    # convert snowfall list from strings to ints
    for i in range(0, n):
        num = int(snow_list_as_strings[i])
        snow_list.append(num)

    # get the sum of all the snow
    snow_sum = snow_list[n - 1]
    # get half of the sum of all the snow
    half = snow_sum / 2

    # initialize found to false
    found = False
    # loop over the length of the snowfall list -2
    for j in range(0, n - 2):
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


pandemic_main()
snowfall_main()