import asyncio
import aiohttp

from queue import Queue
from threading import Thread


class StopWorker:
    pass


async def session_worker(args, kwargs, input_queue, output_queue):
    async with aiohttp.ClientSession(*args, **kwargs) as session:
        while True:
            message = input_queue.get()

            if message is StopWorker:
                input_queue.task_done()
                return

            urls, args, kwargs = message

            tasks = [
                asyncio.create_task(session.request(*args, url=url, **kwargs))
                for url in urls
            ]

            for task in tasks:
                response = await task
                output_queue.put(await response.text())

            input_queue.task_done()


class Session:
    def __init__(self, *args, **kwargs):
        self._input_queue = Queue()
        self._output_queue = Queue()

        worker_coro = session_worker(
            args,
            kwargs,
            self._input_queue,
            self._output_queue,
        )

        self._worker_thread = Thread(target=lambda: asyncio.run(worker_coro))
        self._worker_thread.start()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._input_queue.put(StopWorker)
        self._input_queue.join()
        self._worker_thread.join()

    def request(self, urls, *args, **kwargs):
        self._input_queue.put((urls, args, kwargs))

        for _ in urls:
            yield self._output_queue.get()

    def get(self, urls, *args, **kwargs):
        yield from self.request(urls, *args, method='get', **kwargs)


def get(urls, *args, **kwargs):
    with Session() as session:
        yield from session.get(urls, *args, **kwargs)
