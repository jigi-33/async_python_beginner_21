# Практика по threading и multiprocessing - лабораторная работа N 1

from threading import Thread
from time import sleep
import requests


class RThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        """ Single thread logic """
        requests.get('https://api.covidtracking.com/v1/us/current.json')
        # print(f"{self.name} is running...\n")  # for debug purpose


def main():
    """ perform thread batch """
    N = 10
    for i in range(N):
        name = f"Thread #{i+1} of {N}"
        active_thrd = RThread(name)
        active_thrd.start()


if __name__ == "__main__":
    t = main()
    sleep(3)
    import timeit
    print(timeit.timeit("t", number=1, globals=globals()),
          )
