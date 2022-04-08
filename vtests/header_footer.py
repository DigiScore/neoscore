from helpers import render_vtest

from neoscore.common import *
from neoscore.core import paper

neoscore.setup(paper.A4.modified(gutter=Mm(10)))


def create_page_overlay(page: Page):
    overlay_font = neoscore.default_font.modified(size=neoscore.default_font.size * 0.9)
    page_number = page.page_index + 1
    # Find X coordinate for text on outside margin
    if page.page_side == HorizontalDirection.LEFT:
        # The left margin always lies at 0
        outside_text_x = page.left_margin_x - (page.full_margin_left / 2)
    else:
        # The right margin always lies at
        outside_text_x = page.right_margin_x + (page.full_margin_right / 2)
    # Draw page number at top outside corner
    page_number_y = page.top_margin_y - (page.paper.margin_top / 2)
    Text((outside_text_x, page_number_y), page, str(page_number), overlay_font)
    # Draw footer text
    footer_y = page.bottom_margin_y + (page.paper.margin_bottom / 2)
    footer_text = Text((page.center_x, footer_y), page, "~neoscore~", overlay_font)
    footer_text.x -= footer_text.bounding_rect.width / 2


neoscore.document.pages.overlay_func = create_page_overlay

flowable = Flowable((Mm(0), Mm(0)), None, Mm(5000), Mm(15), Mm(5))
staff = Staff((Mm(0), Mm(0)), flowable, Mm(5000), Mm(1))


render_vtest("header_footer")
