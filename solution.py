"""
Project 2 - Hybrid Sorting
CSE 331 Fall 2025
"""

from datetime import date
from typing import Callable, List, Literal, TypeVar


T = TypeVar("T")  # represents generic type


# This is an optional helper function but HIGHLY recommended, especially for the application problem!
def do_comparison(first: T, second: T, comparator: Callable[[T, T], bool], descending: bool) -> bool:
    """
     Compares two elements according to the comparator and sorting order.

    :param first: The first element being compared.
    :param second: The second element being compared.
    :param comparator: Function that returns True if the first element should come before second element.
    :param descending: If True, the comparison is reversed.
    :return: True if first element should come before second element objectively for the comparator and order.
    """
    if descending:
        return comparator(second,first)
    else:
        return comparator(first, second)


def selection_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                   descending: bool = False) -> None:
    """
    Sorts a list in-place using selection sort.

    :param data: List of elements to sort.
    :param comparator: Function to compare elements.
    :param descending: If True, sorts the list in descending order.
    """
    for i in range(len(data) - 1):
        index_smallest = i
        for j in range(i+1, len(data)):
            if do_comparison(data[j], data[index_smallest], comparator, descending):
                index_smallest = j
        data[i], data[index_smallest] = data[index_smallest], data[i]


def bubble_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                descending: bool = False) -> None:
    """
    Sorts a list in-place using bubble sort.

    :param data: List of elements to sort.
    :param comparator: Function to compare elements.
    :param descending: If True, sorts the list in descending order.
    """

    while True:
        performed_swap = False
        for i in range(len(data) - 1):
            if do_comparison(data[i + 1], data[i], comparator, descending):
                data[i], data[i + 1] = data[i + 1], data[i]
                performed_swap = True
        if not performed_swap:
            break


def insertion_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                   descending: bool = False) -> None:
    """
    Sorts a list in-place using insertion sort.

    :param data: List of elements to sort.
    :param comparator: Function used to compare elements.
    :param descending: If True, sorts the list in descending order.
    """
    for i in range(1, len(data)):
        target = data[i]
        j = i - 1
        while j >= 0 and do_comparison(target, data[j], comparator, descending):
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = target


def hybrid_merge_sort(data: List[T], *, threshold: int = 12,
                      comparator: Callable[[T, T], bool] = lambda x, y: x < y, descending: bool = False) -> None:
    """
    Sort a list in-place using hybrid merge sort algorithm that swaps
    between insertion sort for small sublists.

    :param data: List of elements to sort.
    :param threshold: Max sublist size to use insertion sort instead of merge sort.
    :param comparator: Function to compare elements.
    :param descending: If True, sorts the list in descending order.

    """
    if len(data) <= max(1,threshold):
        insertion_sort(data, comparator=comparator, descending=descending)
    else:
        middle = len(data) // 2
        left = data[:middle]
        right = data[middle:]

        hybrid_merge_sort(left, threshold=threshold, comparator=comparator, descending=descending)
        hybrid_merge_sort(right, threshold=threshold, comparator=comparator, descending=descending)

        left_index = right_index = index = 0

        while left_index < len(left) and right_index < len(right):
            if do_comparison(left[left_index], right[right_index], comparator, descending) or left[left_index] == right[right_index]:
                data[index] = left[left_index]
                left_index += 1
            else:
                data[index] = right[right_index]
                right_index += 1
            index += 1

        if left_index < len(left):
            data[index:] = left[left_index:]
        if right_index < len(right):
            data[index:] = right[right_index:]

