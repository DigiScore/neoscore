import math

from helpers import render_vtest

from neoscore.common import *

neoscore.setup()

# TODO MEDIUM increase sizes here

Path.ellipse((Mm(0), Mm(10)), None, Mm(6), Mm(6), "#00ff00")
ellipse = Path.ellipse(
    (Mm(6), Mm(9)),
    None,
    Mm(20),
    Mm(10),
    Brush(Color(255, 0, 0, 60)),
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

arcs_parent = PositionedObject((Mm(1), Mm(60)))

t = Text(ORIGIN, arcs_parent, "arc start angles:")
print(t.font.size)
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


render_vtest("shapes")
