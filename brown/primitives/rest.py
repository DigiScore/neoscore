from brown.core.music_glyph import MusicGlyph
from brown.models.duration import Duration
from brown.utils.point import Point
from brown.utils.units import Unit


class Rest(MusicGlyph):

    """A simple Rest glyph whose appearance is determined by a Duration

    Currently, the following rest types are not supported:
        * restHalfLegerLine
        * restWholeLegerLine
        * restLonga
        * restMaxima
    """

    _glyphnames = {
        1024: 'rest1024th',
        512: 'rest512th',
        256: 'rest256th',
        128: 'rest128th',
        64: 'rest64th',
        32: 'rest32nd',
        16: 'rest16th',
        8: 'rest8th',
        4: 'restQuarter',
        2: 'restHalf',
        1: 'restWhole',
    }

    def __init__(self, pos_x, duration, parent):
        """
        Args:
            pos_x (StaffUnit):
            staff (Staff):
            duration (Duration or tuple(Duration args)):
        """
        self._duration = Duration(duration)
        super().__init__(Point(pos_x, Unit(0)),
                         self._glyphnames[self.duration.base_division],
                         parent=parent)
        # Currently use a fixed vertical position for rests
        self.pos.y = self.staff.unit(2)

    ######## PUBLIC PROPERTIES ########

    @property
    def duration(self):
        """Duration: The time duration of this Rest"""
        return self._duration
