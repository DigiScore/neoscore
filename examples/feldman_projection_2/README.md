# Feldman's Grid Notation

This is an involved example score demonstrating how you can build sophisticated managed notation systems on top of neoscore. In this example, we implement Morton Feldman's grid notation system and engrave the first page and a half of his piece, _Projection 2_.

To run the score, run `main.py`.

![Preview of Feldman's Projection 2 as built with neoscore](/gallery/feldman_projection_2.png)

Note that this piece is (c) Edition Peters 1951, used here under fair use. The project's open source license does not extend to the musical contents of the piece.

## Limitations

This is far from a complete implementation of Feldman's notation. Most notably:

- Instrument names are not currently supported, although they should be fairly straightforward along the lines of [`InstrumentName`](https://neoscore.org/api/neoscore.western.instrument_name.html?highlight=instrumentname#neoscore.western.instrument_name.InstrumentName).
- Barlines do not display correctly in some (literal) edge cases. The current implementation draws barlines as simple 0-width paths; when these land on line/page breaks, they run into some problems. This is clearly visible in the above render preview, where a floating barline segment appears in the bottom right corner. A more robust implementation would likely involve a dedicated class which uses [flowable render hooks](https://neoscore.org/extending/extending_neoscore#rendering) combined with contextual information (does this instrument-segment of the barline land at the start, middle, or end of the instrument's block?) to decide on which sides of line/page breaks to draw which instrument-segments.
