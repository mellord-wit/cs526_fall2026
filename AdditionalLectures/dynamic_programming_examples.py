# dynamic_programming_examples.py
# Companion code for the Dynamic Programming lecture.
#
# Run:  python3 dynamic_programming_examples.py
#
# Every example follows the same five-step recipe:
#   1. Define the subproblem (say in words what dp[i] / dp[i][j] means)
#   2. Write the recurrence
#   3. Set the base cases
#   4. Pick an evaluation order
#   5. Read the answer (and trace back the choices if needed)

import sys
from functools import lru_cache


# ----------------------------------------------------------------------
# Fibonacci: naive recursion vs. memoization vs. tabulation
# ----------------------------------------------------------------------

call_count = 0


def fib_naive(n):
    """Plain recursion: exponential time, about 1.6**n calls."""
    global call_count
    call_count += 1
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


def fib_memo(n, memo=None):
    """Top-down DP: recursion plus a cache.  O(n) time, O(n) space."""
    global call_count
    call_count += 1
    if memo is None:          # do NOT write memo={} as the default:
        memo = {}             # that single dict would be shared by every call
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


@lru_cache(maxsize=None)
def fib_lru(n):
    """Same as fib_memo, letting functools do the caching."""
    if n <= 1:
        return n
    return fib_lru(n - 1) + fib_lru(n - 2)


def fib_table(n):
    """Bottom-up DP: table[i] = fib(i), filled from small i to large i."""
    if n <= 1:
        return n
    table = [0] * (n + 1)
    table[1] = 1
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]
    return table[n]


def fib_two_vars(n):
    """Bottom-up with O(1) space: each value needs only the previous two."""
    prev, curr = 0, 1
    for _ in range(n):
        prev, curr = curr, prev + curr
    return prev


# ----------------------------------------------------------------------
# Example 1: coin change (fewest coins)
#   dp[a] = fewest coins that add up to exactly a
#   dp[a] = min over coins c <= a of dp[a - c] + 1,   dp[0] = 0
# ----------------------------------------------------------------------

def greedy_coins(coins, amount):
    """Take the largest coin that fits.  Fast, but not always optimal."""
    used = []
    for c in sorted(coins, reverse=True):
        while amount >= c:
            amount -= c
            used.append(c)
    return used if amount == 0 else None


def min_coins(coins, amount):
    INF = float("inf")
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return dp[amount] if dp[amount] != INF else -1


def min_coins_with_choice(coins, amount):
    """Also records the last coin used, so the actual coins can be listed."""
    INF = float("inf")
    dp = [0] + [INF] * amount
    last = [None] * (amount + 1)
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
                last[a] = c
    if dp[amount] == INF:
        return -1, [], dp, last
    used, a = [], amount
    while a > 0:
        used.append(last[a])
        a -= last[a]
    return dp[amount], used, dp, last


def count_ways(coins, amount):
    """Variation: number of combinations (order does not matter)."""
    ways = [1] + [0] * amount
    for c in coins:                       # coins outer: each combination once
        for a in range(c, amount + 1):
            ways[a] += ways[a - c]
    return ways[amount]


# ----------------------------------------------------------------------
# Example 2: 0/1 knapsack
#   K[i][c] = best value using only the first i items with capacity c
#   K[i][c] = max(K[i-1][c], K[i-1][c - w_i] + v_i  if w_i <= c)
# ----------------------------------------------------------------------

