import sys
import math

'''
Alternative O(n^2) solution to the right triangle problem.

Idea: every right triangle has exactly one right angle, so we can count
each triangle once by counting it at the vertex where the right angle is.

For each point P (the candidate right-angle vertex):
  1. For every other point Q, compute the vector (dx, dy) = Q - P and
     reduce it to its simplest integer form by dividing by gcd(|dx|, |dy|).
     Two points that lie on the same ray out of P end up with the same
     reduced direction, e.g. (2, 4) and (3, 6) both become (1, 2).
  2. Count how many points lie along each reduced direction using a
     dictionary (hash map).
  3. A direction (a, b) is perpendicular to (-b, a), which is (a, b)
     rotated +90 degrees. For each direction, every point in that direction
     pairs with every point in the rotated direction to form a right angle
     at P, so add count[(a, b)] * count[(-b, a)].
     Only the +90 rotation is checked so each pair of rays is counted once.

Unlike the polar angle approach this uses only integer arithmetic, so there
is no rounding / margin-of-error problem when comparing angles.

Running time: n pivots * (n - 1) other points * O(1) average dictionary
work (plus O(log C) for gcd, C = coordinate size) = O(n^2 log C).
'''

def reduce_direction(dx, dy):
    g = math.gcd(dx, dy)  # gcd is always non-negative
    return (dx // g, dy // g)

def determine_right_triangle(points_list):
    total_triangles = 0
    for i in range(len(points_list)):
        px, py = points_list[i]

        # count the points along each ray leaving point i
        direction_counts = {}
        for j in range(len(points_list)):
            if i != j:
                qx, qy = points_list[j]
                direction = reduce_direction(qx - px, qy - py)
                direction_counts[direction] = direction_counts.get(direction, 0) + 1

        # pair each ray with the ray rotated +90 degrees
        for (a, b), count in direction_counts.items():
            perpendicular = (-b, a)
            if perpendicular in direction_counts:
                total_triangles += count * direction_counts[perpendicular]

    return total_triangles

def main():
    # read input data and put into a list
    n = int(sys.stdin.readline().strip())
    points_list = []
    for i in range(n):
        x, y = sys.stdin.readline().split()
        points_list.append((int(x), int(y)))

    right_triangle_count = determine_right_triangle(points_list)

    print("The number of right triangles is:", right_triangle_count)

main()
