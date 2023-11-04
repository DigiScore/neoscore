"""A example file that draws a circle.

This will be used for benchmarking.
"""

from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.page import Page
from neoscore.core.path import Path
from neoscore.core.flowable import Flowable
from neoscore.core.point import ORIGIN
from neoscore.core.brush import Brush
from neoscore.core.units import ZERO, Mm
from neoscore.core import *

neoscore.setup()

Path.ellipse((Mm(0), Mm(10)), None, Mm(50), Mm(50), "#000000")

render_example("circle")