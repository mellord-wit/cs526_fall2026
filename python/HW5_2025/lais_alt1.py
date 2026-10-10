# hw5 lais_alt1.py

import sys

'''
Alternative O((n + m) log(n + m)) solution to Problem 3, the longest
alternating increasing sequence (LAIS) taken from two lists A and B.

The rule being solved
---------------------
X must be strictly increasing, and its elements have to alternate between
the two lists: A, B, A, B, ... or B, A, B, A, ... There is one more rule,
which comes from the example in the assignment and is the rule lais1.py
uses: each element of X has to come from a later position than the element
before it, counting positions the same way in both lists. If x_k is at
position i (in either list), x_(k+1) has to be at a position greater than i
in the other list.

The example in the assignment shows why that rule is needed:
    A = {1, 7, 2}, B = {4, 8, 3, 9}, answer X = {4, 7, 9}, length 3
        4 is B[0], 7 is A[1], 9 is B[3]: positions 0 < 1 < 3.
If the positions in A and B were independent, 1, 4, 7, 8 (A[0], B[0], A[1],
B[1]) would be a longer answer, but A[0] and B[0] are both at position 0,
so 4 cannot follow 1.

What is stored
--------------
For every position, store the length of the best X that starts there:
    start_a[i] = length of the longest X whose first element is A[i]
    start_b[j] = length of the longest X whose first element is B[j]
The answer is the largest value in either list (at least 1 if A or B has
any elements, because one element on its own is a valid X).

The recurrence
--------------
An X that starts at A[i] is either just A[i] (length 1), or A[i] followed
by the best X that starts at some B[j] with j > i and B[j] > A[i]. So
    start_a[i] = 1 + max(start_b[j] for j > i where B[j] > A[i])
    start_b[j] = 1 + max(start_a[i] for i > j where A[i] > B[j])
where the max of nothing counts as 0.

lais1.py evaluates this recurrence top-down with recursion and memoization.
For each element it scans every later element of the other list, so it is
O(n * m) overall. This version evaluates the same recurrence bottom-up and
replaces that scan with a fast lookup.

Order of evaluation
-------------------
start_a[i] only depends on start_b values at positions greater than i, and
start_b[j] only on start_a values at positions greater than j. So the
positions are processed from the last one down to 0. At position p:
    1. compute start_a[p] using the B results already stored (all at
       positions > p),
    2. compute start_b[p] using the A results already stored (all at
       positions > p),
    3. only then store start_a[p] and start_b[p].
Both values have to be computed before either is stored, because A[p] and
B[p] are at the same position and so cannot follow one another.

The fast lookup: a max Fenwick tree keyed by value
--------------------------------------------------
Step 1 asks: "of the B elements stored so far, which have value > A[p], and
what is the largest start_b among them?" Scanning every stored element
would bring back the O(n * m) cost, so the stored results are kept in a
Fenwick tree (binary indexed tree) that answers "largest stored length
among values greater than x" in O(log U), where U is the number of distinct
values. There is one tree for A results and one for B results.

  - Compressing values: the values can be large or spread out, so every
    distinct value in A and B is replaced by its rank in sorted order. Only
    the order of the values matters for "greater than", so ranks work just
    as well.

  - Reversing the ranks: a Fenwick tree answers prefix questions ("the max
    over slots 1..k"). Larger values are given smaller slots
    (slot = U - rank), so "all values greater than x" becomes "all slots
    before x's slot", which is a prefix.

  - Each slot of the tree holds the max over a block of slots whose size is
    a power of two, set by the lowest set bit of the slot number
    (slot & -slot). A prefix query walks down by removing that bit; an
    update walks up by adding it. Each walk visits at most about log2(U)
    slots.

  - Lengths only ever get stored, never removed, and a query needs the
    largest one, so a max tree with "keep the larger value" updates is
    enough.

Worked example (longest_seq1.txt)
---------------------------------
    A = 8 2 9 1 4
    B = 4 1 5 3 2 6
    position:   0  1  2  3  4  5
    A:          8  2  9  1  4  -
    B:          4  1  5  3  2  6

Processing from the last position down. "B stored" and "A stored" list the
(value: length) results at positions greater than the current one.

  p = 5: B[5] = 6. No A results are stored yet, so start_b[5] = 1.
         (There is no A[5].)
  p = 4: A[4] = 4. B stored: 6:1. 6 > 4, so start_a[4] = 1 + 1 = 2.
         B[4] = 2. A stored: none (A[4] is not stored until after this
         step), so start_b[4] = 1.
  p = 3: A[3] = 1. B stored: 6:1, 2:1. Both > 1, best 1, start_a[3] = 2.
         B[3] = 3. A stored: 4:2. 4 > 3, so start_b[3] = 1 + 2 = 3.
  p = 2: A[2] = 9. B stored: 6:1, 2:1, 3:3. None > 9, start_a[2] = 1.
         B[2] = 5. A stored: 4:2, 1:2. None > 5, start_b[2] = 1.
  p = 1: A[1] = 2. B stored: 6:1, 2:1, 3:3, 5:1. Values > 2 are 6, 3, 5,
         best is 3:3, so start_a[1] = 1 + 3 = 4.
         B[1] = 1. A stored: 4:2, 1:2, 9:1. Values > 1 are 4, 9, best is
         4:2, so start_b[1] = 1 + 2 = 3.
  p = 0: A[0] = 8. B stored values > 8: none, start_a[0] = 1.
         B[0] = 4. A stored: 4:2, 1:2, 9:1, 2:4. Values > 4 is 9, so
         start_b[0] = 1 + 1 = 2.

    start_a = [1, 4, 1, 2, 2]
    start_b = [2, 3, 1, 3, 1, 1]
The largest value is start_a[1] = 4. Following the choices back gives
X = 2 (A[1]), 3 (B[3]), 4 (A[4]), 6 (B[5]): increasing, alternating, and at
positions 1 < 3 < 4 < 5. Longest Sequence: 4.

Running time
------------
Sorting the values for compression is O((n + m) log(n + m)). Each of the
max(n, m) positions does at most two queries and two updates at O(log U)
each. Total O((n + m) log(n + m)) time and O(n + m) space. There is also no
recursion, so the length of X cannot hit Python's recursion limit.

How to run
----------
    python3 lais_alt1.py < longest_seq1.txt
        prints "Longest Sequence: 4", the same as lais1.py
    python3 lais_alt1.py longest_seq1.txt longest_seq2.txt ...
        prints "File Input: <file>" and "Longest Sequence: <n>" for each file
'''


