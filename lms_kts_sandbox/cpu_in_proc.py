# Практика по threading и multiprocessing - лабораторная работа N 1

import multiprocessing as mp
from time import perf_counter, time


def countdown():
    i = 0
    begin = time()
    while i < 5_000_000:
        i += 1
    print(f"current duration: {time() - begin}")


def in_proc(num=0, ttl=1):
    """ Single process logic """
    print(f" Starting process #{num+1} of {ttl}...")  # for debug purpose
    countdown()


def main():
    ttl = 10
    ctx = mp.get_context('fork')  # 'fork' start method is for unix/lnx only, 'spawn' is universal
    for num in range(ttl):
        p = ctx.Process(target=in_proc, args=(num, ttl)
                        )
        p.start()
        p.join()


if __name__ == '__main__':
    start = perf_counter()
    main()
    end = perf_counter() - start

    print(f"\n Batch completed.\n Total duration: {end:0.4f} seconds")
