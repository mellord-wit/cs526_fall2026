import random
import sys
import matplotlib.pyplot as plt


def generatePalindroneTest(validPalendrone, test_size, odd=0):

    if validPalendrone:
        palendrone = []
        for i in range(test_size):
            char = str(chr(random.randint(97, 122)))
            palendrone.insert(i, char)
            palendrone.insert((i+1), char)


        if odd == 1:
            palendrone.insert(test_size, str(chr(random.randint(97, 122))))
        #print("True Palendrone is: ", palendrone)

    else:
        palendrone = []
        for i in range(test_size):
            char = str(chr(random.randint(97, 122)))
            palendrone.insert(i, char)
            palendrone.insert((i + 1), char)

        if odd == 1:
            palendrone.insert(test_size, str(chr(random.randint(97, 122))))

        badOffset = random.randint(1, test_size//2)
        #print("Bad Offset: ", badOffset)
        for i in range(test_size):
            if i > 0 and i%badOffset == 0:
                palendrone[i] = str(chr(random.randint(97, 122)))

        #print("False Palendrone is: ", palendrone)

    return palendrone

def generatePalendroneTests(size = 'S'):
    numberOfTestCases = 5
    cases = []
    case_answers = []
    for i in range(numberOfTestCases):
        numberOfTests = random.randint(3, 20)
        tests = []
        test_answers = []
        for j in range(numberOfTests):
            if size == 'S':
                testSize = random.randint(5, 10)
            if size == 'L':
                testSize = random.randint(10, 30)
            valid_Invalid = random.randint(0,1)
            odd_even = random.randint(0,1)
            #print("Odd even: ", odd_even)
            if valid_Invalid == 0:
                test = generatePalindroneTest(True, testSize, odd_even)
                tests.append(test)
                test_answers.append(True)
            else:
                test = generatePalindroneTest(False, testSize, odd_even)
                tests.append(test)
                test_answers.append(False)


        cases.append(tests)
        case_answers.append(test_answers)


    for case_counter in range(len(cases)):

        print("Case:", case_counter)
        case = cases[case_counter]
        for tests in case:
            print("Test: ", tests)

        answers = case_answers[case_counter]
        print("Answers: ", answers)

        write_palendrome_input_file(case_counter, case, size)

        true_count = 0
        for answer in answers:
            if answer:
                true_count += 1
        write_palendrome_answer_file(case_counter, answers, true_count, size)


def write_palendrome_input_file(case_number, case, size='S'):
    file_name = "palendrome_"+  str(case_number) +  str(size) + ".txt"
    file = open(file_name, "w")
    for input in case:
        output = " ".join(input)
        file.write(output)
        file.write("\n")

    file.close()

def write_palendrome_answer_file(case_number, answers, total_true=0, size='S'):
    file_name = "palendrome_ans_" +  str(case_number) + str(size) +  ".txt"
    file = open(file_name, "w")
    for answer in answers:
        if answer:
            output = "True"
        else:
            output = "False"
        file.write(output)
        file.write("\n")

    file.write(str(total_true))
    file.close()

def create_tests():
    generatePalendroneTests('S')
    generatePalendroneTests('L')

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


def distinctSubstring(str):
    # Put all distinct substring in a HashSet
    result = set()

    # List All Substrings
    for i in range(len(str) + 1):
        for j in range(i + 1, len(str) + 1):
            # Add each substring in Set
            result.add(str[i:j]);
        # Return size of the HashSet
    return result

def unique_substrings(string, result=None):
    """
    Recursively computes all unique substrings of a given string.

    Args:
        string (str): The input string.
        result (set, optional): A set to store unique substrings.

    Returns:
        set: A set of unique substrings.
    """

    if result is None:
        result = set()

    if not string:
        return result

    for i in range(len(string)):
        for j in range(i + 1, len(string) + 1):
            result.add(string[i:j])

    return unique_substrings(string[1:], result)

def generate_parallel_lines():
    #return lines
    parallel_lines = []
    # generate the slope
    m = random.randint(-50, 50)
    y_offsets = []
    x_offsets = []


    # generate random number of lines
    ghostBusters = random.randint(2, 15)
    for i in range(ghostBusters):
        # generate random y offset
        y_offset_not_used = True
        while y_offset_not_used:
            b = random.randint(-70, 70)
            if b not in y_offsets:
                y_offsets.append(b)
                y_offset_not_used = False

        x_offset_not_used = True
        while x_offset_not_used:
            ghostBuster_x = random.randint(0,40)
            if ghostBuster_x not in x_offsets:
                x_offsets.append(ghostBuster_x)
                x_offset_not_used = False

        ghostBuster_y = (m * ghostBuster_x) + b       #e.g. y = mx + b
        ghostBuster_point = [ghostBuster_x, ghostBuster_y]

        ghost_x = random.randint(0, 40)
        ghost_y = (m * ghost_x) + b
        ghost_point = [ghost_x, ghost_y]

        line = [ghostBuster_point, ghost_point]
        parallel_lines.append(line)

    return parallel_lines

def generate_random_lines():
    #return lines
    parallel_lines = []
    y_offsets = []
    x_offsets = []


    # generate random number of lines
    ghostBusters = random.randint(3, 15)
    for i in range(ghostBusters):
        #generate slopt
        m = random.randint(-50, 50)
        # generate random y offset
        y_offset_not_used = True
        while y_offset_not_used:
            b = random.randint(-70, 70)
            if b not in y_offsets:
                y_offsets.append(b)
                y_offset_not_used = False

        x_offset_not_used = True
        while x_offset_not_used:
            ghostBuster_x = random.randint(0,40)
            if ghostBuster_x not in x_offsets:
                x_offsets.append(ghostBuster_x)
                x_offset_not_used = False

        ghostBuster_y = (m * ghostBuster_x) + b       #e.g. y = mx + b
        ghostBuster_point = [ghostBuster_x, ghostBuster_y]

        ghost_x = random.randint(0, 40)
        ghost_y = (m * ghost_x) + b
        ghost_point = [ghost_x, ghost_y]

        line = [ghostBuster_point, ghost_point]
        parallel_lines.append(line)

    return parallel_lines

def plot_lines(lines):
    if lines == None:
        lines = []
        line1 = []
        line1.append([34,-205])
        line1.append([12,-117])
        lines.append(line1)

        line2 = []
        line2.append([38, 1009])
        line2.append([9, 226])
        lines.append(line2)

        line3 = []
        line3.append([11, 226])
        line3.append([17, 386])
        lines.append(line3)


    for line_number in range(len(lines)):
        line = lines[line_number]
        point1 = line[0]
        point2 = line[1]
        x_vals = []
        x_vals.append(point1[0])
        x_vals.append(point2[0])
        y_vals = []
        y_vals.append(point1[1])
        y_vals.append(point2[1])

        line_label = "line " + str(line_number)
        plt.plot(x_vals, y_vals, label = line_label)

    plt.legend()
    plt.show()


def generate_ghostbusters_inputs():
    print("starting main")
    for i in range(10):
        if (random.randint(0,30) % 3) == 0:
            parallel_lines = generate_parallel_lines()
            #plot_lines(parallel_lines)
            file_name = "ghostbusters_ans_" + str(i) + ".txt"
            file = open(file_name, "w")
            output = "All Ghosts: were eliminated"
            file.write(output)
            file.write("\n")
            file.close()

            file_name = "ghostbusters_input_" + str(i) + ".txt"
            file = open(file_name, "w")
            file.write(str(len(parallel_lines)))
            file.write("\n")
            for line in parallel_lines:
                gb_point = line[0]
                g_point = line[1]
                file.write('B ')
                file.write(str(gb_point[0]))
                file.write(' ')
                file.write(str(gb_point[1]))
                file.write(' ')
                file.write('G ')
                file.write(str(g_point[0]))
                file.write(' ')
                file.write(str(g_point[1]))
                file.write("\n")
            file.close()
        else:
            lines = generate_random_lines()
            file_name = "ghostbusters_ans_" + str(i) + ".txt"
            file = open(file_name, "w")
            output = "All Ghosts: were not eliminated"
            file.write(output)
            file.write("\n")
            file.close()

            file_name = "ghostbusters_input_" + str(i) + ".txt"
            file = open(file_name, "w")
            file.write(str(len(lines)))
            file.write("\n")
            for line in lines:
                gb_point = line[0]
                g_point = line[1]
                file.write('B ')
                file.write(str(gb_point[0]))
                file.write(' ')
                file.write(str(gb_point[1]))
                file.write(' ')
                file.write('G ')
                file.write(str(g_point[0]))
                file.write(' ')
                file.write(str(g_point[1]))
                file.write("\n")
            file.close()
            #plot_lines(lines)

def calc_slope(point1, point2):
    m = (point2[1] - point1[1]) / (point2[0] - point1[0])
    #print("The slope for points: p1", point1, " p2:", point2, " m: ", m)
    return m

def ghostbusters_solution1(fileName):
    input_file = open(fileName, "r")
    read_counter = 0
    totalGhostbusters = 0
    ghostbusters = []
    ghosts = []
    for line in input_file.readlines():
        if read_counter == 0:
            totalGhostbusters = int(line.strip())
            #print("total ghostbusters: ", totalGhostbusters)
        else:
            #print(line.strip())
            split_line = line.split()
            ghostbuster_point = [int(split_line[1]), int(split_line[2])]
            ghost_point = [int(split_line[4]), int(split_line[5])]
            ghostbusters.append(ghostbuster_point)
            ghosts.append(ghost_point)
        read_counter += 1

    all_ghosts_eliminated = True
    match_slope = 0.0
    for i in range(len(ghostbusters)):
        ghostbuster_point = ghostbusters[i]
        ghost_point = ghosts[i]

        slope = round(calc_slope(ghostbuster_point, ghost_point), 3)
        #print("calculated slope: ", slope)
        if i == 0:
            match_slope = slope
        else:
            if slope != match_slope:
                all_ghosts_eliminated = False
                break

    if all_ghosts_eliminated:
        print("All ghosts were eliminated")
    else:
        print("All ghosts were not eliminated")

def ghostbusters_solution(fileLines):
    read_counter = 0
    totalGhostbusters = 0
    ghostbusters = []
    ghosts = []
    for line in fileLines:
        if read_counter == 0:
            totalGhostbusters = int(line.strip())
            #print("total ghostbusters: ", totalGhostbusters)
        else:
            #print(line.strip())
            split_line = line.split()
            ghostbuster_point = [int(split_line[1]), int(split_line[2])]
            ghost_point = [int(split_line[4]), int(split_line[5])]
            ghostbusters.append(ghostbuster_point)
            ghosts.append(ghost_point)
        read_counter += 1

    all_ghosts_eliminated = True
    match_slope = 0.0
    for i in range(len(ghostbusters)):
        ghostbuster_point = ghostbusters[i]
        ghost_point = ghosts[i]

        slope = round(calc_slope(ghostbuster_point, ghost_point), 3)
        #print("calculated slope: ", slope)
        if i == 0:
            match_slope = slope
        else:
            if slope != match_slope:
                all_ghosts_eliminated = False
                break

    if all_ghosts_eliminated:
        print("All ghosts were eliminated")
    else:
        print("All ghosts were not eliminated")

def main1():
    print("ghostbuster solution")
    filelines = []
    for line in sys.stdin:
        filelines.append(line)
    ghostbusters_solution(filelines)

def ghostbuster_test_main():
    ghostbusters_solution1("ghostbusters_input_0.txt")
    ghostbusters_solution1("ghostbusters_input_1.txt")
    ghostbusters_solution1("ghostbusters_input_2.txt")
    ghostbusters_solution1("ghostbusters_input_3.txt")
    ghostbusters_solution1("ghostbusters_input_4.txt")
    ghostbusters_solution1("ghostbusters_input_5.txt")
    ghostbusters_solution1("ghostbusters_input_6.txt")
    ghostbusters_solution1("ghostbusters_input_7.txt")
    ghostbusters_solution1("ghostbusters_input_8.txt")
    ghostbusters_solution1("ghostbusters_input_9.txt")

ghostbuster_test_main()

#print("running test 3")
#ghostbusters_solution1("ghostbusters_input_3.txt")
#main1()
#isPal = isPalendrome("thisisatesttsetasisiht")
#if isPal:
#    print("is a palendrome")
#print("here")

substrings = distinctSubstring("abcab")
for i in substrings:
    print(i)

string1 = "abcab"
recursion_result = unique_substrings(string1, result=None)
print(recursion_result)
print("for string: ", string1)
print("number of unique substrings: ", len(recursion_result))

string2 = "abcabadukab"
recursion_result = unique_substrings(string2, result=None)
print(recursion_result)
print("for string: ", string2)
print("number of unique substrings: ", len(recursion_result))

string3 = "xyzy"
recursion_result = unique_substrings(string3, result=None)
print(recursion_result)
print("for string: ", string3)
print("number of unique substrings: ", len(recursion_result))





