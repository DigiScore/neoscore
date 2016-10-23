import unittest
import pytest

from brown.core import brown
from brown.primitives.staff import Staff



# WARNING: Keep an eye on this global brown state
#          this pattern very likely will not work
#          for all testing needs



def test_centered_position_to_top_down():
    brown.setup()
    test_staff = Staff(0, 0, 100, line_count=5)
    assert(test_staff._centered_position_to_top_down(0) == 4)
