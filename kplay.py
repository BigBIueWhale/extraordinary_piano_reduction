#!/usr/bin/env python3
"""
kplay — player for `extraordinary.k`, the complete musical content of
"Extraordinary (不凡)" in a few hundred bytes.

`extraordinary.k` is a raw arithmetic-coded bitstream. It carries every note,
rhythm, tie, chord roll, tempo marking, dynamic, pedal change and fermata of
all 116 measures, and nothing else: no header, no magic number, no piece-
specific code. This player knows only general music and coding machinery:

  * a 12-bit pitch-class mask (read from the file) turns MIDI pitches into
    diatonic scale degrees, so transposed repeats look identical;
  * each hand is one continuous stream of events anchored on their highest
    note: (rest before, duration, interval to the previous anchor, chord shape
    below the anchor, rolled flag);
  * an event run can be copied from D bars earlier with a diatonic
    transposition T, which is how verses, choruses and accompaniment
    patterns repeat;
  * every decision is one binary symbol, predicted by logistic mixing of a
    few musical contexts (position in the bar, previous duration, previous
    intervals, previous chord shape) and coded with a 32-bit binary
    arithmetic coder. All arithmetic is integer, so decoding is identical on
    every platform.

The rendering half (Virtual Pianist MIDI, LilyPond engraving, 96 kHz
mastering) is reused unchanged from `extraordinary_reduction.py`, while
`build_score()` and its piece-specific functors are never called on that path.
Tempo comes from the file's own BPM markings, not from the YouTube recording.

The optional `extraordinary.labels` sidecar holds the printed text (title,
section names, chord symbols, Roman numerals). It is plain text, it is not
needed for the music, and it is not counted in the file size.

Usage:
  python3 kplay.py [extraordinary.k]   # -> extraordinary_k.{mid,ly,mp3} + extraordinary_k_sheet_music.png
  python3 kplay.py --no-audio          # MIDI, LilyPond source and sheet music only
  python3 kplay.py --midi-only         # MIDI and LilyPond source only (no LilyPond/FluidSynth needed)
  python3 kplay.py --no-labels         # music only: no title block, section names or chord symbols
  python3 kplay.py --encode            # rebuild extraordinary.k + .labels from extraordinary_reduction.build_score()
  python3 kplay.py --verify            # prove that the decoded file equals build_score(), note for note
"""

import argparse
import math
import os
import sys
from typing import Dict, List, NamedTuple, Optional, Tuple

# =============================================================================
# 1. BINARY ARITHMETIC CODER WITH LOGISTIC CONTEXT MIXING (integer-only)
# =============================================================================

_SQUASH_KNOTS = (
    1, 2, 3, 6, 10, 16, 27, 45, 73, 120, 194, 310, 488, 747, 1101, 1546, 2047,
    2549, 2994, 3348, 3607, 3785, 3901, 3975, 4022, 4050, 4068, 4079, 4085, 4089, 4092, 4093, 4094,
)


def squash(d: int) -> int:
    """Logistic function 4096 / (1 + e^(-d/256)) by integer interpolation."""
    if d > 2047:
        return 4095
    if d < -2047:
        return 1
    w = d & 127
    i = (d >> 7) + 16
    return (_SQUASH_KNOTS[i] * (128 - w) + _SQUASH_KNOTS[i + 1] * w + 64) >> 7


def _build_stretch_table() -> List[int]:
    """Inverse of squash: probability (12-bit) -> logit."""
    table = [2047] * 4096
    pi = 0
    for x in range(-2047, 2048):
        v = squash(x)
        for j in range(pi, v + 1):
            table[j] = x
        pi = v + 1
    return table


STRETCH = _build_stretch_table()

MIX_LEARNING_RATE = 5
MIX_INITIAL_WEIGHT = 40000
STATE_COUNT_LIMIT = 30


