# brown.interface.qt_ext

### Custom Qt subclass extensions

This package contains subclasses of Qt classes which extend their behavior to allow things like clipping text and paths. For most cases, the vast library of primitives provided by Qt (and, by extension, PyQt5) is enough to provide the functionality required by `brown`. Modules should only be added here when deemed absolutely necessary, as they are much harder to test.