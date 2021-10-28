# Практика по threading и multiprocessing - лабораторная работа N 1

from threading import Thread
from time import sleep, time


class RThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        """ Single thread logic """
        print(f"{self.name} is running...\n")  # for debug purpose
        self.countdown()

    def countdown(self):
        i = 0
        begin = time()
        while i < 5_000_000:
            i += 1
        print(f"{self.name} duration: {time() - begin}"
              )


def main():
    """ perform thread batch """
    for i in range(10):
        name = f"Thread #{i+1}"
        active_thrd = RThread(name)
        active_thrd.start()


if __name__ == "__main__":
    tar = main()
    sleep(3)
    import timeit
    print("\nTotal duration:", timeit.timeit("tar", number=1, globals=globals(),
                                             )
          )
