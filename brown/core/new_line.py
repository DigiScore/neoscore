from brown.core import brown
from brown.core.layout_controller import LayoutController
from brown.utils.point import Point


class NewLine(LayoutController):
    """A line break controller."""

    def __init__(self, flowable_frame, x, pos, offset_y=0):
        """
        Args:
            flowable_frame (FlowableFrame): The parent frame.
            x (Unit): The x position in the frame's local space where this
                line begins.
            pos (Point): The position of the top left corner of this line.
            offset_y (Unit): The space between the bottom of the
                current line and the top of the next.
        """
        super().__init__(flowable_frame, x)
        self.pos = pos
        self.offset_y = offset_y

    ######## PUBLIC PROPERTIES ########

    @property
    def offset_y(self):
        """Unit: The space in pixels before the next line."""
        return self._offset_y

    @offset_y.setter
    def offset_y(self, value):
        self._offset_y = value

    @property
    def pos(self):
        """Point: The position of the top left corner of this line."""
        return self._pos

    @pos.setter
    def pos(self, value):
        if not isinstance(value, Point):
            value = Point(*value)
        else:
            value = Point.from_existing(value)
        self._pos = value

    @property
    def doc_end_pos(self):
        """Point: The position of the new line's bottom right corner in doc space

        This property is read-only
        """
        return self.pos + Point(self.length, self.height)

    @property
    def length(self):
        """Unit: The length of the line.

        This property is read-only.
        """
        # TODO: When breaks are made more flexible this needs to be updated.
        return brown.document.paper.live_width - self.pos.x

    @property
    def height(self):
        """Unit: The height of the line.

        This property is read-only.
        """
        # TODO: When breaks are made more flexible this needs to be updated.
        return self.flowable_frame.height

    ######## PRIVATE PROPERTIES ########

    @property
    def _is_automatic(self):
        return False
