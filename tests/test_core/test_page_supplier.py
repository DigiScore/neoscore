import unittest

import pytest

from brown.core import brown
from brown.core.page import Page
from brown.core.page_supplier import PageSupplier


class TestPageSupplier(unittest.TestCase):

    def setUp(self):
        brown.setup()

    # noinspection PyStatementEffect
    def test_getitem_with_existing(self):
        supplier = PageSupplier(brown.document)
        supplier._page_list.extend([1, 2])
        assert(supplier[0] == 1)
        assert(supplier[1] == 2)
        assert(supplier[-1] == 2)
        assert(supplier[-2] == 1)
        with pytest.raises(IndexError):
            supplier[-3]

    def test_getitem_generation_needing_1(self):
        supplier = PageSupplier(brown.document)
        supplier._page_list.extend([1, 2])
        new_page = supplier[2]
        assert(len(supplier) == 3)
        assert(new_page == supplier[2])
        assert(isinstance(new_page, Page))
        assert(new_page.pos == brown.document.page_origin(2))
        assert(new_page.parent == brown.document)
        assert(new_page.paper == brown.document.paper)

    def test_getitem_generation_needing_many(self):
        supplier = PageSupplier(brown.document)
        new_page = supplier[2]
        assert(len(supplier) == 3)
        assert(new_page == supplier[2])
        for i in range(3):
            page = supplier[i]
            assert(isinstance(page, Page))
            assert(page.pos == brown.document.page_origin(i))
            assert(page.parent == brown.document)
            assert(page.paper == brown.document.paper)

    def test_iteration(self):
        supplier = PageSupplier(brown.document)
        supplier._page_list.extend([1, 2])
        assert([p for p in supplier] == [1, 2])
