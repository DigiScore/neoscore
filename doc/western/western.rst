Western Notation Primitives
===========================

Neoscore provides a decent collection of notation primitives for writing conventional western-style notation. All of these classes are built directly on the core functionality described above, and they also serve as a collection of examples for how you can build your own notation system with neoscore.

Generally speaking, these classes help manage the vertical layout of objects, but horizontal layout must be explicitly provided. :obj:`.Chordrest` can transform a list of pitches and a duration into a stack of noteheads, accidentals, ledger lines, etc., but it will not automatically position itself in a measure. In fact, the ``western`` package has no concept of measures at all. Barlines are explicitly placed wherever you want, and time signatures are purely cosmetic.

This package also generally strives to provide ways to override glyphs where possible. :obj:`Notehead tables <.notehead_tables>` provide dozens of glyph-sets for noteheads, and if you need something else you can use arbitrary glyphs as noteheads. :obj:`.ClefType` provides a mechanism for creating new clefs with any glyph and pitch offset.

Note that while many of the examples here demonstrate objects used within staves, most can be used outside of staves too as long as they're provided with a :obj:`.MusicFont` or one of their ancestors implements :obj:`.HasMusicFont`.
