import pytest

from neoscore.core import neoscore
from neoscore.core.page import Page
from neoscore.core.page_supplier import PageSupplier

from ..helpers import AppTest


class TestPageSupplier(AppTest):
    # noinspection PyStatementEffect
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
