import marisco


responses = marisco.get([
    'https://python.org',
    'https://pypi.org',
    'https://github.com',
    'https://gitlab.com',
])

for response in responses:
    print(len(response))

urls = (
    f'https://xkcd.com/{i}/'
    for i in range(1, 100)
)

with marisco.Session(max_connections_per_host=20) as session:
    for response in session.get(urls):
        print(len(response))
