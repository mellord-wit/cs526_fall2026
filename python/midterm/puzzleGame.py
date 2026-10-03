import sys
import numpy as np

def commandLineInput():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print("Usage: python read_file.py <filename>")

    boardSize = 0
    input_board = None
    try:
        with open(filename, 'r') as file:

            lineCount = 0
            rowCount = 0
            for line in file:
                stripped_line = line.strip()
                if len(stripped_line) == 0:
                    break
                if lineCount == 0: #this is the first line of the file
                    boardSize = int(stripped_line)
                    # create the input board
                    fill_value = '.'
                    input_board = np.full((9, 9), fill_value)
                if lineCount == 1: #this is the set of symbols
                    symbols = stripped_line
                if lineCount > 1:
                    # copy the input row values into the numpy array
                    colCount = 0
                    #split the incomming row into values based on commas
                    split_input = stripped_line.split(",")
                    for val in split_input:
                        input_board[rowCount][colCount] = val
                        colCount += 1
                    rowCount += 1
                lineCount += 1

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except IOError:
        print(f"Error: Cannot read file '{filename}'.")
    return boardSize, symbols, input_board

def checkRow(inputRow, symbols):
    # create a dictionary of the symbols and the value 0
def checkRows(board_size, symbols, inputBoard):
    for i in range(0, board_size):
        row = inputBoard[i]
        checkRow(row, symbols)


def main():
    print("This is the main program executing.")
    board_size, symbols, input_board = commandLineInput()
    checkRows(board_size, symbols, input_board)

    print("Success")

if __name__ == "__main__":
    main()


