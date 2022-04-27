Beams
=====

Note-group beams can be created by passing a list of :obj:`.Chordrest`\ s to a :obj:`.BeamGroup`.

.. rendered-example::

   staff = Staff(ORIGIN, None, Mm(100))
   Clef(ZERO, staff, 'treble')
   chords = [
       Chordrest(Mm(10), staff, ["c"], (3, 16)),
       Chordrest(Mm(20), staff, ["e"], (1, 16)),
       Chordrest(Mm(30), staff, ["g"], (1, 8)),
       Chordrest(Mm(40), staff, ["bb"], (1, 8))
   ]
   BeamGroup(chords)

