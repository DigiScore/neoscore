from brown.core import brown
from brown.core.auto_new_line import AutoNewLine
from brown.core.invisible_object import InvisibleObject
from brown.utils.exceptions import OutOfBoundsError
from brown.utils.point import Point
from brown.utils.units import Mm, Unit


class FlowableFrame(InvisibleObject):

    """A flowable coordinate space container.

    This provides a virtual horizontal strip of space in which
    objects can be placed, and at render time be automatically
    flowed across line breaks and page breaks in the document.

    To place an object in a `FlowableFrame`, simply parent it
    to one, or to an object already in one.

    In typical scores, there will be a single `FlowableFrame`
    placed in the first page of the document, and the vast
    majority of objects will be placed inside it.
    """

    def __init__(self, pos, width, height, y_padding=None):
        """
        Args:
            pos (Point or tuple): Starting position in relative to
                the top left corner of the live document area of the first page
            width (GraphicUnit): length of the frame
            height (GraphicUnit): height of the frame
            y_padding (GraphicUnit): The min gap between frame sections
        """
        super().__init__(pos)
        self._length = width
        self._height = height
        self._y_padding = y_padding if y_padding else Mm(5)
        self._layout_controllers = []
        self._generate_layout_controllers()

    ######## PUBLIC PROPERTIES ########

    @property
    def length(self):
        """Unit: The length (length) of the unwrapped frame"""
        return self._length

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

        Warning: This overwrites the contents of self.layout_controllers

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
        pos = Point(self.pos.x, self.pos.y)
        current_page = 0
        # Attach initial line controller
        self.layout_controllers.append(
            AutoNewLine(pos, brown.document.pages[current_page],
                        self, x_progress))
        while True:
            delta_x = live_page_width - pos.x
            x_progress += delta_x
            pos.y = pos.y + self.height + self.y_padding
            if x_progress >= self.length:
                # End of breakable width - Done.
                break
            if pos.y > live_page_height:
                # Page break - No y offset
                pos = Point(Mm(0), Mm(0))
                current_page += 1
                self.layout_controllers.append(
                    AutoNewLine(pos, brown.document.pages[current_page],
                                self, x_progress))
            else:
                # Line break - self.y_padding as y offset
                pos.x = Mm(0)
                self.layout_controllers.append(
                    AutoNewLine(pos, brown.document.pages[current_page],
                                self, x_progress, self.y_padding))

    def map_to_canvas(self, local_point):
        """Convert a local point to its position in the canvas.

        Args:
            local_point (Point): A position in the frame's local space.

        Returns:
            Point: The position mapped to the canvas.

        Note: This gives a simple position in the canvas - the graphical
              position of the point when rendered. If you need to know
              more contextual information, use `_map_to_page`
              (TODO: NOT YET IMPLEMENTED)
        """
        line = self.last_break_at(local_point.x)
        line_canvas_pos = brown.document.canvas_pos_of(line)
        return (line_canvas_pos
                + Point(local_point.x - line.local_x, local_point.y))

    def dist_to_line_start(self, local_x):
        """Find the distance of an x-pos to the left edge of its laid-out line.

        Args:
            local_x (Unit): The local x-position.

        Returns: Unit
        """
        line_start = self.last_break_at(local_x)
        return local_x - line_start.local_x

    def dist_to_line_end(self, local_x):
        """Find the distance of an x-pos to the right edge of its laid-out line.

        Args:
            local_x (Unit): The local x coordinate.

        Returns: Unit
        """
        return (self.dist_to_line_start(local_x) -
                brown.document.paper.live_width)

    def last_break_at(self, local_x):
        """Find the last `NewLine` that occurred before a given local local_x-pos

        Args:
            local_x (Unit): The local x coordinate.

        Returns:
            NewLine:
        """
        return self.layout_controllers[self.last_break_index_at(local_x)]

    def last_break_index_at(self, local_x):
        """Like `last_break_at`, but returns an index.

        Args:
            pos (Point): A local local_x-position

        Returns: int
        """
        remaining_x = local_x
        for i, controller in enumerate(self.layout_controllers):
            remaining_x -= controller.length
            if remaining_x < 0:
                return i
        else:
            raise OutOfBoundsError(
                'local_x={} lies outside of this FlowableFrame'.format(local_x))

    def pos_in_frame_of(self, graphic_object):
        """Find the position of an object in (unwrapped) flowable space.

        Args:
            graphic_object (GraphicObject): An object in the frame.

        Returns:
            Point: A non-paged point relative to the flowable frame.

        Raises:
            ValueError: If `graphic_object` is not in the frame.
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

        Raises:
            ValueError: If either `source` or `destination` are not
                in the frame.
        """
        return self.pos_in_frame_of(destination) - self.pos_in_frame_of(source)
