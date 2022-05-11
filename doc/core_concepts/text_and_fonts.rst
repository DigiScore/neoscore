Text
====

:obj:`.Text` is a fundamental neoscore class. As we've seen in previous examples, it is fairly straightforward to work with:

.. rendered-example::

   Text(ORIGIN, None, "Lorem ipsum")

.. note::

  From this point on we'll be omitting imports and ``neoscore.setup()`` / ``neoscore.show()`` calls in most examples.

By default, text objects are positioned by the left edge of the text baseline. Here, the given position is approximately at the left corner of the "L". Text can be horizontally and vertically aligned with the :obj:`alignment_x <.Text.alignment_x>` and :obj:`alignment_y <.Text.alignment_y>` properties (with some caveats in flowable containers).

Fonts
-----

Every text object is drawn in a :obj:`.Font`. If no font is given, the neoscore default `12-pt Lora <https://fonts.google.com/specimen/Lora>`_ is used.

:obj:`.Font`\ s specify a family name ("Lora", "Arial", etc), a size, a weight, and whether to use italics. Font sizes are specified in units, where the base :obj:`.Unit` pixel value corresponds to "points" used in other other applications. ``Unit(12)`` matches 12-point fonts used in Microsoft Word, Google Docs, and so on. Weights (boldness and lightness) are given in a number between 0 and 100, where 50 is regular and larger numbers are more bold. For fonts which do not support variable weight, the exact mapping between numeric weight and font styles varies. The default font Lora supports variable weights, with ``70`` corresponding to standard bold.

You can derive variations of fonts using :obj:`.Font.modified`, where properties can be overridden using keyword arguments. The default font can be accessed for derivation at :obj:`neoscore.default_font <neoscore.core.neoscore.default_font>`.

.. rendered-example::

   default = neoscore.default_font # Alias just for docs legibility
   sample = "The quick brown fox jumps over the lazy dog"
   Text(ORIGIN, None, sample)
   Text((ZERO, Mm(6)), None, sample, default.modified(size=Unit(14)))
   Text((ZERO, Mm(12)), None, sample, default.modified(weight=80))
   Text((ZERO, Mm(18)), None, sample, default.modified(italic=True))
   Text((ZERO, Mm(24)), None, sample, default.modified(weight=80, italic=True))

Fonts can also be created from scratch using the :obj:`.Font` constructor. You can use any font family installed in your environment just by referring to its family name. For example, if your system has Arial installed, you can write with it like so:

.. rendered-example::

   font = Font("Arial", Unit(12)) # Using default weight and italics values
   Text(ORIGIN, None, "Text in another font family", font)

If you want your document to be portable or if you want to use a font not installed on your system, you can register fonts from TrueType and OpenType files with :obj:`neoscore.register_font <neoscore.core.neoscore.register_font>`. This function returns the font family name(s) registered which you can later refer to the font with. Note that for fonts with multiple files for different styles (bold, italic, etc.) you must register each file separately before you can use their styles. ::

  >>> neoscore.register_font('path/to/Arial.ttf')
  ['Arial']

Rich Text
---------

:obj:`.Text` can only be used for fairly simple, single-line text. Long-form text with line wrapping and rich formatting is available with the :obj:`.RichText` class. Instead of taking a plain string, :obj:`.RichText` takes a string of HTML-like markup. An optional text-area width controls automatic line wrapping and text justification.

.. rendered-example::

   html = """
   <p align=justify>
     Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
     eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
     ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
     aliquip ex ea commodo consequat.
   </p>
   <p align=right>
     another paragraph aligned right
     and <span style="color: red">with inline coloring</span>!
   </p>
   """
   RichText(ORIGIN, None, html, Inch(4))


The HTML-like markup supported is documented extensively at `the upstream Qt docs <https://doc.qt.io/qt-5/richtext-html-subset.html>`_.

:obj:`.RichText` also takes a ``font`` argument which controls its default font family and style. Font styles, and even families, can be changed within the text using markup.

.. rendered-example::

   html = """
   <p align=justify>
     Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
     eiusmod tempor incididunt
     <span style="font-family: Arial">
       ut labore et dolore magna aliqua.
     </span>
     <span style="font-style: normal; font-weight: normal;">
       Ut enim ad minim veniam
     </span>
   </p>
   """
   default_font = neoscore.default_font.modified(weight=80, italic=True)
   RichText(ORIGIN, None, html, Inch(4), default_font)
