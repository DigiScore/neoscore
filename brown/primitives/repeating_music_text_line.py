from brown.core.music_text_object import MusicTextObject
from brown.primitives.spanner import Spanner
from brown.utils.point import Point
from brown.utils.anchored_point import AnchoredPoint


class RepeatingMusicTextLine(MusicTextObject, Spanner):

    """A spanner of repeating music text over its length.

    Currently only perfectly horizontal spanners are supported.
    Additionally, the stop position should be to the right of the start.

    TODO: Implement text spanners that are not perfectly horizontal.
    TODO: Support stop.x < start.x
    """

    def __init__(self, start, stop, text, font=None, scale_factor=1):
        """
        Args:
            start (AnchoredPoint or tuple init args):
            stop (AnchoredPoint or tuple init args):
            text (str, tuple, MusicChar, or list of these):
                The text to be repeated over the spanner,
                represented as a str (glyph name), tuple
                (glyph name, alternate number), MusicChar, or a list of them.
            font (MusicFont): The music font to be used. If not specified,
                the font is taken from the ancestor staff.
            scale_factor (float): A hard scaling factor to be applied
                in addition to the size of the music font.
        """
        start = (start if isinstance(start, AnchoredPoint)
                 else AnchoredPoint(*start))
        stop = (stop if isinstance(stop, AnchoredPoint)
                else AnchoredPoint(*stop))
        # init the MusicTextObject to ask it how wide a single
        # repetition of `text` is in order to calculate how many
        # repetitions are needed to cover the spanner.
        MusicTextObject.__init__(self,
                                 (start.x, start.y, start.page),
                                 text,
                                 start.parent,
                                 font,
                                 scale_factor)
        Spanner.__init__(self, Point(stop.x, stop.y, stop.page), stop.parent)
        self.repeating_music_chars = self.music_chars
        self.repeating_text = self.text
        repetitions = self._repetitions_needed
        self.music_chars = self.music_chars * repetitions
        self._text = self.text * repetitions

    ######## PRIVATE PROPERTIES ########

    @property
    def _repetitions_needed(self):
        """int: The number of text repetitions needed to cover the line.

        This value rounds down, such that the real length of the drawn
        text will always be <= self.length.
        """
        base_width = self.font.text_bounding_rect(
            self.repeating_music_chars,
            self._origin_offset,
            self.scale_factor).width
        return int((self.length / base_width).value)
