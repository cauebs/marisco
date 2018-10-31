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
