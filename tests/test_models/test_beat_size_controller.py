import unittest


from brown.models.beat import Beat
from brown.models.beat_size_controller import BeatSizeController
from brown.utils.units import Unit


class TestBeatSizeController(unittest.TestCase):

    def test_init(self):
        controller = BeatSizeController(Beat(5, 4),
                                        Unit(10),
                                        Unit(1),
                                        'MockConcreteBeat')
        assert(controller.x == Beat(5, 4))
        assert(controller.beat._conversion_rate == Unit(10).value)
        assert(controller.beat._constant_offset == Unit(1).value)
        assert(controller.beat.__name__ == 'MockConcreteBeat')
