"""Built-in page overlay helpers"""

from typing import Optional

from neoscore.core import neoscore
from neoscore.core.directions import DirectionX
from neoscore.core.font import Font
from neoscore.core.page import Page
from neoscore.core.page_supplier import PageOverlayFunc
from neoscore.core.text import Text


def simple_header_footer(
    outside_top_text: Optional[str] = None,
    centered_top_text: Optional[str] = None,
    outside_bottom_text: Optional[str] = None,
    centered_bottom_text: Optional[str] = None,
    font: Optional[Font] = None,
) -> PageOverlayFunc:
    """Create an overlay function for simple headers and footers.

    Args:
        outside_top_text: Text to display on the top outside page corner.
        centered_top_text: Text to display centered in the top margin
        outside_bottom_text: Text to display on the bottom outside page corner.
        centered_bottom_text: Text to display centered in the bottom margin
        font: Font to use for all text. If none is provided, this will default
            to a slightly smaller version of the default font.

    The outside corner positions vary based on whether the page is left or right
    sided. The text items are positioned half along the margins. Center text is
    automatically center-aligned, and outside text is aligned to the outside.

    All text items can include a magic template string ``"%page"``, which will be
    automatically replaced by the overlaid page's number. For instance,
    ``simple_header_footer(centered_bottom_text="Page #%page)`` will generate
    footers with the text "Page #1", "Page #2", etc.

    This generates and reutrns a ``PageOverlayFunc`` which should be passed to the
    document's page generator with:

    >>> neoscore.document.pages.overlay_func = simple_header_footer() # doctest: +SKIP

    This only affects pages created after set, so typically this should be done right
    after ``neoscore.setup()``.

    """

    def generated_overlay_func(page: Page):
        n = page.index + 1
        # These different resolved names are needed to prevent closure scoping issues
        top_corner_text = (
            _format_template(outside_top_text, n) if outside_top_text else None
        )
        top_center_text = (
            _format_template(centered_top_text, n) if centered_top_text else None
        )
        bottom_corner_text = (
            _format_template(outside_bottom_text, n) if outside_bottom_text else None
        )
        bottom_center_text = (
            _format_template(centered_bottom_text, n) if centered_bottom_text else None
        )
        text_font = font or neoscore.default_font.modified(
            size=neoscore.default_font.size * 0.9
        )
        if page.page_side == DirectionX.LEFT:
            outside_x = page.left_margin_x - (page.full_margin_left / 2)
        else:
            outside_x = page.right_margin_x + (page.full_margin_right / 2)
        center_x = page.center_x
        top_y = page.top_margin_y - (page.paper.margin_top / 2)
        bottom_y = page.bottom_margin_y + (page.paper.margin_bottom / 2)
        if top_corner_text:
            t = Text((outside_x, top_y), page, top_corner_text, text_font)
            if page.page_side == DirectionX.RIGHT:
                t.x -= t.bounding_rect.width
        if top_center_text:
            t = Text((center_x, top_y), page, top_center_text, text_font)
            t.x -= t.bounding_rect.width / 2
        if bottom_corner_text:
            t = Text((outside_x, bottom_y), page, bottom_corner_text, text_font)
            if page.page_side == DirectionX.RIGHT:
                t.x -= t.bounding_rect.width
        if bottom_center_text:
            t = Text((center_x, bottom_y), page, bottom_center_text, text_font)
            t.x -= t.bounding_rect.width / 2

    return generated_overlay_func


def _format_template(template: str, page_number: int) -> str:
    return template.replace("%page", str(page_number))
