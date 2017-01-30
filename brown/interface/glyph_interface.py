from brown.interface.text_object_interface import TextObjectInterface
from brown.interface.qt_ext.q_offsetable_text_item import QOffsetableTextItem
from brown.interface.qt_to_util import point_to_qt_point_f


class GlyphInterface(TextObjectInterface):

    _interface_class = QOffsetableTextItem

    def __init__(self, pos, text, font, origin_offset=None):
        """
        Args:
            pos (Point[GraphicUnit] or tuple): The position of the path root
                relative to the document.
            text (str): The text for the object
            font (FontInterface): The font object for the text
            bounding_rect (Rect):
            origin_offset (Point):
        """
        q_origin_offset = (point_to_qt_point_f(origin_offset) if origin_offset
                           else None)
        self._qt_object = self._interface_class(
            '', origin_offset=q_origin_offset)
        self.text = text
        self.font = font
        self.pos = pos
