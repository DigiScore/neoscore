from brown.interface.impl.qt import grob_interface_qt


class Grob:

    _interface_class = grob_interface_qt.GrobInterfaceQt

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._interface = Grob._interface_class(x, y)

    def draw(self):
        self._interface.draw()
