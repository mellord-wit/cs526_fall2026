# hw5 lais1.py


import sys

'''
Solution to Problem 3, the longest alternating increasing sequence (LAIS)
taken from two lists A and B, using recursion with memoization.

The rule being solved
---------------------
X must be strictly increasing, and its elements have to alternate between
the two lists: A, B, A, B, ... or B, A, B, A, ... Each element of X also
has to come from a later position than the element before it, counting
positions the same way in both lists. If x_k is at position i (in either
list), x_(k+1) has to be at a position greater than i in the other list.

Algorithm
---------
compute_longest_sequence(list_a, list_b, start_offset, starting_list, ...)
returns the length of the longest X whose first element is
starting_list[start_offset]. Call that value L_A[i] when X starts at A[i]
and L_B[j] when X starts at B[j].

An X that starts at A[i] is either just A[i] on its own (length 1), or A[i]
followed by an X that starts at some B[j] that is allowed to come next,
meaning j > i and B[j] > A[i]. To make the whole X as long as possible,
pick the B[j] whose own X is longest:
    L_A[i] = 1 + max(L_B[j] for j > i where B[j] > A[i])
    L_B[j] = 1 + max(L_A[i] for i > j where A[i] > B[j])
where the max of nothing counts as 0. In the function, the for loop over
the other list is the "for j > i", the if test is "B[j] > A[i]",
longest_sequence holds the running max, and "return longest_sequence + 1"
adds A[i] itself.

The recursion always stops: each call moves to a strictly greater position,
so a call at or near the end of the lists finds nothing to scan and returns
1.

main() calls the function for every position in A and every position in B,
because the best X can start anywhere, and prints the largest result.

Memoization
-----------
Why it is needed: the same subproblem is reached by many different paths.
For example, L_B[5] is needed by every A[i] with i < 5 and A[i] < B[5],
and each of those L_A[i] values is in turn needed by many earlier B
elements. Plain recursion would recompute L_B[5] once for every path that
reaches it, and the number of paths grows exponentially with the length of
the lists.

Why it is allowed: L_A[i] depends only on i (the lists themselves never
change). It does not matter which elements came before A[i] in X, because
the only rules for what comes next are "later position" and "larger
value", and both are checked against A[i] alone. So once L_A[i] has been
computed, the answer is the same every time it is asked for again and can
simply be looked up.

The memo tables:
    longest_lengths_of_a[i] holds L_A[i]
    longest_lengths_of_b[j] holds L_B[j]
Both start filled with -1, which means "not computed yet". -1 is safe as a
marker because every real answer is at least 1.

How the tables are used (the same pattern appears in all four places that
need an L value: the two branches of compute_longest_sequence and the two
loops in main):
    1. Look up the entry.
    2. If it is -1, call compute_longest_sequence to work it out, then
       store the result in the table.
    3. Otherwise, use the stored value and make no recursive call.
The tables are created once in main and passed into every call. Python
lists are passed by reference, so a value stored deep inside the recursion
is visible to every other call and to main.

Note that the lookup happens before the call, not at the start of the
function. The function itself never checks the table for its own entry; the
caller does. That is why main also checks the table: by the time main
reaches a position, an earlier recursive call may already have filled it.

Worked example (the one from the assignment)
--------------------------------------------
    A = {1, 7, 2}, B = {4, 8, 3, 9}
Positions are 0-based in the code. Both tables start as all -1.

main, a_offset 0: L_A[0], A[0] = 1. Scan B at positions 1..3:
    B[1] = 8 > 1, table has -1 -> recurse: L_B[1], B[1] = 8, scan A at
        position 2: A[2] = 2 is not > 8, so L_B[1] = 1. Store it.
    B[2] = 3 > 1, table has -1 -> recurse: L_B[2], no A after position 2,
        so L_B[2] = 1. Store it.
    B[3] = 9 > 1, table has -1 -> recurse: L_B[3] = 1. Store it.
    L_A[0] = 1 + 1 = 2. Store it.
main, a_offset 1: L_A[1], A[1] = 7. Scan B at positions 2..3:
    B[2] = 3 is not > 7.
    B[3] = 9 > 7, table has 1 -> memo hit, no recursion.
    L_A[1] = 1 + 1 = 2. Store it.
main, a_offset 2: L_A[2], A[2] = 2. Scan B at position 3:
    B[3] = 9 > 2, table has 1 -> memo hit.
    L_A[2] = 2. Store it.
main, b_offset 0: L_B[0], B[0] = 4. Scan A at positions 1..2:
    A[1] = 7 > 4, table has 2 -> memo hit.
    A[2] = 2 is not > 4.
    L_B[0] = 1 + 2 = 3. Store it.
main, b_offsets 1, 2, 3: all already in the table -> memo hits.

Final tables:
    longest_lengths_of_a = [2, 2, 2]
    longest_lengths_of_b = [3, 1, 1, 1]
The answer is the largest entry, 3, which is X = {4, 7, 9}: B[0], then
A[1], then B[3].

Cost
----
Every table entry is computed by exactly one call to
compute_longest_sequence; every later request for it is an O(1) lookup.
The call for A[i] scans at most m elements of B, and the call for B[j]
scans at most n elements of A. With n = len(A) and m = len(B), the total
time is O(n * m) and the extra space is O(n + m) for the two tables.

The recursion depth is also small. Each call in a chain of nested calls
starts at an element that is allowed to follow the element of the call
above it, so the chain itself is a valid X. The depth can never be more
than the length of the answer.
'''


