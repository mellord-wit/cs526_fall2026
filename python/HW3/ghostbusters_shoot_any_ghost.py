"""
Ghostbusters "shoot any ghost" solution for HW3.

Uses the same input format as ghostbusters.py: a count line followed by lines of the form
"B x y G x y". Unlike ghostbusters.py, the ghost on each line is not the ghost that
ghostbuster has to shoot. Any ghostbuster may be paired with any ghost, and all ghosts are
eliminated if there is some one-to-one pairing in which every ghostbuster/ghost line is parallel.

Algorithm:
- In any working pairing, ghostbuster 0 is paired with some ghost j, so the shared
  direction must be (ghost j - ghostbuster 0). That gives at most n directions to try.
- For a direction (dx, dy), every point on the same line parallel to it has the same value
  of dy * x - dx * y. A ghostbuster can only be paired with a ghost on its own line, so the
  direction works if every line holds the same number of ghostbusters and ghosts.
- Integer arithmetic is used throughout, so vertical lines and rounding are not a problem.
Trying n directions with an O(n) check each makes the solution O(n^2).
"""
import os
import sys

# The ghostbusters input files live in the ghostbusters_resources folder next to this file.
RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ghostbusters_resources")

# When True, ghostbuster_test_main() prints the test file name in front of each result.
display_test_file_name = True

# When True, ghostbuster_test_main() plots the pairing it found for each test file.
plot_test_lines = True


def read_points(fileLines):
    ghostbusters = []
    ghosts = []
    read_counter = 0
    for line in fileLines:
        if read_counter > 0 and line.strip() != "":
            split_line = line.split()
            ghostbusters.append([int(split_line[1]), int(split_line[2])])
            ghosts.append([int(split_line[4]), int(split_line[5])])
        read_counter += 1
    return ghostbusters, ghosts


def line_key(point, dx, dy):
    # Same value for every point on one line parallel to the direction (dx, dy).
    return dy * point[0] - dx * point[1]


def pair_along_direction(ghostbusters, ghosts, dx, dy):
    # Returns a list of [ghostbuster_point, ghost_point] pairs that are all parallel to
    # (dx, dy), or None if the points cannot all be paired along that direction.
    ghostbusters_on_line = {}
    ghosts_on_line = {}
    for ghostbuster_point in ghostbusters:
        ghostbusters_on_line.setdefault(line_key(ghostbuster_point, dx, dy), []).append(ghostbuster_point)
    for ghost_point in ghosts:
        ghosts_on_line.setdefault(line_key(ghost_point, dx, dy), []).append(ghost_point)

    lines = []
    for key in ghostbusters_on_line:
        if len(ghostbusters_on_line[key]) != len(ghosts_on_line.get(key, [])):
            return None
        # Any pairing on the same line is parallel, so pair them up in order.
        for i in range(len(ghostbusters_on_line[key])):
            lines.append([ghostbusters_on_line[key][i], ghosts_on_line[key][i]])
    return lines


def find_parallel_pairing(ghostbusters, ghosts):
    if len(ghostbusters) == 0:
        return []
    first_ghostbuster = ghostbusters[0]
    for ghost_point in ghosts:
        dx = ghost_point[0] - first_ghostbuster[0]
        dy = ghost_point[1] - first_ghostbuster[1]
        if dx == 0 and dy == 0:
            # Ghost is on top of the ghostbuster, so it gives no direction to try.
            continue
        lines = pair_along_direction(ghostbusters, ghosts, dx, dy)
        if lines != None:
            return lines
    return None


def ghostbusters_shoot_any_ghost_solution(fileLines):
    ghostbusters, ghosts = read_points(fileLines)
    lines = find_parallel_pairing(ghostbusters, ghosts)
    if lines != None:
        result = "All Ghosts: were eliminated"
    else:
        result = "All Ghosts: were not eliminated"
    return result, lines


def ghostbusters_shoot_any_ghost_solution1(fileName):
    with open(fileName, "r") as input_file:
        file_lines = input_file.readlines()
    return ghostbusters_shoot_any_ghost_solution(file_lines)


def plot_initial_pairs(fileName, show=True):
    # Plots each ghostbuster/ghost pair exactly as it is written in the input file,
    # before any re-pairing, so it can be compared with the pairing the solution finds.
    # With show=False the plot is only drawn; see plot_lines() in ghostbusters_plot.py.
    with open(fileName, "r") as input_file:
        file_lines = input_file.readlines()
    ghostbusters, ghosts = read_points(file_lines)
    lines = []
    for i in range(len(ghostbusters)):
        lines.append([ghostbusters[i], ghosts[i]])
    # Imported here so matplotlib is only needed when plotting is turned on.
    from ghostbusters_plot import plot_lines
    plot_lines(lines, title=os.path.basename(fileName) + ": pairs as written", show=show)
    return lines


def main1():
    filelines = []
    for line in sys.stdin:
        filelines.append(line)
    result, lines = ghostbusters_shoot_any_ghost_solution(filelines)
    print(result)


def ghostbuster_test_main():
    for i in range(11):
        test_file_name = "ghostbusters_input_" + str(i) + ".txt"
        result, lines = ghostbusters_shoot_any_ghost_solution1(os.path.join(RESOURCES_DIR, test_file_name))
        if display_test_file_name:
            print(test_file_name + ": " + result)
        else:
            print(result)
        if plot_test_lines and lines != None:
            # Imported here so matplotlib is only needed when plotting is turned on.
            from ghostbusters_plot import plot_lines
            plot_lines(lines)

def ghostbuster_shoot_any_ghost_verify():
    inputFiles = {1,2,3}
    for i in inputFiles:
        test_file_name = "ghostbusters_input_" + str(i) + ".txt"
        result, lines = ghostbusters_shoot_any_ghost_solution1(os.path.join(RESOURCES_DIR, test_file_name))
        if display_test_file_name:
            print(test_file_name + ": " + result)
        else:
            print(result)
        if plot_test_lines:
            # Draw the pairs as written in the file and the pairing that was found, then
            # keep both windows open together until they are closed by hand.
            import matplotlib.pyplot as plt
            from ghostbusters_plot import plot_lines
            plot_initial_pairs(os.path.join(RESOURCES_DIR, test_file_name), show=False)
            if lines != None:
                plot_lines(lines, title=test_file_name + ": parallel pairing found", show=False)
            plt.show()


if __name__ == "__main__":
    '''   if len(sys.argv) >= 2:
        result, lines = ghostbusters_shoot_any_ghost_solution1(sys.argv[1])
        print(result)
    elif not sys.stdin.isatty():
        main1()
    else:
        ghostbuster_test_main()'''
    ghostbuster_shoot_any_ghost_verify()
