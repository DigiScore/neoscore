from brown.models.accidental_type import AccidentalType


class VirtualKeySignature:
    """A key signature descriptor.

    This contains mappings between pitch letter names and `AccidentalType`s.
    """
    c_major = {
        'a': None,
        'b': None,
        'c': None,
        'd': None,
        'e': None,
        'f': None,
        'g': None,
    }

    a_minor = c_major

    df_major = {
        'a': AccidentalType.flat,
        'b': AccidentalType.flat,
        'c': None,
        'd': AccidentalType.flat,
        'e': AccidentalType.flat,
        'f': None,
        'g': AccidentalType.flat,
    }

    bf_minor = df_major

    # Ha
    cs_major = {
        'a': AccidentalType.sharp,
        'b': AccidentalType.sharp,
        'c': AccidentalType.sharp,
        'd': AccidentalType.sharp,
        'e': AccidentalType.sharp,
        'f': AccidentalType.sharp,
        'g': AccidentalType.sharp,
    }

    d_major = {
        'a': None,
        'b': None,
        'c': AccidentalType.sharp,
        'd': None,
        'e': None,
        'f': AccidentalType.sharp,
        'g': None,
    }

    b_minor = d_major
