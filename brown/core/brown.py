from brown.interface.impl.qt import app_interface_qt

# Fetch and initialize app interface
_app_interface_class = app_interface_qt.AppInterfaceQt
_app_interface = None
document = None

def setup(doctype='plane'):
    global _app_interface
    _app_interface = _app_interface_class()
    _app_interface.create_document(doctype)

def show():
    _app_interface.show()

def set_pen(color, style):
    _app_interface.set_pen(color, style)

def set_color(color):
    _app_interface.set_color(color)
