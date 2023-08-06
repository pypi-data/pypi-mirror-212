from .struct import Interval, Scale, Chord


NOTE_NAMES = ["A", "A#", "B", "C", "C#",
              "D", "D#", "E", "F", "F#", "G", "G#"]
ALL_NOTE_NAMES = [name
                  for _ in range(7)
                  for name in NOTE_NAMES] + NOTE_NAMES[:4]


def interval(root, interval_type: Interval):
    return [root, root + interval_type.value]


def scale(root, scale_type: Scale):
    return [root := root + interval for interval in scale_type.value]


def chord(root, chord_type: Chord):
    return [root := root + interval for interval in chord_type.value]


def invert_up(notes):
    return notes[1:] + [notes[0] + 12]


def invert_down(notes):
    return [notes[-1] - 12] + notes[:-1]


def octave_up(notes):
    return [note + 12 for note in notes]


def octave_down(notes):
    return [note - 12 for note in notes]


def int_to_note(note: int):
    return ALL_NOTE_NAMES[note]


def ints_to_notes(notes):
    return [ALL_NOTE_NAMES[note] for note in notes]


def ints_to_chord(notes):
    intervals  = [0] + [notes[i + 1] - note for i, note in enumerate(notes) if i + 1 < len(notes)]
    try:
        return Chord(tuple(intervals))
    except ValueError:
        return None


def ints_to_scale(notes):
    intervals  = [0] + [notes[i + 1] - note for i, note in enumerate(notes) if i + 1 < len(notes)]
    try:
        return Scale(tuple(intervals))
    except ValueError:
        return None


def ints_to_interval(notes):
    try:
        return Interval(max(notes) - min(notes))
    except ValueError:
        return None


def note_to_int(note: str, octave:int = 0):
    return NOTE_NAMES.index(note) + (12 * octave)


def notes_to_ints(chord, octave:int = 0):
    names = ALL_NOTE_NAMES[octave * 12:]
    root = names.index(chord[0])
    names = names[root:]
    return [names.index(note) + (12 * octave) + root for note in chord]
