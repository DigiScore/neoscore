import unittest

from brown.core import brown
from brown.core.invisible_object import InvisibleObject


class TestInvisibleObject(unittest.TestCase):

    def setUp(self):
        brown.setup()

    def test_init(self):
        mock_parent = InvisibleObject((10, 11), parent=None)
        test_object = InvisibleObject((5, 6), parent=mock_parent)
        assert(test_object.x == 5)
        assert(test_object.y == 6)
        assert(test_object.parent == mock_parent)
