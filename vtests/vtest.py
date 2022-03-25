#!/usr/bin/env python3

"""A development sandbox used for manually checking visual outputs."""

import os
import random
import sys
import time

from neoscore.common import *

start_time = time.time()

neoscore.setup()


flow = Flowable((Mm(0), Mm(0)), None, Mm(35000), Mm(30), Mm(10))

counting_string = "    ".join(str(x) for x in range(600))
counting_text = Text((Mm(0), Mm(0)), parent=flow, text=counting_string)
counting_text._length = Mm(10000)

staff = Staff((Mm(0), Mm(0)), flow, Mm(10000), Mm(1))

lower_staff = Staff((Mm(0), Mm(9)), flow, Mm(7000), Mm(1))

lowest_staff = Staff((Mm(10), Mm(18)), flow, Mm(2000), Mm(1))

barline = BarLine(Mm(30), [staff, lower_staff, lowest_staff])

upper_staff_time_signature = TimeSignature(Mm(0), staff, Beat(4, 4))

upper_staff_clef = Clef(Mm(0), staff, "treble")
lower_staff_clef = Clef(Mm(0), lower_staff, "alto")
lowest_staff_clef = Clef(Mm(0), lowest_staff, "bass")
later_lowest_staff_clef = Clef(Mm(100), lowest_staff, "treble")

# Once flowable gutters are implemented, this explicit offsets for
# key/time sigs will not be needed
upper_staff_key_signature = KeySignature(
    upper_staff_clef.bounding_rect.width + staff.unit(0.5), staff, "af_major"
)
lower_staff_key_signature = KeySignature(
    lower_staff_clef.bounding_rect.width + lower_staff.unit(0.5),
    lower_staff,
    "cs_major",
)
lowest_staff_key_signature = KeySignature(
    lowest_staff_clef.bounding_rect.width + lowest_staff.unit(0.5),
    lowest_staff,
    "d_minor",
)

octave_line = OctaveLine((Mm(20), staff.unit(-2)), staff, Mm(1000), indication="8vb")

Chordrest(Mm(10), staff, ["a'", "bs"], Beat(2, 4))
Chordrest(Mm(40), staff, ["a'", "bs"], Beat(2, 4))
Chordrest(Mm(60), staff, ["b'", "bff"], Beat(2, 4))

Chordrest(Mm(10), lowest_staff, [("a", "accidentalQuarterToneSharpStein", 2)], (3, 4))
Chordrest(
    Mm(15),
    lowest_staff,
    [("a", "accidentalFlatRepeatedSpaceStockhausen", 2)],
    (3, 16),
)

font = Font("Lora", Mm(2), weight=100, italic=True)

regular_text = Text((Mm(20), staff.unit(-1)), parent=staff, text="piu mosso", font=font)

p = Dynamic((Mm(20), staff.unit(6)), staff, "p")

sfz = Dynamic.sfz((Mm(25), staff.unit(6)), staff)

hairpin = Hairpin((Mm(0), Mm(3)), p, (Mm(0), Mm(3)), sfz, 1)

slur = Slur((Mm(0), Mm(0)), regular_text, (Mm(0), Mm(0)), sfz)

brace = Brace(Mm(0), {staff, lower_staff, lowest_staff})

random_wiggles = [
    random.choice(["wiggleRandom1", "wiggleRandom2", "wiggleRandom3", "wiggleRandom4"])
    for i in range(100)
]

MusicText((Mm(25), staff.unit(2)), staff, random_wiggles)

scaling_texts = []
for i in range(0, 50, 2):
    scale = 1 + (i / 10)
    scaling_texts.append(
        MusicText(
            (Mm(290 + i), lowest_staff.unit(4)),
            lowest_staff,
            ["brace", ("gClef", 1)],
            scale=scale,
        )
    )

flowing_text = MusicText(
    (Mm(155), lower_staff.unit(3)), lower_staff, ["gClef"] * 130, scale=1
)

pen = Pen(thickness=Mm(0.2), pattern=PenPattern.DASHDOTDOT)
explicit_path = Path((Mm(0), Mm(0)), parent=p, pen=pen)
explicit_path.line_to(Mm(5000), Mm(100))

fake_trill = RepeatingMusicTextLine(
    (Mm(30), staff.unit(-6)), staff, Mm(5000), "wiggleTrill"
)

text_on_first_page = Text((Mm(0), Mm(0)), None, "first page!")

text_on_second_page = Text(
    (Mm(0), Mm(0)), parent=neoscore.document.pages[1], text="second page!"
)

text_on_third_page = Text(
    (Mm(0), Mm(0)), parent=neoscore.document.pages[2], text="third page!"
)

explicit_path_on_second_page = Path((Mm(0), Mm(0)), parent=text_on_second_page)
explicit_path_on_second_page.line_to(Mm(100), Mm(60))

ped_and_star_mark = PedAndStar((Mm(260), staff.unit(7)), staff, (Mm(30), staff.unit(0)))

pedal_line = PedalLine(
    (Mm(500), staff.unit(7)),
    staff,
    Mm(200),
    half_lift_positions=[Mm(30), Mm(60), Mm(100)],
)

Path.rect(
    (Mm(200), lowest_staff.unit(3)),
    lowest_staff,
    Mm(10),
    lowest_staff.unit(1),
    Brush("#00ffaa", BrushPattern.CROSSING_DIAGONAL_LINES),
    "#ff0000",
)

if "--image" in sys.argv:
    image_path = os.path.join(os.path.dirname(__file__), "output", "vtest_image.png")
    neoscore.render_image((Mm(0), Mm(0), Inch(2), Inch(2)), image_path, autocrop=True)
    print(f"Non-setup code took {time.time() - start_time}")
elif "--pdf" in sys.argv:
    # PDF export is currently broken
    pdf_path = os.path.join(os.path.dirname(__file__), "output", "vtest_pdf.pdf")
    neoscore.render_pdf(pdf_path)
else:
    neoscore.show()
