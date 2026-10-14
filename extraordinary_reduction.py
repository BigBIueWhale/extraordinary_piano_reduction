#!/usr/bin/env python3
"""
First-Principles Musical & Mathematical Reduction ("PNG -> SVG") of:
  "A Mortal's Journey — Extraordinary (不凡)"
  Ru's Piano Cover (Han Li's Nascent Soul Breakthrough Version)
  Source Video: https://youtu.be/JB31Aq_5Slw
  Transcribed & synthesized with Gemini 4 Argon high in Antigravity CLI.

Design Philosophy: Pure First Principles
========================================
A true mathematical reduction ("PNG -> SVG") does not reverse-engineer or
hard-code floating-point timing arrays or per-note velocities from a recording.
Instead, it constructs the music from first principles of music theory,
compositional form, and piano performance:

  1. Tonal & Modal Basis:
     - Key: C Natural Minor {C, D, Eb, F, G, Ab, Bb}
     - Modal Inflections:
       * C Dorian (A natural) on the signature IV major chord (F / F/C)
       * G Dominant (Gm / G5) at the climax turnaround
       * C Minor Pentatonic {C, Eb, F, G, Bb} for Gufeng (古風) cascades

  2. Pure Rhythmic Algebra (Standard "1 e & a" 4/4 Meter):
     - Note Durations:
         W  = 16  (Whole)          DH = 12  (Dotted Half)   H  = 8  (Half)
         DQ = 6   (Dotted Quarter) Q  = 4   (Quarter)       DE = 3  (Dotted Eighth)
         E  = 2   (Eighth)         S  = 1   (Sixteenth)     T  = 0.5 (Thirty-second)
     - Measure Positions ("1 e & a 2 e & a 3 e & a 4 e & a"):
         B1 = 0,  B1_E = 1,  B1_AND = 2,  B1_A = 3
         B2 = 4,  B2_E = 5,  B2_AND = 6,  B2_A = 7
         B3 = 8,  B3_E = 9,  B3_AND = 10, B3_A = 11
         B4 = 12, B4_E = 13, B4_AND = 14, B4_A = 15
       Notice that the signature 3+3+2 tresillo falls naturally on
       (B1, B1_A, B2_AND) and (B3, B3_A, B4_AND).

  3. Compositional Functors & Section Generators:
     The 116-measure piece is a composition of modular section generators
     built from 6 left-hand accompaniment functors and 5 right-hand voicing
     operators (`N`, `Oct`, `SixthOct`, `FourthOct`, `Roll`).

  4. Virtual Pianist & 96 kHz Physical/Acoustic Mastering Pipeline:
     - Single canonical mode of operation with strict defensive assertions and
       zero fallbacks.
     - Time is integrated from section tempo markings (BPM), phrase-arch agogic
       breathing, and cadence ritardandos — zero hard-coded audio timestamps.
     - Dynamics are derived from musical markings (pp, p, mp, mf, f, ff),
       metric hierarchy, soprano top-voice projection, hand balance, and
       natural bottom-to-top chord voicing micro-spread.
     - Audio is rendered via dual 96 kHz 32-bit float FluidSynth engines
       (uncompressed MuseScore_General.sf2 + FluidR3_GM.sf2), processed in
       64-bit IEEE float through a 24-mode C-minor sympathetic string resonance
       bank, 5-stage zero-phase RBJ biquad mastering EQ, and a physically
       modeled 2.8-second True-Stereo Concert Hall Impulse Response (FFT
       convolution), then polyphase-resampled to 48 kHz LAME V0 MP3.
"""

from dataclasses import dataclass, field
import os
import subprocess
import tempfile
from typing import List, Tuple
import numpy as np
from PIL import Image
import pretty_midi
from scipy import signal
import soundfile as sf


# =============================================================================
# 1. RHYTHMIC ALGEBRA & TONAL BASIS
# =============================================================================

# Exact musical note durations (in 16th-note units)
W  = 16   # Whole note (4 beats)
DH = 12   # Dotted half note (3 beats)
H  = 8    # Half note (2 beats)
DQ = 6    # Dotted quarter note (1.5 beats)
Q  = 4    # Quarter note (1 beat)
DE = 3    # Dotted eighth note (3/4 beat — tresillo 3+3+2 unit)
E  = 2    # Eighth note (1/2 beat)
S  = 1    # Sixteenth note (1/4 beat)
T  = 0.5  # Thirty-second note (1/8 beat — ornamental cascades)

# Standard "1 e & a" 16th-note positions within a 4/4 measure
B1, B1_E, B1_AND, B1_A = 0,  1,  2,  3
B2, B2_E, B2_AND, B2_A = 4,  5,  6,  7
B3, B3_E, B3_AND, B3_A = 8,  9,  10, 11
B4, B4_E, B4_AND, B4_A = 12, 13, 14, 15

EIGHTH_STEPS = (B1, B1_AND, B2, B2_AND, B3, B3_AND, B4, B4_AND)

PITCH_CLASSES = {
    "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
    "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
    "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11,
}
FLAT_SPELLINGS = ("C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B")

# C Minor Pentatonic pitch classes {C, Eb, F, G, Bb}
C_MINOR_PENTATONIC = (0, 3, 5, 7, 10)

# Musical dynamic markings -> base MIDI velocity
DYNAMICS = {
    "pp": 50,
    "p":  58,
    "mp": 66,
    "mf": 74,
    "f":  82,
    "ff": 90,
}


def pitch(name: str) -> int:
    """Convert scientific pitch name (e.g. 'Eb5', 'Ab1') to MIDI note number."""
    if len(name) >= 3 and name[1] in ("b", "#"):
        pc, octv = name[:2], int(name[2:])
    else:
        pc, octv = name[:1], int(name[1:])
    return (octv + 1) * 12 + PITCH_CLASSES[pc]


def note_name(midi_num: int) -> str:
    """Convert MIDI note number to C-minor flat-spelled pitch name."""
    return f"{FLAT_SPELLINGS[midi_num % 12]}{midi_num // 12 - 1}"


# =============================================================================
# 2. VOICING OPERATORS & ORNAMENTAL GENERATORS
# =============================================================================

def N(*names: str) -> List[int]:
    """Single note or explicit chord voicing from scientific pitch names."""
    return sorted(pitch(n) for n in names)


def Oct(top_name: str) -> List[int]:
    """Octave doubling operator: [p - 12, p]."""
    p = pitch(top_name)
    return [p - 12, p]


def SixthOct(top_name: str) -> List[int]:
    """
    Signature anime-piano 3-note sixth+octave voicing [p - 12, diatonic_6th, p]
    in C minor:
      - Eb6 -> [Eb5, C6, Eb6]  (Cm 1st inversion)
      - F6  -> [F5,  D6, F6]   (Bb major 3rd+5th)
      - G6  -> [G5,  Eb6, G6]  (Cm root+3rd)
      - Bb6 -> [Bb5, G6, Bb6]  (Eb major 3rd+5th)
    """
    p = pitch(top_name)
    pc = p % 12
    interval_below = 3 if pc in (3, 5, 10) else 4
    return [p - 12, p - interval_below, p]


def FourthOct(top_name: str) -> List[int]:
    """Perfect-fourth upper dyad [p - 5, p] (e.g. F6 -> [C6, F6], Eb6 -> [Bb5, Eb6])."""
    p = pitch(top_name)
    return [p - 5, p]


# Canonical right-hand block chords
CHORDS = {
    "Cm":      N("G4", "C5", "Eb5", "G5"),
    "Bb_sus":  N("F4", "Bb4", "D5", "F5"),
    "Ab":      N("Eb4", "Ab4", "C5", "Eb5"),
    "Eb_high": N("Bb4", "Eb5", "G5", "Bb5"),
    "F_dor":   N("C4", "F4", "A4", "C5"),
    "Ab_low":  N("Eb4", "Ab4", "C5"),
}


@dataclass
class Event:
    step: float
    duration: float
    pitches: List[int]
    rolled: bool = False


def E_seq(pairs: List[Tuple[float, float, List[int]]]) -> List[Event]:
    """Convert (step, duration, pitches) tuples into symbolic Event objects."""
    return [Event(s, d, p, False) for s, d, p in pairs]


def Roll(step: float, duration: float, pitches: List[int]) -> Event:
    """Lyrical upward-rolled chord event."""
    return Event(step, duration, pitches, rolled=True)


def pentatonic_cascade(start_name: str, end_name: str, start_step: float, rate: float = T) -> List[Event]:
    """
    Generate a C-minor pentatonic waterfall (ascending or descending)
    between start_name and end_name at uniform subdivision `rate`.
    """
    p_start, p_end = pitch(start_name), pitch(end_name)
    direction = 1 if p_end >= p_start else -1
    pitches = [
        p for p in range(p_start, p_end + direction, direction)
        if (p % 12) in C_MINOR_PENTATONIC
    ]
    return [
        Event(start_step + i * rate, rate * 1.5, [p])
        for i, p in enumerate(pitches)
    ]


@dataclass
class Measure:
    bar_num: int
    section: str
    chord_symbol: str
    roman: str
    bpm: int
    dynamic: str
    lh: List[Event] = field(default_factory=list)
    rh: List[Event] = field(default_factory=list)
    pedal_steps: List[float] = field(default_factory=lambda: [B1])


# =============================================================================
# 3. LEFT-HAND ACCOMPANIMENT FUNCTORS
# =============================================================================

def lh_verse_pedal(harmony: str) -> List[Event]:
    """
    Verse 1 & Verse 2 tonic-pedal accompaniment over C2+C3:
      - 'Cm'        : C2+C3 on Beat 1, G3 on Beat 3
      - 'Bb/C'      : C2+C3+F3+Bb3 on Beat 1, F3+Bb3 on Beat 3
      - 'Ab/C'      : C2+Eb3+Ab3 on Beat 1, Eb3+Ab3 on Beat 3, Eb3+Bb3 pickup
      - 'Bb_cadence': Ab3 suspension on Beat 1 -> Bb2+F3+Bb3 on Beat 3
      - 'F/C'       : C2+C3 on Beat 1, Dorian countermelody A3 - F3 - A3 on Beats 3-4
    """
    if harmony == "Cm":
        return E_seq([(B1, H, N("C2", "C3")), (B3, H, N("G3"))])
    if harmony == "Bb/C":
        return E_seq([(B1, H, N("C2", "C3", "F3", "Bb3")), (B3, H, N("F3", "Bb3"))])
    if harmony == "Ab/C":
        return E_seq([
            (B1, H, N("C2", "Eb3", "Ab3")),
            (B3, DQ, N("Eb3", "Ab3")),
            (B4_AND, E, N("Eb3", "Bb3")),
        ])
    if harmony == "Bb_cadence":
        return E_seq([(B1, H, N("Ab3")), (B3, H, N("Bb2", "F3", "Bb3"))])
    if harmony == "F/C":
        return E_seq([
            (B1, W, N("C2", "C3")),
            (B3, E, N("A3")),
            (B3_AND, E, N("F3")),
            (B4, Q, N("A3")),
        ])
    raise ValueError(f"Unknown verse harmony: {harmony}")


def lh_prechorus_groove(harmony: str) -> List[Event]:
    """
    Pre-Chorus driving eighth-note tonic-pedal groove over C2+C3 (Bars 25-31):
    Pulses on all 8 eighth-note steps with backbeat inner-chord accents.
    """
    if harmony == "Cm":
        return E_seq([
            (B1, E, N("C2", "C3")), (B1_AND, E, N("G2")),
            (B2, E, N("C3")),       (B2_AND, E, N("C3")),
            (B3, E, N("G3", "C4")), (B3_AND, E, N("C3")),
            (B4, E, N("C3")),       (B4_AND, E, N("G2")),
        ])
    if harmony == "Bb/C":
        return E_seq([
            (B1, E, N("C2", "C3")), (B1_AND, E, N("Bb2")),
            (B2, E, N("D3")),       (B2_AND, E, N("D3")),
            (B3, E, N("D3")),       (B3_AND, E, N("Bb3", "D4")),
            (B4, E, N("D3")),       (B4_AND, E, N("D3")),
        ])
    if harmony == "Ab/C":
        return E_seq([
            (B1, E, N("C2", "C3")), (B1_AND, E, N("Ab2")),
            (B2, E, N("C3")),       (B2_AND, E, N("C3")),
            (B3, E, N("Ab3", "C4")),(B3_AND, E, N("C3")),
            (B4, E, N("C3")),       (B4_AND, E, N("Ab2")),
        ])
    raise ValueError(f"Unknown prechorus harmony: {harmony}")


