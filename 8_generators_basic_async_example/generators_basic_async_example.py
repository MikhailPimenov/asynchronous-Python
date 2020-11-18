from collections import deque as my_deque
from time import sleep as my_sleep, time as my_time

tasks = my_deque()


def print_counter():
    counter = 0
    while True:
        print(counter)
        counter += 1
        yield


def count():
    counter = 0
    while True:
        if counter % 3 == 0:
            print('time =', int(my_time()) % 100)
        counter += 1
        yield


def run_event_loop():
    while True:
        task = tasks.popleft()
        next(task)
        tasks.append(task)
        my_sleep(1)


if __name__ == '__main__':
    tasks.append(print_counter())
    tasks.append(count())
    run_event_loop()
