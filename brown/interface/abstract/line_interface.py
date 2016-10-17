from abc import ABC


class LineInterface(ABC):

    def __init__(self, x1, y1, x2, y2):
        # Well defined function, not implemented
        raise NotImplementedError

    def draw(self, color=None, pattern=None):
        # Well defined function, not implemented
        raise NotImplementedError
