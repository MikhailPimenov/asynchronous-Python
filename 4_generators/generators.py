from collections import deque


def generator_1(string: str):
    for symbol in string:
        yield symbol


def generator_2(number: int):
    for n in range(number):
        yield n


g1 = generator_1('ABCDEFGH')
g2 = generator_2(14)
tasks = deque()
tasks.append(g1)
tasks.append(g2)


def loop():
    while tasks:
        #  taking the first generator in the queue and removing it from queue:
        task = tasks.popleft()

        try:
            #  getting what can yield (compute) this generator:
            element = next(task)

            #  printing what was yielded - this is payload:
            print(element)

            #  adding this generator back in the queue but on the last place:
            tasks.append(task)

        except StopIteration:
            pass


if __name__ == '__main__':
    loop()
