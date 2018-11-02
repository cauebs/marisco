import asyncio
import aiohttp

from dataclasses import dataclass
from queue import Queue
from threading import Thread
from typing import Optional, TypeVar


StopWorker = TypeVar('StopWorker')


@dataclass
class Session:
    max_connections: Optional[int] = None
    max_connections_per_host: Optional[int] = None

    def __post_init__(self):
        self._input_queue = Queue()
        self._output_queue = Queue()

        self._worker_thread = Thread(target=self._worker)
        self._worker_thread.start()

    def _worker(self):
        asyncio.run(self._worker_coro())

    async def _worker_coro(self):
        connector_kwargs = {}

        if self.max_connections is not None:
            connector_kwargs['limit'] = self.max_connections

        if self.max_connections_per_host is not None:
            connector_kwargs['limit_per_host'] = self.max_connections_per_host

        connector = aiohttp.TCPConnector(**connector_kwargs)
        session = aiohttp.ClientSession(connector=connector)

        async with session:
            while True:
                message = self._input_queue.get()

                if message is StopWorker:
                    return

                method, urls, kwargs = message

                tasks = [
                    asyncio.create_task(session.request(method, url, **kwargs))
                    for url in urls
                ]

                for task in tasks:
                    response = await task
                    # print(response)
                    self._output_queue.put(await response.text())

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._input_queue.put(StopWorker)
        self._worker_thread.join()

    def request(self, method, urls, **kwargs):
        urls = list(urls)

        self._input_queue.put((method, urls, kwargs))

        for _ in urls:
            yield self._output_queue.get()

    def get(self, urls, **kwargs):
        yield from self.request('get', urls, **kwargs)
