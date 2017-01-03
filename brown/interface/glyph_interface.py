from brown.interface.text_object_interface import TextObjectInterface
from brown.interface.qt_ext.q_glyph import QGlyph
from brown.interface.qt_to_util import point_to_qt_point_f, rect_to_qt_rect_f


class GlyphInterface(TextObjectInterface):

    _interface_class = QGlyph

    def __init__(self, pos, text, font,
                 bounding_rect=None, origin_offset=None, parent=None):
        """
        Args:
            pos (Point[GraphicUnit] or tuple): The position of the path root
                relative to the document.
            text (str): The text for the object
            font (FontInterface): The font object for the text
            bounding_rect (Rect):
            origin_offset (Point):
            parent: The parent interface object
        """
        q_bounding_rect = (rect_to_qt_rect_f(bounding_rect) if bounding_rect
                           else None)
        q_origin_offset = (point_to_qt_point_f(origin_offset) if origin_offset
                           else None)
        self._qt_object = self._interface_class(
            '', bounding_rect=q_bounding_rect, origin_offset=q_origin_offset)
        self.text = text
        self.font = font
        self.pos = pos
        self.parent = parent