class Coder:
    """Encodes when constructed without data, decodes when given the bitstream."""

    def __init__(self, data: Optional[bytes] = None):
        self.encoding = data is None
        self.x1, self.x2 = 0, 0xFFFFFFFF
        self.states: Dict[tuple, List[int]] = {}
        self.mixers: Dict[tuple, List[int]] = {}
        self.bits: Dict[str, float] = {}
        self.out = bytearray()
        if not self.encoding:
            self.data, self.pos, self.x = data, 0, 0
            for _ in range(4):
                self.x = (self.x << 8) | self._next_byte()

    def _next_byte(self) -> int:
        b = self.data[self.pos] if self.pos < len(self.data) else 0xFF
        self.pos += 1
        return b

    def bit(self, mixer_key: tuple, contexts: List[tuple], y: Optional[int] = None) -> int:
        states = [self.states.setdefault(cx, [32768, 0]) for cx in contexts]
        inputs = [STRETCH[s[0] >> 4] for s in states] + [256]
        weights = self.mixers.get(mixer_key)
        if weights is None:
            weights = self.mixers[mixer_key] = [MIX_INITIAL_WEIGHT // len(contexts)] * len(contexts) + [0]
        p = min(4095, max(1, squash(sum(w * x for w, x in zip(weights, inputs)) >> 16)))

        xmid = self.x1 + ((self.x2 - self.x1) >> 12) * p
        if self.encoding:
            field = str(mixer_key[0]).rstrip("+-")
            self.bits[field] = self.bits.get(field, 0.0) - math.log2((p if y else 4096 - p) / 4096)
        else:
            y = int(self.x <= xmid)
        if y:
            self.x2 = xmid
        else:
            self.x1 = xmid + 1
        while ((self.x1 ^ self.x2) & 0xFF000000) == 0:
            if self.encoding:
                self.out.append(self.x2 >> 24)
            else:
                self.x = ((self.x << 8) & 0xFFFFFFFF) | self._next_byte()
            self.x1 = (self.x1 << 8) & 0xFFFFFFFF
            self.x2 = ((self.x2 << 8) & 0xFFFFFFFF) | 0xFF

        err = ((y << 12) - p) * MIX_LEARNING_RATE
        for i, x in enumerate(inputs):
            weights[i] += (x * err) >> 10
        for s in states:
            s[0] = min(65503, max(32, s[0] + ((y << 16) - s[0]) * 2 // (2 * s[1] + 3)))
            s[1] = min(STATE_COUNT_LIMIT, s[1] + 1)
        return y

    def uint(self, key: str, features: List[tuple], v: Optional[int] = None) -> int:
        """Non-negative integer: Elias-gamma bit length (unary), then mantissa bits."""
        n_bits = None if v is None else (v + 1).bit_length()
        k = 1
        while self.bit((key, 'L', k), [(key, f, 'L', k) for f in features], None if v is None else int(n_bits > k)):
            k += 1
        val = 1
        for i in range(k - 2, -1, -1):
            node = ('M', k, val)
            val = (val << 1) | self.bit((key, 'M'), [(key, f, node) for f in features],
                                        None if v is None else ((v + 1) >> i) & 1)
        return val - 1

    def sint(self, key: str, features: List[tuple], v: Optional[int] = None) -> int:
        """Signed integer: zero flag, sign, magnitude."""
        if self.bit((key, 'z'), [(key, f, 'z') for f in features], None if v is None else int(v == 0)):
            return 0
        neg = self.bit((key, 's'), [(key, f, 's') for f in features], None if v is None else int(v < 0))
        mag = self.uint(key + ('-' if neg else '+'), features, None if v is None else abs(v) - 1) + 1
        return -mag if neg else mag

    def finish(self) -> bytes:
        self.out.append(self.x1 >> 24)
        while self.out and self.out[-1] == 0xFF:   # the decoder pads with 0xFF
            self.out.pop()
        return bytes(self.out)


# =============================================================================
# 2. THE MUSIC MODEL (one routine drives both encoding and decoding)
# =============================================================================

TICKS_PER_BAR = 32                       # 32nd notes in a 4/4 bar
DYNAMICS = ("pp", "p", "mp", "mf", "f", "ff")
MIN_COPY = 3


class Song(NamedTuple):
    """Everything in the file. Times are in 32nd-note ticks from the downbeat of bar 1."""
    scale_mask: int                                              # pitch classes of the key
    start: int                                                   # first tick (negative = pickup)
    hands: Tuple[List[Tuple[int, int, Tuple[int, ...], bool]], ...]  # (LH, RH): (onset, duration, pitches, rolled)
    bars: List[Tuple[int, int, Tuple[int, ...], bool]]           # (bpm, dynamic index, pedal ticks, fermata)


def _scale_degrees(scale: List[int]):
    def to_degree(p: int) -> Tuple[int, int]:
        pc, octave = p % 12, p // 12
        if pc in scale:
            return 7 * octave + scale.index(pc), 0
        assert pc - 1 in scale, f"pitch class {pc} is neither in the scale nor a raised scale note"
        return 7 * octave + scale.index(pc - 1), 1

    def to_pitch(degree: int, raised: int) -> int:
        return 12 * (degree // 7) + scale[degree % 7] + raised
    return to_degree, to_pitch


def _relative(ev, cursor: int, to_degree):
    """(rest before, duration, anchor degree, anchor raised, shape below anchor, rolled)."""
    onset, dur, pitches, rolled = ev
    anchor, raised = to_degree(pitches[-1])
    shape = tuple((to_degree(p)[0] - anchor, to_degree(p)[1]) for p in pitches[:-1])
    return onset - cursor, dur, anchor, raised, shape, rolled


def _longest_copy(evs, i, cursor, aref, history, to_degree):
    """Encoder only: best (bars back, transposition, length) copy for events[i:], or None."""
    best = None
    first = _relative(evs[i], cursor, to_degree)
    for bars_back in range(1, cursor // TICKS_PER_BAR + 2):
        src = next((j for j, h in enumerate(history) if h[0] == cursor - TICKS_PER_BAR * bars_back), None)
        if src is None:
            continue
        for transpose in sorted({0, first[2] - history[src][3]}):
            length, cc = 0, cursor
            while i + length < len(evs) and src + length < len(history):
                _, gap, dur, anc, raised, shape, rolled = history[src + length]
                if _relative(evs[i + length], cc, to_degree) != (gap, dur, anc + transpose, raised, shape, rolled):
                    break
                cc = evs[i + length][0] + evs[i + length][1]
                length += 1
            better = best is None or length > best[2] or (length == best[2] and transpose == 0 and best[1] != 0)
            if length >= MIN_COPY and better:
                best = (bars_back, transpose, length)
    return best


def transcode(c: Coder, song: Optional[Song] = None) -> Song:
    """Encode `song` into `c`, or (song=None) decode a Song from `c`."""
    enc = song is not None
    known = (lambda f: f()) if enc else (lambda f: None)

    mask = 0
    for pc in range(12):
        mask |= c.bit(('hdr',), [('scale', pc)], known(lambda: (song.scale_mask >> pc) & 1)) << pc
    to_degree, to_pitch = _scale_degrees([pc for pc in range(12) if mask >> pc & 1])
    start = c.sint('hdr', [()], known(lambda: song.start))

    hands = []
    for h in (0, 1):
        evs = song.hands[h] if enc else None
        n = c.uint('count', [(h,)], known(lambda: len(evs)))
        cursor, aref = start, to_degree(60)[0]
        prev_dur, prev_dd, prev_dd2, prev_shape = 4, 0, 0, ()
        shapes = [()]                                   # move-to-front list of chord shapes
        last_copy, last_bars_back, last_transpose = 0, 4, 0
        history = []                                    # (cursor, gap, dur, anchor, raised, shape, rolled)
        out = []

        def emit(gap, dur, anchor, raised, shape, rolled):
            nonlocal cursor, aref, prev_dur, prev_dd, prev_dd2, prev_shape
            onset = cursor + gap
            pitches = tuple(sorted([to_pitch(anchor, raised)] + [to_pitch(anchor + o, r) for o, r in shape]))
            if enc:
                assert (onset, dur, pitches, rolled) == evs[len(out)], "model failed to reproduce the score"
            history.append((cursor, gap, dur, anchor, raised, shape, rolled))
            out.append((onset, dur, pitches, rolled))
            if shape in shapes:
                shapes.remove(shape)
            shapes.insert(0, shape)
            prev_dd2, prev_dd = prev_dd, anchor - aref
            cursor, aref, prev_dur, prev_shape = onset + dur, anchor, dur, shape

        while len(out) < n:
            i = len(out)
            phase = cursor % TICKS_PER_BAR
            best = _longest_copy(evs, i, cursor, aref, history, to_degree) if enc else None
            if c.bit(('copy', h), [(h, phase == 0, last_copy), (h, phase)], known(lambda: int(best is not None))):
                bars_back = c.uint('bars', [(h,), (h, last_bars_back)], known(lambda: best[0] - 1)) + 1
                transpose = c.sint('trans', [(h,), (h, last_transpose)], known(lambda: best[1]))
                length = c.uint('len', [(h,), (h, bars_back)], known(lambda: best[2] - MIN_COPY)) + MIN_COPY
                src = next(j for j, hh in enumerate(history) if hh[0] == cursor - TICKS_PER_BAR * bars_back)
                for k in range(length):
                    _, gap, dur, anchor, raised, shape, rolled = history[src + k]
                    emit(gap, dur, anchor + transpose, raised, shape, rolled)
                last_copy, last_bars_back, last_transpose = 1, bars_back, transpose
                continue
            last_copy = 0

            rel = None
            if enc:
                gap, dur, anchor, raised, shape, rolled = _relative(evs[i], cursor, to_degree)
                rel = (gap, dur, anchor - aref, raised, shape, rolled)
            gap = c.sint('gap', [(h, phase == 0), (h, phase)], known(lambda: rel[0]))
            pos = (cursor + gap) % TICKS_PER_BAR
            dur = c.uint('dur', [(h, prev_dur), (h, pos), (h, pos % 8, prev_dur), (h, prev_shape)],
                         known(lambda: rel[1]))
            dd = c.sint('pitch', [(h,), (h, prev_dd), (h, prev_dd, prev_dd2), (h, pos), (h, aref % 7), (h, dur)],
                        known(lambda: rel[2]))
            raised = c.bit(('raised', h), [(h, (aref + dd) % 7)], known(lambda: rel[3]))

            idx = (shapes.index(rel[4]) if rel[4] in shapes else len(shapes)) if enc else None
            k = 0
            while k < len(shapes) and not c.bit(('shape', h), [(h, min(k, 8)), (h, k, prev_shape), (h, k, dur), (h, k, pos)],
                                                known(lambda: int(idx == k))):
                k += 1
            if k < len(shapes):
                shape = shapes[k]
            else:
                size = c.uint('newshape', [(h,)], known(lambda: len(rel[4])))
                notes, prev_off = [], 0
                for j in range(size):
                    off = c.uint('below', [(h,), (h, prev_off)], known(lambda: -rel[4][j][0] - 1)) + 1
                    notes.append((-off, c.bit(('below_raised', h), [(h,)], known(lambda: rel[4][j][1]))))
                    prev_off = off
                shape = tuple(sorted(notes))
            rolled = bool(c.bit(('roll', h), [(h, len(shape)), (h, dur)], known(lambda: int(rel[5])))) if shape else False
            emit(gap, dur, aref + dd, raised, shape, rolled)
        hands.append(out)

    n_bars = max(ev[0] for hs in hands for ev in hs) // TICKS_PER_BAR + 1
    bars = []
    bpm, dyn, pedal_patterns = 120, 3, [(0,)]
    for b in range(n_bars):
        bar = song.bars[b] if enc else None
        same_bpm = c.bit(('bpm=',), [()], known(lambda: int(bar[0] == bpm)))
        if not same_bpm:
            bpm += c.sint('bpm', [()], known(lambda: bar[0] - bpm))
        if not c.bit(('dyn=',), [(same_bpm,)], known(lambda: int(bar[1] == dyn))):
            dyn += c.sint('dyn', [()], known(lambda: bar[1] - dyn))
        idx = (pedal_patterns.index(bar[2]) if bar[2] in pedal_patterns else len(pedal_patterns)) if enc else None
        k = 0
        while k < len(pedal_patterns) and not c.bit(('pedal',), [(min(k, 4),)], known(lambda: int(idx == k))):
            k += 1
        if k < len(pedal_patterns):
            pedals = pedal_patterns.pop(k)
        else:
            size = c.uint('pedal_n', [()], known(lambda: len(bar[2])))
            pedals = tuple(c.uint('pedal_at', [()], known(lambda: bar[2][j])) for j in range(size))
        pedal_patterns.insert(0, pedals)
        fermata = bool(c.bit(('fermata',), [()], known(lambda: int(bar[3]))))
        bars.append((bpm, dyn, pedals, fermata))
    return Song(mask, start, tuple(hands), bars)


def encode(song: Song) -> Tuple[bytes, Dict[str, float]]:
    c = Coder()
    transcode(c, song)
    data = c.finish()
    assert decode(data) == song, "round trip failed"
    return data, c.bits


def decode(data: bytes) -> Song:
    return transcode(Coder(data))


# =============================================================================
# 3. SONG <-> MEASURES, LABELS, AND THE FILE'S OWN TEMPO MAP
# =============================================================================

LABEL_HEADER_KEYS = ("title", "subtitle", "subsubtitle", "composer", "arranger")


def _num(ticks: int):
    """32nd-note ticks -> 16th-note units, keeping integers integral."""
    return ticks // 2 if ticks % 2 == 0 else ticks / 2


def song_to_measures(song: Song, labels: Optional[dict] = None):
    from extraordinary_reduction import Event, Measure
    rows = (labels or {}).get("bars", {})
    measures = []
    for b, (bpm, dyn, pedals, fermata) in enumerate(song.bars):
        section, chord, roman = rows.get(b + 1, ("", "", ""))
        measures.append(Measure(b + 1, section, chord, roman, bpm, DYNAMICS[dyn],
                                pedal_steps=[_num(t) for t in pedals], fermata=fermata))
    for h, attr in ((0, "lh"), (1, "rh")):
        for onset, dur, pitches, rolled in song.hands[h]:
            b = max(0, onset // TICKS_PER_BAR)
            getattr(measures[b], attr).append(
                Event(_num(onset - TICKS_PER_BAR * b), _num(dur), list(pitches), rolled))
    return measures


def measures_to_song(measures) -> Song:
    hands = ([], [])
    for b, m in enumerate(measures):
        for h, evs in enumerate((m.lh, m.rh)):
            for e in evs:
                hands[h].append((b * TICKS_PER_BAR + int(round(e.step * 2)), int(round(e.duration * 2)),
                                 tuple(sorted(e.pitches)), bool(e.rolled)))
    for hs in hands:
        hs.sort(key=lambda ev: ev[0])
        assert all(a[0] < b[0] for a, b in zip(hs, hs[1:])), "two events of one hand share an onset"
    pcs = {p % 12 for hs in hands for ev in hs for p in ev[2]}
    mask = sum(1 << pc for pc in (0, 2, 3, 5, 7, 8, 10))     # C natural minor (+ raised notes)
    assert all((mask >> pc & 1) or (mask >> (pc - 1) & 1) for pc in pcs)
    bars = [(m.bpm, DYNAMICS.index(m.dynamic), tuple(int(round(s * 2)) for s in m.pedal_steps), bool(m.fermata))
            for m in measures]
    start = min(hs[0][0] for hs in hands if hs)
    return Song(mask, start, hands, bars)


def read_labels(path: Optional[str]) -> Optional[dict]:
    if not path or not os.path.isfile(path):
        return None
    header, bars = {}, {}
    with open(path, encoding="utf-8") as f:
        section = ""
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            key, *rest = line.split("\t")
            if key in LABEL_HEADER_KEYS:
                header[key] = rest[0]
            else:
                new_section, chord, roman = rest
                section = new_section or section
                bars[int(key)] = (section, chord, roman)
    return {"header": header, "bars": bars}


def write_labels(path: str, measures, header: Dict[str, str]) -> None:
    lines = ["# Optional printed text for extraordinary.k (title block, section names, chord symbols).",
             "# Not needed for the music; kplay.py uses it when present. Tab-separated."]
    lines += [f"{k}\t{header[k]}" for k in LABEL_HEADER_KEYS]
    prev = None
    for m in measures:
        lines.append(f"{m.bar_num}\t{m.section if m.section != prev else ''}\t{m.chord_symbol}\t{m.roman}")
        prev = m.section
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


class TempoMap:
    """t(g): seconds at 16th-note position g, integrated from each bar's own BPM marking."""

    def __init__(self, bpms: List[int], first_g: float = -2.0, lead_in: float = 0.5):
        self.bar_sec = [240.0 / bpm for bpm in bpms]                 # 4 quarter beats per bar
        self.t0 = lead_in - first_g / 16.0 * self.bar_sec[0]         # time of bar 1's downbeat
        self.starts = [self.t0]
        for sec in self.bar_sec:
            self.starts.append(self.starts[-1] + sec)

    def __call__(self, g: float) -> float:
        b = min(max(int(g // 16), 0), len(self.bar_sec) - 1)
        return self.starts[b] + (g - 16.0 * b) / 16.0 * self.bar_sec[b]


# =============================================================================
# 4. COMMAND LINE
# =============================================================================

HERE = os.path.dirname(os.path.abspath(__file__))


def cmd_encode(k_path: str, labels_path: str) -> None:
    import extraordinary_reduction as er
    measures = er.build_score()
    data, bits = encode(measures_to_song(measures))
    with open(k_path, "wb") as f:
        f.write(data)
    write_labels(labels_path, measures, er.SCORE_HEADER)
    song = decode(data)
    print(f"{os.path.basename(k_path)}: {len(data)} bytes = {len(measures)} bars, "
          f"{sum(len(h) for h in song.hands)} events, {sum(len(e[2]) for h in song.hands for e in h)} notes")
    for field, b in sorted(bits.items(), key=lambda kv: -kv[1]):
        print(f"  {field:<14s}{b / 8:6.1f} bytes")
    print(f"{os.path.basename(labels_path)}: {os.path.getsize(labels_path)} bytes of optional printed text")


def cmd_verify(k_path: str, labels_path: str) -> None:
    import tempfile
    import extraordinary_reduction as er
    with open(k_path, "rb") as f:
        data = f.read()
    song = decode(data)
    original = er.build_score()
    decoded = song_to_measures(song, read_labels(labels_path))

    def canon(ms):
        return [(m.bar_num, m.section, m.chord_symbol, m.roman, m.bpm, m.dynamic, list(m.pedal_steps), m.fermata,
                 [sorted((e.step, e.duration, sorted(e.pitches), e.rolled) for e in hand) for hand in (m.lh, m.rh)])
                for m in ms]
    assert canon(decoded) == canon(original), "decoded score differs from build_score()"
    n_notes = sum(len(e.pitches) for m in decoded for e in m.lh + m.rh)
    print(f"[ok] {os.path.basename(k_path)} ({len(data)} bytes) decodes to all {len(decoded)} bars / {n_notes} notes of build_score()")

    assert er.build_lilypond_source(decoded) == er.build_lilypond_source(original)
    print("[ok] LilyPond sheet-music source is identical")

    with tempfile.TemporaryDirectory() as tmp:
        tempo = TempoMap([m.bpm for m in decoded])
        a, b = os.path.join(tmp, "a.mid"), os.path.join(tmp, "b.mid")
        er.compile_to_midi(decoded, a, t_of_g=tempo)
        er.compile_to_midi(original, b, t_of_g=tempo)
        assert open(a, "rb").read() == open(b, "rb").read()
        print("[ok] MIDI performance from the file's own tempo marks is byte-identical")

        video = os.path.join(HERE, "original_from_youtube.mp4")
        if os.path.isfile(video):
            t_map, _ = er.build_dynamic_time_map(decoded, video)
            er.compile_to_midi(decoded, a, t_of_g=t_map)
            same = open(a, "rb").read() == open(os.path.join(HERE, "extraordinary.mid"), "rb").read()
            assert same, "decoded score + YouTube rubato map does not reproduce extraordinary.mid"
            print("[ok] with the YouTube rubato map it reproduces the committed extraordinary.mid byte for byte")


def cmd_play(k_path: str, labels_path: str, out_prefix: str, audio: bool, engrave: bool) -> None:
    with open(k_path, "rb") as f:
        song = decode(f.read())
    labels = read_labels(labels_path)
    measures = song_to_measures(song, labels)
    header = labels["header"] if labels else {"title": os.path.splitext(os.path.basename(k_path))[0]}

    import extraordinary_reduction as er
    mid, ly = f"{out_prefix}.mid", f"{out_prefix}.ly"
    er.compile_to_midi(measures, mid, t_of_g=TempoMap([m.bpm for m in measures]))
    with open(ly, "w", encoding="utf-8") as f:
        f.write(er.build_lilypond_source(measures, header=header))
    print(f"wrote {mid}, {ly}")
    if engrave:
        png = f"{out_prefix}_sheet_music.png"
        er.export_sheet_music_png(measures, png, header=header)
        print(f"wrote {png}")
    if audio:
        mp3 = f"{out_prefix}.mp3"
        er.synthesize_and_master_audio(mid, mp3)
        print(f"wrote {mp3}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("k_file", nargs="?", default=os.path.join(HERE, "extraordinary.k"))
    ap.add_argument("--labels", help="printed-text sidecar (default: <k_file stem>.labels if present)")
    ap.add_argument("--no-labels", action="store_true", help="engrave the music without any printed text")
    ap.add_argument("--out", help="output prefix (default: <k_file stem>_k)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--encode", action="store_true", help="rebuild the .k file and labels from build_score()")
    mode.add_argument("--verify", action="store_true", help="check the .k file against build_score()")
    mode.add_argument("--no-audio", action="store_true", help="skip FluidSynth synthesis and mastering")
    mode.add_argument("--midi-only", action="store_true", help="write MIDI and LilyPond source only")
    args = ap.parse_args()

    stem = os.path.splitext(args.k_file)[0]
    labels = args.labels or f"{stem}.labels"
    sys.path.insert(0, HERE)
    if args.encode:
        cmd_encode(args.k_file, labels)
    elif args.verify:
        cmd_verify(args.k_file, labels)
    else:
        cmd_play(args.k_file, None if args.no_labels else labels, args.out or f"{stem}_k",
                 audio=not (args.no_audio or args.midi_only), engrave=not args.midi_only)


if __name__ == "__main__":
    main()
