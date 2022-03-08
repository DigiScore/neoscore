import unittest

from brown.core import brown
from brown.core.flowable import Flowable
from brown.core.graphic_object import GraphicObject
from brown.core.invisible_object import InvisibleObject
from brown.core.mapping import canvas_pos_of, map_between
from brown.core.paper import Paper
from brown.utils.point import Point
from brown.utils.units import GraphicUnit, Mm, Unit

from ..helpers import assert_almost_equal


class TestMapping(unittest.TestCase):
    def setUp(self):
        brown.setup(Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))
        self.flowable = Flowable((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))

    def test_map_between(self):
        source = InvisibleObject((Unit(5), Unit(6)), brown.document.pages[1])
        destination = InvisibleObject((Unit(99), Unit(90)), brown.document.pages[4])
        relative_pos = map_between(source, destination)

        page_1_pos = canvas_pos_of(brown.document.pages[1])
        page_4_pos = canvas_pos_of(brown.document.pages[4])

        expected = (page_4_pos + Point(Unit(99), Unit(90))) - (
            page_1_pos + Point(Unit(5), Unit(6))
        )
        assert_almost_equal(relative_pos, expected)

    def test_map_between_with_same_source_and_dest(self):
        obj = InvisibleObject((Unit(5), Unit(6)), brown.document.pages[0])
        assert_almost_equal(map_between(obj, obj), Point(Unit(0), Unit(0)))

    def test_map_between_with_common_parent(self):
        parent = InvisibleObject((Unit(5), Unit(6)), brown.document.pages[0])
        source = InvisibleObject((Unit(1), Unit(2)), parent)
        destination = InvisibleObject((Unit(3), Unit(10)), parent)
        relative_pos = map_between(source, destination)
        expected = Point(Unit(2), Unit(8))
        assert_almost_equal(relative_pos, expected)

    def test_map_between_where_dest_parent_is_src(self):
        source = InvisibleObject((Unit(1), Unit(2)), brown.document.pages[0])
        destination = InvisibleObject((Unit(3), Unit(10)), source)
        relative_pos = map_between(source, destination)
        expected = Point(Unit(3), Unit(10))
        assert_almost_equal(relative_pos, expected)

    def test_map_between_where_src_parent_is_dest(self):
        destination = InvisibleObject((Unit(3), Unit(10)), brown.document.pages[0])
        source = InvisibleObject((Unit(1), Unit(2)), destination)
        relative_pos = map_between(source, destination)
        expected = Point(Unit(-1), Unit(-2))
        assert_almost_equal(relative_pos, expected)

    def test_canvas_pos_of(self):
        item = InvisibleObject((Mm(5), Mm(6)), brown.document.pages[2])
        canvas_pos = canvas_pos_of(item)
        page_pos = canvas_pos_of(brown.document.pages[2])
        relative_pos = canvas_pos - page_pos
        assert_almost_equal(relative_pos, Point(Mm(5), Mm(6)))
