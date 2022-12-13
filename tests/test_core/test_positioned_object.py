from neoscore.core import neoscore
from neoscore.core.flowable import Flowable
from neoscore.core.paper import Paper
from neoscore.core.point import ORIGIN, Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.units import ZERO, Mm, Unit

from ..helpers import AppTest, assert_almost_equal


class TestPositionedObject(AppTest):
    def setUp(self):
        super().setUp()
        neoscore.document.paper = Paper(
            *[Mm(val) for val in [210, 297, 20, 20, 20, 20, 10]]
        )
        self.flowable = Flowable((Mm(0), Mm(0)), None, Mm(10000), Mm(30), Mm(5))

    def test_pos_setter_changes_x(self):
        obj = PositionedObject((Unit(5), Unit(6)), None)
        obj.pos = Point(Unit(7), Unit(8))
        assert obj.pos == Point(Unit(7), Unit(8))

    def test_register_child(self):
        parent = PositionedObject(ORIGIN, None)
        child = PositionedObject(ORIGIN, None)
        parent._register_child(child)
        assert child in parent.children

    def test_unregister_child(self):
        parent = PositionedObject(ORIGIN, None)
        child = PositionedObject(ORIGIN, None)
        parent.children = {child}
        parent._unregister_child(child)
        assert child not in parent.children

    def test_setting_parent_registers_self_with_parent(self):
        parent = PositionedObject(ORIGIN, None)
        child = PositionedObject(ORIGIN, parent)
        assert child in parent.children

    def test_descendants(self):
        root = PositionedObject(ORIGIN, None)
        child_1 = PositionedObject(ORIGIN, root)
        child_2 = PositionedObject(ORIGIN, root)
        subchild_1 = PositionedObject(ORIGIN, child_2)
        subchild_2 = PositionedObject(ORIGIN, child_2)
        subsubchild_1 = PositionedObject(ORIGIN, subchild_1)
        descendants = list(root.descendants)
        descendants_set = set(descendants)
        # Assert no duplicates were yielded
        assert len(descendants) == len(descendants_set)
        # Assert root itself was not in the descendants list
        assert root not in descendants_set
        # Assert descendants content
        assert {
            child_1,
            child_2,
            subchild_1,
            subchild_2,
            subsubchild_1,
        } == descendants_set

    def test_descendants_of_class_or_subclass(self):
        # Use two new mock classes for type filter testing
        class MockDifferentClass1(PositionedObject):
            pass

        class MockDifferentClass2(MockDifferentClass1):
            pass

        root = PositionedObject(ORIGIN, None)
        child_1 = PositionedObject(ORIGIN, root)
        child_2 = MockDifferentClass1(ORIGIN, root)
        subchild_1 = MockDifferentClass2(ORIGIN, child_2)
        subchild_2 = MockDifferentClass2(ORIGIN, child_2)
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
        class MockDifferentClass1(PositionedObject):
            pass

        class MockDifferentClass2(MockDifferentClass1):
            pass

        root = PositionedObject(ORIGIN, None)
        child_1 = PositionedObject(ORIGIN, root)
        child_2 = MockDifferentClass1(ORIGIN, root)
        subchild_1 = MockDifferentClass2(ORIGIN, child_2)
        subchild_2 = MockDifferentClass2(ORIGIN, child_2)
        descendants = list(root.descendants_of_exact_class(MockDifferentClass1))
        descendants_set = set(descendants)
        # Assert no duplicates were yielded
        assert len(descendants) == len(descendants_set)
        # Assert root itself was not in the descendants list
        assert root not in descendants_set
        # Assert descendants content
        assert {child_2} == descendants_set

    def test_descendants_with_attribute(self):
        class MockDifferentClass(PositionedObject):
            test_attr = 1

        root = PositionedObject(ORIGIN, None)
        child_1 = PositionedObject(ORIGIN, root)
        child_2 = MockDifferentClass(ORIGIN, root)
        descendants = list(root.descendants_with_attribute("test_attr"))
        descendants_set = set(descendants)
        # Assert no duplicates were yielded
        assert len(descendants) == len(descendants_set)
        # Assert root itself was not in the descendants list
        assert root not in descendants_set
        # Assert descendants content
        assert {child_2} == descendants_set

    def test_ancestors(self):
        root = PositionedObject(ORIGIN, None)
        child_1 = PositionedObject(ORIGIN, root)
        child_2 = PositionedObject(ORIGIN, child_1)
        ancestors = list(child_2.ancestors)
        assert ancestors == [
            child_1,
            root,
            neoscore.document.pages[0],
            neoscore.document,
        ]

    def test_first_ancestor_with_attr(self):
        class MockDifferentClass(PositionedObject):
            test_attr = 1

        root = MockDifferentClass(ORIGIN, None)
        child_1 = PositionedObject(ORIGIN, root)
        child_2 = PositionedObject(ORIGIN, child_1)
        assert child_2.first_ancestor_with_attr("test_attr") == root
        assert child_2.first_ancestor_with_attr("not_found") is None

    def test_length_is_zero(self):
        obj = PositionedObject((Unit(5), Unit(6)), None)
        assert obj.breakable_length == ZERO

    def test_map_to(self):
        source = PositionedObject((Unit(5), Unit(6)), neoscore.document.pages[1])
        destination = PositionedObject((Unit(99), Unit(90)), neoscore.document.pages[4])
        relative_pos = source.map_to(destination)

        page_1_pos = neoscore.document.pages[1].canvas_pos()
        page_4_pos = neoscore.document.pages[4].canvas_pos()

        expected = (page_4_pos + Point(Unit(99), Unit(90))) - (
            page_1_pos + Point(Unit(5), Unit(6))
        )
        assert_almost_equal(relative_pos, expected)

    def test_map_to_with_same_source_and_dest(self):
        obj = PositionedObject((Unit(5), Unit(6)), neoscore.document.pages[0])
        assert_almost_equal(obj.map_to(obj), Point(Unit(0), Unit(0)))

    def test_map_to_with_common_parent(self):
        parent = PositionedObject((Unit(5), Unit(6)), neoscore.document.pages[0])
        source = PositionedObject((Unit(1), Unit(2)), parent)
        destination = PositionedObject((Unit(3), Unit(10)), parent)
        relative_pos = source.map_to(destination)
        expected = Point(Unit(2), Unit(8))
        assert_almost_equal(relative_pos, expected)

    def test_map_to_where_dest_parent_is_src(self):
        source = PositionedObject((Unit(1), Unit(2)), neoscore.document.pages[0])
        destination = PositionedObject((Unit(3), Unit(10)), source)
        relative_pos = source.map_to(destination)
        expected = Point(Unit(3), Unit(10))
        assert_almost_equal(relative_pos, expected)

    def test_map_to_where_src_parent_is_dest(self):
        destination = PositionedObject((Unit(3), Unit(10)), neoscore.document.pages[0])
        source = PositionedObject((Unit(1), Unit(2)), destination)
        relative_pos = source.map_to(destination)
        expected = Point(Unit(-1), Unit(-2))
        assert_almost_equal(relative_pos, expected)

    def test_map_to_x(self):
        source = PositionedObject((Unit(5), Unit(6)), neoscore.document.pages[1])
        destination = PositionedObject((Unit(99), Unit(90)), neoscore.document.pages[4])
        relative_x = source.map_x_to(destination)

        page_1_x = neoscore.document.pages[1].canvas_pos().x
        page_4_x = neoscore.document.pages[4].canvas_pos().x

        expected = (page_4_x + Unit(99)) - (page_1_x + Unit(5))
        assert_almost_equal(relative_x, expected)

    def test_distance_to(self):
        source = PositionedObject((Unit(1), Unit(2)), None)
        destination = PositionedObject((Unit(3), Unit(10)), None)
        assert_almost_equal(
            source.distance_to(destination, Point(Unit(3), Unit(4))), Unit(13)
        )

    def test_canvas_pos(self):
        item = PositionedObject((Mm(5), Mm(6)), neoscore.document.pages[2])
        canvas_pos = item.canvas_pos()
        page_pos = neoscore.document.pages[2].canvas_pos()
        relative_pos = canvas_pos - page_pos
        assert_almost_equal(relative_pos, Point(Mm(5), Mm(6)))
