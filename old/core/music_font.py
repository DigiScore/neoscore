#!/usr/bin/env python


# TODO: Move usages of this class into a more global space so that anonymous instances of it don't need to be made all the time
class MusicFont:
    """
    A container for variables relating to music fonts
    """
    def __init__(self, name):
        """

        Args:
            name (str): Name of the music font (ie. Gonville, Emmentaler, etc.)

        """
        if not isinstance(name, str):
            raise TypeError('MusicFont.name must be a str')
        # The name of the music font
        self.name = name
        # Offsets in staff units which are applied to all instances of this MusicFont
        self.x_offset = None
        self.y_offset = None
        self.registered_font_name = None
        if self.name == 'Gonville':
            self.x_offset = 0
            self.y_offset = -0.25
            self.registered_font_name = 'Gonville-11'
        else:
            raise ValueError('MusicFont.name of %s is not recognized' % name)
