from PyQt5.Qt import Qt
from PyQt5.QtGui import QBitmap, QRegion

from brown.utils.units import Mm, Inch

supported_formats = {'.bmp', '.jpg', '.jpeg', '.png',
                     '.pbm', '.pgm', '.ppm', '.xbm', '.xpm'}

_inches_per_meter = (Inch(1) / Mm(1000)).value


def dpi_to_dpm(dpi):
    """Convert a Dots Per Inch value to Dots Per Meter

    Args:
        dpi (int): A Dots Per Inch value

    Returns:
        int: A Dots Per Meter value
    """
    return dpi / _inches_per_meter


def autocrop(q_image, q_color):
    """Automatically crop a qt image around the pixels not of a given color.

    Args:
        q_image (QImage):
        q_color (QColor):

    Returns:
        QImage: A newly cropped Qt image. The passed-in image is left
            unmodified.
    """

    mask = q_image.createMaskFromColor(q_color.rgb(),
                                       Qt.MaskInColor)
    crop_rect = QRegion(QBitmap.fromImage(mask)).boundingRect()
    return q_image.copy(crop_rect)

