# CS526 Homework 2

## Introduction

This homework is about linked lists and recursion. It has four problems:

| Problem | Topic | Files |
|---|---|---|
| 1 | The advantage of a tail pointer in a linked list | answered [below](#problem-1-answer) |
| 2 | A singly linked list with CRUD methods, and a driver that runs directives from a file | `problem2.py`, `problem2_driver.py` |
| 3 | Counting (and listing) the ways to climb a staircase 1, 2, or 3 steps at a time | `problem3.py`, `problem3_driver.py` |
| 4 | A doubly linked list that always stays sorted, walked with recursion | `problem4.py`, `problem4_driver.py` |

Each driver reads one directive per line, such as `append 12` or `median`, calls the method of the same
name, and prints the result. The drivers for Problems 2 and 4 then print the final list. A bad line prints a
warning to standard error and the driver moves on to the next line.

### Problem 1 answer

A tail pointer keeps a reference to the last node, so adding to the end of the list (`append`) takes O(1) time
instead of O(n). Without one, every append has to walk the whole list from the head to find the last node.
The cost is that every method that can change the last node (`append`, `prepend` on an empty list, `delete`,
`delete_at`) must also keep the tail pointer up to date. In a singly linked list, a tail pointer does not make
deleting the last node faster, because you still have to walk to the node before it.

## Algorithm

### Problem 2: Singly linked list (`problem2.py`)

`SinglyLinkedList` keeps `head`, `tail`, and `length`. Each `Node` holds a `value` and `next`.

- **Create:** `append` links the new node after `tail`, `prepend` makes it the new `head`, and `insert` walks
  to the node before the index and links the new node after it. Inserting at index 0 or at the end reuses
  `prepend` and `append`.
- **Read:** `get` walks to the node at an index. `find` walks from the head and returns the position of the
  first match, or -1.
- **Update:** `update` walks to the node at an index and replaces its value.
- **Delete:** `delete` and `delete_at` both find the node and the one before it, then call `_unlink`, which
  moves `head`, `tail`, and the previous node's `next` around the removed node.

Methods that take an index check it first and raise an `IndexError` if it is out of range.

### Problem 3: Climbing stairs (`problem3.py`)

The first move is 1, 2, or 3 steps. After it, what is left is a smaller staircase, so

```
ways(n) = ways(n-1) + ways(n-2) + ways(n-3)
```

with base cases `ways(0) = 1` (one way to climb nothing), `ways(1) = 1`, and `ways(2) = 2`. Three base cases
are needed because the recursion reaches back to `n-3`.

- `ways_1_or_2(n)` allows only 1 or 2 steps per move: `ways_1_or_2(n-1) + ways_1_or_2(n-2)`. This produces
  the Fibonacci sequence 1, 1, 2, 3, 5, 8, 13, ...
- `print_ways(n, climb="")` prints every climb as well as counting them. It passes the moves taken so far
  down the recursion in `climb`. When `n` reaches exactly 0, `climb` is one complete climb, so it prints it
  (e.g. `1+1+2`) and returns 1. When a move overshoots the top (`n < 0`), it returns 0.

The answers to the Problem 3 questions are in the comments at the end of `problem3.py`.

### Problem 4: Sorted doubly linked list (`problem4.py`)

`SortedDoublyLinkedList` keeps `head`, `tail`, and `length`. Each `Node` holds a `value`, `prev`, and `next`.
The list is always sorted, so the user never chooses where a value goes.

Every walk through the list is a recursive helper that handles one node and then calls itself on `node.next`:

| Helper | Used by | What it does |
|---|---|---|
| `_first_greater` | `add` | finds the first node larger than the new value |
| `_find` | `delete`, `exists` | finds the first node holding a value |
| `_count` | `count` | counts the nodes holding a value |
| `_total` | `total` | adds up every value |
| `_node_at` | `sum_middle_three`, `median` | walks to a position |
| `_to_string` | `print_list` | builds `2 <-> 4 <-> 8` |

- **add:** inserts the new node just before the first larger value. That is a new head, a new tail, or a
  spot in the middle, and each case relinks `prev` and `next` on both sides.
- **sum_middle_three:** with `mid = n // 2`, adds the nodes at `mid-1, mid, mid+1` when `n` is odd, or at
  `mid-2, mid-1, mid` when `n` is even. It raises a `ValueError` for fewer than 3 nodes.
- **median:** the middle value when `n` is odd, or the average of the two middle values when `n` is even. It
  raises a `ValueError` for an empty list.

## Interesting aspects

- **Stopping early in a sorted list.** `_find` and `_count` stop as soon as they reach a value larger than
  the one they are looking for, because nothing after it can match.
- **Duplicates keep their order.** `add` inserts before the first *larger* value rather than the first equal
  one, so equal values stay in the order they were added.
- **Recursion depth.** The Problem 4 helpers recurse once per node, so a list of about 1000 nodes or more hits
  Python's recursion limit. The problem asks for recursion, so this is a deliberate trade-off.
- **Exponential time in Problem 3.** `ways` and `print_ways` recompute the same smaller staircases many
  times, so the number of calls grows exponentially. `ways(30)` already takes a noticeable time, and
  `print_ways(20)` prints 121,415 climbs.
- **Drivers that keep going.** An unknown directive, a missing or extra argument, a value that is not a
  number, an index out of range, or a statistic on a list that is too short each print a `line N: ...`
  warning, and the driver carries on with the next line.
- **Directives map straight to methods.** Each driver has a table of directives and the arguments they
  expect, and it calls the method with the same name using `getattr`. Adding a directive only needs a new
  table entry.
- **Driver input can come from a file or standard input.** Each driver has a `READ_FROM_FILE` toggle. When it
  is `True`, the driver reads `INPUT_FILE`, relative to the script's own folder, so it runs the same from an
  IDE. When it is `False`, it reads standard input.

## How to run

Run every command from the `HW2` folder with Python 3.

### Run the programs on their own

```
python3 problem2.py
python3 problem3.py
python3 problem4.py
```

### Run a driver on an input file

The Problem 2 and Problem 4 drivers have `READ_FROM_FILE = False`, so they read standard input:

```
python3 problem2_driver.py < problem2Resources/problem2_basic.txt
python3 problem4_driver.py < problem4Resources/problem4_example.txt
```

The Problem 3 driver has `READ_FROM_FILE = True`, so it reads `problem3Resources/problem3_input1.txt`:

```
python3 problem3_driver.py
```

To have it read standard input instead, set `READ_FROM_FILE = False` in `problem3_driver.py` and run
`python3 problem3_driver.py < problem3Resources/problem3_input1.txt`.

To run a driver on every input file for its problem:

```
for f in problem2Resources/*.txt; do echo "===== $f"; python3 problem2_driver.py < "$f"; done
for f in problem4Resources/*.txt; do echo "===== $f"; python3 problem4_driver.py < "$f"; done
```

### Run the unit tests

```
python3 -m unittest discover problem2Tests -v
python3 -m unittest discover problem3Tests -v
python3 -m unittest discover problem4Tests -v
```

## Test files and example executions

| Problem | Driver input files | Unit tests | Example executions |
|---|---|---|---|
| 2 | `problem2Resources/` (basic, create, read, update, delete, errors) | `problem2Tests/test_problem2.py` with `problem_test1.txt`–`problem_test12.txt` | `problem2Executions.txt` |
| 3 | `problem3Resources/problem3_input1.txt` | `problem3Tests/test_problem3.py` | `problem3Excutions.txt` |
| 4 | `problem4Resources/` (basic, simple, example, positions, duplicates, statistics, numbers, errors, mixed) | `problem4Tests/test_problem4.py` and `test_problem4_driver.py` with `problem_test1.txt`–`problem_test17.txt` | `problem4Executions.txt` |

`problem2Executions.txt` and `problem4Executions.txt` show each command that was run, followed by
everything it printed. `problem3Excutions.txt` is the output of `python3 problem3.py`.
