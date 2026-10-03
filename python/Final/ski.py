import datetime
import sys

def read_input_data():

    input_lines = []
    i = 0
    num_rows = 0
    num_cols = 0
    for line in sys.stdin:
        if i == 0:
            num_rows = int(line.strip("\n"))
        elif i == 1:
            num_cols = int(line.strip("\n"))
        else:
            input_line = line.split()
            temp_list = []
            for input_val in input_line:
                temp_list.append(int(input_val))
            input_lines.append(temp_list)

        i += 1
        if i == num_rows + 2:
            break

    return num_rows, num_cols, input_lines

def transform_data_into_a_matrix(num_rows, num_cols, input):

    matrix = [None] * num_rows
    for row in range(num_rows):
        col_array = [0] * num_cols
        matrix[row] = col_array

    coordinates = []

    for i in range(len(input)):
        row = input[i]
        for j in range(len(row)):
            col = row[j]
            matrix[i][j] = col
            cur_coordinates = [col, i, j]
            coordinates.append(cur_coordinates)

    for i in range(len(input)):
        col_list = []
        for j in range(len(row)):
            col_list.append(matrix[i][j])
        #print(col_list)

    #sort the coordinates by altitude
    coordinates.sort(key=lambda coordinates: coordinates[0])
    '''print("Sorted Coordinates")
    for offset in range(len(coordinates)-1, -1, -1):
        print(coordinates[offset])'''

    return matrix, coordinates


def compute_longest_path(coordinate, altitude_matrix, longest_path_matrix, num_rows, num_cols):

    coordinate_row = coordinate[1]
    coordinate_col = coordinate[2]

    current_altitude = altitude_matrix[coordinate_row][coordinate_col]

    #recursion formula max of (longest_path_matrix at [row-1 col-1], [row-1 col], [row-1 col], [row col-1], [row col+1]
    #                          [row+1 col-1] [row+1 col] [row+1 col+1] where the altitudes are greater than the current
    #                          cell

    greatest_path_to_this_cell = 0
    local_largest_path = True
    # can do the row-1 calculations
    if coordinate_row - 1 >= 0:
        if coordinate_col - 1 >= 0:
            altitude_val = altitude_matrix[coordinate_row - 1][coordinate_col - 1]
            if altitude_val > current_altitude:
                local_largest_path = False
                longest_path = longest_path_matrix[coordinate_row - 1][coordinate_col - 1]
                if longest_path > greatest_path_to_this_cell:
                    greatest_path_to_this_cell = longest_path

        if coordinate_col + 1 < num_cols:
            altitude_val = altitude_matrix[coordinate_row - 1][coordinate_col + 1]
            if altitude_val > current_altitude:
                local_largest_path = False
                longest_path = longest_path_matrix[coordinate_row - 1][coordinate_col + 1]
                if longest_path > greatest_path_to_this_cell:
                    greatest_path_to_this_cell = longest_path

        altitude_val = altitude_matrix[coordinate_row - 1][coordinate_col]
        if altitude_val > current_altitude:
            local_largest_path = False
            longest_path = longest_path_matrix[coordinate_row - 1][coordinate_col]
            if longest_path > greatest_path_to_this_cell:
                greatest_path_to_this_cell = longest_path

    # can do the row calculations
    if coordinate_col - 1 >= 0:
        altitude_val = altitude_matrix[coordinate_row][coordinate_col - 1]
        if altitude_val > current_altitude:
            local_largest_path = False
            longest_path = longest_path_matrix[coordinate_row][coordinate_col - 1]
            if longest_path > greatest_path_to_this_cell:
                greatest_path_to_this_cell = longest_path

    if coordinate_col + 1 < num_cols:
        altitude_val = altitude_matrix[coordinate_row][coordinate_col + 1]
        if altitude_val > current_altitude:
            local_largest_path = False
            longest_path = longest_path_matrix[coordinate_row][coordinate_col + 1]
            if longest_path > greatest_path_to_this_cell:
                greatest_path_to_this_cell = longest_path

    # can do row + 1 calculations
    if coordinate_row + 1 < num_rows:
        if coordinate_col - 1 >= 0:
            altitude_val = altitude_matrix[coordinate_row + 1][coordinate_col - 1]
            if altitude_val > current_altitude:
                local_largest_path = False
                longest_path = longest_path_matrix[coordinate_row + 1][coordinate_col - 1]
                if longest_path > greatest_path_to_this_cell:
                    greatest_path_to_this_cell = longest_path

        if coordinate_col + 1 < num_cols:
            altitude_val = altitude_matrix[coordinate_row + 1][coordinate_col + 1]
            if altitude_val > current_altitude:
                local_largest_path = False
                longest_path = longest_path_matrix[coordinate_row + 1][coordinate_col + 1]
                if longest_path > greatest_path_to_this_cell:
                    greatest_path_to_this_cell = longest_path

        altitude_val = altitude_matrix[coordinate_row + 1][coordinate_col]
        if altitude_val > current_altitude:
            local_largest_path = False
            longest_path = longest_path_matrix[coordinate_row + 1][coordinate_col]
            if longest_path > greatest_path_to_this_cell:
                greatest_path_to_this_cell = longest_path

    if local_largest_path:
        longest_path_matrix[coordinate_row][coordinate_col] = 0
    else:
        longest_path_matrix[coordinate_row][coordinate_col] = 1 + greatest_path_to_this_cell

def main():

    start_timer = datetime.datetime.now()
    num_rows, num_cols, input_lines = read_input_data()

    '''print("num rows: ", num_rows, "num_cols: ", num_cols)
    print("input_data")
    print(input_lines)'''


    matrix, coordinates = transform_data_into_a_matrix(num_rows, num_cols, input_lines)

    longest_path_matrix = [None] * num_rows
    for row in range(num_rows):
        col_array = [0] * num_cols
        longest_path_matrix[row] = col_array

    #skip the first coordinate because its the greatest altitude and not traversable
    for coordinate_offset in range(len(coordinates)-2, -1, -1):
        coordinate = coordinates[coordinate_offset]
        compute_longest_path(coordinate, matrix, longest_path_matrix, num_rows, num_cols)

    longest_path = 0
    for row_offset in range(len(longest_path_matrix)):
        row = longest_path_matrix[row_offset]
        for col_offset in range(len(row)):
            if row[col_offset] > longest_path:
                longest_path = row[col_offset]

        #print(row)

    end_timer = datetime.datetime.now()

    print(longest_path)
    #print("Elapsed Time: ", (end_timer - start_timer))

main()

# scp ski.py mhm3244@kinks.cs.rit.edu:~/Courses/cs665
