from brown.utils.point import Point
from brown.core import brown
from brown.core.invisible_object import InvisibleObject
from brown.utils.units import Mm
from brown.core.auto_new_line import AutoNewLine
from brown.core.auto_new_page import AutoNewPage


class OutOfBoundsError(Exception):
    """Exception raised when a point lies outside of a FlowableFrame"""
    pass


class FlowableFrame(InvisibleObject):

    def __init__(self, pos, width, height, y_padding=None):
        """
        Args:
            pos (Point or tuple): Starting position in relative to
                the top left corner of the live document area of the first page
            width (GraphicUnit): width of the frame
            height (GraphicUnit): height of the frame
            y_padding (GraphicUnit): The min gap between frame sections
        """
        # NOTE: Position might be off, as different classes may or may not
        #       be expecting `pos` to be relative to the live doc root,
        #       not the true scene origin (0, 0) -- is there a difference?
        super().__init__(pos)
        self._width = width
        self._height = height
        self._y_padding = y_padding if y_padding else Mm(5)
        self._layout_controllers = []
        self._generate_layout_controllers()

    ######## PUBLIC PROPERTIES ########

    @property
    def pos(self):
        """Point: The starting point of the frame on the first page."""
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    @property
    def x(self):
        """GraphicUnit:"""
        return self.pos.x

    @x.setter
    def x(self, value):
        self.pos.x = value

    @property
    def y(self):
        """GraphicUnit:"""
        return self.pos.y

    @y.setter
    def y(self, value):
        self.pos.y = value

    @property
    def width(self):
        """GraphicUnit:"""
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        """GraphicUnit:"""
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def y_padding(self):
        """GraphicUnit:"""
        return self._y_padding

    @y_padding.setter
    def y_padding(self, value):
        self._y_padding = value

    @property
    def layout_controllers(self):
        """list[LayoutController]: Controllers affecting flowable layout"""
        return self._layout_controllers

    @layout_controllers.setter
    def layout_controllers(self, value):
        self._layout_controllers = value

    ######## PRIVATE METHODS ########

    def _generate_layout_controllers(self):
        """Generate automatic layout controllers.

        The generated controllers are stored in `self.layout_controllers`
        in sorted order according to ascending x position

        Warning:
            This overwrites the contents of self.layout_controllers

        Returns: None
        """
        self._layout_controllers = []
        live_page_width = brown.document.paper.live_width
        live_page_height = brown.document.paper.live_height
        # The progress the layout generation has reached along the frame's width.
        # When the entire flowable has been covered, this value will == self.width
        x_progress = Mm(0)
        # Current position on the page relative to the top left corner
        # of the live page area
        pos_on_page = Point(self.pos)
        page_number = 1
        # Attach initial starting NewLine
        self.layout_controllers.append(
            AutoNewPage(self, x_progress, page_number, pos_on_page))
        while True:
            delta_x = live_page_width - pos_on_page.x
            x_progress += delta_x
            pos_on_page.y = pos_on_page.y + self.height + self.y_padding
            if x_progress >= self.width:
                break
            if pos_on_page.y > live_page_height:
                pos_on_page.x = Mm(0)
                pos_on_page.y = Mm(0)
                page_number += 1
                self.layout_controllers.append(
                    AutoNewPage(self, x_progress, page_number, pos_on_page))
            else:
                pos_on_page.x = Mm(0)
                self.layout_controllers.append(
                    AutoNewLine(self, x_progress, page_number, pos_on_page, self.y_padding))

    def _map_to_doc(self, point):
        """Convert a position inside the frame to its position in the document.

        Coordinates relative to the top left corner of the first page.

        Args:
            local_point (tuple or Point): An x-y coordinate in flowable space

        Returns:
            Point: An x-y coordinate in document space

        NOTE: This currently assumes that the frame's direct parent is None (the scene)
        """
        local_point = Point(point)
        if local_point.x < 0 or local_point.x > self.width:
            raise OutOfBoundsError(
                '{} lies outside of the FlowableFrame'.format(local_point))
        last_break_before = self._last_break_at(local_point.x)
        line_start_doc_pos = last_break_before.doc_start_pos
        offset_from_line_start = Point(local_point.x - last_break_before.x,
                                       local_point.y)
        return line_start_doc_pos + offset_from_line_start

    def _x_pos_rel_to_line_start(self, x):
        """Find the distance of an x-pos to the left edge of its laid-out line.

        Args:
            x (Unit): The local x-position.

        Returns: Unit
        """
        line_start = self._last_break_at(x)
        return x - line_start.x

    def _dist_to_line_end(self, x):
        """Find the distance of an x-pos to the right edge of its laid-out line.

        Args:
            x (Unit): The local x coordinate.

        Returns: Unit
        """
        return (self._x_pos_rel_to_line_start(x) -
                brown.document.paper.live_width)

    def _last_break_at(self, x):
        """
        Find the last line/page break that occured before a given local x-pos

        Args:
            pos (Point): A local x-position

        Returns:
            NewLine:
        """
        return self.layout_controllers[self._last_break_index_at(x)]

    def _last_break_index_at(self, x):
        """
        Like `_last_break_at`, but returns the break index instead of the break

        Args:
            pos (Point): A local x-position

        Returns:
            int
        """
        remaining_x = x
        for i, controller in enumerate(self.layout_controllers):
            remaining_x -= controller.length
            if remaining_x < 0:
                return i
        else:
            raise OutOfBoundsError(
                'x={} lies outside of this FlowableFrame'.format(x))
