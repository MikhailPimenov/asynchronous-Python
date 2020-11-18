from time import time as my_time

import requests as my_requests


def get_file(url):
    response = my_requests.get(url, allow_redirects=True)
    return response


def write_file(response):
    filename = response.url.split('/')[-1]

    with open(filename, 'wb') as file:
        file.write(response.content)


def main():
    url = 'https://loremflickr.com/320/240'

    t0 = my_time()

    for k in range(10):
        write_file(get_file(url))

    print('time =', my_time() - t0)

#
# if __name__ == '__main__':
#     main()

# # =============================================================
from collections import deque as my_deque
import aiohttp as my_aiohttp
import asyncio as my_asyncio


def write_file2(data):
    filename = 'file_{}.jpg'.format(int(my_time() * 1000))
    with open(filename, 'wb') as file:
        file.write(data)


async def get_file2(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        write_file2(data)


async def main2():
    url = 'https://loremflickr.com/320/240'
    tasks = my_deque()

    async with my_aiohttp.ClientSession() as session:
        for k in range(10):
            task = my_asyncio.create_task(get_file2(url, session))
            tasks.append(task)
        await my_asyncio.gather(*tasks)


if __name__ == '__main__':
    t0 = my_time()
    my_asyncio.run(main2())
    print(my_time() - t0)
