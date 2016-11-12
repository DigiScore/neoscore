from brown.config import config
from brown.interface.app_interface import AppInterface
from brown.core.brush import Brush
from brown.core.pen import Pen
from brown.core.font import Font
from brown.core.paper import Paper
from brown.core.document import Document
from brown.utils import units


# Fetch and initialize app interface
_app_interface_class = AppInterface
_app_interface = None
music_font = None
text_font = None
document = None

# Color of background between and around pages
_display_background_color = '#dddddd'
# Background color of pages themselves.
_display_paper_color = '#ffffff'

current_pen = Pen()
current_brush = Brush()


def setup(initial_paper=None):
    global _app_interface
    global current_pen
    global current_brush
    global music_font
    global text_font
    global paper
    global document
    _app_interface = _app_interface_class()
    _app_interface.create_document()
    _app_interface.pen = current_pen._interface
    _app_interface.brush = current_brush._interface
    _app_interface.register_font(config.DEFAULT_MUSIC_FONT_PATH)
    music_font = Font(config.DEFAULT_MUSIC_FONT_NAME, 35)
    text_font = Font(config.DEFAULT_TEXT_FONT_NAME, 12, 1, False)
    document = Document(initial_paper)


def show():
    _app_interface.show()


def set_draw_color(color):
    _app_interface.set_color(color)
