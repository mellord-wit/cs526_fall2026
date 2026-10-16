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

'''
Worked example: shopping_resources/shopping_input5.txt
------------------------------------------------------
    python3 shopping.py < shopping_resources/shopping_input5.txt

Aisle positions are 0-based, as in the code:

    0 lunch      4 snacks     8 lunch      12 dinner
    1 dinner     5 lunch      9 breakfast
    2 lunch      6 snacks    10 dinner
    3 lunch      7 snacks    11 breakfast

Each heap entry is [priority, category], where the priority is the last
aisle the category was seen at. The heap list is shown root first, so the
first entry is always the category seen least recently: the one
extract_min would remove. "window" is left..right, the run of aisles
being collected.

right  category   action                        heap after                     window  len  best
-----  ---------  ----------------------------  -----------------------------  ------  ---  ----
  0    lunch      insert(lunch, 0)              [0 lunch]                      0..0     1    1
  1    dinner     insert(dinner, 1)             [0 lunch], [1 dinner]          0..1     2    2
  2    lunch      update(lunch, 2)              [1 dinner], [2 lunch]          0..2     3    3
  3    lunch      update(lunch, 3)              [1 dinner], [3 lunch]          0..3     4    4
  4    snacks     extract_min -> dinner, 1      [3 lunch], [4 snacks]          2..4     3    4
                  left = 2, insert(snacks, 4)
  5    lunch      update(lunch, 5)              [4 snacks], [5 lunch]          2..5     4    4
  6    snacks     update(snacks, 6)             [5 lunch], [6 snacks]          2..6     5    5
  7    snacks     update(snacks, 7)             [5 lunch], [7 snacks]          2..7     6    6
  8    lunch      update(lunch, 8)              [7 snacks], [8 lunch]          2..8     7    7
  9    breakfast  extract_min -> snacks, 7      [8 lunch], [9 breakfast]       8..9     2    7
                  left = 8, insert(breakfast, 9)
 10    dinner     extract_min -> lunch, 8       [9 breakfast], [10 dinner]     9..10    2    7
                  left = 9, insert(dinner, 10)
 11    breakfast  update(breakfast, 11)         [10 dinner], [11 breakfast]    9..11    3    7
 12    dinner     update(dinner, 12)            [11 breakfast], [12 dinner]    9..12    4    7

The steps worth a closer look:

Aisles 2 and 3 (update). lunch is already in a basket, so nothing is
emptied; its priority rises from 0 to 2, then 3. At aisle 2 this moves it
below dinner in the heap: _sift_down swaps it with its child, and dinner
(last seen at aisle 1) becomes the root.

Aisle 4 (the key step). snacks fits neither basket, which hold lunch and
dinner. The basket to empty is the root of the heap, dinner, last seen at
aisle 1. The new window starts right after it, at aisle 2: aisles 2..3 are
all lunch, which is still in a basket, so they stay in the run.

    Emptying the basket that was filled first would be wrong here. lunch
    was put in a basket first (aisle 0), but it was also seen most
    recently (aisle 3). Emptying lunch would move left to 4, keeping only
    snacks, and the run that becomes the answer (aisles 2..8) would be
    lost. This is why the queue is ordered by when a category was last
    seen, not by when its basket was filled.

Aisles 5 to 8 (update). Only lunch and snacks appear, so every step is an
update and the window grows to 2..8, 7 items. Whenever the category just
seen was the root, its update sifts it down and the other category becomes
the root (aisles 5, 6, and 8). At aisle 7 snacks was already below lunch,
so the heap order does not change.

Aisle 9 (extract_min). breakfast fits neither basket. snacks, last seen at
aisle 7, is the root and is emptied, so left = 8. Aisle 8 (lunch) stays in
the run, since lunch keeps its basket.

Aisle 10 (extract_min). dinner fits neither basket (lunch and breakfast).
lunch, last seen at aisle 8, is now the root and is emptied, so left = 9.

Aisles 11 and 12 (update). The window grows to 9..12, 4 items, which does
not beat 7.

Result. best_count = 7, set at aisle 8, with best_start = 2. Each update,
insert, and extract_min touched a heap of at most 2 entries, so every step
took constant time. The program prints:

    Aisles: ['lunch', 'dinner', 'lunch', 'lunch', 'snacks', 'lunch', 'snacks', 'snacks', 'lunch', 'breakfast', 'dinner', 'breakfast', 'dinner']
    Most items collected: 7
    Aisles shopped: ['lunch', 'lunch', 'snacks', 'lunch', 'snacks', 'snacks', 'lunch']
'''

