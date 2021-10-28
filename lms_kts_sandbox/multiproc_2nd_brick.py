import multiprocessing as mp
from time import sleep


def foo(q):
    print('The Queue will started soon...')
    sleep(3)
    q.put('Заложенный Привет')


if __name__ == '__main__':
    ctx = mp.get_context('fork')  # 'fork' start method is for unix/linux only, 'spawn' is universal
    # get_context() is to obtain a context object allow one to use multiple start() methods
    # in the same program
    q = ctx.Queue()  # creates multiprocessing queue first

    p = ctx.Process(target=foo, args=(q,))
    p.start()
    print('извлечено:', q.get())  # получить из q-e данные что были даны целевому процессу и вывожу
    p.join()  # !заканчивать всю тему нужно джойном: the join() method, when used with threading and
              # multiprocessing, it's not actually concatenating anything together as for strings.
              # Rather, it just means "Wait for this [thread/process] to complete!"
