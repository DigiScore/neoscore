# Brown

## A WIP Graphic Music Notation API

![Screenshot](/screenshots/brown_screenshot.jpg)

[![Build Status](https://travis-ci.org/ajyoon/brown.svg?branch=master)](https://travis-ci.org/ajyoon/brown)


Brown is a (WIP) Python API that provides an easy-to-use interface for working with high-level vector graphics in Python, with an emphasis on providing powerful primitives and abstractions for creating music scores which use unconventional notation. It emphasizes easy extensibility, transparent architecture, and striking a balance between convenience and deep customizability.

It uses Python and provides a convenient interface to its Qt backend through a simple yet expressive layer of abstractions, with the hope that its users will never have to make a direct Qt call or worry about the underlying render logic.

At the time of writing, most of the fundamental groundwork is in place, and rapid development is underway on the core music-notation logic and primitives. Users may define staves and place logical musical information in structures which automatically calculate their traditional engraving representations as paths and musical glyphs.

Upcoming developments on the roadmap include:

* Implementing a higher level logical system which allows users to specify musical passages by their semantic content rather than their simple graphical representation. Currently for a user to populate a staff with notes they must pass explicit descriptions of locations for chords and spanners - soon they will be able to specify contents by durations and pitches, grouped into object-oriented abstractions like Measures.
* Implementing layout algorithms for conventionally notated passages
* Increasing consistency across the API (as it stands, many similar functions or classes take the same arguments in different orders)
* Implementing a more robust score preview mode, possible with interactive visual inspection of elements.

This project is in an extremely early stage, and should be
considered nothing but a publicly visible development journal
at this point.

### Getting Started

With a working [Python >= 3.5 installation](https://www.python.org/downloads/), all of the dependencies should be obtainable with `pip`. Begin by cloning (or downloading and extracting [here](https://github.com/ajyoon/brown/archive/master.zip)) the repository:

```sh
$ git clone git@github.com:ajyoon/brown.git
```

`cd` into the package and install its dependencies with pip (depending on your system configuration, you may need to use `pip3` instead):

```sh
# Enter the repository root directory
$ cd brown

# Install dependencies
$ pip install -r requirements.txt
$ pip install -r tests/test_requirements.txt

# Install the package itself
$ pip install -e ./
```

If everything goes right, you should be able to run the test suite (>370 tests and counting!) with:

```sh
$ pytest
```

Let's say hello:
```python
from brown.common import *

brown.setup()

flowable = Flowable((Mm(0), Mm(0)), Mm(2000), Mm(30))
staff = Staff((Mm(0), Mm(0)), Mm(2000), flowable)
clef = Clef(staff, Mm(0), 'bass_8vb')
text = Text((Mm(3), staff.unit(-1)), 'Hello, world!')

brown.show()
```

Run this with `python` and you should see something like:

![Hello world screenshot](/screenshots/readme_hello_world.png)

And you can run the visual test / development sandbox to see a lot more
of the API in action with:

```sh
$ python vtests/vtest.py
```

### documentation

The documentation (also a work in progress) is hosted [here](https://brown-notation.github.io/).

Stay tuned for more!
