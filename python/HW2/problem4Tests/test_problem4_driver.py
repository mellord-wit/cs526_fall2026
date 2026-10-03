"""File-driven unit tests for Problem 4.1.

These mirror the tests in test_problem4.py, but each numbered test feeds the
matching problem_test<N>.txt file in this folder to problem4_driver and
checks the final list and everything the driver printed.

Run from the HW2 folder with either of:
    python3 -m unittest discover problem4Tests -v
    python3 problem4Tests/test_problem4_driver.py -v
"""
import io
import os
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
# problem4.py and problem4_driver.py live one folder up.
sys.path.insert(0, os.path.dirname(TEST_DIR))

from problem4_driver import problem4_driver


class TestProblem4Driver(unittest.TestCase):

    def run_test_file(self, file_name):
        """Run problem4_driver on a test file and return (list, stdout lines, stderr lines)."""
        with open(os.path.join(TEST_DIR, file_name)) as test_file:
            lines = test_file.readlines()

        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            my_list = problem4_driver(lines)
        return my_list, out.getvalue().splitlines(), err.getvalue().splitlines()

    def assertListValues(self, my_list, expected):
        """Walk the list both ways and check the values, length, head and tail."""
        forward = []
        node = my_list.head
        while node is not None:
            forward.append(node.value)
            node = node.next

        backward = []
        node = my_list.tail
        while node is not None:
            backward.append(node.value)
            node = node.prev

        self.assertEqual(forward, expected)
        self.assertEqual(backward, expected[::-1])
        self.assertEqual(len(my_list), len(expected))
        if expected:
            self.assertIsNone(my_list.head.prev)
            self.assertIsNone(my_list.tail.next)
        else:
            self.assertIsNone(my_list.head)
            self.assertIsNone(my_list.tail)

    # ---------- add ----------

    def test_01_add_keeps_sorted_order(self):
        my_list, out, err = self.run_test_file("problem_test1.txt")
        self.assertListValues(my_list, [2, 4, 8, 10, 15, 29, 41])
        self.assertEqual(out, ["Final list: 2 <-> 4 <-> 8 <-> 10 <-> 15 <-> 29 <-> 41"])
        self.assertEqual(err, [])

    def test_02_add_front_end_middle(self):
        # Adds to an empty list, then a new head, a new tail, and a middle value.
        my_list, out, err = self.run_test_file("problem_test2.txt")
        self.assertListValues(my_list, [1, 5, 7, 9])
        self.assertEqual(out, [
            "5",
            "1 <-> 5",
            "1 <-> 5 <-> 9",
            "Final list: 1 <-> 5 <-> 7 <-> 9",
        ])
        self.assertEqual(err, [])

    def test_03_add_duplicates(self):
        my_list, out, err = self.run_test_file("problem_test3.txt")
        self.assertListValues(my_list, [1, 1, 2, 3, 3, 3])
        self.assertEqual(out, ["Final list: 1 <-> 1 <-> 2 <-> 3 <-> 3 <-> 3"])
        self.assertEqual(err, [])

    # ---------- delete ----------

    def test_04_delete_head_middle_tail(self):
        # Deletes the middle, head, and tail; the last add checks the tail moved back.
        my_list, out, err = self.run_test_file("problem_test4.txt")
        self.assertListValues(my_list, [4, 10, 20])
        self.assertEqual(out, [
            "2 <-> 4 <-> 10 <-> 15",
            "4 <-> 10 <-> 15",
            "4 <-> 10",
            "Final list: 4 <-> 10 <-> 20",
        ])
        self.assertEqual(err, [])

    def test_05_delete_missing_and_duplicates(self):
        # Missing values below, between, and above; then removes one copy of 8.
        my_list, out, err = self.run_test_file("problem_test5.txt")
        self.assertListValues(my_list, [2, 8, 10])
        self.assertEqual(out, [
            "2 <-> 8 <-> 8 <-> 10",
            "Final list: 2 <-> 8 <-> 10",
        ])
        self.assertEqual(err, [
            "line 5: 1 not found, nothing deleted",
            "line 6: 5 not found, nothing deleted",
            "line 7: 99 not found, nothing deleted",
        ])

    def test_06_delete_until_empty_then_add(self):
        my_list, out, err = self.run_test_file("problem_test6.txt")
        self.assertListValues(my_list, [7])
        self.assertEqual(out, [
            "(empty)",
            "Final list: 7",
        ])
        self.assertEqual(err, ["line 8: 3 not found, nothing deleted"])

    # ---------- exists ----------

    def test_07_exists(self):
        my_list, out, err = self.run_test_file("problem_test7.txt")
        self.assertListValues(my_list, [2, 4, 8, 10])
        self.assertEqual(out, [
            "exists(1) = False",        # empty list
            "exists(2) = True",
            "exists(4) = True",
            "exists(8) = True",
            "exists(10) = True",
            "exists(1) = False",        # below every value
            "exists(5) = False",        # between values
            "exists(11) = False",       # above every value
            "Final list: 2 <-> 4 <-> 8 <-> 10",
        ])
        self.assertEqual(err, [])

    # ---------- print_list ----------

    def test_08_print_list(self):
        my_list, out, err = self.run_test_file("problem_test8.txt")
        self.assertListValues(my_list, [2, 4, 10])
        self.assertEqual(out, [
            "(empty)",
            "7",
            "2 <-> 4 <-> 10",
            "Final list: 2 <-> 4 <-> 10",
        ])
        self.assertEqual(err, [])

    # ---------- total ----------

    def test_09_total(self):
        # Empty, one value, the example list, then negative values added.
        my_list, out, err = self.run_test_file("problem_test9.txt")
        self.assertListValues(my_list, [-5, -2, 2, 3, 4, 8, 10, 15, 29, 41])
        self.assertEqual(out, [
            "total = 0",
            "total = 7",
            "total = 109",
            "total = 105",
            "Final list: -5 <-> -2 <-> 2 <-> 3 <-> 4 <-> 8 <-> 10 <-> 15 <-> 29 <-> 41",
        ])
        self.assertEqual(err, [])

    # ---------- sum_middle_three ----------

    def test_10_sum_middle_three_odd(self):
        my_list, out, err = self.run_test_file("problem_test10.txt")
        self.assertListValues(my_list, [1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(out, [
            "sum_middle_three = 6",     # 1 + 2 + 3
            "sum_middle_three = 9",     # 2 + 3 + 4
            "sum_middle_three = 12",    # 3 + 4 + 5
            "Final list: 1 <-> 2 <-> 3 <-> 4 <-> 5 <-> 6 <-> 7",
        ])
        self.assertEqual(err, [])

    def test_11_sum_middle_three_even(self):
        # positions mid-2, mid-1, mid where mid = n // 2
        my_list, out, err = self.run_test_file("problem_test11.txt")
        self.assertListValues(my_list, [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(out, [
            "sum_middle_three = 6",     # 4 nodes: 1 + 2 + 3
            "sum_middle_three = 9",     # 6 nodes: 2 + 3 + 4
            "sum_middle_three = 12",    # 8 nodes: 3 + 4 + 5
            "Final list: 1 <-> 2 <-> 3 <-> 4 <-> 5 <-> 6 <-> 7 <-> 8",
        ])
        self.assertEqual(err, [])

    def test_12_sum_middle_three_too_short(self):
        # 0, 1, and 2 nodes each print a warning; 3 nodes works.
        my_list, out, err = self.run_test_file("problem_test12.txt")
        self.assertListValues(my_list, [1, 2, 3])
        self.assertEqual(out, [
            "sum_middle_three = 6",
            "Final list: 1 <-> 2 <-> 3",
        ])
        self.assertEqual(err, [
            "line 1: sum_middle_three needs at least 3 nodes",
            "line 3: sum_middle_three needs at least 3 nodes",
            "line 5: sum_middle_three needs at least 3 nodes",
        ])

    # ---------- median ----------

    def test_13_median(self):
        my_list, out, err = self.run_test_file("problem_test13.txt")
        self.assertListValues(my_list, [1, 2, 7, 10])
        self.assertEqual(out, [
            "median = 7",               # 7
            "median = 4.0",             # 1, 7
            "median = 2",               # 1, 2, 7
            "median = 4.5",             # 1, 2, 7, 10
            "Final list: 1 <-> 2 <-> 7 <-> 10",
        ])
        self.assertEqual(err, [])

    def test_14_median_empty(self):
        my_list, out, err = self.run_test_file("problem_test14.txt")
        self.assertListValues(my_list, [5])
        self.assertEqual(out, [
            "median = 5",
            "Final list: 5",
        ])
        self.assertEqual(err, ["line 1: median of an empty list"])

    # ---------- count ----------

    def test_15_count(self):
        my_list, out, err = self.run_test_file("problem_test15.txt")
        self.assertListValues(my_list, [2, 4, 8, 8, 8, 10, 15])
        self.assertEqual(out, [
            "count(8) = 0",             # empty list
            "count(8) = 3",
            "count(2) = 1",             # first value
            "count(15) = 1",            # last value
            "count(5) = 0",
            "count(99) = 0",
            "Final list: 2 <-> 4 <-> 8 <-> 8 <-> 8 <-> 10 <-> 15",
        ])
        self.assertEqual(err, [])

    # ---------- Everything together ----------

    def test_16_problem_example(self):
        # The example from Problem 4.1 in Homework2.txt.
        my_list, out, err = self.run_test_file("problem_test16.txt")
        self.assertListValues(my_list, [2, 4, 8, 8, 10, 15, 29])
        self.assertEqual(out, [
            "2 <-> 4 <-> 8 <-> 10 <-> 15 <-> 29 <-> 41",
            "total = 109",
            "sum_middle_three = 33",
            "median = 10",
            "2 <-> 4 <-> 8 <-> 10 <-> 15 <-> 29",
            "total = 68",
            "sum_middle_three = 22",
            "median = 9.0",
            "2 <-> 4 <-> 8 <-> 8 <-> 10 <-> 15 <-> 29",
            "count(8) = 2",
            "count(5) = 0",
            "exists(15) = True",
            "exists(5) = False",
            "Final list: 2 <-> 4 <-> 8 <-> 8 <-> 10 <-> 15 <-> 29",
        ])
        self.assertEqual(err, [])

    # ---------- Driver errors ----------

    def test_17_bad_directives(self):
        # Every bad line prints a warning and the driver keeps going. Directives
        # are not case sensitive, and values may be decimals.
        my_list, out, err = self.run_test_file("problem_test17.txt")
        self.assertListValues(my_list, [1, 2.5, 5])
        self.assertEqual(out, ["Final list: 1 <-> 2.5 <-> 5"])
        self.assertEqual(err, [
            "line 2: unknown directive 'insert'",
            "line 3: expected 'add <value>', got 'add'",
            "line 4: value must be a number, got 'add x'",
            "line 5: expected 'total', got 'total 3'",
            "line 6: expected 'delete <value>', got 'delete 5 6'",
        ])


if __name__ == "__main__":
    unittest.main()
