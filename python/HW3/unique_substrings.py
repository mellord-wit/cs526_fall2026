"""
Unique substrings solution for HW3, split out of HW3.py.

distinctSubstring finds every distinct substring of a string with nested loops, and
unique_substrings does the same recursively, one suffix at a time.
"""


def distinctSubstring(str):
    # Put all distinct substring in a HashSet
    result = set()

    # List All Substrings
    for i in range(len(str) + 1):
        for j in range(i + 1, len(str) + 1):
            # Add each substring in Set
            result.add(str[i:j]);
        # Return size of the HashSet
    return result

def unique_substrings(string, result=None):
    """
    Recursively computes all unique substrings of a given string.

    Args:
        string (str): The input string.
        result (set, optional): A set to store unique substrings.

    Returns:
        set: A set of unique substrings.
    """

    if result is None:
        result = set()

    if not string:
        return result

    for i in range(len(string)):
        for j in range(i + 1, len(string) + 1):
            result.add(string[i:j])

    return unique_substrings(string[1:], result)

def unique_substrings_using_recursion(string, result=None):
    """
    Recursively finds and counts the unique substrings of a given string.

    Every substring is a prefix of some suffix of the string, so each call adds the
    prefixes of the current string and then recurses on the string minus its first
    character (the next suffix).

    Args:
        string (str): The input string.
        result (set, optional): A set to store the unique substrings found so far.

    Returns:
        tuple: (count, substrings), where count (int) is the number of unique
        substrings and substrings (set) holds the substrings themselves.
    """

    if result is None:
        result = set()

    if not string:
        return len(result), result

    for j in range(1, len(string) + 1):
        result.add(string[:j])

    return unique_substrings_using_recursion(string[1:], result)

if __name__ == "__main__":
    substrings = distinctSubstring("abcab")
    for i in substrings:
        print(i)

    string1 = "abcab"
    recursion_result, recursion_set = unique_substrings_using_recursion(string1, result=None)
    print(recursion_result)
    print("for string: ", string1)
    print("number of unique substrings using recursion: ", recursion_result)
    print("substrings using recursion were: ", recursion_set)

    string2 = "abcabadukab"
    recursion_result, recursion_set = unique_substrings_using_recursion(string2, result=None)
    print(recursion_result)
    print("for string: ", string2)
    print("number of unique substrings: ", recursion_result)
    print("substrings using recursion were: ", recursion_set)

    string3 = "xyzy"
    recursion_result, recursion_set = unique_substrings_using_recursion(string3, result=None)
    print(recursion_result)
    print("for string: ", string3)
    print("number of unique substrings: ", recursion_result)
    print("substrings using recursion were: ", recursion_set)
