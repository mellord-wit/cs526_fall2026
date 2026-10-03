"""
Unit tests for ghostbusters_shoot_any_ghost.py.

The file tests run ghostbusters_shoot_any_ghost_solution1 on each ghostbusters_input_x.txt and
compare the result with the matching ghostbusters_ans_x.txt. The remaining tests build small
inputs by hand to cover cases the files do not: a pairing other than the one written in the
file, vertical and horizontal lines, and checks on the pairing that is returned.
"""
import os
import sys
import unittest

# The solution lives in the parent HW3 folder and the data files in HW3/ghostbusters_resources.
HW3_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_DIR = os.path.join(HW3_DIR, "ghostbusters_resources")
sys.path.insert(0, HW3_DIR)

from ghostbusters_shoot_any_ghost import ghostbusters_shoot_any_ghost_solution
from ghostbusters_shoot_any_ghost import ghostbusters_shoot_any_ghost_solution1

ELIMINATED = "All Ghosts: were eliminated"
NOT_ELIMINATED = "All Ghosts: were not eliminated"


def make_input(pairs):
    # pairs is a list of (ghostbuster_x, ghostbuster_y, ghost_x, ghost_y) tuples.
    file_lines = [str(len(pairs)) + "\n"]
    for pair in pairs:
        file_lines.append("B " + str(pair[0]) + " " + str(pair[1]) + " G " + str(pair[2]) + " " + str(pair[3]) + "\n")
    return file_lines


class GhostbustersShootAnyGhostFileTest(unittest.TestCase):

    def run_case(self, case_number):
        input_file = os.path.join(RESOURCES_DIR, "ghostbusters_input_" + str(case_number) + ".txt")
        answer_file = os.path.join(RESOURCES_DIR, "ghostbusters_ans_" + str(case_number) + ".txt")

        result, lines = ghostbusters_shoot_any_ghost_solution1(input_file)

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
        # Not compared with ghostbusters_ans_10.txt. That answer is for ghostbusters.py, where the
        # repeated pair puts two streams on the same line. Here the ghosts can be re-paired.
        input_file = os.path.join(RESOURCES_DIR, "ghostbusters_input_10.txt")
        result, lines = ghostbusters_shoot_any_ghost_solution1(input_file)
        self.assertEqual(ELIMINATED, result)


class GhostbustersShootAnyGhostCaseTest(unittest.TestCase):

    def assert_valid_pairing(self, pairs, lines):
        # Every ghostbuster and every ghost is used exactly once, and every line is parallel.
        ghostbusters = sorted([[pair[0], pair[1]] for pair in pairs])
        ghosts = sorted([[pair[2], pair[3]] for pair in pairs])
        self.assertEqual(ghostbusters, sorted([line[0] for line in lines]))
        self.assertEqual(ghosts, sorted([line[1] for line in lines]))

        first_dx = lines[0][1][0] - lines[0][0][0]
        first_dy = lines[0][1][1] - lines[0][0][1]
        for line in lines:
            dx = line[1][0] - line[0][0]
            dy = line[1][1] - line[0][1]
            # Two directions are parallel when their cross product is 0.
            self.assertEqual(0, first_dx * dy - first_dy * dx)

    def test_sample_from_assignment(self):
        # As written the slopes are 1 and -1, and swapping the ghosts gives a vertical line
        # and slope 5/2, so no pairing works.
        pairs = [(0, 0, 5, 5), (3, 0, 0, 3)]
        result, lines = ghostbusters_shoot_any_ghost_solution(make_input(pairs))
        self.assertEqual(NOT_ELIMINATED, result)
        self.assertIsNone(lines)

    def test_file_pairing_fails_but_another_pairing_works(self):
        # As written the slopes are 1/11 and -2/3, but pairing B(0,0)-G(4,4) and B(10,0)-G(11,1)
        # makes both lines slope 1.
        pairs = [(0, 0, 11, 1), (10, 0, 4, 4)]
        result, lines = ghostbusters_shoot_any_ghost_solution(make_input(pairs))
        self.assertEqual(ELIMINATED, result)
        self.assert_valid_pairing(pairs, lines)

    def test_shuffled_ghosts_still_eliminated(self):
        # Each ghost sits 2 right and 3 up from some ghostbuster, but not the one on its line.
        pairs = [(0, 0, 7, 9), (5, 6, 4, 4), (2, 1, 2, 3), (0, 3, 2, 6)]
        result, lines = ghostbusters_shoot_any_ghost_solution(make_input(pairs))
        self.assertEqual(ELIMINATED, result)
        self.assert_valid_pairing(pairs, lines)

    def test_vertical_lines(self):
        # Vertical lines have no slope, which would divide by zero in calc_slope().
        pairs = [(1, 0, 3, 8), (3, 2, 1, 5), (7, 0, 7, -4)]
        result, lines = ghostbusters_shoot_any_ghost_solution(make_input(pairs))
        self.assertEqual(ELIMINATED, result)
        self.assert_valid_pairing(pairs, lines)

    def test_horizontal_lines(self):
        pairs = [(0, 1, 9, 2), (0, 2, -4, 1)]
        result, lines = ghostbusters_shoot_any_ghost_solution(make_input(pairs))
        self.assertEqual(ELIMINATED, result)
        self.assert_valid_pairing(pairs, lines)

    def test_slopes_too_close_to_round(self):
        # Slopes 1000/1001 and 999/1000 both round to 0.999, so a rounded slope check would
        # wrongly call these parallel. Swapping the ghosts gives slopes 1004/1000 and 995/1001.
        pairs = [(0, 0, 1001, 1000), (0, 5, 1000, 1004)]
        result, lines = ghostbusters_shoot_any_ghost_solution(make_input(pairs))
        self.assertEqual(NOT_ELIMINATED, result)

    def test_single_ghostbuster(self):
        # One line is always parallel to itself.
        pairs = [(3, 4, -2, 9)]
        result, lines = ghostbusters_shoot_any_ghost_solution(make_input(pairs))
        self.assertEqual(ELIMINATED, result)
        self.assert_valid_pairing(pairs, lines)

    def test_ghost_on_top_of_first_ghostbuster_is_skipped(self):
        # G(0,0) sits on B(0,0) and gives no direction to try, but G(2,2) does: every point
        # is on the line y = x, so the ghosts can all be paired along it.
        pairs = [(0, 0, 0, 0), (-2, -2, 2, 2)]
        result, lines = ghostbusters_shoot_any_ghost_solution(make_input(pairs))
        self.assertEqual(ELIMINATED, result)
        self.assert_valid_pairing(pairs, lines)

    def test_blank_trailing_line_is_ignored(self):
        file_lines = make_input([(0, 0, 1, 1), (5, 0, 6, 1)]) + ["\n"]
        result, lines = ghostbusters_shoot_any_ghost_solution(file_lines)
        self.assertEqual(ELIMINATED, result)
        self.assertEqual(2, len(lines))

    def test_no_ghostbusters(self):
        result, lines = ghostbusters_shoot_any_ghost_solution(["0\n"])
        self.assertEqual(ELIMINATED, result)
        self.assertEqual([], lines)


if __name__ == "__main__":
    unittest.main()
