from abc import ABC


class GrobInterface(ABC):
    def __init__(self, x, y):
        # Well defined function
        raise NotImplementedError

    def draw(self):
        # Well defined function
        raise NotImplementedError
