"""
Unit tests for unique_substrings.py, covering the strings used in its demo.

Each test reads the string from unique_substrings_input_x.txt, runs one of the two
solutions on it, and compares the substrings it finds and their count with the matching
unique_substrings_ans_x.txt (one substring per line, then the count on the last line).
unique_substrings_using_recursion returns (count, substrings), so its tests check both.
"""
import os
import sys
import unittest

# The solution lives in the parent HW3 folder and the data files in HW3/unique_substrings_resources.
HW3_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_DIR = os.path.join(HW3_DIR, "unique_substrings_resources")
sys.path.insert(0, HW3_DIR)

from unique_substrings import distinctSubstring, unique_substrings_using_recursion


class UniqueSubstringsTest(unittest.TestCase):

    def run_case(self, case_number, solution):
        input_file = os.path.join(RESOURCES_DIR, "unique_substrings_input_" + str(case_number) + ".txt")
        answer_file = os.path.join(RESOURCES_DIR, "unique_substrings_ans_" + str(case_number) + ".txt")

        with open(input_file, "r") as file:
            string = file.read().strip()

        with open(answer_file, "r") as file:
            answer_lines = file.read().split()
        expected_substrings = set(answer_lines[:-1])
        expected_count = int(answer_lines[-1])

        result = solution(string)

        self.assertEqual(expected_substrings, result)
        self.assertEqual(expected_count, len(result))

    def test_distinct_substring_0(self):
        self.run_case(0, distinctSubstring)

    def test_distinct_substring_1(self):
        self.run_case(1, distinctSubstring)

    def test_distinct_substring_2(self):
        self.run_case(2, distinctSubstring)

    def run_recursion_case(self, case_number):
        # unique_substrings_using_recursion returns (count, substrings), so check both.
        input_file = os.path.join(RESOURCES_DIR, "unique_substrings_input_" + str(case_number) + ".txt")
        answer_file = os.path.join(RESOURCES_DIR, "unique_substrings_ans_" + str(case_number) + ".txt")

        with open(input_file, "r") as file:
            string = file.read().strip()

        with open(answer_file, "r") as file:
            answer_lines = file.read().split()
        expected_substrings = set(answer_lines[:-1])
        expected_count = int(answer_lines[-1])

        count, substrings = unique_substrings_using_recursion(string)

        self.assertEqual(expected_substrings, substrings)
        self.assertEqual(expected_count, count)

    def test_unique_substrings_using_recursion_0(self):
        self.run_recursion_case(0)

    def test_unique_substrings_using_recursion_1(self):
        self.run_recursion_case(1)

    def test_unique_substrings_using_recursion_2(self):
        self.run_recursion_case(2)

    def test_unique_substrings_using_recursion_edge_cases(self):
        self.assertEqual((0, set()), unique_substrings_using_recursion(""))
        self.assertEqual((1, {"a"}), unique_substrings_using_recursion("a"))
        self.assertEqual((3, {"a", "aa", "aaa"}), unique_substrings_using_recursion("aaa"))
        self.assertEqual((6, {"a", "b", "c", "ab", "bc", "abc"}), unique_substrings_using_recursion("abc"))


if __name__ == "__main__":
    unittest.main()
