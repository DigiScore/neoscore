import unittest

from brown.utils.units import Unit
from brown.utils.anchored_point import AnchoredPoint
from brown.primitives.spanner import Spanner


class TestSpanner(unittest.TestCase):

    def test_inputs_converted_to_anchored_points(self):
        spanner = Spanner((Unit(0), Unit(1), 0, None),
                          (Unit(2), Unit(3), 0, None))
        assert(spanner.start == AnchoredPoint(Unit(0), Unit(1), 0, spanner))
        assert(spanner.stop == AnchoredPoint(Unit(2), Unit(3), 0, spanner))
