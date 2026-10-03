#create an insertion sort implementation in python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


#explain the insertion sort algorithm
#Insertion sort is a simple sorting algorithm that builds the final
# sorted array one item at a time
# It is much less efficient on large lists than more advanced algorithms
# such as quicksort, heapsort, or merge sort

# Example usage
if __name__ == "__main__":
    arr = [12, 11, 13, 5, 6]
    print("Original array:", arr)
    insertion_sort(arr)
    print("Sorted array:", arr)
