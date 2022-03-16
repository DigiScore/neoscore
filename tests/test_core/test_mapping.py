import unittest

from neoscore.core import neoscore
from neoscore.core.flowable import Flowable
from neoscore.core.mapping import canvas_pos_of, map_between
from neoscore.core.paper import Paper
from neoscore.core.positioned_object import PositionedObject
from neoscore.utils.point import Point
from neoscore.utils.units import Mm, Unit

from ..helpers import assert_almost_equal


class TestMapping(unittest.TestCase):
    def setUp(self):
        neoscore.setup(Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))
        self.flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))

    def test_map_between(self):
        source = PositionedObject((Unit(5), Unit(6)), neoscore.document.pages[1])
        destination = PositionedObject((Unit(99), Unit(90)), neoscore.document.pages[4])
        relative_pos = map_between(source, destination)

        page_1_pos = canvas_pos_of(neoscore.document.pages[1])
        page_4_pos = canvas_pos_of(neoscore.document.pages[4])

        expected = (page_4_pos + Point(Unit(99), Unit(90))) - (
            page_1_pos + Point(Unit(5), Unit(6))
        )
        assert_almost_equal(relative_pos, expected)

    def test_map_between_with_same_source_and_dest(self):
        obj = PositionedObject((Unit(5), Unit(6)), neoscore.document.pages[0])
        assert_almost_equal(map_between(obj, obj), Point(Unit(0), Unit(0)))

    def test_map_between_with_common_parent(self):
        parent = PositionedObject((Unit(5), Unit(6)), neoscore.document.pages[0])
        source = PositionedObject((Unit(1), Unit(2)), parent)
        destination = PositionedObject((Unit(3), Unit(10)), parent)
        relative_pos = map_between(source, destination)
        expected = Point(Unit(2), Unit(8))
        assert_almost_equal(relative_pos, expected)

    def test_map_between_where_dest_parent_is_src(self):
        source = PositionedObject((Unit(1), Unit(2)), neoscore.document.pages[0])
        destination = PositionedObject((Unit(3), Unit(10)), source)
        relative_pos = map_between(source, destination)
        expected = Point(Unit(3), Unit(10))
        assert_almost_equal(relative_pos, expected)

    def test_map_between_where_src_parent_is_dest(self):
        destination = PositionedObject((Unit(3), Unit(10)), neoscore.document.pages[0])
        source = PositionedObject((Unit(1), Unit(2)), destination)
        relative_pos = map_between(source, destination)
        expected = Point(Unit(-1), Unit(-2))
        assert_almost_equal(relative_pos, expected)

    def test_canvas_pos_of(self):
        item = PositionedObject((Mm(5), Mm(6)), neoscore.document.pages[2])
        canvas_pos = canvas_pos_of(item)
        page_pos = canvas_pos_of(neoscore.document.pages[2])
        relative_pos = canvas_pos - page_pos
        assert_almost_equal(relative_pos, Point(Mm(5), Mm(6)))
