import random
import time

import utils


def merge(left, right):
    ''' Сама сортировка '''
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result


def merge_sort(arr, threads=1):
    ''' Деление массива на подсписки и возложение ответственности на потоки'''
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], threads=threads)
    right = merge_sort(arr[mid:], threads=threads)
    if threads == 1:
        return merge(left, right)

    threads_left = threads // 2
    threads_right = threads - threads_left
    left_thread = utils.MyThread(target=merge_sort, args=(left, threads_left))
    right_thread = utils.MyThread(target=merge_sort, args=(right, threads_right))
    left_thread.start()
    right_thread.start()

    left = left_thread.join()
    right = right_thread.join()

    return merge(left, right)


MAX_NUMS = 100
MAX_NUM_VALUE = 500


def main():
    arr = list()
    for _ in range(MAX_NUMS):
        arr.append(random.randint(0, MAX_NUM_VALUE))
    print(f"Arr before sorting: {arr}")
    start = time.time()
    arr_sorted = merge_sort(arr, threads=4)
    end = time.time()
    print(f"Arr after sorting: {arr_sorted}")

    print(f"Sort time: {end-start:.5f} s")


if __name__ == '__main__':
    main()
