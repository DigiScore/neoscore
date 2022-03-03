import math
import os
import sys

from brown.common import *

brown.setup()


static_text = Text((Mm(0), Mm(0)), "static")
moving_text = Text((Mm(20), Mm(10)), "moving")


def refresh_func(time):
    brown._clear_interfaces()
    moving_text.pos = Point(Mm(math.sin(time) * 20), Mm(10))
    brown.document._render()


brown.set_refresh_func(refresh_func)
brown.show()
