"""
Ghostbusters "shoot any ghost" solution for HW3.

Uses the same input format as ghostbusters.py: a count line followed by lines of the form
"B x y G x y". Unlike ghostbusters.py, the ghost on each line is not the ghost that
ghostbuster has to shoot. Any ghostbuster may be paired with any ghost, and all ghosts are
eliminated if there is some one-to-one pairing in which every ghostbuster/ghost line is parallel.

Algorithm:
1. Pick the candidate directions.
   If every ghostbuster/ghost line has to be parallel, they all share one direction. We do
   not know that direction ahead of time, but we do know that in any working pairing,
   ghostbuster 0 is paired with some ghost j. The line from ghostbuster 0 to ghost j then
   points in the shared direction, so the direction must be (ghost j - ghostbuster 0) for
   some j. Trying every ghost j gives at most n candidate directions, and if none of them
   works, no pairing can work. (A ghost sitting exactly on ghostbuster 0 gives no
   direction, so it is skipped.)

2. Group the points into parallel lines for one direction (dx, dy).
   Two points p and q lie on the same line parallel to (dx, dy) exactly when the step
   q - p is a multiple of (dx, dy), which is when the cross product
   dy * (qx - px) - dx * (qy - py) is 0. Rearranging, that is when
   dy * px - dx * py == dy * qx - dx * qy. So the value dy * x - dx * y (line_key) is a
   label for the line a point is on: points on the same parallel line get the same key,
   and points on different parallel lines get different keys.

3. Check that every line can be paired up.
   A ghostbuster's line to its ghost is parallel to (dx, dy) only if the ghost is on the
   ghostbuster's own parallel line, so pairs can never cross from one line to another.
   That means the direction works exactly when every line holds the same number of
   ghostbusters as ghosts. When the counts match, any pairing within a line is fine,
   because all the points on it are already lined up, so they are paired in the order
   they were read.

Line key explained:
   In short: select a line key equation, use it to produce a result for each
   ghostbuster, then a result for each ghost, and check that the ghostbuster results
   match the ghost results. That is essentially what the code does, with two details.

   1. You pick a direction, not a key.
      The direction (dx, dy) comes from ghostbuster 0 -> some ghost, and it sets the
      equation key = dy * x - dx * y. For example, direction (1, 2) gives
      key = 2 * x - y. Then:
      - run every ghostbuster through the equation,
      - run every ghost through the equation,
      - compare the results.
      If the comparison fails, pick the next direction (ghostbuster 0 -> the next
      ghost), which gives a new equation, and repeat.

   2. The rule is equal counts, not exactly one of each.
      For each result value, the number of ghostbusters with that value must equal the
      number of ghosts with that value. Ghostbusters are then paired with ghosts that
      share their key. In the 3-pair example below every count happens to be 1, so it
      looks like one-to-one matching, but several points can share a key when they are
      all on the same line:
          ghostbusters (0, 0) (1, 2), ghosts (2, 4) (3, 6)
          direction (1, 2), key = 2 * x - y
          All four points have key 0, so key 0 holds 2 ghostbusters and 2 ghosts. That
          balances, and pairing (0, 0)-(2, 4) and (1, 2)-(3, 6) gives two shots that
          are both parallel to (1, 2). Since all four points are on one line, any
          pairing would work, so the code pairs them in the order they were read.

   Why checking only the ghostbusters' side is enough:
      The code only loops over the ghostbuster keys and never looks for a ghost whose
      key has no ghostbuster. That is safe because there are n ghostbusters and n
      ghosts: if every ghostbuster key has a matching count of ghosts, those keys
      already account for all n ghosts, so no ghost can be left over.

   So the full rule for one direction is:
      Compute the key for every ghostbuster and every ghost. The direction works if,
      for every key value, #ghostbusters = #ghosts. Then pair ghostbusters with ghosts
      that share a key.

- Integer arithmetic is used throughout, so vertical lines and rounding are not a problem.
Trying n directions with an O(n) check each makes the solution O(n^2).

Example with two ghostbusters and two ghosts (4 points):
    B 0 0 G 3 1        ghostbuster 0 = (0, 0)   ghost 0 = (3, 1)
    B 2 0 G 1 1        ghostbuster 1 = (2, 0)   ghost 1 = (1, 1)

  Try ghost 0: direction = (3, 1) - (0, 0) = (3, 1), so line_key = 1 * x - 3 * y.
      ghostbuster 0 (0, 0) -> 0      ghost 0 (3, 1) -> 0
      ghostbuster 1 (2, 0) -> 2      ghost 1 (1, 1) -> -2
    Line 0 has 1 ghostbuster and 1 ghost, but line 2 has 1 ghostbuster and no ghost,
    so ghostbuster 1 has nothing it can shoot along this direction. Direction fails.

  Try ghost 1: direction = (1, 1) - (0, 0) = (1, 1), so line_key = 1 * x - 1 * y.
      ghostbuster 0 (0, 0) -> 0      ghost 1 (1, 1) -> 0
      ghostbuster 1 (2, 0) -> 2      ghost 0 (3, 1) -> 2
    Line 0 holds ghostbuster 0 and ghost 1, and line 2 holds ghostbuster 1 and ghost 0.
    Every line balances, so the pairing is (0, 0)-(1, 1) and (2, 0)-(3, 1). Both shots
    move by (1, 1), so they are parallel and all ghosts are eliminated.

Example with three ghostbusters and three ghosts (3 pairs):
    B 0 0 G 2 2        ghostbuster 0 = (0, 0)   ghost 0 = (2, 2)
    B 1 0 G 4 2        ghostbuster 1 = (1, 0)   ghost 1 = (4, 2)
    B 3 0 G 1 2        ghostbuster 2 = (3, 0)   ghost 2 = (1, 2)

  Try ghost 0: direction = (2, 2) - (0, 0) = (2, 2), so line_key = 2 * x - 2 * y.
      ghostbuster 0 (0, 0) -> 0      ghost 0 (2, 2) -> 0
      ghostbuster 1 (1, 0) -> 2      ghost 1 (4, 2) -> 4
      ghostbuster 2 (3, 0) -> 6      ghost 2 (1, 2) -> -2
    Line 0 balances (ghostbuster 0 and ghost 0), but line 2 has ghostbuster 1 and no
    ghost, so the check stops there. Direction fails.

  Try ghost 1: direction = (4, 2) - (0, 0) = (4, 2), so line_key = 2 * x - 4 * y.
      ghostbuster 0 (0, 0) -> 0      ghost 0 (2, 2) -> -4
      ghostbuster 1 (1, 0) -> 2      ghost 1 (4, 2) -> 0
      ghostbuster 2 (3, 0) -> 6      ghost 2 (1, 2) -> -6
    Line 0 balances (ghostbuster 0 and ghost 1), but again line 2 has ghostbuster 1 and
    no ghost. Direction fails.

  Try ghost 2: direction = (1, 2) - (0, 0) = (1, 2), so line_key = 2 * x - 1 * y.
      ghostbuster 0 (0, 0) -> 0      ghost 0 (2, 2) -> 2
      ghostbuster 1 (1, 0) -> 2      ghost 1 (4, 2) -> 6
      ghostbuster 2 (3, 0) -> 6      ghost 2 (1, 2) -> 0
    Line 0 holds ghostbuster 0 and ghost 2, line 2 holds ghostbuster 1 and ghost 0, and
    line 6 holds ghostbuster 2 and ghost 1. Every line balances, so the pairing is
    (0, 0)-(1, 2), (1, 0)-(2, 2) and (3, 0)-(4, 2). All three shots move by (1, 2), so
    they are parallel and all ghosts are eliminated. Note that none of the ghosts ends up
    with the ghostbuster written next to it in the input.
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
