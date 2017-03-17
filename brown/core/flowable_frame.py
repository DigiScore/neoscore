from brown.core import brown
from brown.core.auto_new_line import AutoNewLine
from brown.core.auto_new_page import AutoNewPage
from brown.core.invisible_object import InvisibleObject
from brown.utils.exceptions import OutOfBoundsError
from brown.utils.point import Point
from brown.utils.units import Mm, Unit


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
        super().__init__(pos)
        self._width = width
        self._height = height
        self._y_padding = y_padding if y_padding else Mm(5)
        self._layout_controllers = []
        self._generate_layout_controllers()

    ######## PUBLIC PROPERTIES ########

    @property
    def width(self):
        """Unit: The width (length) of the unwrapped frame"""
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        """Unit: The height of the unwrapped frame"""
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def y_padding(self):
        """Unit: The padding between wrapped sections of the frame"""
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
        pos = Point(self.pos.x, self.pos.y, 0)
        # Attach initial starting NewLine
        self.layout_controllers.append(
            AutoNewPage(self, x_progress, pos))
        while True:
            delta_x = live_page_width - pos.x
            x_progress += delta_x
            pos.y = pos.y + self.height + self.y_padding
            if x_progress >= self.width:
                break
            if pos.y > live_page_height:
                pos = Point(Mm(0), Mm(0), pos.page + 1)
                self.layout_controllers.append(
                    AutoNewPage(self, x_progress, pos))
            else:
                pos.x = Mm(0)
                self.layout_controllers.append(
                    AutoNewLine(self, x_progress, pos, self.y_padding))

    def _map_to_doc(self, local_point):
        """Convert a position inside the frame to its position in the document.

        Args:
            local_point (Point): A position in flowable space.
                The page number for this point should be 0.

        Returns:
            Point: A coordinate in document space with a page number.

        TODO: This currently assumes that the frame's direct parent is the document.
        """
        if local_point.x < 0 or local_point.x > self.width:
            raise OutOfBoundsError(
                '{} lies outside of the FlowableFrame'.format(local_point))
        current_line = self._last_break_at(local_point.x)
        return (current_line.pos +
                Point(local_point.x - current_line.x, local_point.y))

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

    def pos_in_frame_of(self, graphic_object):
        """Find the position of an object in (unwrapped) flowable space.

        Args:
            graphic_object (GraphicObject): An object in the frame.

        Returns: Point: A non-paged point relative to the flowable frame.

        Raises: ValueError: If `graphic_object` is not in the frame.
        """
        pos = Point(Unit(0), Unit(0))
        current = graphic_object
        try:
            while current != self:
                pos += current.pos
                current = current.parent
            return pos
        except AttributeError:
            raise ValueError('object is not in this FlowableFrame')

    def map_between_items_in_frame(self, source, destination):
        """Find the relative position between two objects in this frame.

        Args:
            source (GraphicObject): The object to map from
            destination (GraphicObject): The object to map to

        Returns:
            Point: The relative position of `destination`,
                relative to `source` within the local frame space.
                This will have a page number of 0.

        Raises:
            ValueError: If either `source` or `destination` are not
                in the frame.
        """
        return self.pos_in_frame_of(destination) - self.pos_in_frame_of(source)
