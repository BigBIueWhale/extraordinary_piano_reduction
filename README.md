# Extraordinary (不凡) — First-Principles Piano Reduction ("PNG → SVG")

> **Created with Gemini 4 Argon high in Antigravity CLI** — combining innate multimodal audio perception with pure first-principles music-theoretic reduction and a 96 kHz / 64-bit float physical concert-grand mastering pipeline.

- 📱 **Watch the Portrait Mobile Showcase Video (`1080 × 1920`, `9:16`)**: **[`extraordinary_showcase.mp4`](extraordinary_showcase.mp4)** *(Top: 1080p YouTube performance; Middle: Studio HUD & Showmanship A/B Audio Switcher; Bottom: Calm 5-system sheet music with Premultiplied-Alpha "Breeze of Air" visualization, dynamically synchronized & K-weighted loudness-normalized at `-14.0 LUFS`)*
- 🎧 **Listen to the Final Rendered Audio**: **[`extraordinary.mp3`](extraordinary.mp3)** *(48 kHz LAME V0 stereo master, dynamically synchronized & rendered via [`render_in_docker.sh`](render_in_docker.sh) & [`Dockerfile`](Dockerfile))*
- 🎼 **Full-Length Classical Piano Sheet Music (Supersampled Tall PNG)**: **[`extraordinary_sheet_music.png`](extraordinary_sheet_music.png)** *(Engraved via GNU LilyPond 2.24.1 on a continuous `ly:one-page-breaking` canvas, rasterized at 400 DPI & Lanczos-3 supersampled)*
- 🎹 **Playable First-Principles MIDI**: **[`extraordinary.mid`](extraordinary.mid)**
- 🧬 **The Whole Piece in 765 Bytes**: **[`extraordinary.k`](extraordinary.k)** *(every note, rhythm, tempo, dynamic and pedal of all 116 bars; [`kplay.py`](kplay.py) turns it back into MIDI, sheet music and audio on its own, e.g. [`extraordinary_k.mp3`](extraordinary_k.mp3). See [The Whole Piece in 765 Bytes](#the-whole-piece-in-765-bytes-extraordinaryk))*
- 📜 **Complete Bar-by-Bar Symbolic Score**: **[`CHORD_REDUCTION_SCORE.md`](CHORD_REDUCTION_SCORE.md)**
- 🎬 **Source Performance**: [A Mortal's Journey「不凡 Extraordinary」Ru's Piano Cover (YouTube)](https://youtu.be/JB31Aq_5Slw) *(single non-duplicated 1080p MP4 reference [`original_from_youtube.mp4`](original_from_youtube.mp4) included strictly for musical research, dynamic time alignment, A/B comparison, and archival backup purposes)*
- ⚙️ **Unified Generator, Dynamic Rubato Aligner, LilyPond Engraver, 96 kHz Mastering & Video Engine**: **[`extraordinary_reduction.py`](extraordinary_reduction.py)**
- 🚀 **Do It Yourself with OpenRouter (Step-by-Step Agentic Blueprint)**: **[`OPENROUTER_GUIDE.md`](OPENROUTER_GUIDE.md)** *(Complete guide, standalone Python multimodal OpenRouter agent, 7-stage DSP/LilyPond/video architecture breakdown, and copy-paste master prompt)*
- ⚡ **Zero-BS TL;DR (How the Notes Were Actually Transcribed)**: **[`TLDR.md`](TLDR.md)**
- 🔍 **Forensic Documentation of the Transcription & Tool Workflow**: **[`TRANSCRIPTION_WORKFLOW.md`](TRANSCRIPTION_WORKFLOW.md)** *(Step-indexed audit from `transcript_full.jsonl` documenting exact model inputs, `transkun` neural AMT seeding, `librosa.cqt` verification rounds, LilyPond visual audits, and OpenRouter reproduction requirements)*

---

## 1. Philosophy: Intelligence as Compression ("PNG → SVG")

> *"Compression is the mathematical definition of intelligence: to understand a signal is to discover the shortest generative program that reproduces it from first principles."*

Most automated or reverse-engineered MIDI transcriptions treat a musical performance like a raster image (**PNG**): they scrape arrays of floating-point onset timestamps (`[0.81, 2.73, 4.72, ...]`), arbitrary fractional note durations, and per-note MIDI velocities (`61, 60, 57, 72...`). The result is brittle, opaque, and machine-generated.

This repository treats transcription as a **Kolmogorov reduction into symbolic primitives ("SVG")**. Rather than hard-coding scraped per-note floating-point timings or velocity tables, [`extraordinary_reduction.py`](extraordinary_reduction.py) constructs all 116 measures (2,104 notes) of the arrangement from **first principles of music theory, compositional form, and piano performance** in a single canonical, defensively verified pipeline with zero fallbacks:

1. **Pure `"1 e & a"` Rhythmic Algebra & 1:1 Sheet-Music Bijection**: Every note onset and duration in the symbolic score is expressed in exact rational subdivisions of a $4/4$ measure:
   $$\text{W}=16,\quad \text{DH}=12,\quad \text{H}=8,\quad \text{DQ}=6,\quad \text{Q}=4,\quad \text{DE}=3,\quad \text{E}=2,\quad \text{S}=1,\quad \text{T}=0.5$$
   on the standard 16th-note grid (`B1, B1_E, B1_AND, B1_A, B2, ...`). The piece's signature **tresillo (`3 + 3 + 2`)** syncopation falls naturally on `(B1, B1_A, B2_AND)` and `(B3, B3_A, B4_AND)`, cross-barline syncopations (`ev.step + ev.duration > W`) partition cleanly across barlines with ties (`~`), and every symbolic note duration matches its engraved sheet-music notation 1-to-1 (`assert dur_ticks == avail`).
2. **Continuous Dynamic Rubato Synchronization (`build_dynamic_time_map`)**: To lock our synthesized audio and visual notehead tracking onto Ru's continuous expressive rubato in [`original_from_youtube.mp4`](original_from_youtube.mp4) without phase-vocoder pitch artifacts, `build_dynamic_time_map()` extracts multi-band spectral onset flux (`50–350 Hz` bass + `350–4,200 Hz` treble at `5 ms` hop) from the reference video and runs Viterbi dynamic programming across all **930 eighth-note sub-bar grid positions** (`116` bars $\times 8$ eighth notes), fitting a strictly monotonic $C^1$-continuous Hermite spline (`scipy.interpolate.PchipInterpolator`) $t(g)$ prior to 96 kHz synthesis.
3. **Universal Solo-Piano Playability (`<= 1 Octave` Unrolled Hand Span)**: Every unrolled chord or interval across all 116 measures in both hands spans at most one octave (`max(p) - min(p) <= 12`, enforced in `validate_score()`), while wide-span lyrical chords are explicitly marked `Roll(...)` (`\arpeggio`).
4. **Zero Hard-Coded Velocities (Virtual Pianist Model)**: Expressive dynamics are derived from section markings (`pp, p, mp, mf, f, ff`), left/right-hand balance (`-12` velocity on LH accompaniment), metric accent hierarchy, soprano top-voice projection (`+4` velocity on top voice), *legatissimo* finger-overlap on 32nd-note pentatonic cascades (`gate = 1.45` on `T = 0.5`), syncopated legato sustain pedaling (`CC64` released `35 ms` before harmonic change and caught `15 ms` after), and natural bottom-to-top chord voicing micro-spread (`4.5 ms` on block chords/octaves, `20 ms` on lyrical `Roll` chords).

### The Whole Piece in 765 Bytes: [`extraordinary.k`](extraordinary.k)

An earlier version of this README estimated on paper that the piece's musical logic came to about 398 bytes. Nobody ever built a file of that size. [`extraordinary.k`](extraordinary.k) is the real file: **765 bytes**, measured, and checked against the score note for note.

```bash
python3 kplay.py              # extraordinary.k -> extraordinary_k.mid, sheet music PNG, extraordinary_k.mp3
python3 kplay.py --verify     # proves the 765 bytes decode to exactly the score below
```

**What the 765 bytes contain:** all 116 bars and 2,104 notes (1,243 events): every pitch, rhythm, cross-barline tie, rolled chord and the pickup, plus each bar's tempo, dynamic and pedal changes, and both fermatas. The file has no header and no magic number, and the player has no code specific to this piece.

**What they don't contain:**
- **Printed text.** The title block, section names, chord symbols and Roman numerals are in the optional plain-text sidecar [`extraordinary.labels`](extraordinary.labels) (2.6 KB). Without it, `kplay.py` engraves the same music with metronome marks in place of the captions.
- **Ru's rubato.** [`extraordinary.mid`](extraordinary.mid) and [`extraordinary.mp3`](extraordinary.mp3) follow the YouTube performance through 117 measured bar timestamps (`BAR_BOUNDARIES`) and a Viterbi alignment against [`original_from_youtube.mp4`](original_from_youtube.mp4), so no small standalone file can produce them. The `.k` file plays at its own tempo markings instead: [`extraordinary_k.mp3`](extraordinary_k.mp3).
- **The player.** [`kplay.py`](kplay.py) decodes with the Python standard library alone. Rendering reuses the generic MIDI, LilyPond and mastering stages of [`extraordinary_reduction.py`](extraordinary_reduction.py) and never calls `build_score()`.

**How it is coded.** Pitches become diatonic degrees of C minor, with a "raised" flag for the Dorian A♮, so transposed repeats look identical. Each hand is one stream of events anchored on their highest note. A run of events can be copied from *D* bars earlier with a diatonic transposition *T*, which is how the choruses and accompaniment patterns repeat. Every remaining decision is a binary symbol: logistic mixing of a few musical contexts predicts it, and a 32-bit arithmetic coder codes it. All arithmetic is integer, so decoding is identical on every platform.

| Layer | Bytes |
| :--- | ---: |
| Melodic pitch (interval between successive top notes, raised flag) | 216 |
| Chord shapes below the top note, rolled chords | 183 |
| Rhythm (durations and rests) | 145 |
| Repeats (copy flag, bars back, transposition, length) | 134 |
| Per-bar tempo, dynamics, pedal and fermatas | 79 |
| Key, pickup and event counts | 7 |
| Arithmetic-coder flush | 1 |
| **Total** | **765** |

**Why it is not 398 bytes:** the old estimate assumed roughly 2 bits per right-hand note, but 84 of the 116 right-hand bars are not a repeat of any earlier bar, even allowing transposition. For comparison, writing the same events as compact text and compressing it with xz, Brotli or PPMd gives 840–940 bytes before tempo, dynamics and pedal are added. `kplay.py --verify` checks that the decoded file reproduces `build_score()` exactly, the LilyPond sheet-music source character for character, and, with the YouTube rubato map applied, the committed [`extraordinary.mid`](extraordinary.mid) byte for byte.

#### Compression Ratios (measured)
- **vs. Its Own Audio Render (`extraordinary_k.mp3`, `6.3 MB`)**: **$\sim 8{,}300 : 1$**
- **vs. Compiled 2,104-Note MIDI (`extraordinary.mid`, `14.1 KB`)**: **$\sim 18 : 1$**
- **vs. The Python Score Generator** (`build_score()` and its functors, `27.7 KB` with comments and docstrings stripped, `5.2 KB` after xz): **$\sim 7 : 1$** against the xz size

---

## 2. 96 kHz Mastering, Classical Engraving & Portrait Mobile Showcase Video

All artifacts are produced deterministically inside the version-pinned [`Dockerfile`](Dockerfile) via [`render_in_docker.sh`](render_in_docker.sh) (pinned to at most half of the host's physical cores on the Intel Core Ultra 9 285K via `--cpuset-cpus="4-7,16-23" --cpus="12"`):

1. **Dual-Engine 96 kHz 32-Bit Float FluidSynth Synthesis (`fluidsynth=2.3.1-2`)**:
   - [`extraordinary.mid`](extraordinary.mid) is rendered at **96,000 Hz** (`float32` PCM, internal chorus/reverb disabled) through two complementary SoundFonts pinned in Debian Bookworm:
     - **Primary Body Layer (`82%`)**: `musescore-general-soundfont-lossless=0.2.1-1` (`/usr/share/sounds/sf2/MuseScore_General_Full.sf2`, 478 MB uncompressed concert grand with multi-velocity layers).
     - **Close-Mic Hammer & String Definition Layer (`18%`)**: `fluid-soundfont-gm=3.1-5.3` (`/usr/share/sounds/sf2/FluidR3_GM.sf2`), zero-phase bandpass-focused (`180 Hz – 5,800 Hz` via 4th-order Butterworth `scipy.signal.sosfiltfilt`).
2. **24-Mode Physical Sympathetic String & Soundboard Resonance Bank (`scipy==1.13.1` at 96 kHz 64-Bit Float)**:
   - Models the undamped C-minor / $E\flat$-major harmonic overtone series of a 9-foot concert grand (`C2` through `G6`, 24 high-$Q$ parallel resonators via `scipy.signal.iirpeak` + `sosfilt` with natural bass-left / treble-right spatial panning).
3. **5-Stage Zero-Phase RBJ Biquad Mastering EQ & 2.8s True-Stereo Concert Hall FFT Convolution**:
   - Subsonic high-pass (`24 Hz`), wooden soundboard warmth (`+2.0 dB` at `110 Hz`), lower-mid cleanup (`-1.8 dB` at `320 Hz`), hammer-felt upper-mid smoothing (`-2.6 dB` at `3,150 Hz`), silk air sheen (`+1.2 dB` at `8,500 Hz`), and FFT convolution with a deterministic **2.8-second True-Stereo Concert Hall Impulse Response** (`16` specular early reflections + 3-band diffuse tail with `22 ms` pre-delay).
4. **Classical Piano Sheet Music Engraving & Exact Sub-Pixel Notehead Bijection ([`extraordinary_sheet_music.png`](extraordinary_sheet_music.png))**:
   - `export_sheet_music_png()` compiles the 116 symbolic measures into a GNU LilyPond 2.24.1 `PianoStaff` score on a continuous single-page canvas (`page-breaking = #ly:one-page-breaking`), extracts the exact vector `/Rect` bounding boxes for all **2,228 engraved noteheads** across all 29 systems, rasterizes at **400 DPI** via `pdftoppm`, and downsamples with **Lanczos-3** to a crisp `2400 × 13244` PNG.
5. **Portrait Mobile Showcase Video ([`extraordinary_showcase.mp4`](extraordinary_showcase.mp4), `1080 × 1920`, `29.97 fps`)**:
   - **Top (`1080 × 608`)**: Uncropped `16:9` 1080p video of Ru's performance with a live top-right audio source badge.
   - **Middle (`1080 × 144`)**: Studio HUD featuring side-by-side **Showmanship Audio A/B Switcher Pills** (`RU'S ORIGINAL PIANO (YouTube)` vs. `OUR FIRST-PRINCIPLES RENDER`; the committed video still shows the label from its last render, `398-BYTE FIRST-PRINCIPLES RENDER`, until it is rendered again), a dedicated **Live Harmonic Breeze Waveform** lane, and live measure/chord/rubato-BPM/voicing telemetry.
   - **Bottom (`1080 × 1168`)**: Calm, non-nauseating 5-system sheet music view (100% motionless during each 4-bar system, easing smoothly over `0.45s` only at system boundaries) illuminated by a **Premultiplied-Alpha "Breeze of Air"** (3 braided aerodynamic silk wind filaments per hand, drifting spirit-motes, and jewel-ringed active noteheads that keep all black notation ink 100% razor-sharp).
   - **Showmanship A/B Audio Master**: Both pianos are loudness-matched via ITU-R BS.1770-4 K-weighting (`-14.0 LUFS` integrated + smooth phrase-level RMS contour matching for `< 0.1 dB` continuity) and alternate every 4 bars (1 system) with smooth `0.35s` equal-power cosine crossfades ($\cos^2 / \sin^2$), including the End-Card Replay (`233.89s – 257.38s`).

---

## 3. Tonal, Modal & Compositional Basis

### Modal Vocabulary
- **Primary Key**: **C Natural Minor** ($\{C, D, E\flat, F, G, A\flat, B\flat\}$)
- **Modal Inflections**:
  - **C Dorian ($\natural\hat{6}$ = $A\natural$)**: Appears at every major structural cadence on the bright **$\text{IV}$ major chord (`F` / `F/C`)** in Bars 15, 23, 32, 55–56, and 64.
  - **G Dominant ($\text{v} / \text{V}$)**: Propels the high operatic climax turnaround in Bar 96 (`Gm`) and Bar 100 (`Ab -> Gm -> Fm`).
  - **C Minor Pentatonic Subspace ($\{C, E\flat, F, G, B\flat\}$)**: Generates every *Gufeng* (古風) ornamental cascade via `pentatonic_cascade(start_name, end_name, start_step, rate=T)`.

### Left-Hand Accompaniment Functors & The Acoustic Register Law
All 116 measures of left-hand accompaniment are generated by **8 compositional functors**:
- `lh_verse_pedal(harmony)` — Playable 1-octave tonic-pedal voicings (`Cm: C2+G2+C3`, `Bb/C: C2+Bb2+C3`, `Ab/C: C2+Ab2+C3`) and two-voice Dorian pedal counterpoint (`C2+C3` whole-note bass pedal sustaining beneath the `A3 - F3 - A3` tenor countermelody on `F/C`).
- `lh_prechorus_groove(harmony)` — Driving 8-eighth-note tonic-pedal groove (`C2+C3`) with backbeat inner-chord accents.
- `lh_chorus_drive(root_name)` — Signature rock-ballad eighth-note chorus pattern governed by the **Acoustic Register Law**:
  - When the bass root $R < \text{pitch}(\text{"C2"})$ (`Ab1`, `Bb1`), the Beat 3 tenor backbeat voices `[R + 19, R + 24]` (`Eb3+Ab3`, `F3+Bb3`).
  - When $R \ge \text{pitch}(\text{"C2"})$ (`C2`), the tenor backbeat voices `[R + 12, R + 19]` (`C3+G3`) so the left hand never crosses Middle C (`C4`).
- `lh_f_dorian_sweep()` — 2-beat `F1+F2` foundation followed by a 16th-note ascending `F2 - A2 - C3 - F3 - A3` arpeggio sweep into the right-hand `C4 - Eb4 - Ab4 - Bb4` pickup.
- `lh_breakthrough_ostinato(chord_type, driving_pulse)` — Martial eighth-note `C2+G2+C3` / `C2+Bb2+C3` / `C2+Ab2+C3` pulse for Han Li's Nascent Soul Breakthrough (Bars 57–63).
- `lh_lyrical_arch(root_name)` — Wide-span 10th/12th lyrical arch (`[R, R+12] -> [R+19] -> [R+24] -> [R+12]`) for the Operatic Interlude (Bars 49–54).
- `lh_climax_arpeggio(root_name, tresillo_punch, high_span)` — Interval-based wide-span climax arpeggio with optional tresillo (`B1_A`) bass punch.
- `lh_climax_wave(root_name, beat4_bass)` — Sweeping 2-octave eighth-note wave arpeggio (`[R, R+12] -> [R+7] -> [R+12] -> [R+19] -> [R+24, R+31]`).

---

## 4. Symphonic Architecture (Measures 1–116)

| Section | Bars | Tempo | Dynamic | Harmonic Progression & Musical Texture |
| :--- | :---: | :---: | :---: | :--- |
| **I. Intro** | 1–8 | `120 → 108` | *mp – p* | Two 4-bar phrases (`Abmaj7 – Bb – Eb/G – Bb/D – Cm9`) with 32nd-note pentatonic cascades (`Eb6–C6–Bb5–G5`) and a rolled `Cm` fermata |
| **II. Verse 1** | 9–16 | `124 → 122` | *mp – p* | Contemplative melody over a continuous tonic `C2+C3` pedal (`Cm – Bb/C – Ab/C – F/C Dorian IV`) |
| **III. Verse 2** | 17–24 | `124 → 126` | *mf – f* | Intensified repeat of the verse over `C` pedal; Bar 20 lifts to `D5` and Bar 24 drives in rising octaves (`Eb5 – C5 – Eb5 – F5`) |
| **IV. Pre-Chorus** | 25–32 | `128` | *f* | Driving `C2+C3` eighth-note groove with cross-barline tied Beat 4& (`B4_AND`) syncopated RH block-chord anticipations (`Cm – Bb/C – Ab/C`), culminating in the `F` Dorian 16th-note sweep |
| **V. Chorus 1** | 33–40 | `125` | *f* | First explosion of the `Ab – Bb – Cm` chorus groove with `Bb/C -> Cm` tresillo (`3+3+2`) `SixthOct` voicings |
| **VI. Post-Chorus** | 41–48 | `124` | *mp – mf* | Lyrical return of the main pentatonic theme (`Abmaj7–Bb–Cm7–Eb` then `Fm7–Gm7–Cm7–Eb`) ending with a 2-hand 32nd-note pentatonic run |
| **VIIa. Operatic Interlude** | 49–56 | `128 → 138` | *mf – f* | *Xiqing* (戲腔) lyrical interlude over 10th/12th arches (`Ab–Bb–Cm–Fm–Gm`) leading into a 2-bar `F` Dorian 16th-note trill (`D5–C5` then `C6–D6`) |
| **VIIb. Breakthrough Ostinato** | 57–64 | `132` | *f – ff* | Han Li's Nascent Soul Breakthrough: relentless two-handed martial `Cm` eighth-note chord ostinato (`C4+Eb4+G4` over `C2+G2+C3`), erupting into `F` Dorian |
| **VIIIa. Chorus 2** | 65–72 | `130` | *ff* | Full-power high-register (`C6–Bb6`) `Ab – Bb – Cm` chorus |
| **VIIIb. Chorus Extension** | 73–80 | `132` | *ff – f* | Main pentatonic motif blasted in high octaves (`F6–Eb6–C6–G6`) over the `Ab – Bb – Cm` chorus bass |
| **VIIIc. Operatic Climax** | 81–106 | `130 → 128` | *ff – mf* | High Operatic Climax (戲腔變奏高潮) reaching the 7th octave (`C7`, `Eb7`) with `Eb -> Gm` dominant turnaround, 2-bar `Fm` sweep, and final `Eb6 -> Bb4` waterfall |
| **IX. Quiet Outro** | 107–116 | `125 → 80` | *p – pp* | *Molto ritardando* (`Ab/C – Bb/C – Fm7 – Gm7 – Cm9`), closing on a softly rolled `Cm` tonic chord |

---

## 5. Repository Contents & Reproducible Execution

| File | Description |
| :--- | :--- |
| [`extraordinary_showcase.mp4`](extraordinary_showcase.mp4) | Portrait mobile (`1080 × 1920`, `29.97 fps`) full-length showcase video with Showmanship A/B audio switching and "Breeze of Air" sheet music visualization |
| [`extraordinary.mp3`](extraordinary.mp3) | Final 96 kHz → 48 kHz LAME `V0` mastered & dynamically synchronized concert-grand audio render |
| [`extraordinary_sheet_music.png`](extraordinary_sheet_music.png) | Continuous tall PNG (`2400 px` wide, 400 DPI → Lanczos-3 supersampled) of the complete 116-measure GNU LilyPond `PianoStaff` score |
| [`extraordinary.mid`](extraordinary.mid) | Playable MIDI of the complete 116-measure symphonic arrangement dynamically locked to the video rubato |
| [`extraordinary.k`](extraordinary.k) | The complete musical content of all 116 measures in 765 bytes (arithmetic-coded; decoded by `kplay.py`) |
| [`extraordinary.labels`](extraordinary.labels) | Optional plain-text sidecar for `extraordinary.k`: title block, section names, chord symbols and Roman numerals |
| [`kplay.py`](kplay.py) | Player and encoder for `extraordinary.k`: standard-library decoder, `--verify` proof against `build_score()`, and rendering through the shared MIDI, LilyPond and mastering stages |
| [`extraordinary_k.mid`](extraordinary_k.mid) / [`extraordinary_k.mp3`](extraordinary_k.mp3) | What `extraordinary.k` sounds like on its own: Virtual Pianist MIDI at the file's own tempo markings and its 48 kHz LAME `V0` master (its sheet music is [`extraordinary_sheet_music.png`](extraordinary_sheet_music.png): the LilyPond source is identical) |
| [`CHORD_REDUCTION_SCORE.md`](CHORD_REDUCTION_SCORE.md) | Complete bar-by-bar symbolic score (Measures 1–116) with chord symbols, Roman numerals, tempos, dynamics, and exact LH/RH voicings |
| [`extraordinary_reduction.py`](extraordinary_reduction.py) | Unified symbolic generator, 930-knot dynamic rubato aligner, LilyPond sheet music engraver, 96 kHz / 64-bit float acoustic mastering engine, and portrait video renderer |
| [`Dockerfile`](Dockerfile) | Digest- and version-pinned Debian Bookworm + Python 3.11.15 build environment |
| [`render_in_docker.sh`](render_in_docker.sh) | Defensive (`set -euo pipefail`) one-command build, offline `--network=none` render (pinned to `<= 50%` physical cores: `--cpuset-cpus="4-7,16-23" --cpus="12"`), verification, and image cleanup script |
| [`original_from_youtube.mp4`](original_from_youtube.mp4) | Single non-duplicated 1080p MP4 reference from the source YouTube performance (`https://youtu.be/JB31Aq_5Slw`) |
| [`OPENROUTER_GUIDE.md`](OPENROUTER_GUIDE.md) | Complete end-to-end blueprint, standalone Python multimodal agent script, and copy-paste master prompt for reproducing this workflow on any piano performance via OpenRouter |

### Reproducing Everything from Scratch
```bash
./render_in_docker.sh
```

### Playing the 765-Byte File
```bash
python3 kplay.py --verify                 # decode extraordinary.k and prove it equals build_score()
python3 kplay.py                          # extraordinary_k.mid + .ly + _sheet_music.png + .mp3
python3 kplay.py --midi-only              # MIDI + LilyPond source only (no LilyPond/FluidSynth needed)
python3 kplay.py --no-labels             # music only: no title block, chord symbols or section names
python3 kplay.py --encode                 # rebuild extraordinary.k + extraordinary.labels from build_score()
```
Decoding needs nothing but Python 3. Engraving and audio use the same tools as the main pipeline (LilyPond, Poppler, FluidSynth with the MuseScore and FluidR3 SoundFonts, FFmpeg). `render_in_docker.sh` runs `--verify` and the full render inside the pinned image. The committed [`extraordinary_k.mp3`](extraordinary_k.mp3) was rendered outside that image (Ubuntu 24.04: FluidSynth 2.3.4, the same `musescore-general-soundfont-lossless 0.2.1-1` and `fluid-soundfont-gm 3.1-5.3`), because the pinned Debian mirror was not reachable from the build machine.

