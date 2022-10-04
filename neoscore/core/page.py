from __future__ import annotations

from typing import TYPE_CHECKING

from backports.cached_property import cached_property

from neoscore.core.brush import Brush
from neoscore.core.color import Color
from neoscore.core.directions import DirectionX
from neoscore.core.paper import Paper
from neoscore.core.pen import Pen
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.point import Point, PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.rect import Rect
from neoscore.core.units import ZERO, Mm, Unit

if TYPE_CHECKING:
    from neoscore.core.document import Document


_PREVIEW_OUTLINE_COLOR = Color("#551155")
_PREVIEW_SHADOW_COLOR = Color(0, 0, 0, 80)


class Page(PositionedObject):

    """A document page.

    All :obj:`.PositionedObject`\ s will have a ``Page`` as their
    ancestor. All ``Page``\ s are direct children of the global document.

    ``Page`` objects are automatically created by ``Document`` and should
    not be manually created or manipulated.
    """

    _neoscore_page_type_marker = True

    def __init__(
        self,
        pos: PointDef,
        document: Document,
        index: int,
        page_side: DirectionX,
        paper: Paper,
    ):
        """
        Args:
            pos: The position of the top left corner of this page's live area
                in canvas space. Note that this refers to the corner of the *live*
                area bounded by margins, not the actual paper corner.
            document: The global document. This is used as the ``Page`` object's parent.
            index: The index of this page. This should be the same index this page
                can be found at in :obj:`.Document.pages`.
            page_side: The left/right side the page lies on when printed.
            paper: The paper geometry for this page.
        """
        super().__init__(pos, document)  # noqa
        self._document = document
        self._index = index
        self._page_side = page_side
        self.paper = paper
        self._geometry_preview_created = False

    @property
    def index(self):
        """The index of this page in its managing :obj:`.PageSupplier`."""
        return self._index

    @property
    def page_side(self):
        """The left/right side the page lies on when printed.

        This determines which side the gutter should be placed on.
        """
        return self._page_side

    @cached_property
    def bounding_rect(self) -> Rect:
        """The page bounding rect, positioned relative to the ``pos``."""
        if self.page_side == DirectionX.RIGHT:
            # Page is on right side, apply gutter on left side
            rect_x = -(self.paper.gutter + self.paper.margin_left)
        else:
            rect_x = -self.paper.margin_left
        return Rect(
            rect_x,
            -self.paper.margin_top,
            self.paper.width,
            self.paper.height,
        )

    @cached_property
    def document_space_bounding_rect(self) -> Rect:
        """The page bounding rect relative to the document."""
        local_rect = self.bounding_rect
        return Rect(
            local_rect.x + self.x,
            local_rect.y + self.y,
            local_rect.width,
            local_rect.height,
        )

    @cached_property
    def full_margin_left(self) -> Unit:
        """The left margin, including any gutter if the gutter is on the left."""
        if self.page_side == DirectionX.RIGHT:
            return self.paper.margin_left + self.paper.gutter
        else:
            return self.paper.margin_left

    @cached_property
    def full_margin_right(self) -> Unit:
        """The right margin, including any gutter if the gutter is on the right."""
        if self.page_side == DirectionX.RIGHT:
            return self.paper.margin_right
        else:
            return self.paper.margin_right + self.paper.gutter

    @property
    def left_margin_x(self) -> Unit:
        """The X position of the edge of the left margin.

        This is always ``ZERO``, given here as a convenience synonym.
        """
        return ZERO

    @property
    def right_margin_x(self) -> Unit:
        """The X position of the edge of the right margin.

        This is always ``page.paper.live_width``, given here as a convenience synonym.
        """
        return self.paper.live_width

    @property
    def top_margin_y(self) -> Unit:
        """The Y position of the edge of the top margin.

        This is always ``ZERO``, given here as a convenience synonym.
        """
        return ZERO

    @property
    def bottom_margin_y(self) -> Unit:
        """The Y position of the edge of the top margin.

        This is always ``page.paper.live_height``, given here as a convenience synonym.
        """
        return self.paper.live_height

    @property
    def center_x(self) -> Unit:
        """The X position of the center of the live page area.

        This is a convenience method for ``page.paper.live_width / 2``.
        """
        return self.paper.live_width / 2

    def create_geometry_preview(self, background_brush: Brush):
        """Create and render child objects which show the page geometry.

        This shouldn't be called directly; use the setting in :obj:`.neoscore.score`
        instead.

        This is useful for interactive views, but should typically not be called in PDF
        and image export contexts.
        """
        # An implementation note on page geometry previews:

        # Ideally it would make the most sense for page geometry preview objects to be
        # generated at the same time the page is created. However, this goal conflicts
        # with our desire for preview visibility to be set at the top-level
        # `neoscore.show()` call, typically at the end of a user script. This allows
        # users to switch between preview mode and pdf/image export without modifying
        # their setup line. Achieving this requires some ugly workarounds, like passing
        # preview information to the top-level `document.render()` call, and here
        # ensuring this is only ever called once with a private flag. There are more
        # elegant ways to approach this issue, but for now this seems ok.

        # Import here to avoid cyclic import
        from neoscore.core.path import Path

        # Ensure this is only executed once
        if self._geometry_preview_created:
            return
        self._geometry_preview_created = True

        # To ensure these preview objects appear below all real document objects, we
        # need to attach all preview objects to the *first* page. This is necessary
        # because the first page is drawn first. We furthermore need to ensure page
        # preview objects are placed at the beginning of the first page's child list to
        # ensure they are drawn before other first-page children. Some strange hacks
        # here are needed to guarantee this behavior.
        parent = self if self.index == 0 else None
        bounding_rect = self.bounding_rect
        page_drop_shadow_rect = Path.rect(
            self.pos + Point(bounding_rect.x + Mm(1), bounding_rect.y + Mm(1)),
            parent,
            bounding_rect.width,
            bounding_rect.height,
            Brush(_PREVIEW_SHADOW_COLOR),
            Pen.no_pen(),
        )
        page_preview_rect = Path.rect(
            self.pos + Point(bounding_rect.x, bounding_rect.y),
            parent,
            bounding_rect.width,
            bounding_rect.height,
            background_brush,
            pen=Pen(_PREVIEW_OUTLINE_COLOR),
        )
        live_area_preview_rect = Path.rect(
            self.pos,
            parent,
            self.paper.live_width,
            self.paper.live_height,
            Brush.no_brush(),
            pen=Pen(_PREVIEW_OUTLINE_COLOR, pattern=PenPattern.DOT),
        )
        # Terrible hack to ensure preview is always drawn below document contents
        preview_objs_parent = live_area_preview_rect.parent
        preview_objs_parent.children = (
            preview_objs_parent.children[-3:] + preview_objs_parent.children[:-3]
        )
