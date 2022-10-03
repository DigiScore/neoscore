from neoscore.core import neoscore
from neoscore.core.page_overlays import simple_header_footer

from ..helpers import AppTest


class TestSimpleHeaderFooter(AppTest):
    def test_page_number_formatting(self):
        neoscore.document.pages.overlay_func = simple_header_footer(
            "foo %page", "bar %page", "biz %page", "baz %page"
        )
        page = neoscore.document.pages[0]
        assert len(page.children) == 4
        assert page.children[0].text == "foo 1"
        assert page.children[1].text == "bar 1"
        assert page.children[2].text == "biz 1"
        assert page.children[3].text == "baz 1"

    def test_font_override(self):
        font = neoscore.default_font.modified(size=20)
        neoscore.document.pages.overlay_func = simple_header_footer(
            "1", "2", "3", "4", font
        )
        page = neoscore.document.pages[0]
        assert page.children[0].font == font
        assert page.children[1].font == font
        assert page.children[2].font == font
        assert page.children[3].font == font
