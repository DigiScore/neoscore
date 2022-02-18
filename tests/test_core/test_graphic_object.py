import unittest

from brown.core import brown
from brown.core.flowable import Flowable
from brown.core.invisible_object import InvisibleObject
from brown.core.paper import Paper
from brown.utils.point import Point
from brown.utils.units import GraphicUnit, Mm

from ..helpers import assert_almost_equal


class TestGraphicObject(unittest.TestCase):
    def setUp(self):
        brown.setup(Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))
        self.flowable = Flowable((Mm(0), Mm(0)), Mm(10000), Mm(30), Mm(5))

    def test_pos_setter_changes_x(self):
        grob = InvisibleObject((5, 6))
        grob.pos = Point(7, 8)
        # TODO should it be expected that the pos setter converts to
        # Point[GraphicUnit]? Should non-unit values be allowed at
        # all?
        assert grob.pos == Point(7, 8)

    def test_map_between_items(self):
        source = InvisibleObject((5, 6), brown.document.pages[1])
        destination = InvisibleObject((99, 90), brown.document.pages[4])
        relative_pos = InvisibleObject.map_between_items(source, destination)

        page_1_pos = brown.document.canvas_pos_of(brown.document.pages[1])
        page_4_pos = brown.document.canvas_pos_of(brown.document.pages[4])

        expected = (page_4_pos + Point(99, 90)) - (page_1_pos + Point(5, 6))
        assert_almost_equal(relative_pos, expected)

    def test_register_child(self):
        parent = InvisibleObject((0, 0))
        child = InvisibleObject((0, 0))
        parent._register_child(child)
        assert child in parent.children

    def test_unregister_child(self):
        parent = InvisibleObject((0, 0))
        child = InvisibleObject((0, 0))
        parent.children = {child}
        parent._unregister_child(child)
        assert child not in parent.children

    def test_setting_parent_registers_self_with_parent(self):
        parent = InvisibleObject((0, 0))
        child = InvisibleObject((0, 0), parent=parent)
        assert child in parent.children

    def test_descendants(self):
        root = InvisibleObject((0, 0))
        child_1 = InvisibleObject((0, 0), parent=root)
        child_2 = InvisibleObject((0, 0), parent=root)
        subchild_1 = InvisibleObject((0, 0), parent=child_2)
        subchild_2 = InvisibleObject((0, 0), parent=child_2)
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

        root = InvisibleObject((0, 0))
        child_1 = InvisibleObject((0, 0), parent=root)
        child_2 = MockDifferentClass1((0, 0), parent=root)
        subchild_1 = MockDifferentClass2((0, 0), parent=child_2)
        subchild_2 = MockDifferentClass2((0, 0), parent=child_2)
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

        root = InvisibleObject((0, 0))
        child_1 = InvisibleObject((0, 0), parent=root)
        child_2 = MockDifferentClass1((0, 0), parent=root)
        subchild_1 = MockDifferentClass2((0, 0), parent=child_2)
        subchild_2 = MockDifferentClass2((0, 0), parent=child_2)
        descendants = list(root.descendants_of_exact_class(MockDifferentClass1))
        descendants_set = set(descendants)
        # Assert no duplicates were yielded
        assert len(descendants) == len(descendants_set)
        # Assert root itself was not in the descendants list
        assert root not in descendants_set
        # Assert descendants content
        assert {child_2} == descendants_set
