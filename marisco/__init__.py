from .session import Session


def get(urls, **kwargs):
    with Session() as session:
        yield from session.get(urls, **kwargs)
