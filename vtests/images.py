from neoscore.common import *

neoscore.setup()


Image(ORIGIN, None, "tests/resources/pixmap_image.png", 2)

Image((Mm(10), Mm(10)), None, "tests/resources/svg_image.svg", 2)

neoscore.show()