def lh_chorus_drive(root_name: str, omit_last: bool = False) -> List[Event]:
    """
    Signature 8-eighth-note rock-ballad chorus accompaniment on root R.
    Acoustically, when R is in Octave 1 (Ab1, Bb1), the Beat 3 backbeat voices
    the 12th+double-octave [R+19, R+24]; when R is in Octave 2 (C2), it voices
    [R+12, R+19] so the left hand never crosses Middle C (C4):
      Beat 1   : [R, R+12]      (Low octave downbeat)
      Beat 1&  : [R+7]          (Fifth)
      Beat 2   : [R+12]         (Octave)
      Beat 2&  : [R+12] or [R+7]
      Beat 3   : [R+19, R+24] or [R+12, R+19] (Tenor backbeat)
      Beat 3&  : [R+12]         (Octave)
      Beat 4   : [R+12]         (Octave)
      Beat 4&  : [R+7]          (Fifth pickup to next bar)
    """
    r = pitch(root_name)
    low_register = r < pitch("C2")
    backbeat = [r + 19, r + 24] if low_register else [r + 12, r + 19]
    step6 = [r + 12] if low_register else [r + 7]
    seq = [
        (B1,     Q, [r, r + 12]),
        (B1_AND, E, [r + 7]),
        (B2,     E, [r + 12]),
        (B2_AND, E, step6),
        (B3,     E, backbeat),
        (B3_AND, E, [r + 12]),
        (B4,     E, [r + 12]),
    ]
    if not omit_last:
        seq.append((B4_AND, E, [r + 7]))
    return E_seq(seq)


def lh_f_dorian_sweep() -> List[Event]:
    """
    Ascending F-major (C Dorian IV) arpeggio sweep (Bars 32 & 64):
    Eighth-note bass foundation on Beats 1-2 followed by a 16th-note
    F2 - A2 - C3 - F3 - A3 sweep across Beat 3 into Beat 4.
    """
    return E_seq([
        (B1,     E, N("F1", "F2")),
        (B1_AND, E, N("C2")),
        (B2,     E, N("F2")),
        (B2_AND, E, N("A2", "C3")),
        (B3,     S, N("F2")),
        (B3_E,   S, N("A2")),
        (B3_AND, S, N("C3")),
        (B3_A,   S, N("F3")),
        (B4,     E, N("A3")),
    ])


def lh_breakthrough_ostinato(chord_type: str = "Cm", driving_pulse: bool = True) -> List[Event]:
    """
    Martial eighth-note ostinato for Han Li's Nascent Soul Breakthrough (Bars 57-63):
    Resonant C2+G2+C3 downbeats with relentless G2+C3+G3 eighth-note pulse.
    """
    downbeat = {
        "Cm":   N("C2", "G2", "C3"),
        "Bb/C": N("C2", "G2", "C3", "Bb3"),
        "Ab/C": N("C2", "G2", "C3", "Eb3", "Ab3"),
    }[chord_type]
    seq = [(B1, DQ, downbeat)]
    steps = EIGHTH_STEPS[1:] if driving_pulse else EIGHTH_STEPS[2:]
    for s in steps:
        pulse = N("G2", "C3", "G3") if s in (B3, B4) else N("G2", "G3")
        seq.append((s, E, pulse))
    return E_seq(seq)


def lh_climax_arpeggio(root_name: str, tresillo_punch: bool = False, high_span: bool = False) -> List[Event]:
    """
    Wide-span 10th/12th arpeggio for the High Operatic Climax (Bars 81-104)
    constructed from interval offsets relative to root R = pitch(root_name).
    """
    r = pitch(root_name)
    if r < pitch("C2"):
        apex = [r + 19, r + 24, r + 31] if high_span else [r + 19, r + 24]
        seq = [
            (B1,     DE if tresillo_punch else DQ, [r, r + 12]),
            (B2_AND, E,  [r + 19, r + 24]),
            (B3,     E,  apex),
            (B3_AND, E,  [r + 19, r + 24]),
            (B4,     E,  [r + 12, r + 19, r + 24]),
            (B4_AND, E,  [r + 19]),
        ]
        if tresillo_punch:
            seq.insert(1, (B1_A, DE, [r + 12, r + 24]))
    else:
        seq = [
            (B1,     DE if tresillo_punch else DQ, [r, r + 12]),
            (B2_AND, E,  [r + 7, r + 19]),
            (B3,     E,  [r + 12, r + 19]),
            (B3_AND, E,  [r + 7, r + 19]),
            (B4,     E,  [r + 12, r + 19]),
            (B4_AND, E,  [r + 7]),
        ]
        if tresillo_punch:
            seq.insert(1, (B1_A, DE, [r + 12, r + 19]))
    return E_seq(seq)


def lh_lyrical_arch(root_name: str) -> List[Event]:
    """
    Lyrical 10th/12th arch arpeggio for the Operatic Interlude (Bars 49-54):
      Beat 1   (DQ): [R, R+12]
      Beat 2&  (E) : [R+19]
      Beat 3   (Q) : [R+24]
      Beat 4   (Q) : [R+12]
    """
    r = pitch(root_name)
    return E_seq([
        (B1,     DQ, [r, r + 12]),
        (B2_AND, E,  [r + 19]),
        (B3,     Q,  [r + 24]),
        (B4,     Q,  [r + 12]),
    ])


def lh_climax_wave(root_name: str, beat4_bass: List[int] = None) -> List[Event]:
    """
    Sweeping 2-octave eighth-note wave arpeggio for the Operatic Climax (Bars 96-103):
      Beat 1   (E): [R, R+12]
      Beat 1&  (E): [R+7]
      Beat 2   (E): [R+12]
      Beat 2&  (E): [R+19]
      Beat 3   (E): [R+24, R+31]
      Beat 3&  (E): [R+19]
      Beat 4   (Q): [R+12, R+19] (or custom passing bass on Beat 4)
    """
    r = pitch(root_name)
    b4_notes = beat4_bass if beat4_bass is not None else [r + 12, r + 19]
    return E_seq([
        (B1,     E, [r, r + 12]),
        (B1_AND, E, [r + 7]),
        (B2,     E, [r + 12]),
        (B2_AND, E, [r + 19]),
        (B3,     E, [r + 24, r + 31]),
        (B3_AND, E, [r + 19]),
        (B4,     Q, b4_notes),
    ])


# =============================================================================
# 4. RIGHT-HAND MOTIF & PHRASE GENERATORS
# =============================================================================

# The signature 8-eighth-note pentatonic motif of "Extraordinary (不凡)":
#   F5 - Eb5 - C5 - G5 - F5 - Eb5 - C5 - Bb4
MAIN_THEME_PITCHES = ("F5", "Eb5", "C5", "G5", "F5", "Eb5", "C5", "Bb4")
MAIN_THEME_HIGH    = ("F6", "Eb6", "C6", "G6", "F6", "Eb6", "C6", "Bb5")


def rh_main_theme(octave_doubled: bool = False, high_octaves: bool = False) -> List[Event]:
    """Generate the 8-eighth-note main theme in single notes or octaves."""
    pitches = MAIN_THEME_HIGH if high_octaves else MAIN_THEME_PITCHES
    fn = Oct if (octave_doubled or high_octaves) else N
    return [Event(s, E, fn(p)) for s, p in zip(EIGHTH_STEPS, pitches)]


def rh_pickup_cascade(start_step: float = B4_AND) -> List[Event]:
    """4-note 32nd-note pentatonic pickup: Eb6 - C6 - Bb5 - G5."""
    return pentatonic_cascade("Eb6", "G5", start_step, rate=T)


def rh_f_dorian_pickup() -> List[Event]:
    """4-note 16th-note pickup on Beat 4 of the F-Dorian sweep bar: C4 - Eb4 - Ab4 - Bb4."""
    return E_seq([
        (B4,     S, N("C4")),
        (B4_E,   S, N("Eb4")),
        (B4_AND, S, N("Ab4")),
        (B4_A,   S, N("Bb4")),
    ])


def rh_chorus_ab(high_register: bool = False, include_downbeat_chord: bool = False) -> List[Event]:
    """Chorus melody over the Ab measure (Bars 33, 37, 65, 69)."""
    c_n  = "C6"  if high_register else "C5"
    bb_n = "Bb5" if high_register else "Bb4"
    eb_n = "Eb6" if high_register else "Eb5"
    seq = [
        (B2,     E,  Oct(c_n)),
        (B2_AND, E,  Oct(bb_n)),
        (B3,     DE, Oct(c_n)),
        (B3_A,   DE, Oct(eb_n)),
        (B4_AND, Q,  Oct(c_n)),
    ]
    if include_downbeat_chord:
        seq.insert(0, (B1, Q, CHORDS["Ab_low"]))
    return E_seq(seq)


def rh_chorus_bb(high_register: bool = False) -> List[Event]:
    """Chorus melody over the Bb measure (Bars 34, 38, 66, 70)."""
    c_n  = "C6"  if high_register else "C5"
    bb_n = "Bb5" if high_register else "Bb4"
    f_n  = "F6"  if high_register else "F5"
    eb_n = "Eb6" if high_register else "Eb5"
    return E_seq([
        (B2,     E,  Oct(c_n)),
        (B2_AND, E,  Oct(bb_n)),
        (B3,     DE, Oct(c_n)),
        (B3_A,   DE, Oct(f_n)),
        (B4_AND, E,  Oct(eb_n)),
    ])


def rh_chorus_cm1(high_register: bool = False) -> List[Event]:
    """Chorus 1st Cm measure: Bb/C sus4 -> Cm resolution on tresillo grid + Eb6 pickup."""
    if not high_register:
        return E_seq([
            (B1,     DE, CHORDS["Bb_sus"]),
            (B1_A,   DE, CHORDS["Cm"]),
            (B2_AND, DQ, CHORDS["Cm"]),
            (B4_AND, E,  SixthOct("Eb6")),
        ])
    return E_seq([
        (B1,     DE, SixthOct("F6")),
        (B1_A,   DE, SixthOct("G6")),
        (B2_AND, DQ, SixthOct("G6")),
        (B4_AND, E,  SixthOct("Eb6")),
    ])


def rh_chorus_cm2(climax_turn: bool = False, full_sixth_bb: bool = False) -> List[Event]:
    """
    Chorus 2nd Cm measure: Double-tresillo (3+3+2 in both halves of the bar)
    at steps (B1, B1_A, B2_AND) and (B3, B3_A, B4_AND) in SixthOct voicings.
    """
    if not climax_turn:
        return E_seq([
            (B1,     DE, SixthOct("F6")),
            (B1_A,   DE, SixthOct("G6")),
            (B2_AND, E,  SixthOct("G6")),
            (B3,     DE, SixthOct("G6")),
            (B3_A,   DE, SixthOct("F6")),
            (B4_AND, E,  SixthOct("Eb6")),
        ])
    bb_v = SixthOct("Bb6") if full_sixth_bb else Oct("Bb6")
    return E_seq([
        (B1,     DE, SixthOct("F6")),
        (B1_A,   DE, SixthOct("G6")),
        (B2_AND, E,  bb_v),
        (B3,     DE, SixthOct("G6")),
        (B3_A,   DE, SixthOct("F6")),
        (B4_AND, E,  SixthOct("Eb6")),
    ])


# =============================================================================
# 5. MODULAR SECTION GENERATORS (MEASURES 1 TO 116)
# =============================================================================

def _make_adder(sec_name: str, target_list: List[Measure]):
    def add(chord: str, roman: str, bpm: int, dyn: str,
            lh: List[Event], rh: List[Event], pedals: List[float] = None):
        if pedals is None:
            pedals = [B1, B3] if " -> " in chord else [B1]
        target_list.append(Measure(0, sec_name, chord, roman, bpm, dyn, lh, rh, pedals))
    return add


