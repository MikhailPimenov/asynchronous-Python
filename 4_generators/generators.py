from collections import deque as my_deque


def get_one_element(s):
    for k in s:
        yield k


g2 = get_one_element('ARKADY')
g3 = get_one_element([0, 1, 2, 3, 4, 5, 6, 7])

tasks = my_deque()
tasks.append(g2)
tasks.append(g3)

while tasks:
    task = tasks.popleft()

    try:
        print(next(task))
        tasks.append(task)
    except StopIteration:
        print('Done!')




