from typing import Iterable
import time


def rolling_window(iterable: Iterable, length: int, stride: int = 1):
    offset = 0
    while offset < len(iterable):
        yield iterable[offset:offset+length]
        offset += stride


class Timer:
    def __init__(self):
        self.start = None
        self.end = None
        self.interval = None

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.interval = self.end - self.start

    def __str__(self):
        return str(self.interval)

    def __float__(self):
        return float(self.interval)

    def __int__(self):
        return int(self.interval)
