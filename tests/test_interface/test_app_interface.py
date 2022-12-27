import random

from neoscore.core import neoscore

from ..helpers import AppTest


class TestAppInterface(AppTest):
    def test_fuzz_viewport_scale_set_get_identity(self):
        # Regression test for https://github.com/DigiScore/neoscore/issues/89
        for i in range(1000):
            set_scale = random.uniform(0.01, 10)
            neoscore.app_interface.viewport_scale = set_scale
            got_scale = neoscore.app_interface.viewport_scale
            self.assertAlmostEqual(set_scale, got_scale)
