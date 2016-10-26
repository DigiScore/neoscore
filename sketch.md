## Goal
* Draw a chord with 3 notes on a staff on the first line
  of a page of music with a treble clef and an accidental and stem.

## Required components

## hidden land~~~

### interface
Interface layer between backend graphics (QT) and main application.
Divided into two subpackages - `abstract` and `impl` where classes
in `abstract` are abstract classes that declare and specify the API,
and those in `impl` are back-end (QT) specific implementations of the
API. It should be extremely rare that users ever interact with this
interface - `core` acts as the closest point of contact between users
and the graphics implementation details.
* AppInterface
* FontInterface
* GrobInterface
* LineInterface
* TextObjectInterface

## user land~~~~~

### core
Fundamental objects. Nothing in this layer is specific to music -
this layer is essentially the components of a basic multi-page vector
graphics program
* brown (module-level application manager - global state lives here)
* Document
* FlowableObject
* Flowable
* Font
* Glyph
* TextObject
* Page
* Path
* ObjectGroup

### primitives
Musical primitives - the basic constructs needed to make simple scores
* Notehead
* Chordrest
* Staff
* Staff Object

### models
Object models with domain-specific logic. These will contain lots of
convenient music-specific abstractions and methods, and will typically
be composed into `primitives` rather than manipulated manually
* Pitch
* Clef
* Transposition
* Accidental
* Duration
* Position

### Utils
Various utilities
* Units

## Reminders
* Common functionality for interface to QGraphicsItem needs to be pulled out
  into a generic shared GraphicsItemInterface class

## Things to care about during this phase
* _getting it done_  ---- the most important thing by far right now
* Keeping the graphics backend strictly decoupled from the rest of the code
* Primitive objects do not call the interface ever
* Utils are mostly atomic
* Object models are mostly atomic



## Things not to care about right now
* Mutable components (don't worry about updating state -
  assume everything is created at once by API with a script for something)
* GUI - at all!
* Model details
* Fancy things
* Details in general
* Type safety and good property hiding
