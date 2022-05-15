"""Custom hash functions for Qt objects.

These hash functions are mostly needed so Qt objects (or other classes including them)
can be hashed and used in cache dicts.
"""

from PyQt5.QtGui import QPainterPath, QTransform


def hash_transformed_path(path: QPainterPath, transform: QTransform) -> int:
    path_hash = hash_path(path)
    transform_hash = hash_transform(transform)
    return path_hash ^ transform_hash


# For some reason QTransform's qHash method seems to be omitted from PyQt5, so
# we implement our own based on the fields used in Qt's implementation here:
# github.com/qt/qtbase/blob/e05e3c776/src/gui/painting/qtransform.cpp#L778-L791
def hash_transform(t: QTransform) -> int:
    return hash(
        (
            t.m11(),
            t.m12(),
            t.m21(),
            t.m22(),
            t.dx(),
            t.dy(),
            t.m13(),
            t.m23(),
            t.m33(),
        )
    )


def hash_path(path: QPainterPath) -> int:
    h = 35891237 ^ path.fillRule()
    for i in range(path.elementCount()):
        el = path.elementAt(i)
        h ^= hash((el.type, el.x, el.y))
    return h
