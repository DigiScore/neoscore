from brown.core.layout_controller import LayoutController
from brown.core.page import Page
from brown.utils.point import Point
from brown.utils.units import ZERO, Unit


class NewLine(LayoutController):
    """A line break controller."""

    def __init__(
        self,
        pos: Point,
        page: Page,
        flowable_x: Unit,
        height: Unit,
        margin_bottom: Unit = ZERO,
    ):
        """
        Args:
            pos: The position of the top left corner of this line relative
                to the page.
            page: The page this line appears on. This is used as
                the object's parent.
            flowable_x: The x position in the flowable's local space where this
                line begins.
            height: The height of the line
            margin_bottom: The space between the bottom of the
                current line and the top of the next. Defaults to `Unit(0)`
        """
        super().__init__(pos, page, flowable_x)
        self._margin_bottom = margin_bottom
        self._height = height

    ######## PUBLIC PROPERTIES ########

    @property
    def margin_bottom(self) -> Unit:
        """The space before the next line."""
        return self._margin_bottom

    @margin_bottom.setter
    def margin_bottom(self, value: Unit):
        self._margin_bottom = value

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
        return self._height
