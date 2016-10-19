from brown.config import config
from brown.interface.impl.qt import app_interface_qt
from brown.core.brush import Brush
from brown.core.pen import Pen

# Fetch and initialize app interface
_app_interface_class = app_interface_qt.AppInterfaceQt
_app_interface = None
document = None

current_pen = Pen()
current_brush = Brush()

def setup(doctype='plane'):
    global _app_interface
    global current_pen
    global current_brush
    _app_interface = _app_interface_class()
    _app_interface.create_document(doctype)
    _app_interface.register_font(config.DEFAULT_MUSIC_FONT_PATH)
    _app_interface.set_pen(current_pen._interface)
    _app_interface.set_brush(current_brush._interface)

def show():
    _app_interface.show()

def set_draw_color(color):
    _app_interface.set_color(color)
