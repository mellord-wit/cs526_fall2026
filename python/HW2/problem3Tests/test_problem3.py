"""Unit tests for Problem 3.1 (Climbing Stairs) in problem3.py.

Run from the HW2 folder with either of:
    python3 -m unittest discover problem3Tests -v
    python3 problem3Tests/test_problem3.py -v
"""
import io
import os
import sys
import unittest
from contextlib import redirect_stdout
from itertools import product

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
# problem3.py lives one folder up.
sys.path.insert(0, os.path.dirname(TEST_DIR))

# problem3.py prints its answers when it is imported; keep that out of the test output.
with redirect_stdout(io.StringIO()):
    import problem3
from problem3 import ways, ways_1_or_2


def all_climbs(n, moves):
    """Every sequence of moves that adds up to exactly n steps (brute force)."""
    climbs = []
    for length in range(n + 1):
        for climb in product(moves, repeat=length):
            if sum(climb) == n:
                climbs.append(climb)
    return climbs


class TestProblem3(unittest.TestCase):

    # ---------- ways(n): 1, 2, or 3 steps per move ----------

    def test_01_base_cases(self):
        self.assertEqual(ways(0), 1)    # climbing nothing is one way
        self.assertEqual(ways(1), 1)    # 1
        self.assertEqual(ways(2), 2)    # 1+1, 2

    def test_02_problem_example(self):
        # Homework2.txt: a staircase with 4 steps can be climbed in 7 ways.
        self.assertEqual(ways(4), 7)
        expected = {(1, 1, 1, 1), (1, 1, 2), (1, 2, 1), (2, 1, 1), (1, 3), (3, 1), (2, 2)}
        self.assertEqual(set(all_climbs(4, (1, 2, 3))), expected)

    def test_03_required_outputs(self):
        # The values the problem asks students to output.
        self.assertEqual(ways(3), 4)
        self.assertEqual(ways(5), 13)
        self.assertEqual(ways(10), 274)

    def test_04_first_sixteen_values(self):
        expected = [1, 1, 2, 4, 7, 13, 24, 44, 81, 149, 274, 504, 927, 1705, 3136, 5768]
        self.assertEqual([ways(n) for n in range(16)], expected)

    def test_05_matches_brute_force(self):
        # Count every possible climb directly and compare.
        for n in range(13):
            with self.subTest(n=n):
                self.assertEqual(ways(n), len(all_climbs(n, (1, 2, 3))))

    def test_06_recurrence(self):
        # The first move is 1, 2, or 3 steps, so each value is the sum of the three before it.
        for n in range(3, 21):
            with self.subTest(n=n):
                self.assertEqual(ways(n), ways(n - 1) + ways(n - 2) + ways(n - 3))

    def test_07_larger_value(self):
        self.assertEqual(ways(20), 121415)

    def test_08_uses_recursion(self):
        # Count calls to ways by temporarily wrapping it. A recursive solution
        # calls itself through this wrapper; a loop would call it only once.
        calls = []
        original = problem3.ways

        def counting_ways(n):
            calls.append(n)
            return original(n)

        problem3.ways = counting_ways
        try:
            result = problem3.ways(5)
        finally:
            problem3.ways = original

        self.assertEqual(result, 13)
        self.assertGreater(len(calls), 1)

    # ---------- ways_1_or_2(n): question c, 1 or 2 steps per move ----------

    def test_09_one_or_two_steps_is_fibonacci(self):
        expected = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        self.assertEqual([ways_1_or_2(n) for n in range(12)], expected)

    def test_10_one_or_two_steps_matches_brute_force(self):
        for n in range(15):
            with self.subTest(n=n):
                self.assertEqual(ways_1_or_2(n), len(all_climbs(n, (1, 2))))

    # ---------- Comparison with doIt (question b) ----------

    def test_11_same_base_cases_as_doIt(self):
        # doIt in Problem 3 starts 1, 1, 2 as well, but subtracts the third term,
        # so the two sequences split apart from n = 3 on.
        def doIt(n):
            if n == 0 or n == 1:
                return 1
            elif n == 2:
                return 2
            return doIt(n - 1) + doIt(n - 2) - doIt(n - 3)

        self.assertEqual([ways(n) for n in range(3)], [doIt(n) for n in range(3)])
        for n in range(3, 10):
            with self.subTest(n=n):
                self.assertNotEqual(ways(n), doIt(n))


if __name__ == "__main__":
    unittest.main()
