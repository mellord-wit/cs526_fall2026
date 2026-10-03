def ways(n):
    # Base cases: an empty staircase (0 steps) can be climbed exactly one way,
    # by doing nothing. 1 step: 1. 2 steps: 1+1 or 2.
    if n == 0:
        return 1
    elif n == 1:
        return 1
    elif n == 2:
        return 2
    else:
        # The first move is 1, 2, or 3 steps; count the ways to climb what is left.
        return ways(n-1) + ways(n-2) + ways(n-3)


def ways_1_or_2(n):
    # Question c: with only 1 or 2 steps per move, ways(n) is the Fibonacci sequence.
    if n == 0 or n == 1:
        return 1
    else:
        return ways_1_or_2(n-1) + ways_1_or_2(n-2)


def print_ways(n, climb=""):
    # Like ways(n), but also prints every climb, e.g. 1+1+2.
    # climb holds the moves taken so far as a string of digits, e.g. "112".
    if n < 0:
        # Overshot the top, so this is not a valid climb.
        return 0
    elif n == 0:
        # Reached the top exactly: climb is one complete sequence.
        print("+".join(climb) or "(no moves)")
        return 1
    else:
        # The first move is 1, 2, or 3 steps; record it and climb what is left.
        return print_ways(n-1, climb + "1") + print_ways(n-2, climb + "2") + print_ways(n-3, climb + "3")


if __name__ == "__main__":
    #print("ways with 3: ", ways(3))
    print("Step Combinations for an input of 3 steps: ")
    print("Total Step Combinations: ", print_ways(3), "\n")
    print("Step Combinations for an input of 4 steps: ")
    print("Total Step Combinations: ", print_ways(4), "\n")
    print("Step Combinations for an input of 7 steps: ")
    print("Total Step Combinations: ", print_ways(7), "\n")
    #print("ways with 5: ", ways(5))
    print("Step Combinations for an input of 10 steps: ", ways(10), "\n")

    #print("\nclimbs with 4:")
    #print("total: ", print_ways(4))

    #print("1 or 2 steps, n = 0..9: ", [ways_1_or_2(n) for n in range(10)])

# Answers to the questions:
# a) ways(0) = 1 (one way to climb nothing), ways(1) = 1, ways(2) = 2.
#    Three base cases are needed because the recursive step reaches back to n-3.
# b) Like doIt in Problem 3, ways has the same base cases (1, 1, 2) and uses the
#    three previous values. The difference is that ways adds all three, while
#    doIt subtracts the third: doIt(n-1) + doIt(n-2) - doIt(n-3).
# c) The Fibonacci sequence: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...
