Notes, Chords, and Rests
========================

Through the :obj:`.Chordrest` class, neoscore can automatically draw notes, chords, and rests given pitches and a duration. This will automatically create and lay out noteheads, stems, flags, rhythm dots, accidentals, ledger lines, and rest glyphs as requested, with decent room for customization.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(100))
   Clef(ZERO, staff, 'treble')
   Chordrest(staff.unit(2), staff, ["c", "g", "eb'"], (3, 16))

Chordrests are shaped by two main arguments - a list of pitches and a duration.

Pitches
-------

Pitches can be specified using a string shorthand similar to `that used by Lilypond <https://lilypond.org/doc/v2.21/Documentation/notation/writing-pitches>`_. The string shorthand consists of three parts: a pitch letter, an accidental, and octaves marks.

.. The below is mostly duplicated from Pitch.from_str's docstring

* Pitch letters are the standard ``c`` through ``b`` letters.
* The accidental may be ``f`` or ``b`` for flat, ``s`` or ``#`` for sharp, ``n`` for
  natural, ``ss`` or ``x`` for double-sharp, and ``ff`` or ``bb`` for double-flat.
* The octave indication is given by a series of apostrophes (``'``)
  or commas (``,``), where each apostrophe increases the pitch by an octave,
  and each comma decreases it. All octave transformations are relative to
  the octave starting at middle-C. The absence of an octave indicator means a
  pitch is within the octave starting at middle-C. (Note that this differs from
  Lilypond's notation, which starts at the octave *below* middle-C.)

Some examples:

* Middle-C: ``c``
* The B directly below that: ``b,``
* The C one octave below middle-C: ``c,``
* The E-flat above middle-C: ``ef`` or ``eb``
* The F-sharp above middle-C: ``fs`` or ``f#``
* The G-double-sharp above middle-C: ``fx`` or ``fss``
* The A-double-flat above the treble staff: ``aff'`` or ``abb'``

.. note::

   Key signatures are purely cosmetic, so pitches in chordrests should always be given the `written` accidentals desired.

.. note::

   There is a known bug with accidental layout in tight chords. See `Issue #32 <https://github.com/DigiScore/neoscore/issues/32>`_ for a workaround.

Durations
---------

Durations are specified with 2-tuples resembling fractions of a whole note. The lower number should be power of 2, while the upper number can be any value so long as it can be represented in a single note without ties.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(100))
   Clef(ZERO, staff, 'bass')
   Chordrest(Mm(0), staff, ["c"], (1, 4))
   Chordrest(Mm(10), staff, ["c"], (1, 8))
   Chordrest(Mm(20), staff, ["c"], (3, 8))
   Chordrest(Mm(30), staff, ["c"], (1, 1))
   Chordrest(Mm(40), staff, ["c"], (2, 1))
   Chordrest(Mm(50), staff, ["c"], (3, 128))

It can be a bit difficult to work out the numerical representations of durations with many dots, so you can also use :obj:`.Duration.from_description` to specify durations in terms of their base divisions and dot counts::

    # Triple-dotted 16th note
    >>> Duration.from_description(16, 3)
    Duration(fraction=Fraction(15, 128), ...)
    # Double-dotted whole note
    >>> Duration.from_description(1, 2)
    Duration(fraction=Fraction(7, 4), ...)
    # Dotted double-breve (double-breve uses 0 as its base division)
    >>> Duration.from_description(0, 1)
    Duration(fraction=Fraction(3, 1), ...)

.. note::

   Because durations are given as `written`, they have no concept of tuplets. Durations in tuplets should be specified in their written forms, then `tuplet annotations </western/spanners.html#tuplets>`_ can then be placed over the relevant note group.

Rests
-----

Rests are just chordrests without any notes.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(100))
   Clef(ZERO, staff, 'treble')
   Chordrest(Mm(0), staff, None, (1, 4))
   Chordrest(Mm(10), staff, None, (1, 8))
   Chordrest(Mm(20), staff, None, (3, 8))

By default rests are placed in the middle of the staff, but you can override their vertical position if needed.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(100))
   Clef(ZERO, staff, 'treble')
   Chordrest(Mm(0), staff, None, (1, 4), rest_y=staff.unit(-2))
