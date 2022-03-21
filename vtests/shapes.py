import math

from neoscore.common import *

neoscore.setup()

Path.ellipse(ORIGIN, None, Mm(3), Mm(3), "#00ff00")
ellipse = Path.ellipse(
    (Mm(3), Mm(5)),
    None,
    Mm(10),
    Mm(5),
    Brush(Color(255, 0, 0, 60)),
    Pen(thickness=Mm(0.2)),
)

font = Font.modified(neoscore.default_font, size=Mm(0.85))

Text((Mm(5), Mm(-4)), None, "arc start angles:", font)
inc = (2 * math.pi) / 10
for i in range(1, 10):
    angle = i * inc
    pos = Point(Mm(5 * i), ZERO)

    arc = Path.arc(pos, None, Mm(4), Mm(2), angle, 0, Brush(Color(255, 255, 0, 40)))
    # Draw origin +
    # Path.straight_line((ZERO, Mm(-0.5)), arc, (ZERO, Mm(1)))
    # Path.straight_line((Mm(-0.5), ZERO), arc, (Mm(1), ZERO))
    # Label angle
    Text((pos.x, pos.y - Mm(2)), None, f"θ={angle:.2f}", font)

Path.arrow((Mm(20), Mm(10)), None, (Mm(20), Mm(5)))

Path.rect(
    (Mm(0), Mm(25)),
    None,
    Mm(5),
    Mm(8),
    Brush(Color(0, 0, 255, 70)),
    Pen(thickness=Mm(0.3)),
)

neoscore.show()
