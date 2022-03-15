import unittest

from neoscore.core import neoscore
from neoscore.core.flowable import Flowable
from neoscore.core.invisible_object import InvisibleObject
from neoscore.core.paper import Paper
from neoscore.utils.point import Point
from neoscore.utils.units import Mm, Unit


class TestGraphicObject(unittest.TestCase):
    def setUp(self):
        neoscore.setup(Paper(*[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]))
        self.flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))

    def test_pos_setter_changes_x(self):
        grob = InvisibleObject((Unit(5), Unit(6)))
        grob.pos = Point(Unit(7), Unit(8))
        assert grob.pos == Point(Unit(7), Unit(8))

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

    def test_descendants_with_attribute(self):
        class MockDifferentClass(InvisibleObject):
            test_attr = 1

        root = InvisibleObject((Unit(0), Unit(0)))
        child_1 = InvisibleObject((Unit(0), Unit(0)), parent=root)
        child_2 = MockDifferentClass((Unit(0), Unit(0)), parent=root)
        descendants = list(root.descendants_with_attribute("test_attr"))
        descendants_set = set(descendants)
        # Assert no duplicates were yielded
        assert len(descendants) == len(descendants_set)
        # Assert root itself was not in the descendants list
        assert root not in descendants_set
        # Assert descendants content
        assert {child_2} == descendants_set
