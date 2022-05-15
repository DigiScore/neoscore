"""Objects which control flowable layouts"""
from typing import cast

from neoscore.core.page import Page
from neoscore.core.point import Point, PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import Unit


class LayoutController:
    """An abstract layout controller for working with Flowable layouts."""

    def __init__(self, flowable_x: Unit):
        """
        Args:
            flowable_x: The position of this controller within the owning
                flowable's local space.
        """
        self._flowable_x = flowable_x

    @property
    def flowable_x(self) -> Unit:
        """The x position in the flowable's local space."""
        return self._flowable_x


class NewLine(LayoutController, PositionedObject):
    """A line break controller.

    These are currently used only for automatically generated line breaks and should
    generally not be constructed directly. Line breaks can be controlled using
    :obj:`.BreakOpportunity` objects instead.
    """

    def __init__(
        self,
        pos: PointDef,
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
        LayoutController.__init__(self, flowable_x)
        PositionedObject.__init__(self, pos, page)
        self._length = length
        self._height = height

    @property
    def page(self) -> Page:
        """The page this controller appears on.

        This is identical to :obj:`parent <.PositionedObject.parent>`.
        """
        return cast(Page, self.parent)

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


class MarginController(LayoutController):
    """A controller defining flowable line margins.

    A flowable can have any number of different margin layers identified by a given
    ``layer_key``. A margin controller overrides the active margin values only for the
    specified layer. When a flowable generates its layout, it sums the margin values
    from all layers at the point of each new line to determine its margins.

    This layered margin system is useful for situations like staves, where different
    object states will change the required margins. For example, instrument names call
    for a margin size that will often be longer on the first system than later ones,
    while clefs and key signatures contribute their own margin amounts which can vary
    between systems. In this case, one might create separate margin controllers for each
    of these layers.

    These can be manually created and added to a flowable via
    :obj:`.Flowable.add_margin_controller` to control margins.
    """

    def __init__(self, flowable_x: Unit, margin_left: Unit, layer_key: str = ""):
        """
        Args:
            flowable_x: The position of this controller within the owning
                flowable's local space.
            margin_left: The margin value contributed by this controller in
                the specified layer
            layer_key: The layer this controller applies to. Layer keys starting with
                ``_neoscore`` are reserved for internal purposes.
        """
        super().__init__(flowable_x)
        self._margin_left = margin_left
        self._layer_key = layer_key

    @property
    def margin_left(self) -> Unit:
        """The left margin for generated lines while this controller is active"""
        return self._margin_left

    @property
    def layer_key(self) -> str:
        return self._layer_key