def quicksort(data: List[T]) -> None:
    """
    Sorts a list in place using quicksort
    :param data: Data to sort
    """

    def quicksort_inner(first: int, last: int) -> None:
        """
        Sorts portion of list at indices in interval [first, last] using quicksort

        :param first: first index of portion of data to sort
        :param last: last index of portion of data to sort
        """
        # List must already be sorted in this case
        if first >= last:
            return

        left = first
        right = last

        # Need to start by getting median of 3 to use for pivot
        # We can do this by sorting the first, middle, and last elements
        midpoint = (right - left) // 2 + left
        if data[left] > data[right]:
            data[left], data[right] = data[right], data[left]
        if data[left] > data[midpoint]:
            data[left], data[midpoint] = data[midpoint], data[left]
        if data[midpoint] > data[right]:
            data[midpoint], data[right] = data[right], data[midpoint]
        # data[midpoint] now contains the median of first, last, and middle elements
        pivot = data[midpoint]
        # First and last elements are already on right side of pivot since they are sorted
        left += 1
        right -= 1

        # Move pointers until they cross
        while left <= right:
            # Move left and right pointers until they cross or reach values which could be swapped
            # Anything < pivot must move to left side, anything > pivot must move to right side
            #
            # Not allowing one pointer to stop moving when it reached the pivot (data[left/right] == pivot)
            # could cause one pointer to move all the way to one side in the pathological case of the pivot being
            # the min or max element, leading to infinitely calling the inner function on the same indices without
            # ever swapping
            while left <= right and data[left] < pivot:
                left += 1
            while left <= right and data[right] > pivot:
                right -= 1

            # Swap, but only if pointers haven't crossed
            if left <= right:
                data[left], data[right] = data[right], data[left]
                left += 1
                right -= 1

        quicksort_inner(first, left - 1)
        quicksort_inner(left, last)

    # Perform sort in the inner function
    quicksort_inner(0, len(data) - 1)


###########################################################
# DO NOT MODIFY
###########################################################
class Song:
    """
    Class that represents songs.
    """
    __slots__ = ['rock', 'pop', 'rap', 'jazz', 'date_published']

    def __init__(self, rock: float, pop: float, rap: float, jazz: float, date_published: date) -> None:
        """
        Constructor for the Song class.

        :param rock: value to assign as rock relevance.
        :param pop: value to assign as pop relevance.
        :param rap: value to assign as rap relevance.
        :param jazz: value to assign as jazz relevance.
        :param date_published: value to assign as date published.
        :return: None
        """
        self.rock = rock
        self.pop = pop
        self.rap = rap
        self.jazz = jazz
        self.date_published = date_published

    def __repr__(self) -> str:
        """
        Represent the song as a string.

        :return: Representation of the song.
        """
        return str(self)

    def __str__(self) -> str:
        """
        Convert the Song to a string.

        :return: String representation of the Song.
        """
        return f'<date_published: {self.date_published.month}/{self.date_published.day}/{self.date_published.year}, rock: {self.rock}, pop: {self.pop}, rap: {self.rap}, jazz: {self.jazz}>'

    def __eq__(self, other) -> bool:
        """
        Compare two Song objects for equality.

        :param other: The other Song to compare with.
        :return: True if songs are equal, False otherwise.
        """
        return self.date_published == other.date_published and self.rock == other.rock and self.pop == other.pop and\
            self.rap == other.rap and self.jazz == other.jazz



def get_relevant_songs(songs: List[Song], genres_user: List[Literal['rock', 'pop', 'rap', 'jazz']], order_by: Literal['newest', 'oldest'] ) -> List[Song]:
    """
    Returns a list of songs sorted by user-preferred genres and date published.

    Sorts the list according to the genres provided in priority order,
    then sorts by date published either newest to oldest or oldest to newest.

    :param songs: List of Songs to sort.
    :param genres_user: List of genres to prioritize when sorting.
    :param order_by: 'newest' or 'oldest' to sort by date published.
    :return: Sorted list of Song objects.
    """
    if not songs:
        return []


    for genre in genres_user:
        hybrid_merge_sort(songs,threshold=len(songs) + 1,
        comparator=lambda x, y, g=genre: getattr(x, g) < getattr(y, g),descending=True)

    topSongs = songs[:10]

    dateCompare = lambda x, y: x.date_published < y.date_published
    descending = (order_by == "newest")

    hybrid_merge_sort(
        topSongs,threshold=len(topSongs) + 1,comparator=dateCompare,
        descending=descending)

    return topSongs
