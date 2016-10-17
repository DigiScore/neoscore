from brown.interface.impl.qt import app_interface_qt
from brown.core import line

# Fetch and initialize app interface
_app_interface_class = app_interface_qt.AppInterfaceQt
_app_interface = None
document = None

def setup(doctype='plane'):
    global _app_interface
    _app_interface = _app_interface_class()
    _app_interface.create_document(doctype)

def draw_line(x1, y1, x2, y2):
    # Create a line, draw it, and return the brown Line object
    new_line = line.Line(x1, y1, x2, y2)
    new_line.draw()
    return new_line

def draw_circle(x, y, radius):
    _app_interface.draw_circle(x, y, radius)

def show():
    _app_interface.show()

def set_pen(color, style):
    _app_interface.set_pen(color, style)

def set_color(color):
    _app_interface.set_color(color)
