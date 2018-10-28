# marisco

_Asynchronous requests for everyone._

`marisco` stands for Make Asynchronous Requests In Synchronous Code, but it's also portuguese for shellfish. If you come up with a nice metaphor let me know.


# Installation

```
pip install marisco
```

I personally recommend [Poetry](https://github.com/sdispater/poetry/) for dependency management and packaging:

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
    print(len(response.text))
```
