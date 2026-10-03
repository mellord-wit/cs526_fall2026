"""
Ghostbusters solution for HW3, split out of HW3.py.

Each input has a count line followed by lines of the form "B x y G x y" (a ghostbuster
point and its ghost). Each stream is the infinite line through a ghostbuster and its ghost.
All ghosts are eliminated only if no two streams cross: every stream must be parallel, and
no two streams may lie on the same line (streams on the same line count as crossing).

The check uses integer arithmetic instead of slopes, so vertical streams (where the slope
would divide by zero) and rounding are not a problem.
"""
import os
import sys

# The ghostbusters input and answer files live in the ghostbusters_resources folder next to this file.
RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ghostbusters_resources")

# When True, ghostbuster_test_main() prints the test file name in front of each result.
display_test_file_name = True

# When True, ghostbuster_test_main() plots each test file's ghostbuster/ghost lines.
plot_test_lines = True


def streams_do_not_cross(ghostbusters, ghosts):
    # The first stream's direction (dx, dy) is the one every other stream must match.
    dx = ghosts[0][0] - ghostbusters[0][0]
    dy = ghosts[0][1] - ghostbusters[0][1]
    lines_used = set()
    for i in range(len(ghostbusters)):
        ghostbuster_point = ghostbusters[i]
        ghost_point = ghosts[i]
        stream_dx = ghost_point[0] - ghostbuster_point[0]
        stream_dy = ghost_point[1] - ghostbuster_point[1]
        if stream_dx == 0 and stream_dy == 0:
            # The ghostbuster is standing on its ghost, so the stream has no direction.
            return False
        # Two directions are parallel when their cross product is 0. Unlike comparing
        # slopes, this also works for vertical streams.
        if dx * stream_dy - dy * stream_dx != 0:
            return False
        # Every point on one line parallel to (dx, dy) has the same value of dy*x - dx*y,
        # so two streams with the same value lie on the same line and count as crossing.
        line_key = dy * ghostbuster_point[0] - dx * ghostbuster_point[1]
        if line_key in lines_used:
            return False
        lines_used.add(line_key)
    return True

def ghostbusters_solution1(fileName):
    with open(fileName, "r") as input_file:
        file_lines = input_file.readlines()
    read_counter = 0
    totalGhostbusters = 0
    ghostbusters = []
    ghosts = []
    for line in file_lines:
        if read_counter == 0:
            totalGhostbusters = int(line.strip())
            #print("total ghostbusters: ", totalGhostbusters)
        else:
            #print(line.strip())
            split_line = line.split()
            #print("split line: ", split_line)
            ghostbuster_point = [int(split_line[1]), int(split_line[2])]
            ghost_point = [int(split_line[4]), int(split_line[5])]
            ghostbusters.append(ghostbuster_point)
            ghosts.append(ghost_point)
        read_counter += 1

    all_ghosts_eliminated = streams_do_not_cross(ghostbusters, ghosts)

    if all_ghosts_eliminated:
        result = "All Ghosts: were eliminated"
    else:
        result = "All Ghosts: were not eliminated"
    #print(result)

    # Each line is a [ghostbuster_point, ghost_point] pair, the format plot_lines() expects.
    lines = []
    for i in range(len(ghostbusters)):
        lines.append([ghostbusters[i], ghosts[i]])
    return result, lines

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

    all_ghosts_eliminated = streams_do_not_cross(ghostbusters, ghosts)

    if all_ghosts_eliminated:
        result = "All Ghosts: were eliminated"
    else:
        result = "All Ghosts: were not eliminated"
    #print(result)
    return result

def main1():
    print("ghostbuster solution")
    filelines = []
    for line in sys.stdin:
        filelines.append(line)
    ghostbusters_solution(filelines)

def ghostbuster_test_main():
    for i in range(11):
        test_file_name = "ghostbusters_input_" + str(i) + ".txt"
        result, lines = ghostbusters_solution1(os.path.join(RESOURCES_DIR, test_file_name))
        if display_test_file_name:
            print(test_file_name + ": " + result)
        else:
            print(result)
        if plot_test_lines:
            # Imported here so matplotlib is only needed when plotting is turned on.
            from ghostbusters_plot import plot_lines
            plot_lines(lines)


if __name__ == "__main__":
    ghostbuster_test_main()
    #main1()
