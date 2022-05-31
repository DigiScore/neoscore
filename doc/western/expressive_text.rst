Expressive Text
===============

Expressive text markings like dynamics and tempo marks can be written using simple :obj:`.Text` and :obj:`.MusicText` objects, but we provide some built-in functionality for convenience.

Dynamics
--------

Classical dynamics can be easily written in their idiomatic style with the :obj:`.Dynamic` class.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(30))
   Dynamic((ZERO, staff.unit(7)), staff, "p")

Dynamic strings can consist of any of the following letters: `p, m, f, r, s, z, n`.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(30))
   Dynamic((ZERO, staff.unit(7)), staff, "sfz")

Metronome Markings
------------------

Metronome marks are supported with the :obj:`.MetronomeMark` class.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(30))
   MetronomeMark((ZERO, staff.unit(-2)), staff, "metNoteQuarterUp", "= 60")

:obj:`.MetronomeMark` works like a combined :obj:`.MusicText` and :obj:`.Text` object. It takes two text arguments, the first in ``MusicText``\ s format, and the second a plain text string, and it takes two fonts (optionally inheriting the :obj:`.MusicFont` from an ancestor).

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(30))
   MetronomeMark(
      (ZERO, staff.unit(-2)),
      staff,
      ["metNoteQuarterUp", "metAugmentationDot"],
      "≈ 96",
   )

See `the metronome marks SMuFL range <https://w3c.github.io/smufl/latest/tables/metronome-marks.html>`_ for commonly used glyphs in the left-side text.

Articulations and Ornaments
---------------------------

Articulations and ornaments are created as regular :obj:`.MusicText` objects. SMuFL provides a large collection of `articulation glyphs here <https://w3c.github.io/smufl/latest/tables/articulation.html>`_ and `ornament glyphs here <https://w3c.github.io/smufl/latest/tables/common-ornaments.html>`_. For convenience, :obj:`.Chordrest` provides an attachment point above or below the outermost notehead with :obj:`.Chordrest.extra_attachment_point`; placing centered ``MusicText`` here can often work out of the box.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(30))
   Clef(ZERO, staff, 'treble')
   c = Chordrest(Mm(2), staff, ["c'", "e'"], (1, 8))
   MusicText(c.extra_attachment_point, c, "ornamentTurnInverted",
      alignment_x=AlignmentX.CENTER, alignment_y=AlignmentY.CENTER)

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(30))
   Clef(ZERO, staff, 'treble')
   c = Chordrest(Mm(2), staff, ["c#", "g"], (1, 8))
   MusicText(c.extra_attachment_point, c, "articAccentBelow",
      alignment_x=AlignmentX.CENTER, alignment_y=AlignmentY.CENTER)
