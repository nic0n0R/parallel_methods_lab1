import utils


def calculate_pi(n: int, start_index: int, end_index: int):
    ''' Расчитывает число П по формуле ряда: 4*(1 - 1/3 + 1/5 - 1/7 + 1/9 + ...)'''
    res = 0
    for k in range(start_index, end_index):
        res += (-1)**k / (2*k+1)
    return 4*res


@utils.Timing
def main():
    n = 1000000
    threads = []
    thread_nums = 4
    for i in range(thread_nums):
        start_index = n // thread_nums * i
        end_index = start_index + n // thread_nums

        # Если есть остаток
        if n % thread_nums != 0:
            if i == thread_nums-1:
                end_index += n % thread_nums

        threads.append(utils.MyThread(target=calculate_pi, args=(n, start_index, end_index)))

    for t in threads:
        t.start()
    pi = 0.0
    for t in threads:
        num = t.join()
        pi += num

    print(f'{pi=}')



if __name__ == '__main__':
    main()
