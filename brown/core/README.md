# brown.core

### The most fundamental building blocks of brown

This package contains most of the classes central to `brown`, including basic graphic primitives (`Path`, `Text`, etc), document layout primitives, and SMuFL music font binding logic.

Note that the contents of this package are relatively low level. Many classes are mixins or abstract classes meant to be combined with other classes to give different types of functionality. While everything here is considered public API, you may often find what you're trying to do can be done much more easily with a class from the `primitives` package.
