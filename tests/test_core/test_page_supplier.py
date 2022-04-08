import pytest

from neoscore.core import neoscore
from neoscore.core.directions import HorizontalDirection
from neoscore.core.page import Page
from neoscore.core.page_supplier import PageSupplier
from neoscore.core.point import Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import Unit

from ..helpers import AppTest


class TestPageSupplier(AppTest):
    def test_getitem_with_existing(self):
        supplier = PageSupplier(neoscore.document)
        supplier._page_list.extend([1, 2])
        assert supplier[0] == 1
        assert supplier[1] == 2
        assert supplier[-1] == 2
        assert supplier[-2] == 1
        with pytest.raises(IndexError):
            supplier[-3]

    def test_getitem_generation_needing_1(self):
        supplier = PageSupplier(neoscore.document)
        supplier._page_list.extend([1, 2])
        new_page = supplier[2]
        assert len(supplier) == 3
        assert new_page == supplier[2]
        assert isinstance(new_page, Page)
        assert new_page.pos == neoscore.document.page_origin(2)
        assert new_page.parent == neoscore.document
        assert new_page.paper == neoscore.document.paper

    def test_getitem_generation_needing_many(self):
        supplier = PageSupplier(neoscore.document)
        new_page = supplier[2]
        assert len(supplier) == 3
        assert new_page == supplier[2]
        for i in range(3):
            page = supplier[i]
            assert isinstance(page, Page)
            assert page.pos == neoscore.document.page_origin(i)
            assert page.parent == neoscore.document
            assert page.paper == neoscore.document.paper

    def test_iteration(self):
        supplier = PageSupplier(neoscore.document)
        supplier._page_list.extend([1, 2])
        assert [p for p in supplier] == [1, 2]

    def test_page_side_selection(self):
        supplier = PageSupplier(neoscore.document)
        assert supplier[0].page_side == HorizontalDirection.RIGHT
        assert supplier[1].page_side == HorizontalDirection.LEFT
        assert supplier[2].page_side == HorizontalDirection.RIGHT
        assert supplier[3].page_side == HorizontalDirection.LEFT

    def test_overlay_func(self):
        # Use an overlay func passed in supplier init
        def test_overlay_func(page: Page):
            PositionedObject((Unit(1), Unit(2)), page)

        supplier = PageSupplier(neoscore.document, test_overlay_func)
        page = supplier[0]
        assert len(page.children) == 1
        assert page.children[0].pos == Point(Unit(1), Unit(2))

        # Now change the supplier and show it working on a newly generated page
        def second_test_overlay_func(page: Page):
            PositionedObject((Unit(3), Unit(4)), page)

        supplier.overlay_func = second_test_overlay_func
        page_2 = supplier[1]
        assert len(page_2.children) == 1
        assert page_2.children[0].pos == Point(Unit(3), Unit(4))

        # Now show that the change does not retroactively apply to existing pages

        page = supplier[0]
        assert len(page.children) == 1
        assert page.children[0].pos == Point(Unit(1), Unit(2))