'''
Second worked example: the same aisles with one more dinner at aisle 13
----------------------------------------------------------------------
    ['lunch', 'dinner', 'lunch', 'lunch', 'snacks', 'lunch', 'snacks',
     'snacks', 'lunch', 'breakfast', 'dinner', 'breakfast', 'dinner',
     'dinner']

First, what the heap holds
--------------------------
The heap does not hold items, and it does not count how many times a
category appears. It holds one entry per basket, so never more than 2:
    [last aisle this category was seen at, category]
Seeing the same category again does not add a second entry. It changes
the number in the entry that is already there. So whether there are 3 or
4 dinners makes no difference to the heap; what matters is only where the
last dinner was.

Entries come and go in exactly two ways:
    comes in:  insert       a new category gets a free basket
    goes out:  extract_min  a third category arrives and both baskets
                            are full, so the entry with the smallest
                            number (the category seen longest ago) is
                            removed and its basket is emptied
Every other step is an update: the entry stays, only its number changes,
and the two entries may swap places so that the smaller number is at
index 0, the root.

With 2 entries the heap is just a list of length 2:
    index 0 (root): the category seen longest ago, the next to go out
    index 1:        the category seen most recently

Step by step
------------
"before" and "after" are the heap list. "swap" means _sift_up or
_sift_down exchanged index 0 and index 1.

aisle  category   before                        what happens                        after                         window  len  best
-----  ---------  ----------------------------  ----------------------------------  ----------------------------  ------  ---  ----
  0    lunch      []                            lunch comes in (insert)             [0 lunch]                     0..0     1    1
  1    dinner     [0 lunch]                     dinner comes in (insert)            [0 lunch], [1 dinner]         0..1     2    2
  2    lunch      [0 lunch], [1 dinner]         lunch 0 -> 2, swap                  [1 dinner], [2 lunch]         0..2     3    3
  3    lunch      [1 dinner], [2 lunch]         lunch 2 -> 3, no swap               [1 dinner], [3 lunch]         0..3     4    4
  4    snacks     [1 dinner], [3 lunch]         dinner goes out (extract_min),      [3 lunch], [4 snacks]         2..4     3    4
                                                left = 1 + 1 = 2;
                                                snacks comes in (insert)
  5    lunch      [3 lunch], [4 snacks]         lunch 3 -> 5, swap                  [4 snacks], [5 lunch]         2..5     4    4
  6    snacks     [4 snacks], [5 lunch]         snacks 4 -> 6, swap                 [5 lunch], [6 snacks]         2..6     5    5
  7    snacks     [5 lunch], [6 snacks]         snacks 6 -> 7, no swap              [5 lunch], [7 snacks]         2..7     6    6
  8    lunch      [5 lunch], [7 snacks]         lunch 5 -> 8, swap                  [7 snacks], [8 lunch]         2..8     7    7
  9    breakfast  [7 snacks], [8 lunch]         snacks goes out (extract_min),      [8 lunch], [9 breakfast]      8..9     2    7
                                                left = 7 + 1 = 8;
                                                breakfast comes in (insert)
 10    dinner     [8 lunch], [9 breakfast]      lunch goes out (extract_min),       [9 breakfast], [10 dinner]    9..10    2    7
                                                left = 8 + 1 = 9;
                                                dinner comes in (insert)
 11    breakfast  [9 breakfast], [10 dinner]    breakfast 9 -> 11, swap             [10 dinner], [11 breakfast]   9..11    3    7
 12    dinner     [10 dinner], [11 breakfast]   dinner 10 -> 12, swap               [11 breakfast], [12 dinner]   9..12    4    7
 13    dinner     [11 breakfast], [12 dinner]   dinner 12 -> 13, no swap            [11 breakfast], [13 dinner]   9..13    5    7

Aisles 0 to 12 are exactly the same as in the first example. Adding an
aisle at the end cannot change anything that happened before it.

Aisle 13, the new dinner
------------------------
dinner already has a basket (it came in at aisle 10), so this is an
update, not an insert. Nothing comes in and nothing goes out:
    1. position["dinner"] says dinner's entry is at index 1.
    2. Its number changes from 12 to 13.
    3. The number went up, so update calls _sift_down(1). Index 1 has no
       children (they would be at 3 and 4), so nothing moves.
dinner was already at index 1, the "seen most recently" spot, because the
previous aisle was also dinner. A swap only happens when the category
just seen was at the root, index 0, since only then is the root's number
raised above the other entry's.

The window grows from 9..12 to 9..13, 5 items, all breakfast or dinner.
5 is not more than 7, so the answer stays 7 (aisles 2..8). The program
prints:
    Most items collected: 7
    Aisles shopped: ['lunch', 'lunch', 'snacks', 'lunch', 'snacks', 'snacks', 'lunch']

The life of each entry
----------------------
Reading the table by category instead of by aisle shows each entry
coming and going:
    lunch      comes in at aisle 0,  goes out at aisle 10
    dinner     comes in at aisle 1,  goes out at aisle 4
    snacks     comes in at aisle 4,  goes out at aisle 9
    breakfast  comes in at aisle 9,  still in a basket at the end
    dinner     comes in at aisle 10, still in a basket at the end
dinner comes in twice. When it went out at aisle 4 its entry was deleted
completely; the dinner at aisle 10 is a brand-new entry, inserted because
neither basket held dinner at that point. Each "goes out" happens on the
same aisle as some other category "comes in", because a basket is only
emptied to make room for the new category.

How many more dinners would change the answer?
----------------------------------------------
The breakfast/dinner run starts at aisle 9. More dinners each grow it by
one with a simple update, like aisle 13:
    dinners through aisle 13:  9..13 = 5 items, best stays 7
    dinners through aisle 15:  9..15 = 7 items, a tie; best stays at
                               aisles 2..8, because the code only
                               replaces best_count when the new run is
                               strictly longer (>)
    dinners through aisle 16:  9..16 = 8 items, the new answer:
        ['breakfast', 'dinner', 'breakfast', 'dinner', 'dinner',
         'dinner', 'dinner', 'dinner']
'''