def max_tree_update(tree, slot, length):
    # Make every tree slot that covers this slot hold at least length.
    while slot < len(tree):
        if length > tree[slot]:
            tree[slot] = length
        slot += slot & -slot


def max_tree_query(tree, slot):
    # Largest length stored in slots 1..slot (0 if none).
    best = 0
    while slot > 0:
        if tree[slot] > best:
            best = tree[slot]
        slot -= slot & -slot
    return best


def compute_longest_sequence(list_a, list_b):
    # Replace each value with a slot where larger values get smaller slots,
    # so "values greater than x" is the prefix of slots before x's slot.
    sorted_values = sorted(set(list_a) | set(list_b))
    value_count = len(sorted_values)
    slot_of = {}
    for rank in range(value_count):
        slot_of[sorted_values[rank]] = value_count - rank

    a_tree = [0] * (value_count + 1)
    b_tree = [0] * (value_count + 1)
    overall_longest = 0

    for position in range(max(len(list_a), len(list_b)) - 1, -1, -1):
        start_a = 0
        start_b = 0
        if position < len(list_a):
            start_a = 1 + max_tree_query(b_tree, slot_of[list_a[position]] - 1)
        if position < len(list_b):
            start_b = 1 + max_tree_query(a_tree, slot_of[list_b[position]] - 1)

        # Store only after both are computed: A[position] and B[position]
        # cannot follow each other.
        if start_a > 0:
            max_tree_update(a_tree, slot_of[list_a[position]], start_a)
        if start_b > 0:
            max_tree_update(b_tree, slot_of[list_b[position]], start_b)

        overall_longest = max(overall_longest, start_a, start_b)

    return overall_longest


def read_lists(lines):
    # Line 3 is the A values and line 4 is the B values.
    list_a_ints = [int(a) for a in lines[2].split()]
    list_b_ints = [int(b) for b in lines[3].split()]
    return list_a_ints, list_b_ints


def main():
    if len(sys.argv) > 1:
        for file_name in sys.argv[1:]:
            with open(file_name, "r") as input_file:
                list_a_ints, list_b_ints = read_lists(input_file.readlines())
            print("File Input:", file_name)
            print("Longest Sequence:", compute_longest_sequence(list_a_ints, list_b_ints))
            print()
    else:
        list_a_ints, list_b_ints = read_lists(sys.stdin.readlines())
        print("Longest Sequence:", compute_longest_sequence(list_a_ints, list_b_ints))


if __name__ == "__main__":
    main()
