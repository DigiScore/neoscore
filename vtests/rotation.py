from neoscore.common import *

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


tfont = neoscore.default_font.modified(size=GraphicUnit(10))
text_crossing_break = Text(
    (Mm(160), Mm(-10)),
    flowable,
    "Z".join((str(n) for n in range(10))),
    tfont,
    rotation=45,
)


html = "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>"
rich_text = RichText((Mm(30), Mm(50)), None, html, Mm(30), tfont, rotation=-20)


neoscore.show()
