import math

from neoscore.core import neoscore
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.point import Point
from neoscore.core.rich_text import RichText
from neoscore.core.text import Text
from neoscore.core.text_alignment import AlignmentX, AlignmentY
from neoscore.core.units import ZERO, Mm

neoscore.setup()

annotation = """
By default, scaling and rotation occurs about the object's local origin (0, 0). This can
be changed using the transform_origin property. In this example, we slide the transform
origin along the X axis while changing the rotation. The object's given position is
marked with an "x" while the transform origin is marked with an "o".
"""
RichText((Mm(1), Mm(1)), None, annotation, width=Mm(120))


mfont = MusicFont("Bravura", Mm)

transform_origin_label = Text((ZERO, Mm(50)), None, "")
rotation_label = Text((ZERO, Mm(60)), None, "")

obj_pos = Point(Mm(50), Mm(75))

obj_pos_marker = Text(
    obj_pos,
    None,
    "x",
    alignment_x=AlignmentX.CENTER,
    alignment_y=AlignmentY.CENTER,
)

obj_transform_origin_marker = Text(
    obj_pos,
    None,
    "o",
    alignment_x=AlignmentX.CENTER,
    alignment_y=AlignmentY.CENTER,
)


obj = MusicText(
    obj_pos,
    None,
    ["wiggleArpeggiatoUp"] * 10 + ["wiggleArpeggiatoUpArrow"],
    mfont,
    rotation=45,
)


def refresh_func(time):
    origin = Point(Mm(math.sin((time / 2)) * 20), ZERO)
    rotation = math.sin((time / 4)) * 30
    obj.transform_origin = origin
    obj.rotation = rotation

    transform_origin_label.text = f"transform_origin: {origin}"
    rotation_label.text = f"rotation: {round(rotation, 2)}"
    obj_transform_origin_marker.pos = obj_pos + origin


if __name__ == "__main__":
    neoscore.show(refresh_func)
