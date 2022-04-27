Staves, Clefs, and Signatures
=============================

Staves can be created just like any other object.

.. rendered-example::

   Staff(ORIGIN, None, Mm(100))

Staves can be made to wrap around page edges by placing them in flowable containers.

.. rendered-example::

   flowable = Flowable(ORIGIN, None, Mm(300), Mm(30))
   Staff(ORIGIN, flowable, Mm(300))

Each staff has an associated :obj:`unit <.Staff.unit>` type which encodes the distance between two staff lines.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(100))
   Text((Mm(0), staff.music_font.unit(1)), staff, "text on second staff line")

Staves support customization out of the box; they can be any size, have any number of lines, and they can be drawn with different pens.

.. rendered-example::

   Staff(ORIGIN, None, Mm(100))
   Staff((ZERO, Mm(15)), None, Mm(100), line_spacing=Mm(1))
   Staff((ZERO, Mm(30)), None, Mm(100), line_count=1)
   Staff((ZERO, Mm(45)), None, Mm(100), line_count=3)
   Staff((ZERO, Mm(60)), None, Mm(100), line_count=8)
   Staff((ZERO, Mm(85)), None, Mm(100), pen=Pen("#ff0000", pattern=PenPattern.DASH))

Clefs
-----

:obj:`.Clef`\ s control staff pitch layout. They're automatically drawn once wherever placed, and then at the beginning of every subsequent staff system until another clef is encountered.

.. rendered-example::

    flowable = Flowable(ORIGIN, None, Mm(500), Mm(15))
    staff = Staff(ORIGIN, flowable, Mm(500))
    Clef(Mm(20), staff, 'treble')
    Clef(Mm(200), staff, 'bass')

Several common clef types are built in, and for convenience these can be passed in by their string names. These include:

* ``'treble'``
* ``'treble_8vb'``
* ``'bass'``
* ``'bass_8vb'``
* ``'tenor'``
* ``'alto'``
* ``'percussion_1'``
* ``'percussion_2'``

Custom clefs can also be defined using arbitrary glyphs and pitch offsets using :obj:`.ClefType`.

Key Signatures
--------------

Cosmetic standard key signatures are supported out of the box. Like clefs, they are automatically drawn once were placed and then at every subsequent line until canceled by another. They're also automatically offset to be placed after clefs.

.. rendered-example::

   flowable = Flowable(ORIGIN, None, Mm(500), Mm(15))
   staff = Staff(ORIGIN, flowable, Mm(500))
   Clef(Mm(0), staff, 'treble')
   KeySignature(Mm(0), staff, 'gf_major')

.. note::

   Key signatures must be placed at a point in the staff with an active clef. Note also that key signatures are purely cosmetic and have no effect on how note accidentals are written.

Key signature types can be given as string shorthands of the form ``[pitch letter][f|s]_[major|minor]``, for example ``'c_major'``, ``'fs_minor'``, or ``'df_major'``. You can also specify enum variants of :obj:`.KeySignatureType`.

Time Signatures
---------------

Time signatures can also be attached to staves.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(100))
   TimeSignature(ZERO, staff, (4, 4))

Meters can be defined in a few different ways. A 2-tuple as seen above will give a simple two-number signature. You can also specify additive signatures by passing a list in the upper number. The special glyphs for "common" and "cut" time can be specified using :obj:`.COMMON_TIME` and :obj:`.CUT_TIME`. Arbitrary glyphs can also be used by directly creating :obj:`.Meter` objects.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(100))
   TimeSignature(ZERO, staff, (3, 16))
   TimeSignature(Mm(20), staff, ([3, 3, 2], 8))
   TimeSignature(Mm(50), staff, COMMON_TIME)
   TimeSignature(Mm(70), staff, Meter(['accidentalSharp'], ['accidentalFlat']))


.. note::

   Time signatures are purely cosmetic since neoscore's limited engraving knowledge is not meter-aware.