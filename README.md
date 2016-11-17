# Brown

## A (very early) WIP Graphic Music Notation API

Brown is a (WIP) Python API that provides an easy-to-use interface for working with high-level vector graphics in Python, with an emphasis on provide powerful primitives and abstractions for creating music scores which use unconventional notation. It emphasizes easy extensibility, transparent architecture, and striking a balance between convenience and deep customizability.

It uses Python and provides a convenient interface to its Qt backend through a simple yet expressive layer of abstractions, with the hope that its users will never have to make a direct Qt call or worry about the underlying interface logic.

At the time of writing, most of the fundamental groundwork is in place, and rapid development is underway on the core music-notation logic and primitives. Users may define staves and place logical musical information in structures which automatically calculate their traditional engraving representations as paths and musical glyphs. As of this writing, the current priority is implementing a robust flowable coordinate system to allow automatic flowing of systems across lines and pages.

This project is in an extremely early stage, and should be
considered nothing but a publicly visible development journal
at this point.

### Getting Started

All of the dependencies for `brown` can be installed with pip except for the graphics engine - Qt5, which needs to be set up separately. Visit [this page](https://www.qt.io/download-open-source/) for instructions to install Qt5.

For the rest, you just need a working [Python 3.5 installation](https://www.python.org/downloads/).

From there, you can clone this repository and get the rest of the dependencies from `pip`:

```sh
$ git clone git@github.com:ajyoon/brown.git
$ cd brown
$ pip install -r requirements.txt
$ pip install -r tests/test_requirements.txt
```

If everything goes right, you should be able to run the test suite (>200 tests and counting!) with:

```sh
$ pytest
```

Everything should go green, except for some currently expected errors in `test_app_interface`.

And you can run the visual test to see some of the API actually in action with:

```sh
$ python vtest.py
```

Stay tuned for more!
