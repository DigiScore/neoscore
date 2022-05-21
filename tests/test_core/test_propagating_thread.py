import unittest

import pytest

from neoscore.core.propagating_thread import PropagatingThread


class TestPropagatingThread(unittest.TestCase):
    def test_without_throwing(self):
        thread = PropagatingThread(target=lambda: None)
        thread.start()
        thread.join()

    def test_exception_is_propagated(self):
        def func():
            raise ValueError()

        with pytest.raises(ValueError):
            thread = PropagatingThread(target=func)
            thread.start()
            thread.join()
