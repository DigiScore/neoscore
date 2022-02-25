from brown.core.layout_controller import LayoutController
from brown.utils.point import Point
from brown.utils.units import ZERO, Unit


class NewLine(LayoutController):
    """A line break controller."""

    # TODO update docs and typeify signature. not doing signature
    # types now because it seems like there might be a circular import
    # concern (flowable import AutoNewLine)

    def __init__(self, pos, page, flowable, local_x, offset_y=None):
        """
        Args:
            flowable (Flowable): The parent flowable.
            x (Unit): The x position in the flowable's local space where this
                line begins.
            pos (Point): The position of the top left corner of this line.
            offset_y (Unit): The space between the bottom of the
                current line and the top of the next. Defaults to `Unit(0)`
        """
        super().__init__(pos, page, flowable, local_x)
        self._offset_y = offset_y if offset_y else ZERO

    ######## PUBLIC PROPERTIES ########

    @property
    def offset_y(self) -> Unit:
        """The space before the next line."""
        return self._offset_y

    @offset_y.setter
    def offset_y(self, value: Unit):
        self._offset_y = value

    @property
    def doc_end_pos(self) -> Point:
        """The position of the new line's bottom right corner.

        This position is relative to the page.
        """
        return Point(self.pos.x + self.length, self.pos.y + self.height)

    @property
    def length(self) -> Unit:
        """The length of the line."""
        return self.page.paper.live_width - self.pos.x

    @property
    def height(self) -> Unit:
        """The height of the line."""
        return self.flowable.height
