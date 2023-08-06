import requests


class FreeOpenAI:
    def __init__(self) -> None:
        self.url = "https://freeopenai.xyz/api.txt"
        self.keys = None

    def __iter__(self):
        if self.keys is None:
            self.refresh()

        if self.keys:
            yield from self.keys

    def refresh(self):
        resp = requests.get(self.url)
        self.keys = map(str.strip, resp.content.decode().strip().split())


def keys():
    api = FreeOpenAI()
    yield from api
