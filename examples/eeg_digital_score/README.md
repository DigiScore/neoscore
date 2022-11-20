# eeg_score_demo
Demo digital score using eeg brainwaves and Neoscore for live rendering

This digital score creates notes for a quartet using realtime brainwave data.

The system uses the BrainBit eeg reader to generate the brainwave stream. The script uses these to seed a note generator, which chooses notes from a pre-defined midi file. In this case a piece by Purcell.

In realtime it generates the notes for bar 1 then bar 2, so that the next bar is always waiting for the musicians.

It can be used without a headset by declaring headset=False, in which case the brainflow library is not required

# Requirements
brainflow

neoscore

music21


