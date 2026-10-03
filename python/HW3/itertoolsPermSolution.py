from itertools import permutations


def get_all_string_permutations(input_string):
    """
    Computes all possible permutations of a given string.

    Args:
      input_string: The string for which to compute permutations.

    Returns:
      A list of all unique permutations as strings.
    """
    # Generate all permutations as tuples of characters
    perms_tuples = permutations(input_string)

    # Convert each tuple back into a string and store in a list
    all_permutations = ["".join(p) for p in perms_tuples]

    return all_permutations


# Example usage:
my_string = "abcab"
result = get_all_string_permutations(my_string)
print("number of permutations: ", len(result))
print(f"Permutations of '{my_string}': {result}")

'''
my_string_with_duplicates = "aab"
result_duplicates = get_all_string_permutations(my_string_with_duplicates)
print(f"Permutations of '{my_string_with_duplicates}': {result_duplicates}")
'''