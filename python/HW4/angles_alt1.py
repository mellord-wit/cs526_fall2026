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
For the 1000-point test file that is about 1,000,000 directions, well under
the 30 second limit.

========================================================================
More Complete Explanation
========================================================================

Big idea: count each triangle at its right angle
    Every right triangle has exactly one right angle (the other two angles add up
    to 90 degrees, so neither can be 90). So if we stand at each point P in turn
    and count the right triangles whose right angle is AT P, every triangle is
    counted exactly once.

    A right angle at P means there are two other points Q and R such that the
    leg P->Q is perpendicular to the leg P->R. So for each P we need to answer:
    "how many pairs (Q, R) leave P in perpendicular directions?"

Step 1: turn every other point into a reduced direction (a ray out of P)
    For each other point Q, the vector from P to Q is (dx, dy) = Q - P.
    Divide both parts by g = gcd(|dx|, |dy|) to get the smallest integer
    vector pointing the same way:
        (2, 4) -> gcd 2 -> (1, 2)
        (3, 6) -> gcd 3 -> (1, 2)      same ray as (2, 4)
        (0, 4) -> gcd 4 -> (0, 1)      straight up
        (-6, 0)-> gcd 6 -> (-1, 0)     straight left
    Points that lie on the same ray out of P get the same reduced direction.

    - gcd is always >= 0, so the signs of dx and dy are kept. That means
      (1, 2) and (-1, -2) stay DIFFERENT: they are opposite rays. That is what
      we want, because each ray has exactly one ray 90 degrees counterclockwise
      from it (see Step 3).
    - g is never 0, because Q != P means dx and dy are not both 0.
    - dx // g is exact (g divides dx), so // gives the right answer even when
      dx is negative.
    - Only integers are used, so there is no rounding error. Two directions are
      either exactly equal or not.

Step 2: count the points on each ray
    direction_counts[(a, b)] = how many points are on ray (a, b) out of P.

Step 3: pair each ray with the ray rotated +90 degrees
    Rotating (a, b) by 90 degrees counterclockwise gives (-b, a).
    They are perpendicular because the dot product is 0:
        (a, b) . (-b, a) = a*(-b) + b*a = 0
    If ray (a, b) has c1 points and ray (-b, a) has c2 points, then any of the
    c1 points can be Q and any of the c2 points can be R. That makes
    c1 * c2 different right triangles with the right angle at P.

    Why only +90 and not -90 too?
        Suppose rays u and v are perpendicular, with v = u rotated +90.
        - Looking at u, we check u + 90 = v      -> found, counted.
        - Looking at v, we check v + 90 = -u     -> a different ray, so this
          pair is not counted again.
        If we also checked -90 from v we would find u, and every triangle
        would be counted twice.

    Points in a line are never counted: two points on the same ray as P, or on
    opposite rays, have directions 0 or 180 degrees apart, never 90.

Simple example 1 (rightangles_1.txt, answer 4)
    A = (0, 0)   B = (0, 4)   C = (0, 7)   D = (3, 0)   E = (9, 0)

        y
        7  C
        4  B
        0  A . . D . . . . . E
           0     3           9   x

    P = A (0, 0):
        B: (0, 4) -> (0, 1)      C: (0, 7) -> (0, 1)
        D: (3, 0) -> (1, 0)      E: (9, 0) -> (1, 0)
        direction_counts = {(0, 1): 2, (1, 0): 2}
        (1, 0) rotated +90 is (0, 1): present -> 2 * 2 = 4
        (0, 1) rotated +90 is (-1, 0): not present -> 0
        Triangles at A: ABD, ABE, ACD, ACE = 4

    P = B (0, 4):
        A: (0, -4) -> (0, -1)    C: (0, 3) -> (0, 1)
        D: (3, -4) -> (3, -4)    E: (9, -4) -> (9, -4)
        Rotated +90: (1, 0), (-1, 0), (4, 3), (4, 9) -> none present -> 0
        (A and C are on opposite rays, 180 degrees apart, so no triangle.)

    P = C, D, E: no perpendicular pairs either -> 0
        (e.g. at D the rays are (-1, 0), (-3, 4), (-3, 7), (1, 0); their
         +90 rotations (0, -1), (-4, -3), (-7, -3), (0, 1) are all missing.)

    Total = 4 + 0 + 0 + 0 + 0 = 4

Simple example 2 (a tilted right angle, answer 1)
    P = (0, 0)   Q = (4, 2)   R = (-1, 2)

    P = (0, 0):
        Q: (4, 2) -> gcd 2 -> (2, 1)
        R: (-1, 2)          -> (-1, 2)
        (2, 1) rotated +90 is (-1, 2): present -> 1 * 1 = 1
        (-1, 2) rotated +90 is (-2, -1): not present -> 0
        This is why only +90 is checked: the pair is found once, from (2, 1).

    P = (4, 2):
        rays (-2, -1) and (-1, 0); +90 gives (1, -2) and (0, -1) -> 0
    P = (-1, 2):
        rays (1, -2) and (1, 0); +90 gives (2, 1) and (0, 1) -> 0

    Total = 1. The right angle is at (0, 0) even though no side is horizontal
    or vertical. A slope test would need floats here; the reduced directions
    don't.
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
