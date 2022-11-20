import score_draw
from random import random, choice, seed

from random import choice
from brainbit import BrainbitReader

from neoscore.core import neoscore
from neoscore.core.rich_text import RichText
from neoscore.core.text import Text
from neoscore.core.units import ZERO, Mm
from neoscore.western.staff import Staff
from neoscore.western.chordrest import Chordrest
from neoscore.western.clef import Clef
from neoscore.western.duration import Duration
from neoscore.western.barline import Barline
from neoscore.western.pedal_line import PedalLine


class Main:
    """Main thread for running this digital score.
    Args:
        headset: True for headset available. This can be used without a headset (False)"""
    def __init__(self, headset: bool = True):
        # start brainbit reading
        self.bb = BrainbitReader(headset)
        self.bb.start()

        # get all midi note lists for s a t b
        self.s, self.a, self.t, self.b = score_draw.get_midi_lists()
        self.part_list = [self.s, self.a, self.t, self.b]

        # start neoscore
        neoscore.setup()

        # build digital score UI
        self.make_UI()

        # build first bar
        self.eegdata = self.bb.read()
        self.beat_size = 20
        self.beat = 1
        self.build_bar(1)
        self.build_bar(2)

    def build_bar(self, bar):
        """Populates an entire bar of SATB with notes.
        Args:
            bar = current bar for population"""
        if bar == 1:
            start_pos = Mm(10)
            self.notes_on_staff_list_1 = []

        else:
            start_pos = Mm(100)
            self.notes_on_staff_list_2 = []

        # populate the bar on each part until full
        for i, part in enumerate(self.part_list):
            breakflag = False
            seed(self.eegdata[i])
            # one beat = 20 mm's
            note_duration_sum = 0
            while note_duration_sum < 80:
                # position in bar
                pos_x = Mm(note_duration_sum) + start_pos

                # 70% chance of note or rest
                if random() >= 0.3:
                    # get a random note from original source list,
                    neoname, raw_duration = self.get_note(part)

                    # calculate duration
                    # double length of original duration
                    raw_duration *= 2
                    if isinstance(raw_duration, float):
                        raw_duration, neoduration = self.calc_duration(raw_duration)
                    else:
                        raw_duration, neoduration = self.calc_duration(1)
                    length = raw_duration * self.beat_size

                # or its a crotchet rest
                else:
                    length = 20
                    neoduration = Duration(1, 4)
                    neoname = []

                # print note on neoscore unless over bar limit
                if note_duration_sum + length > 80:
                    # what is remaining?
                    raw_rest_gap = (80 - note_duration_sum) / 20
                    raw_duration, neoduration = self.calc_duration(raw_rest_gap)
                    neoname = []
                    breakflag = True

                # add the note/rest to the score and to the note list
                n = Chordrest(pos_x, self.staff_list[i], neoname, neoduration)
                if bar == 1:
                    self.notes_on_staff_list_1.append(n)
                else:
                    self.notes_on_staff_list_2.append(n)

                # if end of bar length: break
                if breakflag:
                    break
                else:
                    note_duration_sum += length

    def calc_duration(self, raw_duration: float) -> (float, Duration(int, int)):
        """Takes raw duration infomation from Music21 midi note/ rest
        and converts to neoscore duration.
        Args:
            raw duration: quaternote length from Music21 midi message e.g. 0.5 = quaver (1/8th note)
            """
        if raw_duration < 0.25:
            neo_duration = (1, 16)
        elif raw_duration == 0.25:
            neo_duration = (1, 16)
        elif raw_duration == 0.5:
            neo_duration = (1, 8)
        elif raw_duration == 0.75:
            neo_duration = (3, 16)
        elif raw_duration == 1:
            neo_duration = (1, 4)
        elif raw_duration == 1.5:
            neo_duration = (3, 8)
        elif raw_duration == 2:
            neo_duration = (1, 2)

        else:
            neo_duration = (1, 4)
            raw_duration = 1

        return raw_duration, Duration(neo_duration[0], neo_duration[1])

    def get_note(self, part: str) -> (str, float):
        """Random choice from passed part list e.g. 'S'.
        Args:
            part: str: current part
        Returns:
            name of note in neoscore format, duration in neoscore format
            """
        pitch, octave, duration = choice(part)
        # calc neonote (octave and name)
        if pitch[-1] == "#":
            pitch = f"{pitch[0]}s"
        elif pitch[-1] == "-":
            pitch = f"{pitch[0]}f"

        # check octave in range
        if 2 <= octave <= 6:
            if octave > 4:
                ticks = octave - 4
                for tick in range(ticks):
                    pitch += "'"
            elif octave < 4:
                if octave == 3:
                    pitch += ","
                elif octave == 2:
                    pitch += ",,"

        neoname = [pitch.lower()]
        return neoname, duration

    def make_UI(self):
        """Called at the start, this sets up the UI for the digital score."""

        annotation = """
        DEMO digital score using EEG brain wave data
        and deconstructed source music. One of the musicians wears the BrainBit
        headset. Let the score count through the beats 1-4, then start at bar 1.
        Musicians plays through the stable bar, while the other bar generates notes.
        This is indicated by a pedal line.
        Players instructions:
        Dynamics = mp   
        Time Sig = 4/4  
        Tempo = 60 BPM
        
        """
        # add text at top
        RichText((Mm(1), Mm(1)), None, annotation, width=Mm(170))
        # mfont = MusicFont("Bravura", Mm)
        self.eeg_output = Text((ZERO, Mm(170)), None, "")

        # make 4 2 bar staves
        self.s_staff = Staff((ZERO, Mm(70)), None, Mm(180))
        self.a_staff = Staff((ZERO, Mm(90)), None, Mm(180))
        self.t_staff = Staff((ZERO, Mm(110)), None, Mm(180))
        self.b_staff = Staff((ZERO, Mm(130)), None, Mm(180))
        self.staff_list = [self.s_staff, self.a_staff, self.t_staff, self.b_staff]

        # add barlines
        Barline(Mm(90), [self.s_staff, self.b_staff])
        Barline(Mm(180), [self.s_staff, self.b_staff])

        # add clefs
        s_clef = Clef(ZERO, self.s_staff, "treble")
        Clef(ZERO, self.a_staff, "treble")
        Clef(ZERO, self.t_staff, "alto")
        Clef(ZERO, self.b_staff, "bass")

        # mark conductor points
        bar1_origin = Mm(10)
        self.conductor_1_1 = Text((bar1_origin, Mm(50)), None, "1")
        self.conductor_1_2 = Text((bar1_origin + Mm(40), Mm(50)), None, "2")
        self.conductor_2_1 = Text((bar1_origin + Mm(90), Mm(50)), None, "3")
        self.conductor_2_2 = Text((bar1_origin + Mm(130), Mm(50)), None, "4")
        self.conductor_list = [self.conductor_1_1,
                               self.conductor_1_2,
                               self.conductor_2_1,
                               self.conductor_2_2
                               ]

        self.bar_indicator = PedalLine(
            (Mm(0), Mm(20)),
            self.b_staff,
            Mm(90)
        )

    def change_beat(self, beat):
        """Changes the visual beat indicator on the UI.
        Args:
            ""beat = current beat of the bar"""
        if beat > 4:
            beat -= 4
        # flatten all scales
        for b in self.conductor_list:
            b.scale = 1
        # boost the beat
        self.conductor_list[beat-1].scale = 3

    def refresh_func(self, time):
        """Updates the UI with refreshed data of notes, eeg reader,
        beat and bar."""
        # get data from brainbit
        self.eegdata = self.bb.read()
        # print(f"EEG read = {data}")
        self.eeg_output.text = f"eeg output = T2 {round(self.eegdata[0], 2)}; " \
                               f"T4 {round(self.eegdata[1], 2)}; " \
                               f"N1 {round(self.eegdata[2], 2)}; " \
                               f"N2 {round(self.eegdata[3], 2)}"

        # calc which beat and change score
        now_beat = (int(time) % 8) + 1 # 8 beats = 2 bars
        if now_beat != self.beat:
            self.change_beat(now_beat)
            self.beat = now_beat
        if now_beat == 1:
            self.bar_indicator.pos = (Mm(0), Mm(20))
            for n in self.notes_on_staff_list_2:
                n.remove()
            self.build_bar(2)
        elif now_beat == 5:
            self.bar_indicator.pos = (Mm(90), Mm(20))
            for n in self.notes_on_staff_list_1:
                n.remove()
            self.build_bar(1)
        # sleep(0.05)


if __name__ == "__main__":
    run = Main(headset=False)
    neoscore.show(run.refresh_func,
                  display_page_geometry=False)
