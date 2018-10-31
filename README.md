# marisco (WIP)

_This is a work in progress: any feedback is much appreciated._

## Asynchronous requests for everyone.

- You want to **make a bunch of requests** (fetching pages, downloading files...)
- You don't want to **do it sequentially** because it would take too long
- You don't really want to spawn an **absurd amount of threads**
- You don't want to use a thread pool and **limit the number of concurrent connections**
- You don't really want to **learn async** right now _(and that's ok!)_

Maybe **marisco** is the right library for you. Just give it a
list of URLs and it will fetch them concurrently using `asyncio` and `aiohttp`
internally, saving you the headache.

If you want more control, I highly encourage you to take the time to [learn
async](https://docs.python.org/3/library/asyncio.html) and directly use the
brilliant `aiohttp` library.


# Installation

```
pip install marisco
```

I personally recommend [Poetry](https://github.com/sdispater/poetry/)
for dependency management and packaging:

```
poetry add marisco
```


# Usage

```python
import marisco

urls = [
    'https://python.org',
    'https://pypi.org',
    'https://github.com',
    'https://gitlab.com',
]

responses = marisco.get(urls)

for response in responses:
    print(len(response))
```


# Why is it called that?

`marisco` stands for Make Asynchronous Requests In Synchronous Code, amazingly
enough. It's also portuguese for shellfish.

If you come up with some nice metaphor, let me know.
