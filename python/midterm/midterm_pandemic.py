'''
a healthy person switches from healthy to infected if 2 of their neighbors is infected
a neighbor is defined as up or down vertically or right or left horizontally
'''
import sys


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
    day_count = 2
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


        #check the board to see if all people are infected
        new_infected = False
        for row_num in range(row_count):
            for col_num in range(col_count):
                if input_board[row_num][col_num] == "H":
                    new_infected = True
                    break

            if new_infected:
                break

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
    number_of_rows_columns = 0
    pandemic_input_lines = []
    input_line_count = 0
    for line in sys.stdin:
        if input_line_count == 0:
            # read n number of nodes
            number_of_rows_columns = int(line.strip())
        else:
            pandemic_input_lines.append(line)
        input_line_count += 1

    row_count = number_of_rows_columns
    col_count = number_of_rows_columns
    input_board = []
    for i in range(row_count):
        row = []
        for j in range(col_count):
            row.append('H')
        input_board.append(row)

    for input_line in pandemic_input_lines:
        row_val = int(input_line[0])
        col_val = int(input_line[2])
        input_board[row_val][col_val] = 'I'


    print("Initial State Test 1")
    print_pandemic(input_board, row_count, col_count)
    print("")

    process_pandemic(input_board, row_count, col_count)

pandemic_main()