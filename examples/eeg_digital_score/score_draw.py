from music21 import converter

def get_midi_lists():
    """Parses the note and rest data from a given midifile
    into separate part lists.
    Returns: s, a, t, b lists"""

    # This works for this midi file.
    # For others to work may need some adjustment in the code.

    mf = 'purcell_low.mid'
    score_in = converter.parse(mf)
    s = []
    a = []
    t = []
    b = []
    part_list = [s, a, t, b]

    for i, parts in enumerate(score_in.parts):
        print(parts)
        active_part = part_list[i]

        for msg in parts.recurse().notes:

            # if note length is not 0 then make longer and print out as individual png
            try:
                if msg.duration.quarterLength != 0:
                    # convert to neoscore
                    active_part.append((msg.pitch.name, msg.pitch.octave, msg.duration.quarterLength))
            except:
                pass

    return s, a, t, b

if __name__ == "__main__":
    s, a, t, b = get_midi_lists()
    print(s, a, t, b)
