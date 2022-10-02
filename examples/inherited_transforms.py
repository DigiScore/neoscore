from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.text import Text
from neoscore.core.units import ZERO, Mm

neoscore.setup()


prev = Text((ZERO, Mm(150)), None, "root")

for i in range(1, 11):
    prev = Text((Mm(20), ZERO), prev, f"desc_{i}", scale=1.1, rotation=5)

render_example("inherited_transforms")
