from PyQt5.QtGui import QPainterPath, QTransform

from neoscore.interface.qt import hashing


def test_hash_path():
    path_1 = QPainterPath()
    path_1.lineTo(100, 200)
    hash_1 = hashing.hash_path(path_1)
    # Identical paths hash identically
    path_2 = QPainterPath()
    path_2.lineTo(100, 200)
    hash_2 = hashing.hash_path(path_2)
    assert hash_1 == hash_2
    # Paths with different fill rules hash differently
    path_3 = QPainterPath()
    path_3.setFillRule(1)  # WindingFill
    path_3.lineTo(100, 200)
    hash_3 = hashing.hash_path(path_3)
    assert hash_1 != hash_3
    # Paths with different elements hash differently
    path_4 = QPainterPath()
    path_4.lineTo(100, 200)
    path_4.lineTo(123, 123)
    hash_4 = hashing.hash_path(path_4)
    assert hash_4 != hash_1


def test_hash_transform():
    transform_1 = QTransform()
    hash_1 = hashing.hash_transform(transform_1)
    assert hash_1 == hashing.hash_transform(QTransform())
    transform_2 = QTransform()
    transform_2.scale(0.1, 0.1)
    hash_2 = hashing.hash_transform(transform_2)
    transform_3 = QTransform()
    transform_3.rotate(20)
    hash_3 = hashing.hash_transform(transform_3)
    transform_4 = QTransform()
    transform_4.translate(1, 2)
    hash_4 = hashing.hash_transform(transform_4)
    assert len({hash_1, hash_2, hash_3, hash_4}) == 4


def test_hash_transformed_path():
    path = QPainterPath()
    path.lineTo(100, 200)
    transform_1 = QTransform()
    hash_1 = hashing.hash_transformed_path(path, transform_1)
    transform_2 = QTransform()
    transform_2.scale(0.1, 0.1)
    hash_2 = hashing.hash_transformed_path(path, transform_2)
    assert hash_1 != hash_2
