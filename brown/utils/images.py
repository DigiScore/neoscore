from brown.utils.units import Mm, Inch

supported_formats = set(['.bmp',
                         '.jpg',
                         '.jpeg',
                         '.png',
                         '.pbm',
                         '.pgm',
                         '.ppm',
                         '.xbm',
                         '.xpm'])

_inches_per_meter = (Inch(1) / Mm(1000)).value


def dpi_to_dpm(dpi):
    """Convert a Dots Per Inch value to Dots Per Meter

    Args:
        dpi (int): A Dots Per Inch value

    Returns:
        int: A Dots Per Meter value
    """
    return dpi / _inches_per_meter
