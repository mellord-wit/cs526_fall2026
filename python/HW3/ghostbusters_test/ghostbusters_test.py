"""
Unit tests for ghostbusters.py, one per execution in ghostbuster_test_main().

Each test runs ghostbusters_solution1 on ghostbusters_input_x.txt and compares the
result it returns with the contents of the matching ghostbusters_ans_x.txt.
"""
import os
import sys
import unittest

# The solution lives in the parent HW3 folder and the data files in HW3/ghostbusters_resources.
HW3_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_DIR = os.path.join(HW3_DIR, "ghostbusters_resources")
sys.path.insert(0, HW3_DIR)

from ghostbusters import ghostbusters_solution1


class GhostbustersTest(unittest.TestCase):

    def run_case(self, case_number):
        input_file = os.path.join(RESOURCES_DIR, "ghostbusters_input_" + str(case_number) + ".txt")
        answer_file = os.path.join(RESOURCES_DIR, "ghostbusters_ans_" + str(case_number) + ".txt")

        result, lines = ghostbusters_solution1(input_file)

        with open(answer_file, "r") as file:
            expected = file.read().strip()

        self.assertEqual(expected, result)

    def test_ghostbusters_input_0(self):
        self.run_case(0)

    def test_ghostbusters_input_1(self):
        self.run_case(1)

    def test_ghostbusters_input_2(self):
        self.run_case(2)

    def test_ghostbusters_input_3(self):
        self.run_case(3)

    def test_ghostbusters_input_4(self):
        self.run_case(4)

    def test_ghostbusters_input_5(self):
        self.run_case(5)

    def test_ghostbusters_input_6(self):
        self.run_case(6)

    def test_ghostbusters_input_7(self):
        self.run_case(7)

    def test_ghostbusters_input_8(self):
        self.run_case(8)

    def test_ghostbusters_input_9(self):
        self.run_case(9)

    def test_ghostbusters_input_10(self):
        self.run_case(10)


if __name__ == "__main__":
    unittest.main()