def intro_section() -> List[Measure]:
    """I. Intro (Bars 1-8): Two 4-bar phrases (Half Cadence -> Full Cadence)."""
    bars: List[Measure] = []
    add = _make_adder("I. Intro", bars)
    for phrase in (1, 2):
        rh_bar1 = (rh_pickup_cascade(start_step=-E) if phrase == 1 else []) + rh_main_theme()
        add(
            "Abmaj7", "VI", 120, "mp",
            lh=E_seq([(B1, DH, N("Ab1", "Ab2")), (B4, Q, N("G3"))]),
            rh=rh_bar1,
        )
        add(
            "Bb -> Eb/G -> Bb/D", "VII -> III6 -> VII6", 120, "mp",
            lh=E_seq([(B1, H, N("Bb2", "F3", "Bb3")), (B3, Q, N("Eb3", "Bb3")), (B4, Q, N("D3", "Bb3"))]),
            rh=E_seq([(B1_AND, Q, N("F4")), (B2_AND, DQ, N("G4")), (B4, DE, N("Bb4")), (B4_A, S, N("F4"))]),
            pedals=[B1, B4],
        )
        if phrase == 1:
            add(
                "Cm9", "i9", 120, "p",
                lh=[Roll(B1, W + DH, N("C3", "G3", "D4", "Eb4"))],
                rh=[Roll(B1, H + E, N("G4", "C5"))] + E_seq([(B3_AND, E, N("Bb4")), (B4, E, N("Bb4")), (B4_AND, E, N("C5"))]),
            )
            add(
                "Cm -> G(half)", "i -> V", 116, "p",
                lh=[],
                rh=E_seq([(B1, H, N("Eb4")), (B3, Q, N("D4"))]) + rh_pickup_cascade(start_step=B4_AND),
                pedals=[],
            )
        else:
            add(
                "Cm9", "i9", 118, "p",
                lh=[Roll(B1, DH, N("C3", "G3", "D4", "Eb4"))],
                rh=[Roll(B1, H + E, N("G4", "C5"))] + pentatonic_cascade("G5", "Eb4", start_step=B3_AND, rate=T),
            )
            add(
                "Cm (Fermata)", "i", 108, "p",
                lh=E_seq([(B1, W, N("C2", "G2", "C3"))]),
                rh=[Roll(B1, W, N("G3", "C4", "Eb4"))],
            )
    return bars


def verse_section(verse_num: int) -> List[Measure]:
    """II & III. Verse 1 (Bars 9-16) and Verse 2 (Bars 17-24) over tonic C pedal."""
    sec_name = "II. Verse 1" if verse_num == 1 else "III. Verse 2"
    dyn = "mp" if verse_num == 1 else "mf"
    bars: List[Measure] = []
    add = _make_adder(sec_name, bars)

    for subphrase in (1, 2):
        # Bar 1 of subphrase (Bar 9/13/17/21): Cm over C pedal
        add(
            "Cm", "i", 124, dyn,
            lh=lh_verse_pedal("Cm"),
            rh=E_seq([
                (B1_AND, E, N("Eb4", "Eb5")), (B2, E, N("D4", "D5")), (B2_AND, E, N("C5")),
                (B3, E, N("C4", "Eb4")), (B3_AND, E, N("C5")), (B4, E, N("Bb4")), (B4_AND, E, N("G4")),
            ]),
        )
        if subphrase == 1:
            # Bar 10 / 18: Bb/C
            add(
                "Bb/C", "VII/1", 124, dyn,
                lh=lh_verse_pedal("Bb/C"),
                rh=E_seq([
                    (B1, E, N("D4")), (B1_AND, E, N("G4")), (B2, E, N("F4")), (B2_AND, E, N("Eb4")),
                    (B3, DE, N("D4", "F4")), (B3_A, DE, N("G4")), (B4_AND, Q, N("C4")),
                ]),
            )
            # Bar 11 / 19: Ab/C
            add(
                "Ab/C", "VI/1", 124, "p",
                lh=lh_verse_pedal("Ab/C"),
                rh=E_seq([(B2, Q, N("C4", "Eb4")), (B3, DQ, N("C4", "Eb4"))]),
            )
            # Bar 12 / 20: Ab/C -> Bb (Verse 2 lifts step B3_A from Bb4 to D5)
            peak_note = "Bb4" if verse_num == 1 else "D5"
            add(
                "Ab/C -> Bb", "VI/1 -> VII", 124, dyn,
                lh=lh_verse_pedal("Bb_cadence"),
                rh=E_seq([
                    (B1, E, N("C4")), (B1_AND, E, N("F4")), (B2, E, N("G4")), (B2_AND, E, N("Bb4")),
                    (B3, DE, N("D4", "F4", "C5")), (B3_A, DE, N(peak_note)), (B4_AND, E, N("G4")),
                ]),
            )
        else:
            # Bar 14 / 22: Bb/C
            add(
                "Bb/C", "VII/1", 124, dyn,
                lh=lh_verse_pedal("Bb/C"),
                rh=E_seq([
                    (B1, E, N("D4")), (B1_AND, E, N("F4")), (B2, E, N("Eb4")), (B2_AND, E, N("F4")),
                    (B3, DE, N("D4", "G4")), (B3_A, DE, N("Bb4")), (B4_AND, Q, N("C5")),
                ]),
            )
            # Bar 15 / 23: F/C (C Dorian IV major chord over C pedal)
            rh_dorian = [Roll(B1, DH, N("C4", "F4", "A4"))]
            if verse_num == 1:
                rh_dorian += E_seq([(B4_E, S, N("C5")), (B4_AND, S, N("C4", "G4")), (B4_A, S, N("F4"))])
            else:
                rh_dorian += E_seq([(B4_AND, E, N("D4", "F4", "A4"))])
            add("F/C (Dorian IV)", "IV/1", 124, dyn, lh=lh_verse_pedal("F/C"), rh=rh_dorian)

            # Bar 16 (Quiet turnaround) vs Bar 24 (Rising octave build-up into Pre-Chorus)
            if verse_num == 1:
                add(
                    "Cm -> Bb", "i -> VII", 122, "mp",
                    lh=E_seq([(B1, DQ, N("C3", "G3")), (B2_AND, E, N("G2")), (B3, H, N("Bb2", "Bb3"))]),
                    rh=E_seq([(B1, H, N("C4", "Eb4")), (B3, Q, N("D4", "G4")), (B4, Q, N("D4", "G4", "D5"))]),
                )
            else:
                add(
                    "Cm -> Gm -> Bb", "i -> v -> VII", 126, "f",
                    lh=E_seq([(B1, DQ, N("C3")), (B2_AND, E, N("G2", "G3")), (B3, H, N("Bb2", "Bb3"))]),
                    rh=E_seq([
                        (B1, E, Oct("Eb5")), (B1_AND, E, Oct("Eb5")), (B2, E, Oct("Eb5")),
                        (B2_AND, E, Oct("C5")), (B3, Q, Oct("Eb5")), (B4, Q, Oct("F5")),
                    ]),
                    pedals=[B1, B3],
                )
    return bars


def prechorus_section() -> List[Measure]:
    """IV. Pre-Chorus (Bars 25-32): Syncopated block chords over C2+C3 groove."""
    bars: List[Measure] = []
    add = _make_adder("IV. Pre-Chorus", bars)

    # Subphrase 1 (Bars 25-28): Eighth-note syncopated RH chord anticipations (-E)
    add("Cm", "i", 128, "f", lh=lh_prechorus_groove("Cm"), rh=E_seq([(-E, DH, CHORDS["Cm"]), (B4, E, Oct("G5"))]), pedals=[-E, B1])
    add("Bb/C", "VII/1", 128, "f", lh=lh_prechorus_groove("Bb/C"), rh=E_seq([(-E, DH, CHORDS["Bb_sus"]), (B3_AND, E, Oct("G5")), (B4, E, Oct("F5"))]), pedals=[-E, B1])
    add("Ab/C", "VI/1", 128, "f", lh=lh_prechorus_groove("Ab/C"), rh=E_seq([(-E, DH, CHORDS["Ab"]), (B3_AND, E, Oct("D5")), (B4, E, Oct("Eb5"))]), pedals=[-E, B1])
    add("Bb/C", "VII/1", 128, "f", lh=lh_prechorus_groove("Bb/C"), rh=E_seq([(-E, H + E, CHORDS["Bb_sus"]), (B3, Q, N("D4", "F4", "Bb4", "D5")), (B4, E, N("F4", "A4", "D5"))]), pedals=[-E, B1])

    # Subphrase 2 (Bars 29-32): On-beat climb -> F Dorian IV arpeggio sweep
    add("Cm -> Eb/G", "i -> III6", 128, "f", lh=lh_prechorus_groove("Cm"), rh=E_seq([(B1, DQ, CHORDS["Cm"]), (B2_AND, DQ, CHORDS["Eb_high"]), (B4, E, Oct("C6")), (B4_AND, E, N("Eb5"))]), pedals=[B1])
    add("Bb/C", "VII/1", 128, "f", lh=lh_prechorus_groove("Bb/C"), rh=E_seq([(B1, H, CHORDS["Bb_sus"]), (B3_AND, E, Oct("G5")), (B4, Q, Oct("F5"))]))
    add("Ab/C", "VI/1", 128, "f", lh=lh_prechorus_groove("Ab/C"), rh=E_seq([(B1, E, CHORDS["Ab"]), (B1_AND, E, Oct("D5")), (B2, E, Oct("Eb5")), (B2_AND, DQ, Oct("C5"))]))
    add("F (Dorian IV)", "IV", 128, "f", lh=lh_f_dorian_sweep(), rh=E_seq([(B1, DH, CHORDS["F_dor"])]) + rh_f_dorian_pickup())
    return bars


def chorus_section(high_register: bool, section_name: str, bpm: int, dyn: str) -> List[Measure]:
    """V & VIIIa. Chorus 1 (Bars 33-40) and Chorus 2 (Bars 65-72)."""
    bars: List[Measure] = []
    add = _make_adder(section_name, bars)
    for half in (1, 2):
        add("Ab", "VI", bpm, dyn, lh=lh_chorus_drive("Ab1"), rh=rh_chorus_ab(high_register=high_register, include_downbeat_chord=(half == 1)))
        add("Bb", "VII", bpm, dyn, lh=lh_chorus_drive("Bb1"), rh=rh_chorus_bb(high_register=high_register))
        add("Bb/C -> Cm", "VII/1 -> i", bpm, dyn, lh=lh_chorus_drive("C2"), rh=rh_chorus_cm1(high_register=high_register), pedals=[B1])
        add("Cm", "i", bpm, dyn, lh=lh_chorus_drive("C2", omit_last=(half == 2 and not high_register)), rh=rh_chorus_cm2(climax_turn=(half == 2), full_sixth_bb=high_register))
    return bars


def postchorus_section() -> List[Measure]:
    """VI. Post-Chorus Instrumental Theme (Bars 41-48)."""
    bars: List[Measure] = []
    add = _make_adder("VI. Post-Chorus", bars)
    for phrase in (1, 2):
        if phrase == 1:
            add("Abmaj7 -> Bb", "VI -> VII", 124, "mp", lh=E_seq([(B1, H, N("Ab3")), (B3, H, N("F3", "Bb3"))]), rh=E_seq([(B1, Q, N("Eb4")), (B3, Q, N("D4"))]) + rh_main_theme())
        else:
            add("Fm7 -> Gm7", "iv7 -> v7", 124, "mp", lh=E_seq([(B1, H, N("F2", "C3")), (B3, H, N("G2", "D3", "G3"))]), rh=E_seq([(B1, E, N("C5"))]) + rh_main_theme())
        add("Cm7 -> Eb", "i7 -> III", 124, "mp", lh=E_seq([(B1, H, N("C3", "G3", "Bb3")), (B3, H, N("Eb3"))]), rh=E_seq([(B1_AND, Q, N("F4")), (B2_AND, Q, N("G4")), (B3_AND, Q, N("Bb4")), (B4_A, S, N("Ab4"))]))
        add(
            "Ab -> Bb", "VI -> VII", 124, "mp",
            lh=E_seq([(B1, H, N("Ab2", "Eb3", "Ab3") if phrase == 2 else N("Ab2", "Eb3")), (B3, H, N("Bb2", "F3", "Bb3"))]),
            rh=E_seq([
                (B1, E, N("C5", "F5")), (B1_AND, E, N("Eb5")), (B2, E, N("C5")), (B2_AND, E, N("G5")),
                (B3, E, N("F5")), (B3_AND, E, N("Eb5")), (B4, E, N("Bb4")), (B4_AND, Q if phrase == 2 else DQ, N("C5")),
            ]),
        )
        if phrase == 1:
            add(
                "Cm", "i", 124, "mp",
                lh=E_seq([(B1, W, N("C3", "G3"))]),
                rh=E_seq([(B1, DQ, N("C4"))])
                + pentatonic_cascade("Eb5", "G4", start_step=B2_AND, rate=T)
                + E_seq([(B3, E, N("C4", "F4")), (B3_AND, E, N("Eb4", "G4")), (B4, E, N("F4", "Bb4")), (B4_AND, S, N("G4", "C5")), (B4_A, S, N("Ab4"))]),
            )
        else:
            add(
                "Cm (Pentatonic Run)", "i", 124, "mf",
                lh=E_seq([(B1, Q, N("C2", "C3"))]) + pentatonic_cascade("C3", "Bb3", start_step=B2, rate=T),
                rh=pentatonic_cascade("C4", "Bb4", start_step=B3, rate=T)
                + pentatonic_cascade("Eb6", "Eb5", start_step=B3_A, rate=T),
            )
    return bars


