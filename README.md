# Brown

## A WIP Graphic Music Notation API

![Screenshot](/screenshots/brown_screenshot.jpg)

Brown is a (WIP) Python API that provides an easy-to-use interface for working with high-level vector graphics in Python, with an emphasis on providing powerful primitives and abstractions for creating music scores which use unconventional notation. It emphasizes easy extensibility, transparent architecture, and striking a balance between convenience and deep customizability.

It uses Python and provides a convenient interface to its Qt backend through a simple yet expressive layer of abstractions, with the hope that its users will never have to make a direct Qt call or worry about the underlying render logic.

At the time of writing, most of the fundamental groundwork is in place, and rapid development is underway on the core music-notation logic and primitives. Users may define staves and place logical musical information in structures which automatically calculate their traditional engraving representations as paths and musical glyphs.

Upcoming developments on the roadmap include:

* Implementing a higher level logical system which allows users to specify musical passages by their semantic content rather than their simple graphical representation. Currently for a user to populate a staff with notes they must pass explicit descriptions of locations for chords and spanners - soon they will be able to specify contents by durations and pitches, grouped into object-oriented abstractions like Measures.
* Implementing layout algorithms for conventionally notated passages
* Increasing consistency across the API (as it stands, many similar functions or classes take the same arguments in different orders)
* Implementing PDF / svg export of scores
* Implementing a more robust score preview mode, possible with interactive visual inspection of elements.

This project is in an extremely early stage, and should be
considered nothing but a publicly visible development journal
at this point.

### Getting Started

All of the dependencies for `brown` can be installed with pip except for the graphics engine - Qt5, which needs to be set up separately. Visit [this page](https://www.qt.io/download-open-source/) for instructions to install Qt5.

For the rest, you just need a working [Python >= 3.5 installation](https://www.python.org/downloads/).

From there, you can clone this repository and get the rest of the dependencies from `pip`, and install the local `brown` package:

```sh
$ git clone git@github.com:ajyoon/brown.git
$ cd brown
$ pip install -r requirements.txt
$ pip install -r tests/test_requirements.txt
$ pip install -e ./
```

If everything goes right, you should be able to run the test suite (>330 tests and counting!) with:

```sh
$ pytest
```



And you can run the visual test to see some of the API actually in action with:

```sh
$ python vtests/vtest.py
```

Stay tuned for more!
