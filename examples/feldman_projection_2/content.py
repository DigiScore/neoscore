"""The score's content data.

The managed notation system built out in this example can turn this raw data into an
almost fully notated score.
"""


from examples.feldman_projection_2.glyph_name import GlyphName
from examples.feldman_projection_2.grid_unit import GridUnit as G
from examples.feldman_projection_2.instrument_data import EventData, InstrumentData
from examples.feldman_projection_2.measure import Measure as M
from examples.feldman_projection_2.register import Register as Reg

fl = "Flute"
tpt = "Trumpet"
vln = "Violin"
vc = "Cello"
pno1 = "Piano1"
pno2 = "Piano2"


DIAMOND = GlyphName("noteheadDiamondWhite")
PZ = "Pz"


events = [
    EventData(*data)
    for data in [
        # (instrument, pos_x, Register, text, length)
        # Page 1 (of original score)
        (pno2, M(0) + G(1), Reg.L, "5", G(3) + M(1) + G(2)),
        (tpt, M(0) + G(2), Reg.M, "", G(3)),
        (pno1, M(1), Reg.M, "1", G(1)),
        (tpt, M(2), Reg.L, "", G(2)),
        (vln, M(2) + G(1), Reg.H, DIAMOND, G(1)),
        (vc, M(2) + G(2), Reg.M, PZ, G(1)),
        (pno1, M(2) + G(2), Reg.L, "1", G(1)),
        (fl, M(2) + G(3), Reg.H, "", G(1) + G(3)),
        (tpt, M(2) + G(3), Reg.H, "", G(1)),
        (pno1, M(2) + G(3), Reg.H, "7", G(1)),
        (vc, M(3) + G(2), Reg.L, PZ, G(1)),
        (vln, M(3) + G(3), Reg.M, "A", G(1) + G(1)),
        (pno1, M(4) + G(1), Reg.L, "2", G(1)),
        (vc, M(4) + G(2), Reg.H, PZ, G(1)),
        (fl, M(5), Reg.M, "", G(1)),
        (pno2, M(5) + G(2), Reg.M, "1", G(2) + G(3)),
        (vc, M(6) + G(1), Reg.L, "A", G(1)),
        (vc, M(6) + G(2), Reg.H, DIAMOND, G(1)),
        (fl, M(6) + G(3), Reg.L, "", G(1)),
        (tpt, M(6) + G(3), Reg.H, "", G(1)),
        (pno1, M(6) + G(3), Reg.M, "3", G(1)),
        (vc, M(7) + G(3), Reg.M, PZ, G(1)),
        (vln, M(7) + G(3), Reg.M, PZ, G(1)),
        (fl, M(8) + G(3), Reg.L, "", G(1) + G(2)),
        (tpt, M(8) + G(3), Reg.L, "", G(1) + G(2)),
        (vln, M(8) + G(3), Reg.M, "A", G(1) + G(2)),
        (vc, M(8) + G(3), Reg.M, "A", G(1) + G(2)),
        (vc, M(9) + G(2), Reg.H, "A", G(1)),
        (pno1, M(9) + G(3), Reg.L, "1", G(1)),
        # Page 2 (of original score)
        (fl, M(10), Reg.M, "", G(1)),
        (vln, M(10), Reg.L, DIAMOND, G(1)),
        (tpt, M(10) + G(1), Reg.H, "", G(1)),
        (tpt, M(10) + G(2), Reg.L, "", G(1)),
        (tpt, M(11) + G(1), Reg.H, "", G(1)),
        (pno2, M(11) + G(2), Reg.M, "2", G(2) + M(1) + G(2)),
        (vc, M(12) + G(2), Reg.L, "A", G(1)),
        (tpt, M(12) + G(3), Reg.H, "", G(2)),
        (pno1, M(14) + G(1), Reg.H, "3", G(1)),
        (fl, M(14) + G(2), Reg.L, "", G(1)),
        (tpt, M(14) + G(2), Reg.L, "", G(1)),
        (vc, M(14) + G(2), Reg.H, PZ, G(1)),
        (tpt, M(15), Reg.M, "", G(1)),
        (fl, M(15) + G(1), Reg.H, "", G(3)),
        (vln, M(15) + G(1), Reg.L, "A", G(3)),
        (vc, M(15) + G(1), Reg.H, DIAMOND, G(3)),
        (tpt, M(16), Reg.H, "", G(1)),
        (tpt, M(17) + G(1), Reg.H, "", G(1)),
        (vc, M(17) + G(1), Reg.H, PZ, G(1)),
        (pno1, M(17) + G(2), Reg.H, "3", G(1)),
        (vln, M(17) + G(3), Reg.L, DIAMOND, G(1)),
        (pno1, M(19) + G(1), Reg.L, "1", G(1)),
        (fl, M(19) + G(3), Reg.H, "", G(1)),
        (vln, M(19) + G(3), Reg.M, DIAMOND, G(1)),
        (vc, M(19) + G(3), Reg.L, PZ, G(1)),
    ]
]

instruments = [
    InstrumentData(i, [e for e in events if e.instrument == i])
    for i in [fl, tpt, vln, vc, pno1, pno2]
]
