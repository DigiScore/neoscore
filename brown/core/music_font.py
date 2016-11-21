from brown.interface.font_interface import FontInterface
from brown.core.font import Font


class MusicFont(Font):

    """A SMuFL compliant music font"""

    _interface_class = FontInterface

    def __init__(self, family_name, size):
        super().__init__(family_name, size, 1, False)
        self._cached_em_size = self._calculate_approximate_em_size()


    ######## PUBLIC PROPERTIES ########

    @property
    def em_size(self):
        """GraphicUnit: The em size for the font."""
        return self._cached_em_size

    ######## PRIVATE METHODS ########

    def _calculate_approximate_em_size(self):
        """Approximate the em size in the font.

        HACK: Because Qt doesn't make it clear how to find the true em height,
              we have to compute the em height by taking the height of a simple
              notehead (1/4 em unit) and multiply it by 4.

        Returns: GraphicUnit
        """
        return self._interface.tight_bounding_rect_around('\uE0A4').height * 4