def operatic_interlude() -> List[Measure]:
    """VIIa. Lyrical Operatic Interlude & 2-Bar Dorian Trill (Bars 49-56)."""
    bars: List[Measure] = []
    add = _make_adder("VIIa. Operatic Interlude", bars)

    add("Ab", "VI", 128, "mf", lh=lh_lyrical_arch("Ab1"), rh=E_seq([(B1, Q, N("C5")), (B2, H, N("G4")), (B4, E, N("F4", "Bb4")), (B4_AND, E, N("Eb4"))]))
    add("Bb", "VII", 128, "mf", lh=lh_lyrical_arch("Bb1"), rh=E_seq([(B1, DQ, N("F4"))]) + pentatonic_cascade("Eb5", "G4", start_step=B2_AND, rate=T) + E_seq([(B3, Q, N("F4")), (B4, E, N("Eb4")), (B4_AND, E, N("C4"))]))
    add("Cm -> Gm", "i -> v", 128, "mp", lh=E_seq([(B1, Q, N("C2", "C3")), (B2, E, N("G3")), (B2_AND, E, N("C2")), (B3, Q, N("G2", "C3")), (B4, Q, N("G2", "Bb3"))]), rh=E_seq([(B1, Q, N("Eb4")), (B2, H, N("C4")), (B4, Q, N("D4"))]), pedals=[B1])
    add("Cm", "i", 128, "mp", lh=E_seq([(B1, H, N("C3")), (B3, H, N("C2", "C3"))]), rh=E_seq([(B1, H + E, N("C4", "Eb4"))]) + pentatonic_cascade("Eb6", "C5", start_step=B3_A, rate=T), pedals=[])
    add("Fm", "iv", 128, "mf", lh=lh_lyrical_arch("F1"), rh=E_seq([(B1, H, N("G4", "Bb4")), (B3, Q, N("G4")), (B4, E, N("Bb4")), (B4_AND, E, N("F4"))]))
    add("Gm", "v", 128, "mf", lh=lh_lyrical_arch("G1"), rh=pentatonic_cascade("Eb5", "G4", start_step=B2_AND, rate=T) + E_seq([(B3, E, N("F4")), (B3_AND, E, N("G4")), (B4, E, N("Bb4")), (B4_AND, E, N("C5"))]))

    # Bar 55: F (Dorian IV) 16th-note D5-C5 Trill + Ascending C-Dorian Scale Run
    trill_55 = [Event(s, S, N("D5" if s % 2 == 0 else "C5")) for s in range(B3_AND)]
    run_55 = E_seq([(B3_AND, S, N("D5")), (B3_A, S, N("Eb5")), (B4, S, N("F5")), (B4_E, S, N("G5")), (B4_AND, S, N("C4", "A5")), (B4_A, S, N("Bb5"))])
    add(
        "F (Dorian Trill I)", "IV", 136, "mf",
        lh=E_seq([(B1, E, N("F1", "F2")), (B1_AND, E, N("C2")), (B2, E, N("F2")), (B2_AND, E, N("A2", "C3")), (B3, E, N("F2")), (B3_AND, E, N("A2", "C3")), (B4, E, N("F3")), (B4_AND, E, N("A3"))]),
        rh=trill_55 + run_55,
    )
    # Bar 56: F (Dorian IV) High 16th-note C6-D6 Trill
    trill_56 = [Event(s, S, N("F4", "C6") if s == B1 else (N("C4", "D6") if s == B1_E else N("C6" if s % 2 == 0 else "D6"))) for s in range(W)]
    add(
        "F (Dorian Trill II)", "IV", 138, "f",
        lh=E_seq([(B1_AND, E, N("A3")), (B2, E, N("F3")), (B2_AND, E, N("C3")), (B3, E, N("A2")), (B3_AND, E, N("F3")), (B4, E, N("C3")), (B4_AND, E, N("A2", "F2"))]),
        rh=trill_56,
        pedals=[],
    )
    return bars


def breakthrough_ostinato_section() -> List[Measure]:
    """VIIb. Nascent Soul Breakthrough Ostinato (Bars 57-64)."""
    bars: List[Measure] = []
    add = _make_adder("VIIb. Breakthrough Ostinato", bars)

    for phrase in (1, 2):
        # Bar 57 / 61: Cm martial eighth-note chord ostinato
        add("Cm", "i", 132, "f", lh=lh_breakthrough_ostinato("Cm", driving_pulse=True), rh=E_seq([(s, E, N("C4", "Eb4", "G4")) for s in EIGHTH_STEPS]))
        # Bar 58 / 62: Bb/C -> Cm ostinato
        if phrase == 1:
            rh_bb = E_seq([(B1, E, N("D4", "F4", "D5"))] + [(s, E, N("C4", "G4")) for s in EIGHTH_STEPS[1:6]] + [(B4, E, N("F4", "G4")), (B4_AND, E, N("G4"))])
        else:
            rh_bb = E_seq([(B1, E, N("D4", "F4", "D5"))] + [(s, E, N("C4", "G4")) for s in EIGHTH_STEPS[1:]])
        add("Bb/C -> Cm", "VII/1 -> i", 132, "f", lh=lh_breakthrough_ostinato("Bb/C", driving_pulse=True), rh=rh_bb, pedals=[B1])

        if phrase == 1:
            # Bar 59: Ab/C -> Cm ostinato
            add("Ab/C -> Cm", "VI/1 -> i", 132, "f", lh=lh_breakthrough_ostinato("Ab/C", driving_pulse=True), rh=E_seq([(s, E, N("C4", "Eb4", "G4", "Ab4") if s < B2_AND else N("C4", "Eb4", "G4")) for s in EIGHTH_STEPS]), pedals=[B1])
            # Bar 60: Heroic Cm Melodic Call
            add("Cm", "i", 132, "ff", lh=lh_breakthrough_ostinato("Cm", driving_pulse=False), rh=E_seq([(B1, E, N("C4", "F4")), (B1_AND, E, N("F4")), (B2, E, N("G4")), (B2_AND, E, N("G4", "Bb4")), (B3, DE, N("G4", "C5")), (B3_A, DE, N("G4", "Bb4")), (B4_AND, E, N("G4"))]))
        else:
            # Bar 63: Ab/C -> Cm Rising Call
            add("Ab/C -> Cm", "VI/1 -> i", 132, "ff", lh=lh_breakthrough_ostinato("Ab/C", driving_pulse=False), rh=E_seq([(B1, E, N("C4", "Ab4")), (B1_AND, E, N("C4", "G4")), (B2, E, N("C4", "F4")), (B2_AND, E, N("F4")), (B3, DE, N("F4", "G4")), (B3_A, DE, N("F4", "G4", "Bb4")), (B4_AND, E, N("G4"))]), pedals=[B1])
            # Bar 64: F (Dorian IV) + 16th-note ascending sweep into Chorus 2
            add("F (Dorian IV)", "IV", 132, "ff", lh=lh_f_dorian_sweep(), rh=E_seq([(B1, DH, N("F4", "A4", "C5", "F5"))]) + rh_f_dorian_pickup())
    return bars


def chorus_extension() -> List[Measure]:
    """VIIIb. Chorus 2 High-Octave Theme Extension (Bars 73-80)."""
    bars: List[Measure] = []
    add = _make_adder("VIIIb. Chorus Ext", bars)

    for phrase in (1, 2):
        # Bar 73 / 77: Ab with High-Octave Main Theme
        add("Ab", "VI", 132, "ff", lh=lh_chorus_drive("Ab1", omit_last=True), rh=rh_main_theme(high_octaves=True))
        # Bar 74 / 78: Bb
        b4_step = B3_AND if phrase == 1 else B4
        add("Bb", "VII", 132, "ff", lh=lh_chorus_drive("Bb1"), rh=E_seq([(B1_AND, Q, Oct("F5")), (B2_AND, Q, Oct("G5")), (b4_step, Q, Oct("Bb5"))]))
        if phrase == 1:
            # Bar 75: Cm with High-Octave Main Theme variant
            add("Cm", "i", 132, "ff", lh=lh_chorus_drive("C2"), rh=E_seq([(B1, E, Oct("F6")), (B1_AND, E, Oct("Eb6")), (B2, E, Oct("C6")), (B2_AND, E, Oct("G6")), (B3, E, Oct("F6")), (B3_AND, E, Oct("Eb6")), (B4, E, Oct("Bb5")), (B4_AND, Q, Oct("C6"))]))
            # Bar 76: Cm
            add("Cm", "i", 132, "f", lh=lh_chorus_drive("C2"), rh=E_seq([(B1, DQ, N("C4", "F5")), (B2_AND, DQ, N("C4", "G4", "G5")), (B4, Q, N("Eb5"))]))
        else:
            # Bar 79: Cm Fourths Motif ([C6,F6] -> [Bb5,Eb6] -> [G5,C6])
            add("Cm", "i", 132, "f", lh=lh_chorus_drive("C2"), rh=E_seq([(B1, E, FourthOct("F6")), (B1_AND, E, FourthOct("Eb6")), (B2, H, FourthOct("C6")), (B4, E, FourthOct("F6")), (B4_AND, E, FourthOct("Eb6"))]))
            # Bar 80: Cm Fourths Resolution
            add("Cm", "i", 132, "f", lh=lh_chorus_drive("C2"), rh=E_seq([(B1, W, N("C4", "Eb4", "G4", "G5", "C6"))]))
    return bars


