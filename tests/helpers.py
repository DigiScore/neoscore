import os
import sys
import tempfile
import unittest
from typing import Optional, Union

from neoscore.core import neoscore
from neoscore.core.path_element import CurveTo
from neoscore.core.point import Point
from neoscore.core.units import Mm, Unit


def assert_almost_equal(
    left: Union[Point, Unit],
    right: Union[Point, Unit],
    places: float = 7,
    epsilon: Optional[float] = None,
):
    """Compare points or units for approximate equality

    This compares based on the arguments' unit base values
    (corresponding to Qt pixels). If ``epsilon`` is given, compare
    equality within a difference of its value. Otherwise, compare the
    base values rounded to ``places``.
    """
    if isinstance(left, Unit):
        _assert_units_almost_equal(left, right, places, epsilon)
    elif isinstance(left, Point):
        _assert_points_almost_equal(left, right, places, epsilon)
    else:
        raise TypeError("Unsupported types")


def _assert_units_almost_equal(left, right, places, epsilon):
    if epsilon is not None:
        eq = abs(left.base_value - right.base_value) < epsilon
    else:
        eq = round(left.base_value - right.base_value, places) == 0
    if not eq:
        left_type = type(left)
        right_type = type(right)
        raise AssertionError(
            "{} and {} not equal within {} Unit decimal places.\n"
            "Both as {}: {} vs {}\n"
            "Both as {}: {} vs {}".format(
                left,
                right,
                places,
                left_type.__name__,
                left,
                left_type(right),
                right_type.__name__,
                right_type(left),
                right,
            )
        )


def _assert_points_almost_equal(left, right, places, epsilon):
    _assert_units_almost_equal(left.x, right.x, places, epsilon)
    _assert_units_almost_equal(left.y, right.y, places, epsilon)


def assert_path_els_equal(
    left,
    right,
    places: float = 7,
    epsilon: Optional[float] = None,
    compare_parents=True,
):
    """Assert equality of the basic attributes of two PathElements

    This only checks position and parents, skipping their incidental
    attributes inherited from PaintedObject like ``children``.
    """
    if isinstance(left, list) and isinstance(right, list):
        assert len(left) == len(right)
        for left_el, right_el in zip(left, right):
            assert_path_els_equal(
                left_el, right_el, places, epsilon, compare_parents=True
            )
        return
    assert type(left) == type(right)
    assert_almost_equal(left.pos, right.pos, places, epsilon)
    if compare_parents:
        assert left.parent == right.parent
    if isinstance(left, CurveTo):
        assert_path_els_equal(
            left.control_1, right.control_1, places, epsilon, compare_parents
        )
        assert_path_els_equal(
            left.control_2, right.control_2, places, epsilon, compare_parents
        )


def render_scene():
    out_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    out_file.close()
    try:
        neoscore.render_image((Mm(-100), Mm(-100), Mm(100), Mm(100)), out_file.name)
    finally:
        os.unlink(out_file.name)


class AppTest(unittest.TestCase):
    """Superclass for tests requiring neoscore application.

    Tests using ``setUp`` and ``tearDown`` functions should make sure to
    run the super functions as well.
    """

    @staticmethod
    def running_on_linux():
        return sys.platform.startswith("linux")

    def setUp(self):
        neoscore.setup()

    def tearDown(self):
        neoscore.shutdown()
