import asyncio
import aiohttp

from queue import Queue
from threading import Thread
from typing import List


def request(urls: List[str], *args, **kwargs):
    q: Queue = Queue(maxsize=len(urls))
    coro = request_coro(urls, args, kwargs, q)
    Thread(target=lambda: asyncio.run(coro)).start()

    for _ in urls:
        yield q.get()


async def request_coro(urls: List[str], args, kwargs, queue: Queue):
    # in_order = kwargs.pop('in_order', True)

    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(session.request(*args, url=url, ** kwargs))
            for url in urls
        ]

        for task in tasks:
            response = await task
            queue.put(await response.text())


def get(urls: List[str], *args, **kwargs):
    yield from request(urls, *args, method='get', **kwargs)