def operatic_climax() -> List[Measure]:
    """VIIIc. High Operatic Climax (戲腔變奏高潮, Bars 81-106)."""
    bars: List[Measure] = []
    add = _make_adder("VIIIc. Operatic Climax", bars)

    # Phrase 1 (Bars 81-88): Rising Octave/Sixth Operatic Call
    for sub in (1, 2):
        add("Ab", "VI", 130, "ff", lh=lh_climax_arpeggio("Ab1", tresillo_punch=False), rh=E_seq([(B2, Q, Oct("C5")), (B3, Q, Oct("D5")), (B4, Q, Oct("Eb5"))]))
        add(
            "Bb", "VII", 130, "ff",
            lh=lh_climax_arpeggio("Bb1", tresillo_punch=True),
            rh=E_seq([(B1, DQ, SixthOct("F5")), (B2_AND, DQ if sub == 2 else H + E, Oct("Eb5"))] + ([(B4, Q, SixthOct("G5"))] if sub == 2 else [])),
        )
        add("Cm", "i", 130, "ff", lh=lh_climax_arpeggio("C2", tresillo_punch=False), rh=E_seq([(B2, E, N("C4", "G4", "C5")), (B2_AND, E, N("C4", "G4", "C5")), (B3, Q, Oct("D5")), (B4, Q, Oct("Eb5"))]))
        add("Cm", "i", 130, "ff", lh=lh_climax_arpeggio("C2", tresillo_punch=(sub == 1)), rh=E_seq([(B1, DQ, SixthOct("F5")), (B2_AND, DQ, SixthOct("G5")), (B4, Q, SixthOct("Eb5" if sub == 1 else "G5"))]))

    # Phrase 2 (Bars 89-96): 7th-Octave Soaring Peak
    for sub in (1, 2):
        add("Ab", "VI", 132, "ff", lh=lh_climax_arpeggio("Ab1", high_span=True), rh=E_seq([(B1, DE, Oct("C7")), (B1_A, S, Oct("Bb6")), (B2, Q, Oct("C7")), (B3, H, Oct("Bb6"))]))
        add("Bb", "VII", 132, "ff", lh=lh_climax_arpeggio("Bb1", tresillo_punch=True, high_span=True), rh=E_seq([(B1, DQ, Oct("G6")), (B2_AND, E, Oct("C7" if sub == 1 else "Bb6")), (B3, H, Oct("Bb6" if sub == 1 else "F6"))]))
        if sub == 1:
            add("Cm", "i", 132, "ff", lh=lh_chorus_drive("C2"), rh=E_seq([(B1, DQ, SixthOct("G6")), (B2_AND, E, Oct("Bb6")), (B3, Q, Oct("G6")), (B4, Q, Oct("F6"))]))
            add("Cm", "i", 132, "ff", lh=lh_chorus_drive("C2"), rh=E_seq([(B1, H, SixthOct("Eb6")), (B3, H, N("Eb4", "G4", "C5", "Eb5", "G5", "C6"))]))
        else:
            add("Eb", "III", 132, "ff", lh=lh_climax_arpeggio("Eb2", tresillo_punch=False), rh=E_seq([(B1, H, N("Eb6", "Bb6", "Eb7")), (B3, E, Oct("Bb6")), (B3_AND, S, Oct("C7")), (B3_A, S, Oct("Bb6")), (B4, E, Oct("G6")), (B4_AND, E, Oct("F6"))]))
            add("Gm (Dominant v)", "v", 132, "ff", lh=lh_climax_wave("G1"), rh=E_seq([(B1, W, N("G4", "G5", "D6", "G6"))]))

    # Phrase 3 (Bars 97-106): Final Climax Descent & Resolution
    add("Ab", "VI", 132, "ff", lh=lh_climax_arpeggio("Ab1", high_span=True), rh=E_seq([(B1, DE, Oct("C7")), (B1_A, S, Oct("Bb6")), (B2, Q, Oct("C7")), (B3, H, N("Eb5", "Eb6", "Eb7"))]))
    add("Bb", "VII", 132, "ff", lh=lh_climax_arpeggio("Bb1", tresillo_punch=True, high_span=True), rh=E_seq([(B1, DQ, Oct("G6")), (B2_AND, E, Oct("C7")), (B3, H, Oct("Bb6"))]))
    add("Cm", "i", 132, "ff", lh=lh_chorus_drive("C2"), rh=E_seq([(B1, DQ, Oct("G6")), (B2_AND, E, Oct("Eb7")), (B3, Q, Oct("C7")), (B4, Q, Oct("Bb6"))]))
    add("Ab -> Gm", "VI -> v", 132, "ff", lh=lh_climax_wave("Ab1", beat4_bass=N("G1", "G2")), rh=E_seq([(B1, DH, Oct("C7")), (B4, E, Oct("G6")), (B4_AND, S, Oct("Bb6")), (B4_A, S, Oct("G6"))]), pedals=[B1, B4])

    # Bars 101-102: 2-Bar Fm Dramatic Arpeggio Sweep
    add("Fm", "iv", 132, "ff", lh=lh_climax_wave("F1", beat4_bass=N("F3", "Ab3", "F4")), rh=E_seq([(B1, W + H, N("F4", "F5", "F6"))]))
    add(
        "Fm", "iv", 132, "ff",
        lh=E_seq([(B1, E, N("F4")), (B1_AND, E, N("F3", "Ab3")), (B2, E, N("F3")), (B2_AND, E, N("C3")), (B3, E, N("F3")), (B3_AND, E, N("C3")), (B4, Q, N("F2", "F3"))]),
        rh=E_seq([(B3, Q, N("F4", "Eb5", "Eb6")), (B4, Q, N("F4", "F5", "F6"))]),
        pedals=[],
    )
    add("Ab", "VI", 132, "ff", lh=lh_climax_wave("Ab1"), rh=E_seq([(B1, DH, Oct("G6")), (B4, Q, Oct("Bb6"))]))
    add("Bb", "VII", 132, "ff", lh=lh_climax_arpeggio("Bb1", tresillo_punch=True, high_span=True), rh=E_seq([(B1, DE, Oct("F6")), (B1_A, S, Oct("Eb6")), (B2, Q, Oct("F6")), (B3, Q, Oct("G6")), (B4, Q, Oct("Bb6"))]))
    add("Cm", "i", 130, "ff", lh=E_seq([(B1, W + H, N("C2", "C3"))]), rh=E_seq([(B1, DQ, SixthOct("Eb7")), (B2_AND, W, N("C4", "G4", "C6", "G6", "C7"))]))
    add("Cm (Waterfall)", "i", 128, "mf", lh=E_seq([(B1, H, N("C3"))]), rh=E_seq([(B1, H, N("Eb4", "G4", "Eb5"))]) + pentatonic_cascade("Eb6", "Eb4", start_step=B3, rate=T), pedals=[])
    return bars


def quiet_outro() -> List[Measure]:
    """IX. Quiet Outro (Bars 107-116): Molto ritardando & final tonic resolution."""
    bars: List[Measure] = []
    add = _make_adder("IX. Outro", bars)

    add("Ab/C", "VI/1", 125, "p", lh=E_seq([(B1, H, N("C2", "C3")), (B4, W, N("C3"))]), rh=[Roll(B1, H, N("C4", "Eb4", "Ab4")), Roll(B3, H, N("C4", "Eb4", "Ab4"))])
    add("Bb/C", "VII/1", 125, "p", lh=E_seq([(B1, DH, N("C3"))]), rh=[Roll(B1, H, N("F4", "Ab4", "Bb4"))] + E_seq([(B3, DQ, N("F4"))]) + rh_pickup_cascade(start_step=B4_AND))

    for outro_phrase in (1, 2):
        tempo = 122 if outro_phrase == 1 else 118
        add("Fm7", "iv7", tempo, "p", lh=E_seq([(B1, W, N("F2", "C3", "F3"))]), rh=rh_main_theme())
        add("Gm7", "v7", tempo, "p", lh=E_seq([(B1, W, N("G2", "D3"))]), rh=E_seq([(B1_AND, Q, N("F4")), (B2_AND, DQ, N("G4")), (B4, DE, N("Bb4")), (B4_A, S, N("F4"))]))
        if outro_phrase == 1:
            add("Cm9", "i9", 118, "p", lh=[Roll(B1, W + DH, N("C3", "G3", "D4", "Eb4"))], rh=[Roll(B1, DH, N("G4", "C5"))] + E_seq([(B4, E, N("Bb4")), (B4_AND, E, N("C5"))]))
            add("Cm -> G(half)", "i -> V", 122, "p", lh=[], rh=E_seq([(B1, H, N("Eb4")), (B3, Q, N("D4"))]) + rh_pickup_cascade(start_step=B4_AND), pedals=[])
        else:
            add("Cm9", "i9", 104, "pp", lh=[Roll(B1, DH, N("C3", "G3", "Eb4", "F4"))], rh=[Roll(B1, H, N("C5"))] + pentatonic_cascade("Eb6", "Eb4", start_step=B3, rate=T))
            add("Cm (Final Tonic)", "i", 80, "pp", lh=E_seq([(B1, W, N("C2", "G2", "C3"))]), rh=[Roll(B1, W, N("G3", "C4", "Eb4"))])
    return bars


def build_score() -> List[Measure]:
    """Assemble the complete 116-measure symphonic form from modular section generators."""
    measures = (
        intro_section()
        + verse_section(verse_num=1)
        + verse_section(verse_num=2)
        + prechorus_section()
        + chorus_section(high_register=False, section_name="V. Chorus 1", bpm=125, dyn="f")
        + postchorus_section()
        + operatic_interlude()
        + breakthrough_ostinato_section()
        + chorus_section(high_register=True, section_name="VIIIa. Chorus 2", bpm=130, dyn="ff")
        + chorus_extension()
        + operatic_climax()
        + quiet_outro()
    )
    for idx, m in enumerate(measures):
        m.bar_num = idx + 1
    return measures


# =============================================================================
# 6. DEFENSIVE SCORE VALIDATION & VIRTUAL PIANIST MIDI COMPILER
# =============================================================================

PHRASE_CADENCE_BARS = frozenset({4, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 96, 106, 116})


def validate_score(measures: List[Measure]) -> None:
    """Strictly verify all structural and musical invariants (zero fallbacks)."""
    assert len(measures) == 116, f"Expected exactly 116 measures, got {len(measures)}"
    for idx, m in enumerate(measures):
        assert m.bar_num == idx + 1, f"Non-sequential bar number at index {idx}: {m.bar_num}"
        assert 60 <= m.bpm <= 200, f"Out-of-range BPM in bar {m.bar_num}: {m.bpm}"
        assert m.dynamic in DYNAMICS, f"Invalid dynamic in bar {m.bar_num}: {m.dynamic}"
        assert len(m.lh) + len(m.rh) > 0, f"Empty measure at bar {m.bar_num}"
        for hand_events in (m.lh, m.rh):
            for ev in hand_events:
                assert -E <= ev.step < W, f"Invalid step {ev.step} in bar {m.bar_num}"
                assert ev.duration > 0, f"Non-positive duration {ev.duration} in bar {m.bar_num}"
                assert len(ev.pitches) > 0, f"Empty pitch list in bar {m.bar_num}"
                for p in ev.pitches:
                    assert 21 <= p <= 108, f"Pitch {p} outside 88-key piano range in bar {m.bar_num}"


def compute_note_velocity(base_dyn: str, hand: str, step: float, pitch_idx: int, num_pitches: int) -> int:
    """
    Derive MIDI velocity from first principles of piano performance:
      1. Base section dynamic (pp, p, mp, mf, f, ff)
      2. Hand balance (Left-hand accompaniment is voiced softer than Right-hand melody)
      3. Metric accent (Beat 1, Beat 3, and tresillo syncopations receive natural weight)
      4. Soprano voicing (The top voice of a right-hand chord/octave projects +4 louder)
    """
    v = DYNAMICS[base_dyn]
    if hand == "lh":
        v -= 12
    s_mod = step % W
    if s_mod == B1:
        v += 5
    elif s_mod in (B3, B1_A, B3_A):
        v += 3
    elif s_mod in (B2, B4, B2_AND, B4_AND):
        v += 1
    else:
        v -= 3
    if hand == "rh" and num_pitches > 1:
        if pitch_idx == num_pitches - 1:
            v += 4
        else:
            v -= 3
    return max(30, min(115, int(round(v))))


