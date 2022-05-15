from helpers import render_example

from neoscore.core import neoscore
from neoscore.core.flowable import Flowable
from neoscore.core.music_font import MusicFont
from neoscore.core.music_text import MusicText
from neoscore.core.point import ORIGIN
from neoscore.core.repeating_music_text_line import RepeatingMusicTextLine
from neoscore.core.rich_text import RichText
from neoscore.core.text import Text
from neoscore.core.units import ZERO, Mm, Unit

neoscore.setup()

mfont = MusicFont("Bravura", Mm)

flowable = Flowable(ORIGIN, None, Mm(1000), Mm(30))

arp = MusicText(ORIGIN, None, ["wiggleArpeggiatoUp"] * 10, mfont, rotation=20)

for angle in range(0, 360, 10):
    MusicText(
        (Mm(50), ZERO),
        None,
        ["wiggleArpeggiatoUp"] * 10 + ["wiggleArpeggiatoUpArrow"],
        mfont,
        rotation=angle,
    )


tfont = neoscore.default_font.modified(size=Unit(10))
text_crossing_break = Text(
    (Mm(160), Mm(-10)),
    flowable,
    "Z".join((str(n) for n in range(10))),
    tfont,
    rotation=45,
)


html = (
    "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
    + "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>"
)
rich_text = RichText((Mm(30), Mm(50)), None, html, Mm(30), tfont, rotation=-20)


arp = RepeatingMusicTextLine(
    (Mm(60), Mm(50)),
    None,
    (Mm(0), Mm(-10)),
    None,
    "wiggleArpeggiatoUp",
    None,
    "wiggleArpeggiatoUpArrow",
    mfont,
)


render_example("rotation")
