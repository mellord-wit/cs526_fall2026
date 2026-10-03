"""
Unit tests for palendrome.py, one per input file in palendrome_resources.

Each test feeds palendrome_x.txt to run_palendrome_homework as stdin, captures what it
prints, and compares it with the contents of the matching palendrome_ans_x.txt.
"""
import io
import os
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

# The solution lives in the parent HW3 folder and the data files in HW3/palendrome_resources.
HW3_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_DIR = os.path.join(HW3_DIR, "palendrome_resources")
sys.path.insert(0, HW3_DIR)

from palendrome import run_palendrome_homework


class PalendromeTest(unittest.TestCase):

    def run_case(self, case_name):
        input_file = os.path.join(RESOURCES_DIR, "palendrome_" + case_name + ".txt")
        answer_file = os.path.join(RESOURCES_DIR, "palendrome_ans_" + case_name + ".txt")

        output = io.StringIO()
        with open(input_file, "r") as file, patch("sys.stdin", file), redirect_stdout(output):
            run_palendrome_homework()

        with open(answer_file, "r") as file:
            expected = file.read().strip()

        self.assertEqual(expected, output.getvalue().strip())

    def test_palendrome_0(self):
        self.run_case("0")

    def test_palendrome_1(self):
        self.run_case("1")

    def test_palendrome_2(self):
        self.run_case("2")

    def test_palendrome_3(self):
        self.run_case("3")

    def test_palendrome_4(self):
        self.run_case("4")

    def test_palendrome_0S(self):
        self.run_case("0S")

    def test_palendrome_1S(self):
        self.run_case("1S")

    def test_palendrome_2S(self):
        self.run_case("2S")

    def test_palendrome_3S(self):
        self.run_case("3S")

    def test_palendrome_4S(self):
        self.run_case("4S")

    def test_palendrome_0L(self):
        self.run_case("0L")

    def test_palendrome_1L(self):
        self.run_case("1L")

    def test_palendrome_2L(self):
        self.run_case("2L")

    def test_palendrome_3L(self):
        self.run_case("3L")

    def test_palendrome_4L(self):
        self.run_case("4L")


if __name__ == "__main__":
    unittest.main()
