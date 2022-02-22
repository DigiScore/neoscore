import unittest

from brown.core import brown
from brown.core.flowable import Flowable
from brown.core.graphic_object import GraphicObject
from brown.core.invisible_object import InvisibleObject
from brown.core.paper import Paper
from brown.utils.point import Point
from brown.utils.units import GraphicUnit, Mm, Unit

from ..helpers import assert_almost_equal


class TestGraphicObject(unittest.TestCase):
    def setUp(self):
        brown.setup(Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))
        self.flowable = Flowable((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))

    def test_pos_setter_changes_x(self):
        grob = InvisibleObject((Unit(5), Unit(6)))
        grob.pos = Point(Unit(7), Unit(8))
        # TODO should it be expected that the pos setter converts to
        # Point[GraphicUnit]? Should non-unit values be allowed at
        # all?
        assert grob.pos == Point(Unit(7), Unit(8))

    def test_map_between_items(self):
        source = InvisibleObject((Unit(5), Unit(6)), brown.document.pages[1])
        destination = InvisibleObject((Unit(99), Unit(90)), brown.document.pages[4])
        relative_pos = GraphicObject.map_between_items(source, destination)

        page_1_pos = brown.document.canvas_pos_of(brown.document.pages[1])
        page_4_pos = brown.document.canvas_pos_of(brown.document.pages[4])

        expected = (page_4_pos + Point(Unit(99), Unit(90))) - (
            page_1_pos + Point(Unit(5), Unit(6))
        )
        assert_almost_equal(relative_pos, expected)

    def test_map_between_items_with_same_source_and_dest(self):
        obj = InvisibleObject((Unit(5), Unit(6)), brown.document.pages[0])
        assert_almost_equal(
            GraphicObject.map_between_items(obj, obj), Point(Unit(0), Unit(0))
        )

    def test_map_between_items_with_common_parent(self):
        parent = InvisibleObject((Unit(5), Unit(6)), brown.document.pages[0])
        source = InvisibleObject((Unit(1), Unit(2)), parent)
        destination = InvisibleObject((Unit(3), Unit(10)), parent)
        relative_pos = GraphicObject.map_between_items(source, destination)
        expected = Point(Unit(2), Unit(8))
        assert_almost_equal(relative_pos, expected)

    def test_map_between_items_where_dest_parent_is_src(self):
        source = InvisibleObject((Unit(1), Unit(2)), brown.document.pages[0])
        destination = InvisibleObject((Unit(3), Unit(10)), source)
        relative_pos = GraphicObject.map_between_items(source, destination)
        expected = Point(Unit(3), Unit(10))
        assert_almost_equal(relative_pos, expected)

    def test_map_between_items_where_src_parent_is_dest(self):
        destination = InvisibleObject((Unit(3), Unit(10)), brown.document.pages[0])
        source = InvisibleObject((Unit(1), Unit(2)), destination)
        relative_pos = GraphicObject.map_between_items(source, destination)
        expected = Point(Unit(-1), Unit(-2))
        assert_almost_equal(relative_pos, expected)

    def test_register_child(self):
        parent = InvisibleObject((Unit(0), Unit(0)))
        child = InvisibleObject((Unit(0), Unit(0)))
        parent._register_child(child)
        assert child in parent.children

    def test_unregister_child(self):
        parent = InvisibleObject((Unit(0), Unit(0)))
        child = InvisibleObject((Unit(0), Unit(0)))
        parent.children = {child}
        parent._unregister_child(child)
        assert child not in parent.children

    def test_setting_parent_registers_self_with_parent(self):
        parent = InvisibleObject((Unit(0), Unit(0)))
        child = InvisibleObject((Unit(0), Unit(0)), parent=parent)
        assert child in parent.children

    def test_descendants(self):
        root = InvisibleObject((Unit(0), Unit(0)))
        child_1 = InvisibleObject((Unit(0), Unit(0)), parent=root)
        child_2 = InvisibleObject((Unit(0), Unit(0)), parent=root)
        subchild_1 = InvisibleObject((Unit(0), Unit(0)), parent=child_2)
        subchild_2 = InvisibleObject((Unit(0), Unit(0)), parent=child_2)
        descendants = list(root.descendants)
        descendants_set = set(descendants)
        # Assert no duplicates were yielded
        assert len(descendants) == len(descendants_set)
        # Assert root itself was not in the descendants list
        assert root not in descendants_set
        # Assert descendants content
        assert {child_1, child_2, subchild_1, subchild_2} == descendants_set

    def test_descendants_of_class_or_subclass(self):
        # Use two new mock classes for type filter testing
        class MockDifferentClass1(InvisibleObject):
            pass

        class MockDifferentClass2(MockDifferentClass1):
            pass

        root = InvisibleObject((Unit(0), Unit(0)))
        child_1 = InvisibleObject((Unit(0), Unit(0)), parent=root)
        child_2 = MockDifferentClass1((Unit(0), Unit(0)), parent=root)
        subchild_1 = MockDifferentClass2((Unit(0), Unit(0)), parent=child_2)
        subchild_2 = MockDifferentClass2((Unit(0), Unit(0)), parent=child_2)
        descendants = list(root.descendants_of_class_or_subclass(MockDifferentClass1))
        descendants_set = set(descendants)
        # Assert no duplicates were yielded
        assert len(descendants) == len(descendants_set)
        # Assert root itself was not in the descendants list
        assert root not in descendants_set
        # Assert descendants content
        assert {child_2, subchild_1, subchild_2} == descendants_set

    def test_descendants_of_exact_class(self):
        # Use two new mock classes for type filter testing
        class MockDifferentClass1(InvisibleObject):
            pass

        class MockDifferentClass2(MockDifferentClass1):
            pass

        root = InvisibleObject((Unit(0), Unit(0)))
        child_1 = InvisibleObject((Unit(0), Unit(0)), parent=root)
        child_2 = MockDifferentClass1((Unit(0), Unit(0)), parent=root)
        subchild_1 = MockDifferentClass2((Unit(0), Unit(0)), parent=child_2)
        subchild_2 = MockDifferentClass2((Unit(0), Unit(0)), parent=child_2)
        descendants = list(root.descendants_of_exact_class(MockDifferentClass1))
        descendants_set = set(descendants)
        # Assert no duplicates were yielded
        assert len(descendants) == len(descendants_set)
        # Assert root itself was not in the descendants list
        assert root not in descendants_set
        # Assert descendants content
        assert {child_2} == descendants_set
