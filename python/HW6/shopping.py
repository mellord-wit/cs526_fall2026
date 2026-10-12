# hw6 shopping.py

import sys

'''
Solution to Problem 1, collecting the most items from the store aisles with
2 baskets, using a priority queue.

The problem
-----------
The aisles are a list of categories, visited from left to right. Starting
at any aisle, one item is taken from every aisle in a row and placed in a
basket. Each basket holds only one category, so once an aisle's category
fits in neither basket, shopping stops. The items collected are therefore a
run of consecutive aisles that contains at most 2 different categories, and
the goal is the longest such run.

For example:
    ['dinner', 'lunch', 'dinner', 'snacks', 'snacks', 'dinner']
The best start is aisle 2 ('dinner'): dinner, snacks, snacks, dinner is 4
items using the baskets 'dinner' and 'snacks'.

Algorithm: a sliding window
---------------------------
Walk through the aisles once, keeping a window [left, right] that is the
longest valid run ending at the current aisle, right.
    - If the category at right is already in a basket, the window just
      grows by one.
    - If there is a free basket, the category goes into it and the window
      grows by one.
    - Otherwise one basket has to be emptied. The basket to empty is the
      one whose category was seen least recently: its last aisle is the
      earliest, so emptying it gives up the fewest aisles. The window then
      starts right after that category's last aisle, because every aisle
      from there to right holds one of the categories still in a basket.
After each aisle, the window length right - left + 1 is a candidate answer.

Where the priority queue comes in
---------------------------------
The step "find the category seen least recently" is exactly what a min
priority queue answers. The queue holds one entry per basket:
    item     = the category in the basket
    priority = the index of the last aisle where that category was seen
    - Seeing a category that is already in a basket raises its priority
      to the current aisle (update).
    - Putting a category into a free basket adds an entry (insert).
    - Emptying a basket removes the entry with the smallest priority
      (extract_min), whose priority is the aisle just before the new left.

The priority queue is a binary min-heap stored in a list, plus a dictionary
from each item to its index in the list. The dictionary is what makes
update possible: it finds the item's entry in O(1), and then the entry is
sifted up or down to restore the heap order.

With only 2 baskets the queue never holds more than 2 entries, but the code
works unchanged for any number of baskets (BASKETS below).

Cost
----
Each aisle does at most one update, insert, or extract_min, each
O(log k) for k baskets. With n aisles the total time is O(n log k), which
is O(n) for k = 2, and the extra space is O(k).
'''

BASKETS = 2


class PriorityQueue:
    '''Min priority queue of items, each with a priority that can change.'''

    def __init__(self):
        self.heap = []          # list of [priority, item], a binary min-heap
        self.position = {}      # item -> index of its entry in self.heap

    def __len__(self):
        return len(self.heap)

    def __contains__(self, item):
        return item in self.position

    def insert(self, item, priority):
        self.heap.append([priority, item])
        self.position[item] = len(self.heap) - 1
        self._sift_up(len(self.heap) - 1)

    def update(self, item, priority):
        index = self.position[item]
        old_priority = self.heap[index][0]
        self.heap[index][0] = priority
        if priority < old_priority:
            self._sift_up(index)
        else:
            self._sift_down(index)

    def extract_min(self):
        priority, item = self.heap[0]
        last = self.heap.pop()
        del self.position[item]
        if self.heap:
            self.heap[0] = last
            self.position[last[1]] = 0
            self._sift_down(0)
        return item, priority

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.position[self.heap[i][1]] = i
        self.position[self.heap[j][1]] = j

    def _sift_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[index][0] >= self.heap[parent][0]:
                break
            self._swap(index, parent)
            index = parent

    def _sift_down(self, index):
        size = len(self.heap)
        while True:
            smallest = index
            for child in (2 * index + 1, 2 * index + 2):
                if child < size and self.heap[child][0] < self.heap[smallest][0]:
                    smallest = child
            if smallest == index:
                break
            self._swap(index, smallest)
            index = smallest


def most_items(aisles, baskets):
    '''Return (count, start) for the longest run of aisles that fits.'''
    last_seen = PriorityQueue()
    left = 0
    best_count = 0
    best_start = 0

    for right in range(len(aisles)):
        category = aisles[right]

        if category in last_seen:
            last_seen.update(category, right)
        else:
            if len(last_seen) == baskets:
                emptied, emptied_last_aisle = last_seen.extract_min()
                left = emptied_last_aisle + 1
            last_seen.insert(category, right)

        if right - left + 1 > best_count:
            best_count = right - left + 1
            best_start = left

    return best_count, best_start


def parse_aisles(text):
    # accepts ['dinner', 'lunch'] (straight or curly quotes) or dinner lunch
    for ch in "[],'\"‘’“”":
        text = text.replace(ch, " ")
    return text.split()


def main():
    aisles = parse_aisles(sys.stdin.read())

    count, start = most_items(aisles, BASKETS)

    print("Aisles:", aisles)
    print("Most items collected:", count)
    if count > 0:
        print("Aisles shopped:", aisles[start:start + count])

main()
