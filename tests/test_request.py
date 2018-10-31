import marisco


urls = [
    'https://python.org',
    'https://pypi.org',
    'https://github.com',
    'https://gitlab.com',
]

# with marisco.Session() as session:
#     for response in session.get(urls):
#         print(len(response))

for response in marisco.get(urls):
    print(len(response))
