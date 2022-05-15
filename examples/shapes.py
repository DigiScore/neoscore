import math

from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.brush import Brush
from neoscore.core.color import Color
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.point import ORIGIN, Point
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.text import Text
from neoscore.core.units import ZERO, Mm

neoscore.setup()

Path.ellipse((Mm(0), Mm(10)), None, Mm(6), Mm(6), "#00ff00")
Path.ellipse_from_center(
    (Mm(20), Mm(10)),
    None,
    Mm(20),
    Mm(10),
    "#f004",
    Pen(thickness=Mm(0.5)),
)

Path.arrow((Mm(40), Mm(20)), None, (Mm(40), Mm(10)))

Path.rect(
    (Mm(0), Mm(35)),
    None,
    Mm(10),
    Mm(16),
    Brush(Color(0, 0, 255, 70)),
    Pen(thickness=Mm(0.5)),
)

arcs_parent = PositionedObject((Mm(1), Mm(60)), None)

t = Text(ORIGIN, arcs_parent, "arc start angles:")
inc = (2 * math.pi) / 10
for i in range(1, 10):
    angle = i * inc
    pos = Point(Mm(18 * (i - 1)), Mm(10))
    arc = Path.arc(
        pos, arcs_parent, Mm(12), Mm(8), angle, 0, Brush(Color(255, 255, 0, 40))
    )
    # Draw origin +
    # Path.straight_line((ZERO, Mm(-0.5)), arc, (ZERO, Mm(1)))
    # Path.straight_line((Mm(-0.5), ZERO), arc, (Mm(1), ZERO))
    # Label angle
    Text((ZERO, Mm(-4)), arc, f"θ={angle:.2f}")


render_example("shapes")
