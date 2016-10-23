from brown.config import config
from brown.interface.impl.qt import app_interface_qt
from brown.core.brush import Brush
from brown.core.pen import Pen
from brown.core.font import Font

# Fetch and initialize app interface
_app_interface_class = app_interface_qt.AppInterfaceQt
_app_interface = None
document = None
music_font = None
text_font = None

current_pen = Pen()
current_brush = Brush()

def setup(doctype='plane'):
    global _app_interface
    global current_pen
    global current_brush
    global document
    global music_font
    global text_font
    _app_interface = _app_interface_class()
    _app_interface.create_document(doctype)
    _app_interface.set_pen(current_pen._interface)
    _app_interface.set_brush(current_brush._interface)
    _app_interface.register_font(config.DEFAULT_MUSIC_FONT_PATH)
    music_font = Font(config.DEFAULT_MUSIC_FONT_NAME, 35)
    text_font = Font(config.DEFAULT_TEXT_FONT_NAME, 12, 1, False)

def show():
    _app_interface.show()

def set_draw_color(color):
    _app_interface.set_color(color)
