from helpers import render_vtest

from neoscore.common import *

neoscore.setup()

Text(ORIGIN, None, "Hello, world!")

x_centered = Text(
    (Mm(100), Mm(100)),
    None,
    "Horizontally centered",
    horizontal_alignment=HorizontalAlignment.CENTER,
)

left_aligned = Text(
    (Mm(100), Mm(110)),
    None,
    "Left aligned",
    horizontal_alignment=HorizontalAlignment.LEFT,
)

right_aligned = Text(
    (Mm(100), Mm(120)),
    None,
    "Right aligned",
    horizontal_alignment=HorizontalAlignment.RIGHT,
)

Path.straight_line((ZERO, Mm(-5)), x_centered, (ZERO, Mm(30)))

y_centered = Text(
    (Mm(100), Mm(200)),
    None,
    "Vertically centered",
    vertical_alignment=VerticalAlignment.CENTER,
)
Path.straight_line((Mm(-15), ZERO), y_centered, (Mm(30), ZERO))

# Demonstrate how horizontally centered text crossing flowable lines *doesn't work*
# See https://github.com/DigiScore/neoscore/issues/21
flowable = Flowable(ORIGIN, neoscore.document.pages[1], Mm(500), Mm(50))
Path.rect(ORIGIN, flowable, Mm(500), Mm(50), Brush.no_brush())
flowable_x_centered = Text(
    (Mm(145), Mm(25)),
    flowable,
    "Centered text doesn't work across flowable lines :(",
    horizontal_alignment=HorizontalAlignment.CENTER,
)
Path.straight_line((ZERO, Mm(-5)), flowable_x_centered, (ZERO, Mm(10)))


render_vtest("text")
