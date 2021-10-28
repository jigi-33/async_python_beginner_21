# Практика по threading и multiprocessing - лабораторная работа N 1

import multiprocessing as mp
from time import perf_counter
import requests


def requ(num=0, ttl=1):
    """ Single process logic """
    name = f" Process #{num+1} of {ttl}"
    res = requests.get('https://api.covidtracking.com/v1/us/current.json')
    print(name)  # for debug purpose
    # print(res.json())  # for raw debug purpose


def main():
    TTL = 10
    ctx = mp.get_context('fork')  # 'fork' start method is for unix/lnx only, 'spawn' is universal
    for num in range(TTL):
        p = ctx.Process(target=requ, args=(num, TTL)
                        )
        p.start()
        p.join()


if __name__ == '__main__':
    start = perf_counter()
    main()
    end = perf_counter() - start

    print(f"\n Completed.\n The script finished in {end:0.4f} seconds")