def knapsack_table(weights, values, cap):
    n = len(weights)
    K = [[0] * (cap + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, v = weights[i - 1], values[i - 1]
        for c in range(cap + 1):
            K[i][c] = K[i - 1][c]                 # skip item i
            if w <= c:                            # or take it
                take = K[i - 1][c - w] + v
                K[i][c] = max(K[i][c], take)
    return K


def knapsack(weights, values, cap):
    return knapsack_table(weights, values, cap)[len(weights)][cap]


def chosen_items(K, weights, cap):
    """Trace back: if a cell differs from the one above, that item was taken."""
    items, c = [], cap
    for i in range(len(weights), 0, -1):
        if K[i][c] != K[i - 1][c]:
            items.append(i - 1)
            c -= weights[i - 1]
    return items[::-1]


def knapsack_1d(weights, values, cap):
    """Value only, O(C) space.  Looping c downward keeps each item to one use."""
    best = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(cap, w - 1, -1):
            best[c] = max(best[c], best[c - w] + v)
    return best[cap]


def knapsack_brute(weights, values, cap):
    """Try all 2**n subsets.  Only for checking small cases."""
    n = len(weights)
    best = 0
    for mask in range(1 << n):
        w = sum(weights[i] for i in range(n) if mask >> i & 1)
        if w <= cap:
            best = max(best, sum(values[i] for i in range(n) if mask >> i & 1))
    return best


# ----------------------------------------------------------------------
# Example 3: longest common subsequence
#   L[i][j] = LCS length of x[:i] and y[:j]
#   match:     L[i-1][j-1] + 1
#   otherwise: max(L[i-1][j], L[i][j-1])
# ----------------------------------------------------------------------

def lcs_table(x, y):
    m, n = len(x), len(y)
    L = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
    return L


def lcs_length(x, y):
    return lcs_table(x, y)[len(x)][len(y)]


def lcs_string(x, y):
    """Trace back from the bottom-right corner to recover one LCS."""
    L = lcs_table(x, y)
    i, j = len(x), len(y)
    out = []
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            out.append(x[i - 1])
            i -= 1
            j -= 1
        elif L[i - 1][j] >= L[i][j - 1]:   # on a tie, move up
            i -= 1
        else:
            j -= 1
    return "".join(reversed(out))


def lcs_brute(x, y):
    """Plain recursion on the same recurrence (exponential).  For checking."""
    if not x or not y:
        return 0
    if x[-1] == y[-1]:
        return lcs_brute(x[:-1], y[:-1]) + 1
    return max(lcs_brute(x[:-1], y), lcs_brute(x, y[:-1]))


# ----------------------------------------------------------------------
# Practice problem solutions
# ----------------------------------------------------------------------

def unique_paths(rows, cols):
    """p[r][c] = number of right/down paths from (0, 0) to (r, c)."""
    p = [[1] * cols for _ in range(rows)]
    for r in range(1, rows):
        for c in range(1, cols):
            p[r][c] = p[r - 1][c] + p[r][c - 1]
    return p[rows - 1][cols - 1]


def edit_distance(a, b):
    """d[i][j] = fewest edits to turn a[:i] into b[:j]."""
    m, n = len(a), len(b)
    d = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        d[i][0] = i                    # delete everything
    for j in range(n + 1):
        d[0][j] = j                    # insert everything
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = 1 + min(d[i - 1][j],       # delete
                                  d[i][j - 1],       # insert
                                  d[i - 1][j - 1])   # substitute
    return d[m][n]


def longest_increasing_subsequence(nums):
    """dp[i] = length of the longest increasing subsequence ending at i."""
    if not nums:
        return 0
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


# ----------------------------------------------------------------------
# Demo
# ----------------------------------------------------------------------

def print_table(title, row_labels, col_labels, table):
    print(title)
    cells = col_labels + [v for row in table for v in row]
    width = max(len(str(v)) for v in cells) + 2
    print(" " * 12 + "".join(str(c).rjust(width) for c in col_labels))
    for label, row in zip(row_labels, table):
        print(str(label).ljust(12) + "".join(str(v).rjust(width) for v in row))
    print()


def main():
    global call_count

    print("=" * 60)
    print("Fibonacci")
    print("=" * 60)
    for n in (5, 20, 30):
        call_count = 0
        value = fib_naive(n)
        print(f"fib_naive({n}) = {value:,}   calls: {call_count:,}")
    print("fib_naive(40) would make 331,160,281 calls (2*F(41) - 1)")
    call_count = 0
    value = fib_memo(40)
    print(f"fib_memo(40)  = {value:,}   calls: {call_count}")
    print(f"fib_table(40) = {fib_table(40):,}")
    print(f"fib_two_vars(90) = {fib_two_vars(90):,}")
    print(f"fib_lru(90)      = {fib_lru(90):,}")
    try:
        fib_memo(5000)
    except RecursionError:
        print("fib_memo(5000) -> RecursionError (limit is "
              f"{sys.getrecursionlimit()}); fib_table(5000) has "
              f"{len(str(fib_table(5000)))} digits")
    print()

    print("=" * 60)
    print("Example 1: coin change, coins [1, 3, 4], amount 6")
    print("=" * 60)
    coins = [1, 3, 4]
    print("greedy:", greedy_coins(coins, 6))
    best, used, dp, last = min_coins_with_choice(coins, 6)
    print("DP:    ", used, f"({best} coins)")
    print("dp       :", ["-" if v == float("inf") else v for v in dp])
    print("last coin:", ["-" if v is None else v for v in last])
    print("min_coins([5, 10], 3) =", min_coins([5, 10], 3))
    print("count_ways([1, 3, 4], 6) =", count_ways(coins, 6))
    print()

    print("=" * 60)
    print("Example 2: 0/1 knapsack, capacity 7")
    print("=" * 60)
    names = ["A", "B", "C", "D"]
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    K = knapsack_table(weights, values, 7)
    rows = ["none"] + [f"+{nm} ({w}, {v})" for nm, w, v in zip(names, weights, values)]
    print_table("K[i][c]:", rows, list(range(8)), K)
    taken = chosen_items(K, weights, 7)
    print("best value:", K[4][7], " items:", [names[i] for i in taken])
    print("1-D version:", knapsack_1d(weights, values, 7))
    print()

    print("=" * 60)
    print("Example 3: LCS of BACDB and BDCB")
    print("=" * 60)
    x, y = "BACDB", "BDCB"
    print_table("L[i][j]:", ["-"] + list(x), ["-"] + list(y), lcs_table(x, y))
    print("length:", lcs_length(x, y), " one LCS:", lcs_string(x, y))
    print()

    print("=" * 60)
    print("Practice problems")
    print("=" * 60)
    print("unique_paths(3, 7) =", unique_paths(3, 7))
    print("edit_distance('kitten', 'sitting') =", edit_distance("kitten", "sitting"))
    print("LIS of [10, 9, 2, 5, 3, 7, 101, 18] =",
          longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]))
    print()

    # Self-test: compare each DP against brute force on small inputs.
    import itertools
    import random
    rng = random.Random(526)
    for n in range(20):
        assert fib_naive(n) == fib_memo(n) == fib_table(n) == fib_two_vars(n)
    for _ in range(200):
        ws = [rng.randint(1, 6) for _ in range(rng.randint(0, 6))]
        vs = [rng.randint(0, 9) for _ in ws]
        cap = rng.randint(0, 12)
        assert knapsack(ws, vs, cap) == knapsack_brute(ws, vs, cap) == knapsack_1d(ws, vs, cap)
    for a, b in itertools.product(["", "A", "AB", "BAC", "ABCB"], repeat=2):
        assert lcs_length(a, b) == lcs_brute(a, b) == len(lcs_string(a, b))
    print("Self-test passed: DP answers match brute force.")


if __name__ == "__main__":
    main()