def compute_longest_sequence(list_a, list_b, start_offset, starting_list, longest_lengths_of_a, longest_lengths_of_b):
    longest_sequence = 0

    if starting_list == "A":
        test_value = list_a[start_offset]
        for b_offset in range(start_offset+1, len(list_b)):
            if list_b[b_offset] > test_value:
                if longest_lengths_of_b[b_offset] == -1:
                    longest_length = compute_longest_sequence(list_a, list_b, b_offset, "B", longest_lengths_of_a, longest_lengths_of_b)
                    longest_lengths_of_b[b_offset] = longest_length
                else:
                    longest_length = longest_lengths_of_b[b_offset]

                if longest_length > longest_sequence:
                    longest_sequence = longest_length

    else:
        test_value = list_b[start_offset]
        for a_offset in range(start_offset+1, len(list_a)):
            if list_a[a_offset] > test_value:
                if longest_lengths_of_a[a_offset] == -1:
                    longest_length = compute_longest_sequence(list_a, list_b, a_offset, "A", longest_lengths_of_a, longest_lengths_of_b)
                    longest_lengths_of_a[a_offset] = longest_length
                else:
                    longest_length = longest_lengths_of_a[a_offset]

                if longest_length > longest_sequence:
                    longest_sequence = longest_length

    return longest_sequence + 1


def main():

    # read input data and put into a list
    i = 0
    for line in sys.stdin:
        if i == 2:
            list_a_string = line.split()
        if i == 3:
            list_b_string = line.split()
            break
        i+=1

    list_a_ints = []
    for a in list_a_string:
        list_a_ints.append(int(a))

    list_b_ints = []
    for b in list_b_string:
        list_b_ints.append(int(b))

    '''print("list a:", list_a_ints)
    print("list b:", list_b_ints)'''

    longest_lengths_of_a = [-1] * len(list_a_ints)
    longest_lengths_of_b = [-1] * len(list_b_ints)
    overall_longest = -1

    for a_offset in range(len(list_a_ints)):
        if longest_lengths_of_a[a_offset] == -1:
            longest_length = compute_longest_sequence(list_a_ints, list_b_ints, a_offset, "A", longest_lengths_of_a, longest_lengths_of_b)
            longest_lengths_of_a[a_offset] = longest_length
        else:
            longest_length = longest_lengths_of_a[a_offset]

        if longest_length > overall_longest:
            overall_longest = longest_length


    for b_offset in range(len(list_b_ints)):
        if longest_lengths_of_b[b_offset] == -1:
            longest_length = compute_longest_sequence(list_a_ints, list_b_ints, b_offset, "B", longest_lengths_of_a, longest_lengths_of_b)
            longest_lengths_of_b[b_offset] = longest_length
        else:
            longest_length = longest_lengths_of_b[b_offset]

        if longest_length > overall_longest:
            overall_longest = longest_length


    print("Longest Sequence:", overall_longest)

main()
