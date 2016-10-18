from abc import ABC


class TextObjectInterface(ABC):
    def __init__(self, x, y, text, font):
        raise NotImplementedError

    @property
    def x(self):
        raise NotImplementedError

    @x.setter
    def x(self, value):
        raise NotImplementedError

    @property
    def y(self):
        raise NotImplementedError

    @y.setter
    def y(self, value):
        raise NotImplementedError

    @property
    def text(self):
        raise NotImplementedError

    @text.setter
    def text(self, value):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError
