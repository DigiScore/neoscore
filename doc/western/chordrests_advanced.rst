Advanced Chordrests
===================

Custom Accidentals
------------------

:obj:`.Chordrest`\ s can use custom accidentals by passing in fully constructed :obj:`.Pitch`\ s or init arg tuples. In this case, you specify the pitch letter, accidental, and octave separately, allowing you to give an arbitrary SMuFL glyph name for an accidental. (In this integer octave notation, ``4`` is the octave starting at middle-C)

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(100))
   Clef(ZERO, staff, 'treble')
   Chordrest(staff.unit(3), staff, [("g", "accidentalDoubleFlatTwoArrowsUp", 4)], (3, 16))

`SMuFL provides a very large collection of accidental glyphs you can find at the spec <https://w3c.github.io/smufl/latest/tables/standard-accidentals-12-edo.html>`_, but you can also use any glyph name even if it's not meant to be an accidental.

Notehead Tables
---------------

By default neoscore uses the standard set of noteheads, automatically selecting the appropriate one for the specified duration, but you can easily tell it to use alternate sets of noteheads using :obj:`notehead tables <.notehead_tables>`.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(100))
   Clef(ZERO, staff, 'tenor')
   Chordrest(Mm(0), staff, ["c"], (1, 4), table=notehead_tables.DIAMOND)
   Chordrest(Mm(10), staff, ["c"], (1, 4), table=notehead_tables.PARENTHESIS)
   Chordrest(Mm(20), staff, ["c"], (1, 4), table=notehead_tables.SLASH)
   Chordrest(Mm(30), staff, ["c"], (1, 4), table=notehead_tables.INVISIBLE)

You can check out the complete set of built-in notehead tables in `the noteheads example <https://github.com/DigiScore/neoscore/blob/main/examples/noteheads.py>`_.

Individual Notehead Glyphs
--------------------------

You can also override notehead glyphs within a chord by giving a pitch as a tuple of a pitch and a glyphname.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(100))
   Clef(ZERO, staff, 'treble')
   Chordrest(staff.unit(1), staff, [
       "f", ("bb", "noteheadDiamondHalf"), ("f''", "noteheadBlackParens")
   ], (1, 4))