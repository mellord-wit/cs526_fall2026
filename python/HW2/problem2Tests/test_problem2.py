"""Unit tests for Problem 2.

Each numbered test feeds the matching problem_test<N>.txt file in this folder
to problem2_driver and checks the final list and everything it printed.

Run from the HW2 folder with either of:
    python3 -m unittest discover problem2Tests -v
    python3 problem2Tests/test_problem2.py -v
"""
import io
import os
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
# problem2.py and problem2_driver.py live one folder up.
sys.path.insert(0, os.path.dirname(TEST_DIR))

from problem2_driver import problem2_driver


class TestProblem2Driver(unittest.TestCase):

    def run_test_file(self, file_name):
        """Run problem2_driver on a test file and return (list, stdout lines, stderr lines)."""
        with open(os.path.join(TEST_DIR, file_name)) as test_file:
            lines = test_file.readlines()

        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            my_list = problem2_driver(lines)
        return my_list, out.getvalue().splitlines(), err.getvalue().splitlines()

    def assertListContents(self, my_list, expected):
        """Check the values, the length, and that head and tail are consistent."""
        self.assertEqual(list(my_list), expected)
        self.assertEqual(len(my_list), len(expected))
        if expected:
            self.assertEqual(my_list.head.value, expected[0])
            self.assertEqual(my_list.tail.value, expected[-1])
            self.assertIsNone(my_list.tail.next)
        else:
            self.assertIsNone(my_list.head)
            self.assertIsNone(my_list.tail)

    # ---------- Create ----------

    def test_01_append(self):
        my_list, out, err = self.run_test_file("problem_test1.txt")
        self.assertListContents(my_list, [12, 3, 5, 2])
        self.assertEqual(out, ["Final list: 12 -> 3 -> 5 -> 2"])
        self.assertEqual(err, [])

    def test_02_prepend(self):
        # The final append checks that prepend on an empty list also set the tail.
        my_list, out, err = self.run_test_file("problem_test2.txt")
        self.assertListContents(my_list, [12, 3, 5, 2, 7])
        self.assertEqual(out, ["Final list: 12 -> 3 -> 5 -> 2 -> 7"])
        self.assertEqual(err, [])

    def test_03_insert(self):
        # Inserts into an empty list, at the front, at the end, and in the middle.
        my_list, out, err = self.run_test_file("problem_test3.txt")
        self.assertListContents(my_list, [1, 3, 5, 7, 9, 11])
        self.assertEqual(out, ["Final list: 1 -> 3 -> 5 -> 7 -> 9 -> 11"])
        self.assertEqual(err, [])

    # ---------- Read ----------

    def test_04_get(self):
        my_list, out, err = self.run_test_file("problem_test4.txt")
        self.assertListContents(my_list, [12, 3, 5, 2])
        self.assertEqual(out, [
            "get(0) = 12",
            "get(2) = 5",
            "get(3) = 2",
            "Final list: 12 -> 3 -> 5 -> 2",
        ])
        self.assertEqual(err, [])

    def test_05_find(self):
        # find returns the first match, -1 when missing, and works on text values.
        my_list, out, err = self.run_test_file("problem_test5.txt")
        self.assertListContents(my_list, [12, 3, 5, 3, "hello world"])
        self.assertEqual(out, [
            "find(12) = 0",
            "find(3) = 1",
            "find(42) = -1",
            "find(hello world) = 4",
            "Final list: 12 -> 3 -> 5 -> 3 -> hello world",
        ])
        self.assertEqual(err, [])

    def test_06_len(self):
        my_list, out, err = self.run_test_file("problem_test6.txt")
        self.assertListContents(my_list, [3])
        self.assertEqual(out, [
            "len = 0",
            "len = 2",
            "len = 1",
            "Final list: 3",
        ])
        self.assertEqual(err, [])

    # ---------- Update ----------

    def test_07_update(self):
        # Updates the head, a middle node, and the tail.
        my_list, out, err = self.run_test_file("problem_test7.txt")
        self.assertListContents(my_list, [1, 3, 50, 20])
        self.assertEqual(out, [
            "get(3) = 20",
            "Final list: 1 -> 3 -> 50 -> 20",
        ])
        self.assertEqual(err, [])

    # ---------- Delete ----------

    def test_08_delete(self):
        # Deletes only the first duplicate, then the head, then the tail;
        # the append checks the tail moved back, and 42 is not in the list.
        my_list, out, err = self.run_test_file("problem_test8.txt")
        self.assertListContents(my_list, [5, 3, 8])
        self.assertEqual(out, ["Final list: 5 -> 3 -> 8"])
        self.assertEqual(err, ["line 10: 42 not found, nothing deleted"])

    def test_09_delete_at(self):
        # Deletes from the middle, front and end, empties the list, then refills it.
        my_list, out, err = self.run_test_file("problem_test9.txt")
        self.assertListContents(my_list, [4])
        self.assertEqual(out, [
            "delete_at(1) = 3",
            "delete_at(0) = 12",
            "delete_at(1) = 2",
            "delete_at(0) = 5",
            "delete_at(0) = 9",
            "Final list: 4",
        ])
        self.assertEqual(err, [])

    # ---------- Print ----------

    def test_10_print_list(self):
        my_list, out, err = self.run_test_file("problem_test10.txt")
        self.assertListContents(my_list, [])
        self.assertEqual(out, [
            "(empty)",
            "12 -> 3",
            "3",
            "(empty)",
            "Final list: (empty)",
        ])
        self.assertEqual(err, [])

    # ---------- Errors and everything together ----------

    def test_11_bad_directives(self):
        # Every bad line prints a warning and the driver keeps going.
        my_list, out, err = self.run_test_file("problem_test11.txt")
        self.assertListContents(my_list, [1, 2])
        self.assertEqual(out, ["Final list: 1 -> 2"])
        self.assertEqual(err, [
            "line 2: unknown directive 'remove'",
            "line 3: expected 'append <value>', got 'append'",
            "line 4: index must be a whole number, got 'insert x 4'",
            "line 5: index 5 out of range",
            "line 6: expected 'update <index> <value>', got 'update 1'",
            "line 7: index -1 out of range",
            "line 8: expected 'len', got 'len 3'",
        ])

    def test_12_all_verbs(self):
        # Every directive in one file, plus a comment, a blank line and an
        # upper-case directive.
        my_list, out, err = self.run_test_file("problem_test12.txt")
        self.assertListContents(my_list, [12, 3, 5])
        self.assertEqual(out, [
            "get(2) = 99",
            "find(5) = 4",
            "len = 5",
            "1 -> 12 -> 100 -> 3 -> 5",
            "delete_at(0) = 1",
            "Final list: 12 -> 3 -> 5",
        ])
        self.assertEqual(err, [])


if __name__ == "__main__":
    unittest.main()
