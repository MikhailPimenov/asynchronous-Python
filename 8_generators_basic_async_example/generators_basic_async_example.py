from collections import deque, namedtuple
from time import time, sleep


def print_numbers_1():
    counter = 0
    while True:
        counter += 1
        print(counter)
        yield


def print_time_1():
    t0 = time()
    counter = 0
    while True:
        if counter % 3 == 0:
            print('Seconds passed:', int(time() - t0))
        counter += 1
        yield


def main_1():
    tasks = deque()
    tasks.append(print_numbers_1())
    tasks.append(print_time_1())

    while True:
        task = tasks.popleft()
        next(task)
        sleep(1)
        tasks.append(task)


def print_numbers_2():
    counter = 0
    delay = 0.25
    while True:
        print(counter)
        counter += 1
        yield time() + delay


def print_time_2():
    t0 = time()
    delay = 1
    while True:
        print('Seconds passed:', int(time() - t0))
        yield time() + delay


generator_and_type = namedtuple('generator_and_type', ['generator_as_task', 'task_type'])


def main_2():
    tasks = deque()
    tasks.append(generator_and_type(print_numbers_2(), 'number'))
    tasks.append(generator_and_type(print_time_2(), 'time'))
    task_type_and_time = {task.task_type: 0 for task in tasks}

    while True:
        task = tasks.popleft()

        if time() > task_type_and_time[task.task_type]:
            time_to_execute_next_time = next(task.generator_as_task)
            task_type_and_time[task.task_type] = time_to_execute_next_time

        tasks.append(task)


if __name__ == '__main__':
    # main_1()
    main_2()
