from brown.core import brown
from brown.core.graphic_object import GraphicObject
from brown.interface.text_interface import TextInterface
from brown.utils.point import Point
from brown.utils.units import GraphicUnit


class Text(GraphicObject):

    """A graphical text object."""

    def __init__(self, pos, text, font=None, parent=None, scale_factor=1):
        """
        Args:
            pos (Point or init tuple): The position of the path root
                relative to the document.
            text (str): The text to be displayed
            font (Font): The font for the object.
            parent (GraphicObject): The parent (core-level) object or None
            scale_factor (float): A hard scaling factor.
        """
        if font:
            self._font = font
        else:
            self._font = brown.default_font
        self._text = text
        self._scale_factor = scale_factor
        super().__init__(pos, parent=parent)

    ######## PUBLIC PROPERTIES ########

    @property
    def text(self):
        """str: The text to be drawn"""
        return self._text

    @property
    def font(self):
        """Font: The text font"""
        return self._font

    @font.setter
    def font(self, value):
        self._font = value

    @property
    def baseline_y(self):
        """Unit: The y coordinate of the first text line's baseline."""
        return self.y + self.font.ascent

    @property
    def scale_factor(self):
        """float: A hard scale factor to be applied to the rendered text"""
        return self._scale_factor

    @scale_factor.setter
    def scale_factor(self, value):
        self._scale_factor = value

    ######## PRIVATE PROPERTIES ########

    @property
    def bounding_rect(self):
        """The bounding rect override for this text."""
        return self.font.bounding_rect_of(self.text)

    @property
    def _origin_offset(self):
        """Point: The origin offset override for this glyph."""
        return Point(GraphicUnit(0),
                     GraphicUnit(self.font.ascent))

    ######## PRIVATE METHODS ########

    def _render_slice(self, pos, clip_start_x=None, clip_width=None):
        """Render a horizontal slice of a text object.

        Args:
            pos (Point): The doc-space position of the slice beginning
                (at the top-left corner of the slice)
            clip_start_x (Unit): The starting local x position in of the slice
            clip_width (Unit): The horizontal length of the slice to
                be rendered

        Returns: None
        """
        slice_interface = TextInterface(
            self,
            pos,
            self.text,
            self.font._interface,
            self.brush._interface,
            origin_offset=self._origin_offset,
            scale_factor=self.scale_factor,
            clip_start_x=clip_start_x,
            clip_width=clip_width)
        slice_interface.render()
        self.interfaces.add(slice_interface)

    def _render_complete(self, pos, dist_to_line_start=None, local_start_x=None):
        self._render_slice(pos, None, None)

    def _render_before_break(self, local_start_x, start, stop, dist_to_line_start):
        self._render_slice(start, GraphicUnit(0), stop.x - start.x)

    def _render_after_break(self, local_start_x, start, stop):
        self._render_slice(start, local_start_x, stop.x - start.x)

    def _render_spanning_continuation(self, local_start_x, start, stop):
        self._render_slice(start, local_start_x, stop.x - start.x)