def compile_to_midi(measures: List[Measure], out_path: str) -> pretty_midi.PrettyMIDI:
    """
    Single-mode Virtual Pianist MIDI compiler:
      - Integrates the section tempo curve BPM(m) with phrase-arch agogic breathing
        on cadence measures.
      - Voices chords with natural bottom-to-top micro-spread (4.5 ms on block
        chords/octaves, 20 ms on lyrical Roll chords).
      - Applies syncopated legato sustain pedaling (CC64).
    """
    validate_score(measures)
    pm = pretty_midi.PrettyMIDI(initial_tempo=measures[0].bpm)
    piano = pretty_midi.Instrument(program=0, name="Concert Grand Piano (First-Principles Reduction)")

    t_cursor = 0.60  # Concert-hall pre-roll before Bar 1

    for m in measures:
        # Subtle phrase-end agogic broadening (+4% on cadence bars)
        agogic_factor = 1.04 if m.bar_num in PHRASE_CADENCE_BARS else 1.00
        bar_dur = (240.0 / m.bpm) * agogic_factor
        step_dur = bar_dur / W

        # Syncopated legato sustain pedal (release 35 ms before change, catch 15 ms after)
        for p_step in m.pedal_steps:
            t_ped = max(0.05, t_cursor + p_step * step_dur)
            piano.control_changes.append(pretty_midi.ControlChange(64, 0, max(0.0, t_ped - 0.035)))
            piano.control_changes.append(pretty_midi.ControlChange(64, 110, t_ped + 0.015))

        for hand_label, ev_list in (("lh", m.lh), ("rh", m.rh)):
            for ev in ev_list:
                t_on_base = max(0.0, t_cursor + ev.step * step_dur)
                t_off = t_on_base + (ev.duration * 0.98) * step_dur
                n_p = len(ev.pitches)
                spread_sec = 0.020 if ev.rolled else (0.0045 if n_p > 1 else 0.0)
                for idx, p in enumerate(sorted(ev.pitches)):
                    voice_offset = idx * spread_sec
                    vel = compute_note_velocity(m.dynamic, hand_label, ev.step, idx, n_p)
                    piano.notes.append(pretty_midi.Note(
                        velocity=vel,
                        pitch=p,
                        start=t_on_base + voice_offset,
                        end=max(t_on_base + voice_offset + 0.05, t_off),
                    ))

        t_cursor += bar_dur

    # Release pedal cleanly after final chord resonance
    piano.control_changes.append(pretty_midi.ControlChange(64, 0, t_cursor + 1.50))

    # Clean overlapping identical-pitch notes for crisp hammer re-articulation
    piano.notes.sort(key=lambda x: (x.pitch, x.start))
    cleaned: List[pretty_midi.Note] = []
    for n in piano.notes:
        if cleaned and cleaned[-1].pitch == n.pitch and cleaned[-1].end > n.start:
            cleaned[-1].end = max(cleaned[-1].start + 0.03, n.start - 0.012)
        cleaned.append(n)
    piano.notes = sorted(cleaned, key=lambda x: (x.start, x.pitch))

    pm.instruments.append(piano)
    pm.write(out_path)
    assert os.path.isfile(out_path) and os.path.getsize(out_path) > 1000, f"MIDI write failed: {out_path}"
    return pm


# =============================================================================
# 7. 96 kHz / 64-BIT FLOAT PHYSICAL PIANO & CONCERT HALL MASTERING ENGINE
# =============================================================================

SF2_MUSESCORE_LOSSLESS = "/usr/share/sounds/sf2/MuseScore_General_Full.sf2"
SF2_FLUIDR3_GM         = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
INTERNAL_SR            = 96000
EXPORT_SR              = 48000


def _peaking_eq_sos(f0: float, gain_db: float, q: float, fs: int) -> np.ndarray:
    """
    Exact RBJ Audio EQ Cookbook peaking biquad filter formatted as a single
    second-order section (SOS). Halves gain_db so forward-backward zero-phase
    filtering (`sosfiltfilt`) yields the exact target dB response.
    """
    a_amp = 10.0 ** ((gain_db / 2.0) / 40.0)
    w0 = 2.0 * np.pi * f0 / fs
    alpha = np.sin(w0) / (2.0 * q)
    cos_w0 = np.cos(w0)

    b0 = 1.0 + alpha * a_amp
    b1 = -2.0 * cos_w0
    b2 = 1.0 - alpha * a_amp
    a0 = 1.0 + alpha / a_amp
    a1 = -2.0 * cos_w0
    a2 = 1.0 - alpha / a_amp

    return np.array([[b0 / a0, b1 / a0, b2 / a0, 1.0, a1 / a0, a2 / a0]], dtype=np.float64)


