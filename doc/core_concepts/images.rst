Images
======

External images can be embedded in your document with the :obj:`.Image` class.

.. rendered-example::

   import pathlib
   # Just a black rectangle here, but this can be anything.
   # These paths are relative to the docs build dir, if you want to try this out
   # yourself you'll need to provide your own images
   file_path = pathlib.Path("..") / "tests" / "resources" / "pixmap_image.png"
   Image(ORIGIN, None, file_path)

Neoscore can import most common bitmap image types, in addition to vector-graphics SVG images which can scale without artifacts.

.. rendered-example::

   import pathlib
   file_path = pathlib.Path("..") / "tests" / "resources" / "svg_image.svg"
   Image(ORIGIN, None, file_path, scale=1.2)
