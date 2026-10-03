"""
Sample data generation for HW3, split out of HW3.py.

Creates the palindrome test files (palendrome_<n><S|L>.txt / palendrome_ans_<n><S|L>.txt)
in the palendrome_resources folder and the ghostbusters test files
(ghostbusters_input_<n>.txt / ghostbusters_ans_<n>.txt) in the ghostbusters_resources
folder, both next to this file. Running this overwrites any existing files of those names.
"""
import os
import random
import matplotlib.pyplot as plt

# The input and answer files live in resource folders next to this file.
RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ghostbusters_resources")
PALENDROME_RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "palendrome_resources")


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
    file_name = os.path.join(PALENDROME_RESOURCES_DIR, "palendrome_"+  str(case_number) +  str(size) + ".txt")
    file = open(file_name, "w")
    for input in case:
        output = " ".join(input)
        file.write(output)
        file.write("\n")

    file.close()

def write_palendrome_answer_file(case_number, answers, total_true=0, size='S'):
    file_name = os.path.join(PALENDROME_RESOURCES_DIR, "palendrome_ans_" +  str(case_number) + str(size) +  ".txt")
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
    os.makedirs(PALENDROME_RESOURCES_DIR, exist_ok=True)
    generatePalendroneTests('S')
    generatePalendroneTests('L')

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
    os.makedirs(RESOURCES_DIR, exist_ok=True)
    for i in range(10):
        if (random.randint(0,30) % 3) == 0:
            parallel_lines = generate_parallel_lines()
            #plot_lines(parallel_lines)
            file_name = os.path.join(RESOURCES_DIR, "ghostbusters_ans_" + str(i) + ".txt")
            file = open(file_name, "w")
            output = "All Ghosts: were eliminated"
            file.write(output)
            file.write("\n")
            file.close()

            file_name = os.path.join(RESOURCES_DIR, "ghostbusters_input_" + str(i) + ".txt")
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
            file_name = os.path.join(RESOURCES_DIR, "ghostbusters_ans_" + str(i) + ".txt")
            file = open(file_name, "w")
            output = "All Ghosts: were not eliminated"
            file.write(output)
            file.write("\n")
            file.close()

            file_name = os.path.join(RESOURCES_DIR, "ghostbusters_input_" + str(i) + ".txt")
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


if __name__ == "__main__":
    create_tests()
    generate_ghostbusters_inputs()
