#create a radix sort implementation in python
def counting_sort_for_radix(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1

    for i in range(n):
        arr[i] = output[i]
#expalin the radix sort algorithm
#Radix sort is a non-comparative integer sorting algorithm that sorts
# numbers by processing individual digits. It works by sorting the numbers
# based on each digit, starting from the least significant digit (LSD)
# to the most significant digit (MSD). It uses a stable sorting algorithm,
# such as counting sort, as a subroutine to sort the digits.
# The main idea is to group the numbers by each digit and sort them
# iteratively until all digits have been processed.

# Main function to implement radix sort
def radix_sort(arr):
    max1 = max(arr)

    exp = 1
    while max1 // exp > 0:
        counting_sort_for_radix(arr, exp)
        exp *= 10
# Example usage
if __name__ == "__main__":
    arr = [170, 45, 75, 90, 802, 24, 2, 66]
    print("Original array:", arr)
    radix_sort(arr)
    print("Sorted array:", arr)
