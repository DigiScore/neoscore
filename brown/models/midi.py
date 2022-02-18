from typing import Optional

from brown.models.key_signature_type import KeySignatureType
from brown.models.pitch import Pitch

# TODO this takes a KeySignatureType, but that's just an enum of
# conventional signatures in dicts. We could support custom key
# signatures here if we made a new type, say KeySignatureSpec, which
# is those dicts.

# Maybe it would be better to import or implement an existing
# algorithm for pitch spelling. A quick look online suggests there are
# many.

# https://duckduckgo.com/?t=ffab&q=pitch+spelling+algorithm&ia=web


def midi_to_pitch(midi: int, key_signature: Optional[KeySignatureType] = None) -> Pitch:
    """Derive a Pitch instance from a midi pitch code.

    If a key signature is provided, this attempts to create pitches
    with spellings aligning with it.

    While MIDI codes refer to absolute pitches, `Pitch` instances
    encode additional spelling information which is subtle and often
    subjective. This method attempts to provide decent results by
    applying common spelling rules of thumb, but this will sometimes
    fail, resulting in confusing spellings.

    This algorithm applies the following spelling principles:
    1. Avoid accidentals when possible
    2. Avoid double accidentals when possible
    3. In flat keys, avoid sharps; and vice-versa in sharp keys.
    4. In conventional key signatures, spell leading tones as such
    """
    # TODO
    pass