def _render_fluidsynth_stem(midi_path: str, sf2_path: str, wav_out: str) -> np.ndarray:
    """Render a 96 kHz 32-bit float stereo stem via FluidSynth with internal effects disabled."""
    assert os.path.isfile(sf2_path), f"Missing required SoundFont: {sf2_path}"
    assert os.path.getsize(sf2_path) > 100_000_000, f"SoundFont unexpectedly small: {sf2_path}"
    cmd = [
        "fluidsynth", "-ni",
        "-g", "0.85",
        "-r", str(INTERNAL_SR),
        "-O", "float",
        "-T", "wav",
        "-C", "0",
        "-R", "0",
        "-F", wav_out,
        sf2_path,
        midi_path,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    audio, sr = sf.read(wav_out, dtype="float64", always_2d=True)
    assert sr == INTERNAL_SR, f"Expected {INTERNAL_SR} Hz from FluidSynth, got {sr} Hz"
    assert audio.ndim == 2 and audio.shape[1] == 2 and audio.shape[0] > INTERNAL_SR * 60
    return audio


def _apply_sympathetic_string_resonance(stereo: np.ndarray, fs: int) -> np.ndarray:
    """
    Model the undamped C-minor / Eb-major harmonic string & soundboard modes
    of a 9-foot concert grand piano using 24 high-Q parallel resonator modes
    with natural bass-left / treble-right spatial panning.
    """
    resonator_notes = (
        "C2", "G2", "C3", "Eb3", "F3", "G3", "Ab3", "Bb3",
        "C4", "D4", "Eb4", "F4", "G4", "Ab4", "Bb4", "C5",
        "D5", "Eb5", "F5", "G5", "Bb5", "C6", "Eb6", "G6",
    )
    mono_excit = 0.5 * (stereo[:, 0] + stereo[:, 1])
    symp_l = np.zeros_like(mono_excit)
    symp_r = np.zeros_like(mono_excit)

    n_modes = len(resonator_notes)
    for i, name in enumerate(resonator_notes):
        midi_p = pitch(name)
        freq = 440.0 * (2.0 ** ((midi_p - 69.0) / 12.0))
        q_factor = 38.0 + 1.2 * i
        b, a = signal.iirpeak(freq, q_factor, fs=fs)
        sos = signal.tf2sos(b, a)
        mode_sig = signal.sosfilt(sos, mono_excit)
        # Bass strings pan slightly left (0.68 L / 0.32 R), treble strings slightly right
        pan = 0.32 + 0.36 * (i / (n_modes - 1))
        weight = 1.0 / np.sqrt(1.0 + 0.12 * i)
        symp_l += weight * (1.0 - pan) * mode_sig
        symp_r += weight * pan * mode_sig

    symp = np.column_stack((symp_l, symp_r)) * (0.012 / np.sqrt(n_modes))
    return stereo + symp


def _build_concert_hall_ir(fs: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Deterministically synthesize a 2.8-second True-Stereo Concert Hall Impulse
    Response at 96 kHz:
      - 16 specular timber-hall early reflections (14 ms to 84 ms) with ITD/ILD
      - 3-band frequency-dependent diffuse late reverberation tail with natural
        air absorption and a 22 ms pre-delay envelope.
    """
    rng = np.random.default_rng(20261015)
    ir_len = int(2.8 * fs)
    t = np.arange(ir_len, dtype=np.float64) / fs

    early_l = np.zeros(ir_len, dtype=np.float64)
    early_r = np.zeros(ir_len, dtype=np.float64)
    reflections_ms = (
        (14.2, -0.45,  0.72, 0.38), (18.7,  0.42,  0.35, 0.70),
        (23.5,  0.36,  0.65, 0.42), (27.9, -0.33,  0.40, 0.62),
        (33.4,  0.29,  0.58, 0.45), (39.1,  0.26,  0.44, 0.57),
        (44.8, -0.24,  0.55, 0.46), (50.3,  0.22,  0.46, 0.54),
        (56.0,  0.19,  0.52, 0.48), (61.7, -0.17,  0.48, 0.52),
        (67.2,  0.15,  0.51, 0.49), (72.8,  0.14,  0.49, 0.51),
        (77.5, -0.12,  0.50, 0.50), (83.6,  0.11,  0.50, 0.50),
    )
    for delay_ms, sign, gl, gr in reflections_ms:
        idx_l = int((delay_ms / 1000.0) * fs)
        idx_r = int(((delay_ms + 0.22 * sign) / 1000.0) * fs)
        if 0 <= idx_l < ir_len and 0 <= idx_r < ir_len:
            early_l[idx_l] += sign * gl * 0.22
            early_r[idx_r] += sign * gr * 0.22

    # Warm wooden wall damping on early reflections (low-pass at 3.8 kHz)
    sos_early = signal.butter(2, 3800.0, btype="low", fs=fs, output="sos")
    early_l = signal.sosfilt(sos_early, early_l)
    early_r = signal.sosfilt(sos_early, early_r)

    # Decorrelated stereo Gaussian diffuse noise fields
    noise_l = rng.standard_normal(ir_len)
    noise_r = rng.standard_normal(ir_len)

    # 22 ms pre-delay & smooth 18 ms bloom attack envelope
    predelay_s = 0.022
    bloom = np.clip((t - predelay_s) / 0.018, 0.0, 1.0) ** 2

    # 3-band RT60 decay envelopes (T60 -> exp(-6.9078 * t / RT60))
    env_low  = bloom * np.exp(-6.9078 * np.maximum(0.0, t - predelay_s) / 1.75)
    env_mid  = bloom * np.exp(-6.9078 * np.maximum(0.0, t - predelay_s) / 2.05)
    env_high = bloom * np.exp(-6.9078 * np.maximum(0.0, t - predelay_s) / 1.10)

    sos_low  = signal.butter(2, 260.0, btype="low", fs=fs, output="sos")
    sos_mid  = signal.butter(2, [260.0, 2800.0], btype="bandpass", fs=fs, output="sos")
    sos_high = signal.butter(2, [2800.0, 7200.0], btype="bandpass", fs=fs, output="sos")

    tail_l = (
        0.45 * signal.sosfilt(sos_low, noise_l) * env_low
        + 0.85 * signal.sosfilt(sos_mid, noise_l) * env_mid
        + 0.35 * signal.sosfilt(sos_high, noise_l) * env_high
    )
    tail_r = (
        0.45 * signal.sosfilt(sos_low, noise_r) * env_low
        + 0.85 * signal.sosfilt(sos_mid, noise_r) * env_mid
        + 0.35 * signal.sosfilt(sos_high, noise_r) * env_high
    )

    ir_l = early_l + tail_l
    ir_r = early_r + tail_r
    norm = np.sqrt(np.max(np.sum(ir_l ** 2) + np.sum(ir_r ** 2)))
    return ir_l / norm, ir_r / norm


def synthesize_and_master_audio(midi_path: str, out_mp3_path: str) -> None:
    """
    Execute the complete 96 kHz / 64-bit float dual-soundfont synthesis,
    sympathetic string resonance, zero-phase mastering EQ, concert-hall FFT
    convolution, and 48 kHz LAME V0 encoding pipeline.
    """
    with tempfile.TemporaryDirectory(prefix="extraordinary_master_") as tmpdir:
        wav_ms = os.path.join(tmpdir, "stem_musescore_96k.wav")
        wav_fl = os.path.join(tmpdir, "stem_fluidr3_96k.wav")
        wav_48k = os.path.join(tmpdir, "master_48k.wav")

        # 1. Dual 96 kHz 32-bit float FluidSynth renders
        stem_ms = _render_fluidsynth_stem(midi_path, SF2_MUSESCORE_LOSSLESS, wav_ms)
        stem_fl = _render_fluidsynth_stem(midi_path, SF2_FLUIDR3_GM, wav_fl)
        n_samples = min(stem_ms.shape[0], stem_fl.shape[0])
        stem_ms = stem_ms[:n_samples]
        stem_fl = stem_fl[:n_samples]

        # 2. Zero-phase spectral crossover blend (82% MuseScore Concert Grand + 18% focused FluidR3)
        sos_fl_bp = signal.butter(4, [180.0, 5800.0], btype="bandpass", fs=INTERNAL_SR, output="sos")
        stem_fl_focused = signal.sosfiltfilt(sos_fl_bp, stem_fl, axis=0)
        stereo = 0.82 * stem_ms + 0.18 * stem_fl_focused

        # 3. 24-mode C-minor sympathetic string & soundboard resonance bank
        stereo = _apply_sympathetic_string_resonance(stereo, fs=INTERNAL_SR)

        # 4. 5-stage zero-phase RBJ biquad mastering EQ at 96 kHz
        sos_hp = signal.butter(4, 24.0, btype="high", fs=INTERNAL_SR, output="sos")
        sos_lp = signal.butter(4, 16500.0, btype="low", fs=INTERNAL_SR, output="sos")
        sos_eq = np.vstack([
            sos_hp,
            _peaking_eq_sos(110.0,  +2.0, 1.0, INTERNAL_SR),  # Concert grand soundboard warmth
            _peaking_eq_sos(320.0,  -1.8, 1.4, INTERNAL_SR),  # Boxiness / lower-mid cleanup
            _peaking_eq_sos(3150.0, -2.6, 1.5, INTERNAL_SR),  # Hammer-felt upper-mid smoothing
            _peaking_eq_sos(8500.0, +1.2, 0.9, INTERNAL_SR),  # Silk upper-harmonic sheen
            sos_lp,
        ])
        stereo = signal.sosfiltfilt(sos_eq, stereo, axis=0)

        # 5. True-Stereo 96 kHz Concert Hall Impulse Response FFT Convolution
        ir_l, ir_r = _build_concert_hall_ir(fs=INTERNAL_SR)
        rev_ll = signal.fftconvolve(stereo[:, 0], ir_l, mode="full")[:n_samples]
        rev_rr = signal.fftconvolve(stereo[:, 1], ir_r, mode="full")[:n_samples]
        rev_lr = signal.fftconvolve(stereo[:, 0], ir_r, mode="full")[:n_samples]
        rev_rl = signal.fftconvolve(stereo[:, 1], ir_l, mode="full")[:n_samples]
        wet_l = 0.85 * rev_ll + 0.15 * rev_rl
        wet_r = 0.85 * rev_rr + 0.15 * rev_lr
        wet = np.column_stack((wet_l, wet_r))

        stereo = 0.81 * stereo + 0.19 * wet

        # 6. Mid/Side stereo imaging (+10% high-frequency width) & soft-knee saturation
        mid = 0.5 * (stereo[:, 0] + stereo[:, 1])
        side = 0.5 * (stereo[:, 0] - stereo[:, 1])
        sos_side_hp = signal.butter(2, 220.0, btype="high", fs=INTERNAL_SR, output="sos")
        side = signal.sosfiltfilt(sos_side_hp, side) * 1.10
        stereo = np.column_stack((mid + side, mid - side))

        # Peak-normalize into soft-knee analog transformer saturation
        peak_pre = float(np.max(np.abs(stereo)))
        assert peak_pre > 1e-4 and np.all(np.isfinite(stereo)), "Invalid audio signal before mastering"
        stereo = stereo / peak_pre
        drive = 1.18
        stereo = np.tanh(drive * stereo) / np.tanh(drive)

        # Smooth 1.5s cosine fade-out on final tail and -0.8 dBFS true-peak ceiling
        fade_len = int(1.5 * INTERNAL_SR)
        fade_curve = 0.5 * (1.0 + np.cos(np.linspace(0.0, np.pi, fade_len)))
        stereo[-fade_len:, 0] *= fade_curve
        stereo[-fade_len:, 1] *= fade_curve

        target_peak = 10.0 ** (-0.8 / 20.0)
        stereo = stereo * (target_peak / float(np.max(np.abs(stereo))))

        # 7. High-precision polyphase downsample (96 kHz -> 48 kHz) & LAME V0 encode
        master_48k = signal.resample_poly(stereo, up=1, down=2, axis=0)
        master_48k = np.clip(master_48k, -1.0, 1.0)
        sf.write(wav_48k, master_48k, EXPORT_SR, subtype="FLOAT")

        ffmpeg_cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", wav_48k,
            "-c:a", "libmp3lame",
            "-q:a", "0",
            "-compression_level", "0",
            "-ar", str(EXPORT_SR),
            out_mp3_path,
        ]
        subprocess.run(ffmpeg_cmd, check=True)

    assert os.path.isfile(out_mp3_path), f"MP3 output missing: {out_mp3_path}"
    mp3_size = os.path.getsize(out_mp3_path)
    assert 2_000_000 <= mp3_size <= 10_000_000, f"Unexpected MP3 size: {mp3_size} bytes"


# =============================================================================
# 8. HUMAN-READABLE MARKDOWN SCORE EXPORTER
# =============================================================================

def format_events(events: List[Event]) -> str:
    """Format a measure's symbolic events cleanly for human reading."""
    by_step = {}
    for ev in sorted(events, key=lambda x: x.step):
        s_lbl = f"{int(ev.step)}" if ev.step == int(ev.step) else f"{ev.step:.1f}"
        names = "+".join(note_name(p) for p in sorted(set(ev.pitches)))
        if ev.rolled:
            names = f"~{names}"
        if s_lbl in by_step:
            by_step[s_lbl] += f"+{names}"
        else:
            by_step[s_lbl] = names
    return "  ".join(f"`{k}`:{v}" for k, v in by_step.items()) if by_step else "*(tacet)*"


def export_markdown_score(measures: List[Measure], out_md: str) -> None:
    """Export the complete first-principles bar-by-bar chord & voicing score."""
    lines = [
        "# First-Principles Mathematical & Musical Reduction: *Extraordinary (不凡)*",
        "",
        "- **Piece**: *A Mortal's Journey「不凡 Extraordinary」— Ru's Piano Cover*",
        "- **Source Performance**: [https://youtu.be/JB31Aq_5Slw](https://youtu.be/JB31Aq_5Slw)",
        "- **Rendered Audio**: [`extraordinary.mp3`](extraordinary.mp3) | **MIDI**: [`extraordinary.mid`](extraordinary.mid) | **Sheet Music**: [`extraordinary_sheet_music.png`](extraordinary_sheet_music.png)",
        "- **Created With**: **Gemini 4 Argon high in Antigravity CLI**",
        "- **Key**: **C Natural Minor** (`C, D, Eb, F, G, Ab, Bb`) with **C Dorian** (`A` natural on the `F` major IV chord) & **G Dominant** (`Gm/G5` at the climax)",
        "- **Meter**: **4/4** on a pure rational 16th-note grid (`0` = Beat 1, `4` = Beat 2, `8` = Beat 3, `12` = Beat 4; `~` denotes an upward rolled chord)",
        "",
        "## 1. First-Principles Architecture (\"PNG to SVG\")",
        "",
        "| Domain | First-Principles Generator | Musical Meaning |",
        "| :--- | :--- | :--- |",
        "| **Tonal Basis** | C Minor + Dorian $\\natural\\hat{6}$ + Pentatonic $\\{C, E\\flat, F, G, B\\flat\\}$ | Modal Gufeng (古風) harmonic & ornamental space |",
        "| **Rhythmic Algebra** | Pure rational subdivisions (`W=16, H=8, Q=4, DE=3, E=2, S=1, T=0.5`) | Zero hard-coded timestamps; exact metric & tresillo (`3+3+2`) geometry |",
        "| **Left-Hand Functors** | `lh_verse_pedal`, `lh_prechorus_groove`, `lh_chorus_drive`, `lh_f_dorian_sweep`, `lh_breakthrough_ostinato`, `lh_climax_arpeggio`, `lh_lyrical_arch`, `lh_climax_wave` | 8 accompaniment archetypes spanning all 116 measures |",
        "| **Right-Hand Operators** | `N`, `Oct`, `SixthOct`, `FourthOct`, `Roll`, `pentatonic_cascade` | Idiomatic solo-piano voicings & pentatonic waterfalls |",
        "| **Virtual Pianist & 96 kHz Mastering** | Phrase-arch agogic breathing + Dual 96 kHz SoundFont synthesis + 24-mode sympathetic string bank + Concert-Hall FFT IR convolution | Studio-grade concert grand piano rendering (`extraordinary.mp3`) |",
        "",
        "## 2. Complete Bar-by-Bar Symbolic Score (Measures 1–116)",
        "",
    ]

    cur_sec = None
    for m in measures:
        if m.section != cur_sec:
            cur_sec = m.section
            lines.extend([
                f"### {cur_sec}",
                "",
                "| Bar | Tempo | Dyn | Chord | Roman | Left Hand (`step`:voicing) | Right Hand (`step`:voicing) |",
                "| :---: | :---: | :---: | :---: | :---: | :--- | :--- |",
            ])
        lh_str = format_events(m.lh)
        rh_str = format_events(m.rh)
        lines.append(
            f"| **{m.bar_num}** | `{m.bpm:3d}` | *{m.dynamic}* | **{m.chord_symbol}** | `{m.roman}` | {lh_str} | {rh_str} |"
        )
        if m.bar_num in (8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 106, 116):
            lines.append("")

    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    assert os.path.isfile(out_md) and os.path.getsize(out_md) > 5000, f"Score write failed: {out_md}"


# =============================================================================
# 9. CLASSICAL PIANO SHEET MUSIC ENGRAVER (LILYPOND + SUPERSAMPLED TALL PNG)
# =============================================================================

LY_PITCH_NAMES = ("c", "des", "d", "ees", "e", "f", "fis", "g", "aes", "a", "bes", "b")

LY_DUR_TABLE: Tuple[Tuple[int, str], ...] = (
    (32, "1"),
    (24, "2."),
    (16, "2"),
    (12, "4."),
    (8,  "4"),
    (6,  "8."),
    (4,  "8"),
    (3,  "16."),
    (2,  "16"),
    (1,  "32"),
)


def _midi_to_ly_pitch(midi_num: int) -> str:
    """Convert MIDI pitch number to C-minor spelled LilyPond absolute pitch."""
    pc = midi_num % 12
    octv = midi_num // 12 - 1
    marks = ("'" * (octv - 3)) if octv >= 3 else ("," * (3 - octv))
    return f"{LY_PITCH_NAMES[pc]}{marks}"


def _pitches_to_ly_chord(pitches: List[int]) -> str:
    """Format one or more MIDI pitches as a LilyPond note or <...> chord."""
    unique = sorted(set(pitches))
    assert len(unique) > 0
    if len(unique) == 1:
        return _midi_to_ly_pitch(unique[0])
    return "<" + " ".join(_midi_to_ly_pitch(p) for p in unique) + ">"


def _ticks_to_ly_chunks(dur_ticks: int) -> List[str]:
    """
    Decompose an exact 32nd-note tick duration (1..32) into standard LilyPond
    duration tokens whose sum is guaranteed to equal `dur_ticks`.
    """
    assert 1 <= dur_ticks <= 32, f"Invalid tick duration: {dur_ticks}"
    chunks: List[str] = []
    rem = dur_ticks
    for ticks, tok in LY_DUR_TABLE:
        while rem >= ticks:
            chunks.append(tok)
            rem -= ticks
    assert rem == 0
    return chunks


def _prepare_engraving_measures(
    measures: List[Measure],
) -> Tuple[List[List[Event]], List[List[Event]], List[bool]]:
    """
    Prepare per-measure RH and LH event lists on the [0, 16) measure grid,
    converting Pre-Chorus (-E) syncopated chord anticipations into idiomatic
    Beat 4& eighth-note chords tied (`~`) across the barline.
    """
    n_bars = len(measures)
    rh_bars: List[List[Event]] = []
    lh_bars: List[List[Event]] = []
    tie_rh_end: List[bool] = [False] * n_bars

    for m in measures:
        rh_bars.append([Event(ev.step, ev.duration, list(ev.pitches), ev.rolled) for ev in m.rh if ev.step >= 0])
        lh_bars.append([Event(ev.step, ev.duration, list(ev.pitches), ev.rolled) for ev in m.lh if ev.step >= 0])

    for idx, m in enumerate(measures):
        neg_evs = [ev for ev in m.rh if ev.step < 0]
        if not neg_evs or idx == 0:
            continue
        ev = neg_evs[0]
        prev_rh = rh_bars[idx - 1]
        prev_end = max((e.step + e.duration for e in prev_rh), default=0.0)
        if prev_end <= B4_AND:
            # Place eighth-note anticipation on Beat 4& (step 14) of previous bar tied into current bar
            prev_rh.append(Event(B4_AND, E, list(ev.pitches), False))
            tie_rh_end[idx - 1] = True
            rh_bars[idx].insert(0, Event(B1, max(E, ev.duration - E), list(ev.pitches), ev.rolled))
        else:
            rh_bars[idx].insert(0, Event(B1, ev.duration, list(ev.pitches), ev.rolled))

    return rh_bars, lh_bars, tie_rh_end


def _rest_span_to_ly_tokens(start_tick: int, end_tick: int) -> List[str]:
    """
    Decompose a rest interval [start_tick, end_tick) into metric-aligned
    LilyPond rest tokens (advancing from fine offbeats to coarser beat boundaries).
    """
    assert 0 <= start_tick < end_tick <= 32
    if start_tick == 0 and end_tick == 32:
        return ["R1"]
    tokens: List[str] = []
    cur = start_tick
    while cur < end_tick:
        rem = end_tick - cur
        if cur % 16 == 0 and rem >= 16:
            tokens.append("r2")
            cur += 16
        elif cur % 8 == 0 and rem >= 8:
            tokens.append("r4")
            cur += 8
        elif cur % 4 == 0 and rem >= 4:
            tokens.append("r8")
            cur += 4
        elif cur % 2 == 0 and rem >= 2:
            tokens.append("r16")
            cur += 2
        else:
            tokens.append("r32")
            cur += 1
    return tokens


def _render_hand_measure_ly(
    events: List[Event],
    is_rh: bool,
    tie_at_end: bool,
    header_markup: str,
    dyn_markup: str,
    cur_ottava: int,
) -> Tuple[str, int]:
    """
    Compile one hand of a single 4/4 measure into LilyPond tokens totaling
    exactly 32 thirty-second-note ticks.
    """
    if not events:
        prefix = ""
        if cur_ottava != 0:
            prefix = "\\ottava #0 "
            cur_ottava = 0
        return f"{prefix}R1{header_markup}{dyn_markup}", cur_ottava

    # Group events by integer 32nd-note start tick (0..31)
    by_tick = {}
    for ev in sorted(events, key=lambda e: e.step):
        t_start = max(0, min(31, int(round(ev.step * 2))))
        t_dur = 1 if ev.duration < S else max(2, int(round(ev.duration * 2)))
        if t_start not in by_tick:
            by_tick[t_start] = [t_dur, set(ev.pitches), ev.rolled]
        else:
            by_tick[t_start][0] = min(by_tick[t_start][0], t_dur)
            by_tick[t_start][1].update(ev.pitches)
            by_tick[t_start][2] = by_tick[t_start][2] or ev.rolled

    sorted_ticks = sorted(by_tick.keys())
    tokens: List[str] = []
    cursor = 0
    attached_first = False

    # Switch 8va cleanly at measure boundary so beams are never split mid-measure
    if is_rh:
        bar_top_p = max(max(v[1]) for v in by_tick.values())
        desired_ottava = 1 if bar_top_p >= pitch("G6") else (0 if bar_top_p < pitch("F6") else cur_ottava)
        if desired_ottava != cur_ottava:
            tokens.append(f"\\ottava #{desired_ottava}")
            cur_ottava = desired_ottava

    for i, t_start in enumerate(sorted_ticks):
        if t_start > cursor:
            for r_idx, r_tok in enumerate(_rest_span_to_ly_tokens(cursor, t_start)):
                extra = ""
                if not attached_first and r_idx == 0:
                    extra = f"{header_markup}{dyn_markup}"
                    attached_first = True
                tokens.append(f"{r_tok}{extra}")
            cursor = t_start

        next_t = sorted_ticks[i + 1] if i + 1 < len(sorted_ticks) else 32
        avail = next_t - t_start
        raw_dur, pitch_set, rolled = by_tick[t_start]
        if raw_dur == 1:
            dur_ticks = 1
        else:
            dur_ticks = avail if avail <= raw_dur + 4 else min(avail, raw_dur)

        pitches = sorted(pitch_set)
        chord_str = _pitches_to_ly_chord(pitches)
        chunks = _ticks_to_ly_chunks(dur_ticks)
        arp_str = "\\arpeggio" if rolled and len(pitches) > 1 else ""

        for c_idx, c_tok in enumerate(chunks):
            extra = ""
            if c_idx == 0:
                extra += arp_str
                if not attached_first:
                    extra += f"{header_markup}{dyn_markup}"
                    attached_first = True
            tie_str = " ~" if (c_idx < len(chunks) - 1 or (i == len(sorted_ticks) - 1 and tie_at_end and cursor + dur_ticks == 32)) else ""
            tokens.append(f"{chord_str}{c_tok}{extra}{tie_str}")

        cursor += dur_ticks

    if cursor < 32:
        for r_tok in _rest_span_to_ly_tokens(cursor, 32):
            tokens.append(r_tok)
        cursor = 32

    assert cursor == 32, f"Measure tick sum mismatch: {cursor} != 32"
    return " ".join(tokens), cur_ottava


def build_lilypond_source(measures: List[Measure]) -> str:
    """Generate a complete, Classical-Urtext GNU LilyPond 2.24 score from the symbolic measures."""
    validate_score(measures)
    rh_bars, lh_bars, tie_rh_end = _prepare_engraving_measures(measures)

    rh_lines: List[str] = [
        "  \\clef treble",
        "  \\key c \\minor",
        "  \\numericTimeSignature",
        "  \\time 4/4",
        "  \\tempo \"I. Intro\" 4 = 120",
        "  \\partial 8 ees'''32([\\mp c''' bes'' g'']) |",
    ]
    lh_lines: List[str] = [
        "  \\clef bass",
        "  \\key c \\minor",
        "  \\numericTimeSignature",
        "  \\time 4/4",
        "  \\partial 8 r8 |",
    ]

    cur_sec = measures[0].section
    cur_bpm = measures[0].bpm
    cur_dyn = measures[0].dynamic
    cur_ottava = 0

    for idx, m in enumerate(measures):
        header_parts: List[str] = []
        if m.section != cur_sec:
            cur_sec = m.section
            cur_bpm = m.bpm
            rh_lines.append(f'  \\tempo "{m.section}" 4 = {m.bpm}')
        elif m.bpm != cur_bpm:
            cur_bpm = m.bpm
            rh_lines.append(f"  \\tempo 4 = {m.bpm}")

        # Chord symbol & Roman numeral above the measure
        safe_chord = m.chord_symbol.replace('"', "'")
        header_parts.append(
            f'^\\markup {{ \\override #\'(font-name . "Noto Sans CJK SC Bold") \\small "{safe_chord}" \\tiny " ({m.roman})" }}'
        )
        header_markup = "".join(header_parts)

        dyn_markup = ""
        if idx == 0 or m.dynamic != cur_dyn:
            cur_dyn = m.dynamic
            dyn_markup = f"\\{m.dynamic}" if idx > 0 else ""

        rh_measure_str, cur_ottava = _render_hand_measure_ly(
            rh_bars[idx],
            is_rh=True,
            tie_at_end=tie_rh_end[idx],
            header_markup=header_markup,
            dyn_markup=dyn_markup,
            cur_ottava=cur_ottava,
        )
        lh_measure_str, _ = _render_hand_measure_ly(
            lh_bars[idx],
            is_rh=False,
            tie_at_end=False,
            header_markup="",
            dyn_markup="",
            cur_ottava=0,
        )

        line_break = " \\break" if (m.bar_num % 4 == 0 and m.bar_num < len(measures)) else ""
        barline = ' \\bar "|."' if m.bar_num == len(measures) else " |"

        if m.bar_num == len(measures) and cur_ottava != 0:
            rh_measure_str += " \\ottava #0"
            cur_ottava = 0

        rh_lines.append(f"  % Bar {m.bar_num} ({m.chord_symbol})")
        rh_lines.append(f"  {rh_measure_str}{barline}{line_break}")
        lh_lines.append(f"  % Bar {m.bar_num}")
        lh_lines.append(f"  {lh_measure_str}{barline}")

    ly_doc = f"""\\version "2.24.1"

#(set-global-staff-size 18)

\\header {{
  title = \\markup {{ \\override #'(font-name . "Noto Serif CJK SC Bold") \\abs-fontsize #22 "Extraordinary 「不凡」" }}
  subtitle = \\markup {{ \\override #'(font-name . "Noto Sans CJK SC Medium") \\abs-fontsize #13 "A Mortal's Journey to Immortality (凡人修仙傳 · 韓立元嬰突破版) — Concert Piano Reduction" }}
  subsubtitle = \\markup {{ \\abs-fontsize #10 "First-Principles Mathematical & Musical Reduction (C Minor / C Dorian IV) · Source: https://youtu.be/JB31Aq_5Slw" }}
  composer = \\markup {{ \\override #'(font-name . "Noto Sans CJK SC") "Original: Wang Zhengliang (王錚亮) & Yusheng · Piano Arrangement: Ru's Piano" }}
  arranger = \\markup {{ \\italic "Transcribed & Engraved from First Principles with Gemini 4 Argon high in Antigravity CLI" }}
  tagline = ##f
}}

\\paper {{
  page-breaking = #ly:one-page-breaking
  paper-width = 240\\mm
  top-margin = 14\\mm
  bottom-margin = 14\\mm
  left-margin = 14\\mm
  right-margin = 14\\mm
  indent = 0\\mm
  system-system-spacing.basic-distance = #15
  system-system-spacing.padding = #3.5
  score-Markup-spacing.basic-distance = #10
}}

upper = {{
{chr(10).join(rh_lines)}
}}

lower = {{
{chr(10).join(lh_lines)}
}}

\\score {{
  \\new PianoStaff \\with {{
    instrumentName = \\markup {{ \\bold "Piano" }}
    \\accidentalStyle piano
  }} <<
    \\new Staff = "upper" \\upper
    \\new Staff = "lower" \\lower
  >>
  \\layout {{
    \\context {{
      \\Score
      \\override BarNumber.break-visibility = ##(#f #t #t)
      \\override BarNumber.font-size = #1
      \\override RehearsalMark.font-size = #1
    }}
  }}
}}
"""
    return ly_doc


def export_sheet_music_png(measures: List[Measure], out_png_path: str) -> None:
    """
    Compile the symbolic score to GNU LilyPond vector PDF on a single continuous
    tall page, rasterize at supersampled 400 DPI via Poppler `pdftoppm`, and
    downsample with Lanczos-3 anti-aliasing to a crisp 2400px-wide tall PNG.
    """
    Image.MAX_IMAGE_PIXELS = None
    ly_source = build_lilypond_source(measures)

    with tempfile.TemporaryDirectory(prefix="extraordinary_sheet_") as tmpdir:
        ly_path = os.path.join(tmpdir, "extraordinary_score.ly")
        pdf_prefix = os.path.join(tmpdir, "extraordinary_score")
        pdf_path = f"{pdf_prefix}.pdf"
        raw_png_prefix = os.path.join(tmpdir, "supersampled_raw")
        raw_png_path = f"{raw_png_prefix}.png"

        with open(ly_path, "w", encoding="utf-8") as f:
            f.write(ly_source)

        subprocess.run(
            ["lilypond", "--pdf", "-dno-point-and-click", "-o", pdf_prefix, ly_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        assert os.path.isfile(pdf_path) and os.path.getsize(pdf_path) > 10_000, "LilyPond PDF generation failed"

        # Rasterize vector PDF at supersampled 400 DPI
        subprocess.run(
            ["pdftoppm", "-png", "-r", "400", "-singlefile", pdf_path, raw_png_prefix],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        assert os.path.isfile(raw_png_path), "pdftoppm supersampled rasterization failed"

        # 2x supersampled Lanczos-3 anti-aliased downsample to 2400 px width
        with Image.open(raw_png_path) as img:
            img_rgb = img.convert("RGB")
            w_raw, h_raw = img_rgb.size
            assert w_raw > 3000 and h_raw > 10000, f"Unexpected raw sheet size: {w_raw}x{h_raw}"
            target_w = 2400
            target_h = int(round(h_raw * (target_w / float(w_raw))))
            downsampled = img_rgb.resize((target_w, target_h), resample=Image.Resampling.LANCZOS)
            downsampled.save(out_png_path, format="PNG", optimize=True, compress_level=9)

    assert os.path.isfile(out_png_path) and os.path.getsize(out_png_path) > 500_000, f"PNG output invalid: {out_png_path}"


if __name__ == "__main__":
    score = build_score()
    compile_to_midi(score, "extraordinary.mid")
    export_markdown_score(score, "CHORD_REDUCTION_SCORE.md")
    export_sheet_music_png(score, "extraordinary_sheet_music.png")
    synthesize_and_master_audio("extraordinary.mid", "extraordinary.mp3")
    print(
        "Successfully compiled extraordinary.mid, CHORD_REDUCTION_SCORE.md, "
        "extraordinary_sheet_music.png, and 96 kHz mastered extraordinary.mp3."
    )

