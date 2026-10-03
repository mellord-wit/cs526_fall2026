"""Unit tests for Problem 4.1 (SortedDoublyLinkedList in problem4.py).

Run from the HW2 folder with either of:
    python3 -m unittest discover problem4Tests -v
    python3 problem4Tests/test_problem4.py -v
"""
import io
import os
import sys
import unittest
from contextlib import redirect_stdout

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
# problem4.py lives one folder up.
sys.path.insert(0, os.path.dirname(TEST_DIR))

from problem4 import SortedDoublyLinkedList


def build(values):
    my_list = SortedDoublyLinkedList()
    for value in values:
        my_list.add(value)
    return my_list


class TestProblem41(unittest.TestCase):

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

    def printed(self, my_list):
        out = io.StringIO()
        with redirect_stdout(out):
            my_list.print_list()
        return out.getvalue()

    # ---------- add ----------

    def test_01_add_keeps_sorted_order(self):
        my_list = build([10, 4, 29, 8, 2, 15, 41])
        self.assertListValues(my_list, [2, 4, 8, 10, 15, 29, 41])

    def test_02_add_front_end_middle(self):
        my_list = SortedDoublyLinkedList()
        my_list.add(5)                  # empty list
        self.assertListValues(my_list, [5])
        my_list.add(1)                  # new head
        self.assertListValues(my_list, [1, 5])
        my_list.add(9)                  # new tail
        self.assertListValues(my_list, [1, 5, 9])
        my_list.add(7)                  # middle
        self.assertListValues(my_list, [1, 5, 7, 9])

    def test_03_add_duplicates(self):
        my_list = build([3, 1, 3, 2, 3, 1])
        self.assertListValues(my_list, [1, 1, 2, 3, 3, 3])

    # ---------- delete ----------

    def test_04_delete_head_middle_tail(self):
        my_list = build([2, 4, 8, 10, 15])
        self.assertTrue(my_list.delete(8))      # middle
        self.assertListValues(my_list, [2, 4, 10, 15])
        self.assertTrue(my_list.delete(2))      # head
        self.assertListValues(my_list, [4, 10, 15])
        self.assertTrue(my_list.delete(15))     # tail
        self.assertListValues(my_list, [4, 10])
        my_list.add(20)                         # tail was updated correctly
        self.assertListValues(my_list, [4, 10, 20])

    def test_05_delete_missing_and_duplicates(self):
        my_list = build([2, 8, 8, 10])
        self.assertFalse(my_list.delete(1))     # smaller than everything
        self.assertFalse(my_list.delete(5))     # between values
        self.assertFalse(my_list.delete(99))    # larger than everything
        self.assertListValues(my_list, [2, 8, 8, 10])
        self.assertTrue(my_list.delete(8))      # removes only one copy
        self.assertListValues(my_list, [2, 8, 10])

    def test_06_delete_until_empty_then_add(self):
        my_list = build([3, 1, 2])
        for value in [2, 1, 3]:
            self.assertTrue(my_list.delete(value))
        self.assertListValues(my_list, [])
        self.assertFalse(my_list.delete(3))
        my_list.add(7)
        self.assertListValues(my_list, [7])

    # ---------- exists ----------

    def test_07_exists(self):
        my_list = build([2, 4, 8, 10])
        for value in [2, 4, 8, 10]:
            self.assertTrue(my_list.exists(value))
        for value in [1, 5, 11]:
            self.assertFalse(my_list.exists(value))
        self.assertFalse(SortedDoublyLinkedList().exists(1))

    # ---------- print_list ----------

    def test_08_print_list(self):
        self.assertEqual(self.printed(SortedDoublyLinkedList()), "(empty)\n")
        self.assertEqual(self.printed(build([7])), "7\n")
        self.assertEqual(self.printed(build([10, 2, 4])), "2 <-> 4 <-> 10\n")

    # ---------- total ----------

    def test_09_total(self):
        self.assertEqual(SortedDoublyLinkedList().total(), 0)
        self.assertEqual(build([7]).total(), 7)
        self.assertEqual(build([10, 4, 29, 8, 2, 15, 41]).total(), 109)
        self.assertEqual(build([-5, 3, -2]).total(), -4)

    # ---------- sum_middle_three ----------

    def test_10_sum_middle_three_odd(self):
        self.assertEqual(build([2, 4, 8, 10, 15, 29, 41]).sum_middle_three(), 33)  # 8 + 10 + 15
        self.assertEqual(build([1, 2, 3]).sum_middle_three(), 6)                   # all three
        self.assertEqual(build([1, 2, 3, 4, 5]).sum_middle_three(), 9)             # 2 + 3 + 4

    def test_11_sum_middle_three_even(self):
        # positions mid-2, mid-1, mid where mid = n // 2
        self.assertEqual(build([2, 4, 8, 10, 15, 29]).sum_middle_three(), 22)      # 4 + 8 + 10
        self.assertEqual(build([1, 2, 3, 4]).sum_middle_three(), 6)                # 1 + 2 + 3
        self.assertEqual(build([1, 2, 3, 4, 5, 6, 7, 8]).sum_middle_three(), 12)   # 3 + 4 + 5

    def test_12_sum_middle_three_too_short(self):
        for values in [[], [1], [1, 2]]:
            with self.assertRaises(ValueError):
                build(values).sum_middle_three()

    # ---------- median ----------

    def test_13_median(self):
        self.assertEqual(build([7]).median(), 7)
        self.assertEqual(build([10, 4, 29, 8, 2, 15, 41]).median(), 10)
        self.assertEqual(build([2, 4, 8, 10, 15, 29]).median(), 9.0)   # (8 + 10) / 2
        self.assertEqual(build([1, 2]).median(), 1.5)

    def test_14_median_empty(self):
        with self.assertRaises(ValueError):
            SortedDoublyLinkedList().median()

    # ---------- count ----------

    def test_15_count(self):
        my_list = build([2, 4, 8, 8, 10, 8, 15])
        self.assertEqual(my_list.count(8), 3)
        self.assertEqual(my_list.count(2), 1)
        self.assertEqual(my_list.count(15), 1)
        self.assertEqual(my_list.count(5), 0)
        self.assertEqual(my_list.count(99), 0)
        self.assertEqual(SortedDoublyLinkedList().count(8), 0)

    # ---------- Everything together ----------

    def test_16_problem_example(self):
        # The example from Problem 4.1 in Homework2.txt.
        my_list = build([10, 4, 29, 8, 2, 15, 41])
        self.assertEqual(self.printed(my_list), "2 <-> 4 <-> 8 <-> 10 <-> 15 <-> 29 <-> 41\n")
        self.assertEqual(my_list.total(), 109)
        self.assertEqual(my_list.sum_middle_three(), 33)
        self.assertEqual(my_list.median(), 10)

        my_list.delete(41)
        self.assertEqual(self.printed(my_list), "2 <-> 4 <-> 8 <-> 10 <-> 15 <-> 29\n")
        self.assertEqual(my_list.total(), 68)
        self.assertEqual(my_list.sum_middle_three(), 22)
        self.assertEqual(my_list.median(), 9.0)

        my_list.add(8)
        self.assertEqual(self.printed(my_list), "2 <-> 4 <-> 8 <-> 8 <-> 10 <-> 15 <-> 29\n")
        self.assertEqual(my_list.count(8), 2)
        self.assertEqual(my_list.count(5), 0)
        self.assertTrue(my_list.exists(15))
        self.assertFalse(my_list.exists(5))


if __name__ == "__main__":
    unittest.main()
