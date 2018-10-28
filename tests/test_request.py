import marisco


urls = [
    'https://python.org',
    'https://pypi.org',
    'https://github.com',
    'https://gitlab.com',
]

for response in marisco.get(urls):
    print(len(response))
