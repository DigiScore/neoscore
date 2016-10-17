from brown.interface.impl.qt import line_interface_qt


class Line:

    _interface_class = line_interface_qt.LineInterfaceQt

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self._interface = Line._interface_class(
            self.x1, self.y1, self.x2, self.y2)

    def draw(self, color=None, pattern=None):
        self._interface.draw(color, pattern)
