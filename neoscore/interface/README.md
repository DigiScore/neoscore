# neoscore.interface

### interfaces to the Qt backend graphics engine

This subpackage contains abstractions over the Qt graphics engine. Using these interface objects, hopefully users will never have to worry about low-level Qt logic.

Its various classes are meant to be created and managed by `neoscore.core` classes, and should typically not be called directly by user-land code.

The common pattern used by `interface` classes is that they have a `_qt_object` attribute which refers to a PyQt5 object. In many cases, their API closely reflects those of their counterparts in the `core` subpackage, while providing lower-level implementation details and API binding concerns (see `Path` vs `PathInterface`).
