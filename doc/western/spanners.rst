Spanners
========

A common pattern in notation is objects which span between one and another, for example hairpins, slurs, and octave lines. Neoscore supports this through a family of :obj:`.Spanner` classes. Most spanners are created in the same way by providing an initial position and parent, and an end position and parent.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(40))
   Clef(ZERO, staff, 'treble')
   start = Chordrest(Mm(2), staff, ["f"], (1, 4))
   Chordrest(Mm(12), staff, ["a"], (1, 4))
   end = Chordrest(Mm(22), staff, ["c#'"], (1, 2))
   Hairpin((ZERO, staff.unit(6)), start, (ZERO, staff.unit(6)), end)

The ending parent can usually be omitted to make the ending position relative to the initial position.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(40))
   Clef(ZERO, staff, 'treble')
   start = Chordrest(Mm(2), staff, ["f"], (1, 4))
   Hairpin((ZERO, staff.unit(6)), start, (staff.unit(3), ZERO))

Hairpins
--------

Crescendo and diminuendo :obj:`.Hairpin`\ s, demonstrated above, can be configured in several ways. By default the opening points right, but this can be changed with the ``direction`` argument. They can also lie at angles and the default opening width can be configured.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(40))
   Clef(ZERO, staff, 'treble')
   start = Chordrest(Mm(2), staff, ["f"], (1, 4))
   Hairpin((ZERO, staff.unit(6)), start, (staff.unit(3), staff.unit(-4)),
       direction=DirectionX.LEFT, width=staff.unit(1))

Slurs and Ties
--------------

Slur and ties are both created with the :obj:`.Slur` class. By default they arch upward, but this can be changed with the ``direction`` argument.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(40))
   Clef(ZERO, staff, 'treble')
   start = Chordrest(Mm(2), staff, ["f"], (1, 4))
   Chordrest(Mm(12), staff, ["a"], (1, 4))
   end = Chordrest(Mm(22), staff, ["c#'"], (1, 2))
   Slur((ZERO, staff.unit(-1)), start.stem.end_point, end.extra_attachment_point, end)

Ties are just horizontal slurs. (`Though we're open to contributions making this easier <https://github.com/DigiScore/neoscore/issues/22>`_)

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(40))
   Clef(ZERO, staff, 'treble')
   start = Chordrest(Mm(2), staff, ["f"], (1, 4))
   Slur(start.extra_attachment_point, start, (Mm(10), ZERO), direction=DirectionY.DOWN)

A reasonable curvature is automatically derived from the spanner length, but this can be overridden with the ``height`` and ``arch_length`` arguments.

Octave Lines
------------

Cosmetic :obj:`.OctaveLine`\ s can be drawn with a common variety of octave indications, but note that they do not automatically transpose the notes under them.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(40))
   Clef(ZERO, staff, 'treble')
   Chordrest(Mm(2), staff, ["c''"], (1, 4))
   Chordrest(Mm(12), staff, ["e''"], (1, 4))
   # Note that this transposition is manual
   Chordrest(Mm(22), staff, ["g#'"], (1, 2))
   OctaveLine((Mm(18), staff.unit(-4)), staff, Mm(15))

Repeating Music Text Lines
--------------------------

:obj:`.RepeatingMusicTextLine` allows you to repeat some music text over a spanner. This is useful for things like trill lines.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(40))
   Clef(ZERO, staff, 'treble')
   c = Chordrest(Mm(2), staff, ["c'"], (1, 1))
   RepeatingMusicTextLine((ZERO, staff.unit(-1)), c, (Mm(20), ZERO), None, "wiggleTrill")

You can optionally provide a glyph to use as an end cap.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(40))
   Clef(ZERO, staff, 'treble')
   start = Chordrest(Mm(2), staff, ["c'"], (1, 1))
   end = Chordrest(Mm(25), staff, ["c''"], (1, 4))
   RepeatingMusicTextLine((staff.unit(2), ZERO), start.highest_notehead,
      (staff.unit(-1), ZERO), end.highest_notehead, "wiggleGlissando", "wiggleArpeggiatoUpArrow")

See `SMuFL's collection of multi-segment line glyphs here <https://w3c.github.io/smufl/latest/tables/multi-segment-lines.html>`_ for common applications.

Arpeggio Lines
--------------

Arpeggio lines can be built with :obj:`.RepeatingMusicTextLine`, but for convenience we provide one out of the box with :obj:`.ArpeggioLine`.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(40))
   Clef(ZERO, staff, 'treble')
   c = Chordrest(staff.unit(3), staff, ["c", "g", "eb"], (1, 16))
   ArpeggioLine((staff.unit(-2), staff.unit(-1)), c.highest_notehead,
       (staff.unit(-2), staff.unit(2)), c.lowest_notehead, include_arrow=True)

For chordrests specifically, the dedicated :obj:`.ArpeggioLine.for_chord` can automatically work out the line positions for you.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(40))
   Clef(ZERO, staff, 'treble')
   c = Chordrest(staff.unit(3), staff, ["c", "g", "eb'"], (1, 16))
   ArpeggioLine.for_chord(c, DirectionY.UP)

Other Spanners
--------------

Other available spanners include:

* :obj:`.PedalLine`
* :obj:`.PedAndStar`