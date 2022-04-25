from neoscore.core.layout_controller import LayoutController
from neoscore.core.page import Page
from neoscore.core.point import Point
from neoscore.core.units import Unit


class NewLine(LayoutController):
    """A line break controller."""

    def __init__(
        self,
        pos: Point,
        page: Page,
        flowable_x: Unit,
        length: Unit,
        height: Unit,
    ):
        """
        Args:
            pos: The position of the top left corner of this line relative
                to the page.
            page: The page this line appears on. This is used as
                the object's parent.
            flowable_x: The x position in the flowable's local space where this
                line begins.
            length: The line length
            height: The line height
        """
        super().__init__(pos, page, flowable_x)
        self._length = length
        self._height = height

    ######## PUBLIC PROPERTIES ########

    @property
    def doc_end_pos(self) -> Point:
        """The position of the new line's bottom right corner.

        This position is relative to the page.
        """
        return Point(self.pos.x + self.length, self.pos.y + self.height)

    @property
    def length(self) -> Unit:
        """The length of the line."""
        return self._length

    @length.setter
    def length(self, value: Unit):
        self._length = value

    @property
    def height(self) -> Unit:
        """The height of the line."""
        return self._height

    @height.setter
    def height(self, value: Unit):
        self._height = value
