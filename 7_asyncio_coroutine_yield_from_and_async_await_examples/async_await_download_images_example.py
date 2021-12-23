import asyncio
from collections import deque
from time import time

import aiohttp
import requests


def get_file_synchronous(url: str):
    response = requests.get(url=url, allow_redirects=True)
    return response


def write_file_synchronous(response: requests.Response):
    filename = f'file-{response.url.split("/")[-1]}.jpeg'
    with open(filename, 'wb') as file:
        file.write(response.content)


def main_synchronous(number_of_files: int, url: str):
    for i in range(number_of_files):
        write_file_synchronous(response=get_file_synchronous(url=url))


def write_file_async_but_still_synchronous(filenumber: int, data: bytes):
    filename = f'file-{int(time() * 1000)}-{filenumber}.jpeg'
    with open(filename, 'wb') as file:
        file.write(data)


async def get_file_async(url: str, filenumber: int, session: aiohttp.ClientSession):
    async with session.get(url=url, allow_redirects=True) as response:
        data = await response.read()
        write_file_async_but_still_synchronous(filenumber=filenumber, data=data)


async def main_async(url: str, number_of_files: int):
    tasks = deque()

    async with aiohttp.ClientSession() as session:
        for i in range(number_of_files):
            task = asyncio.create_task(get_file_async(url=url, filenumber=i, session=session))
            tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    url = 'https://loremflickr.com/320/240'

    t0 = time()
    main_synchronous(number_of_files=50, url=url)
    print('synchronous:', time() - t0)

    t0 = time()
    asyncio.run(main_async(number_of_files=50, url=url))
    print('asynchronous:', time() - t0)
