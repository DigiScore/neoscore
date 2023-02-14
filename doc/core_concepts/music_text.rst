Music Text
==========

Congratulations on making it to the first mention of music in these docs!

Neoscore is able to draw thousands of common and uncommon musical glyphs by writing them as text in musical fonts.

.. rendered-example::

    font = MusicFont("Bravura", Mm(2))
    MusicText(ORIGIN, None, "gClef", font)

:obj:`.MusicFont` and :obj:`.MusicText` are used much like their plaintext counterparts, but instead of specifying text as plain strings you provide glyph names. These glyph names are used as keys to look up their corresponding unicode codepoints in the `Standard Music Font Layout (SMuFL) schema <https://w3c.github.io/smufl/latest/index.html>`_ with which all supported music fonts comply.

Unlike text fonts which are sized to a given line height, music fonts are sized to a given *staff unit* - the distance between two staff lines. This size may be given either as a unit value or a unit type where ``unit(1)`` is that distance.

.. rendered-example::

    MusicText(ORIGIN, None, "ornamentTurn", MusicFont("Bravura", Mm))
    MusicText((Mm(3), ZERO), None, "ornamentTurn", MusicFont("Bravura", Mm(1)))
    MusicText((Mm(6), ZERO), None, "ornamentTurn", MusicFont("Bravura", Mm(2)))
    MusicText((Mm(11), ZERO), None, "noteheadBlack", MusicFont("Bravura", Mm(2)))

The way glyphs are aligned relative to the given :obj:`.MusicText` position varies based on the SMuFL schema. For example noteheads are locally aligned such that they can be placed at the Y position of a staff line or space-center, while the treble clef glyph expects to be placed on the fourth staff line.

.. rendered-example::

    font = MusicFont("Bravura", Mm(2))
    Path.straight_line(ORIGIN, None, (Mm(30), ZERO))
    MusicText(ORIGIN, None, "gClef", font)
    MusicText((Mm(8), ZERO), None, "fClef", font)
    MusicText((Mm(16), ZERO), None, "cClef", font)
    MusicText((Mm(24), ZERO), None, "noteheadWhole", font)

While the vast majority of :obj:`.MusicText` objects consist of just a single glyph, multi-character text can be specified by passing a list instead.

.. rendered-example::

    font = MusicFont("Bravura", Mm(2))
    MusicText(ORIGIN, None,
        ["noteheadBlack", "noteheadHalf", "noteheadWhole"], font)

Glyphs with `SMuFL alternate codes <https://w3c.github.io/smufl/latest/specification/glyphswithalternates.html>`_ can be specified with tuples.

.. rendered-example::

    font = MusicFont("Bravura", Mm(2))
    MusicText(ORIGIN, None, "flag16thUp", font)
    # straight-flagged alternate, aka "flag16thUpStraight"
    MusicText((Mm(4), ZERO), None, ("flag16thUp", 1), font)
    # short-flagged alternate, also accessible with the "flag16thUpShort" glyph name
    MusicText((Mm(8), ZERO), None, ("flag16thUp", 2), font)

Each resolved :obj:`.MusicChar` is placed in :obj:`.MusicText.music_chars`, through which you can access rich glyph metadata provided by SMuFL::

    >>> font = MusicFont("Bravura", Mm)
    >>> mt = MusicText(ORIGIN, None, "gClef", font)
    >>> mt.text
    '\ue050'
    >>> mt.music_chars[0].glyph_info
    GlyphInfo(canonical_name='gClef', codepoint='\ue050', description='G clef',
        bounding_rect=Rect(x=Mm(0.0), y=Mm(-4.392), width=Mm(2.684), height=Mm(7.024)),
        advance_width=Mm(2.684), anchors=None)

If you expect to use music text often, we strongly recommend getting familiar with `the SMuFL documentation <https://w3c.github.io/smufl/latest/index.html>`_, both to understand how it works and what metadata it offers, and to get a sense of what kinds of glyphs it offers.

Using other music fonts
-----------------------

Neoscore comes with Bravura built-in, but in theory it should support all SMuFL-compliant music fonts. SMuFL provides `a list of compatible fonts here <http://www.smufl.org/fonts/>`_. To use a new font, simply register it with the application with :obj:`.neoscore.register_music_font` and request its family name where needed. `See the relevant example here <https://github.com/DigiScore/neoscore/tree/main/examples/other_music_fonts.py>`_.


