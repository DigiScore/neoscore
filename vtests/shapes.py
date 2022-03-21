import math

from neoscore.common import *

neoscore.setup()


# Path.ellipse(ORIGIN, None, Mm(3), Mm(3), "#00ff00")
# ellipse = Path.ellipse(
#     (Mm(3), Mm(5)),
#     None,
#     Mm(10),
#     Mm(5),
#     Brush(Color(255, 0, 0, 60)),
#     Pen(thickness=Mm(0.2)),
# )

font = Font.modified(neoscore.default_font, size=Mm(1))

# Draw base line

# Path.straight_line(
#     (Mm(5), ZERO), None, (Mm(50), ZERO), pen=Pen("#0000ff", pattern=PenPattern.DASH)
# )

inc = (2 * math.pi) / 10
for i in range(1, 10):
    angle = i * inc
    pos = Point(Mm(5 * i), ZERO)

    arc = Path.arc(pos, None, Mm(4), Mm(2), angle, 0, NO_BRUSH)
    # Draw origin +
    Path.straight_line((ZERO, Mm(-0.5)), arc, (ZERO, Mm(1)))
    Path.straight_line((Mm(-0.5), ZERO), arc, (Mm(1), ZERO))
    # Label angle
    Text((pos.x, pos.y - Mm(4)), None, f"θ={angle:.2f}", font)

Path.arrow((Mm(10), Mm(10)), None, (Mm(20), Mm(5)))
Path.straight_line((Mm(10), Mm(10)), None, (Mm(20), Mm(5)), pen="#ff0000")


neoscore.show()
