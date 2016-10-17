Graphic Interface Layer
=================================================




Fundamental
=================================================

* Units
* Fraction --> Support arbitrary compound fractions
* Document
* Page
* Flow
* Point
* Path
* GraphicObject(ABC.Meta?) --> Anything that has a draw() function
* PathObject(GraphicObject)
* TextObject(GraphicObject)
* 
* Bitmap(GraphicObject)
* ObjectGroup(GraphicObject)


Lib
==============================================
* Pitch
* RhythmicValue
* StaffSystem(ObjectGroup)
* Staff(PathObject)
* KeySignature(ObjectGroup)
* TimeSignature(TextObject)
* Clef(GlyphObject)
* Accidental(TextObject)
* Notehead(TextObject)
* Rest(TextObject)
* Flag(TextObject)
* Beam(PathObject)
* BeamGroup(ObjectGroup)
* RhythmDot(TextObject)
* Stem(PathObject)
* ChordRest(ObjectGroup)
* Spanner(GraphicObject)
* Hairpin(Spanner)
* OctaveLine(Spanner)
* ExpressionText(TextObject)
* PlainText(TextObject)
* LyricText(TextObject)
* 


