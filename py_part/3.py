import threading

from utils import Timing


@Timing
def qsort(arr, left, right):
    i = left
    j = right
    pivot = arr[(i + j) // 2]
    while i <= j:
        while pivot > arr[i]:
            i += 1
        while pivot < arr[j]:
            j -= 1
        if i <= j:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1

    lthread = None
    rthread = None
    if left < j:
        lthread = threading.Thread(target=lambda: qsort(arr, left, j))
        lthread.start()
    if i < right:
        rthread = threading.Thread(target=lambda: qsort(arr, i, right))
        rthread.start()

    if lthread is not None: lthread.join()
    if rthread is not None: rthread.join()
    return arr


def main():
    arr1 = [10, 5, 2, 7, 8, 3, 1, 4, 6]
    qsort(arr1, 0, len(arr1) - 1)
    print(arr1)


if __name__ == '__main__':
    main()
