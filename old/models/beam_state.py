#!/usr/bin/env python


class BeamState:
    """
    A container of legal beaming states for NoteColumn objects.

    Essentially a flag which validates itself
    """
    legal_states = ['NO_BEAM', 'BEAM_RIGHT', 'BEAM_LEFT', 'BEAM-THROUGH']

    def __init__(self, state='NO_BEAM'):
        if state not in self.legal_states:
            raise ValueError("BeamState.state of %s is invalid. Legal values are: "
                             "['NO_BEAM', 'BEAM_RIGHT', 'BEAM_LEFT', 'BEAM-THROUGH']" % state)
        self.state = state
