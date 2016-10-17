from abc import ABC


class FontInterface(ABC):
    def __init__(self, family_name, size, weight=1, italic=False):
        # Well defined function
        raise NotImplementedError
