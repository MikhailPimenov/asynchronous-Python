import asyncio
from time import time
from collections import deque, namedtuple

generator_and_type = namedtuple('generator_and_type', ['generator', 'task_type'])


def print_numbers_generators_only():
    counter = 0
    delay = 0.5
    while True:
        print(counter)
        counter += 1
        yield time() + delay


def print_time_generators_only():
    t0 = time()
    delay = 2
    while True:
        print(f'Seconds passed: {int(time() - t0)}')
        yield time() + delay


def event_loop_generators_only():
    tasks = deque()

    tasks.append(
        generator_and_type(
            generator=print_numbers_generators_only(),
            task_type='numbers',
        )
    )
    tasks.append(
        generator_and_type(
            generator=print_time_generators_only(),
            task_type='time',
        )
    )

    type_and_time = {task.task_type: 0 for task in tasks}

    while tasks:
        task = tasks.popleft()
        if time() >= type_and_time[task.task_type]:
            time_when_to_execute = next(task.generator)
            type_and_time[task.task_type] = time_when_to_execute
        tasks.append(task)


@asyncio.coroutine
def print_number_asyncio_coroutine_decorator_and_yield_from():
    counter = 0
    delay = 0.5
    while True:
        print(counter)
        counter += 1
        yield from asyncio.sleep(delay)


@asyncio.coroutine
def print_time_asyncio_coroutine_decorator_and_yield_from():
    t0 = time()
    delay = 1
    while True:
        print(f'Seconds passed:{int(time() - t0)}')
        yield from asyncio.sleep(delay)


@asyncio.coroutine
def event_loop_asyncio_coroutine_decorator_and_yield_from():
    task1 = asyncio.ensure_future(print_number_asyncio_coroutine_decorator_and_yield_from())
    task2 = asyncio.ensure_future(print_time_asyncio_coroutine_decorator_and_yield_from())

    yield from asyncio.gather(task1, task2)


async def print_number_async_await():
    counter = 0
    delay = 0.2
    while True:
        print(counter)
        counter += 1
        await asyncio.sleep(delay)


async def print_time_async_await():
    t0 = time()
    delay = 3
    while True:
        print(f'Seconds passed:{int(time() - t0)}')
        await asyncio.sleep(delay)


async def loop():
    task1 = asyncio.create_task(print_number_async_await())
    task2 = asyncio.create_task(print_time_async_await())

    await asyncio.gather(task1, task2)


if __name__ == '__main__':
    event_loop_generators_only()

    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(event_loop_asyncio_coroutine_decorator_and_yield_from())
    #     loop.close()

    # asyncio.run(loop())
    pass
