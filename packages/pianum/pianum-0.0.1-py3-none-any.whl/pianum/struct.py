from enum import Enum


class Interval(Enum):
    Unison = 0
    m2 = 1
    M2 = 2
    m3 = 3
    M3 = 4
    P4 = 5
    Tritone = 6
    P5 = 7
    m6 = 8
    M6 = 9
    m7 = 10
    M7 = 11
    Octave = 12


class Scale(Enum):
    Major = (0, 2, 2, 1, 2, 2, 2)
    Minor = (0, 2, 1, 2, 2, 1, 2)
    PentatonicMajor = (0, 2, 2, 3, 2)
    PentatonicMinor = (0, 3, 2, 2, 3)
    HarmonicMajor = (0, 2, 2, 1, 2, 1, 3)
    HarmonicMinor = (0, 2, 1, 2, 2, 1, 3)
    WholeTone = (0, 2, 2, 2, 2, 2)


class Chord(Enum):
    Major = (0, 4, 3)
    Minor = (0, 3, 4)
    Diminished = (0, 3, 3)
    Augmented = (0, 4, 4)
    Sus2 = (0, 2, 5)
    Sus4 = (0, 5, 2)
    Major7 = (0, 4, 3, 4)
    Minor7 = (0, 3, 4, 3)
    Diminished7 = (0, 3, 3, 3)
    HalfDiminished = (0, 3, 3, 4)
    Dominant = (0, 4, 3, 3)
