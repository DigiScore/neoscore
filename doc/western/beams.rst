Beams
=====

Note-group beams can be created by passing a list of :obj:`.Chordrest`\ s to a :obj:`.BeamGroup`.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(100))
   Clef(ZERO, staff, "treble")
   chords = [
       Chordrest(Mm(1), staff, ["f"], (3, 16)),
       Chordrest(Mm(11), staff, ["a"], (1, 16)),
       Chordrest(Mm(21), staff, ["c"], (1, 8)),
       Chordrest(Mm(31), staff, ["e"], (1, 8)),
   ]
   BeamGroup(chords)

.. this is mostly copied from BeamGroup's docstring

Because neoscore has no internal understanding of meter or logical beat placement, the beaming algorithm does not automatically insert subdivisions. Instead it greedily tries to beam together as many notes as possible. Subdivisions can be specified by setting :obj:`.Chordrest.beam_break_depth`, which indicates a break after the chord to the given beam count.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(100))
   Clef(ZERO, staff, 'treble')
   chords = [
       Chordrest(Mm(1), staff, ["f"], (3, 16)),
       Chordrest(Mm(11), staff, ["a"], (1, 16)),
       Chordrest(Mm(21), staff, ["c"], (1, 32)),
       Chordrest(Mm(31), staff, ["e"], (1, 32))
   ]
   BeamGroup(chords)
   chords_2 = [
       Chordrest(Mm(40), staff, ["bb"], (3, 16)),
       Chordrest(Mm(50), staff, ["g"], (1, 16), beam_break_depth=1),
       Chordrest(Mm(60), staff, ["e"], (1, 32)),
       Chordrest(Mm(70), staff, ["c#",], (1, 32))
   ]
   BeamGroup(chords_2)

While in most situations beamlet "hooks" (as in a dotted 8th note
followed by a 16th note) unambiguously must point right or left,
there are some cases where it is ambiguous. For example, a
16th note between two 8th notes could have its beamlet point left
or right. In these situations, ``BeamGroup`` will point it left by
default, but users can override this by setting
:obj:`.Chordrest.beam_hook_dir`.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(100))
   Clef(ZERO, staff, 'treble')
   chords = [
       Chordrest(Mm(1), staff, ["c"], (1, 8)),
       Chordrest(Mm(11), staff, ["eb"], (1, 16)),
       Chordrest(Mm(21), staff, ["g"], (1, 8))
   ]
   BeamGroup(chords)
   chords_2 = [
       Chordrest(Mm(31), staff, ["c"], (1, 8)),
       Chordrest(Mm(41), staff, ["eb"], (1, 16), beam_hook_dir=DirectionX.RIGHT),
       Chordrest(Mm(51), staff, ["g"], (1, 8))
   ]
   BeamGroup(chords_2)

The beam direction and slant angle are determined automatically
based on the given notes. The direction can be overridden in
``BeamGroup``'s constructor.
