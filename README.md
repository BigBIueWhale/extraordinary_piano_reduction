# Extraordinary (不凡) — First-Principles Piano Reduction ("PNG → SVG")

> **Created with Gemini 4 Argon high in Antigravity CLI** — combining innate multimodal audio perception with pure first-principles music-theoretic reduction and a 96 kHz / 64-bit float physical concert-grand mastering pipeline.

- 🎧 **Listen to the Final Rendered Audio**: **[`extraordinary.mp3`](extraordinary.mp3)** *(48 kHz LAME V0 stereo master, rendered via [`render_in_docker.sh`](render_in_docker.sh) & [`Dockerfile`](Dockerfile))*
- 🎹 **Playable First-Principles MIDI**: **[`extraordinary.mid`](extraordinary.mid)**
- 📜 **Complete Bar-by-Bar Symbolic Score**: **[`CHORD_REDUCTION_SCORE.md`](CHORD_REDUCTION_SCORE.md)**
- 🎬 **Source Performance**: [A Mortal's Journey「不凡 Extraordinary」Ru's Piano Cover (YouTube)](https://youtu.be/JB31Aq_5Slw)
- ⚙️ **Single-Mode Generator & 96 kHz Mastering Engine**: **[`extraordinary_reduction.py`](extraordinary_reduction.py)**

---

## 1. Philosophy: Musical "PNG → SVG" Reduction

Most automated or reverse-engineered MIDI transcriptions treat a musical performance like a raster image (**PNG**): they scrape arrays of floating-point onset timestamps (`[0.81, 2.73, 4.72, ...]`), arbitrary fractional note durations, and per-note MIDI velocities (`61, 60, 57, 72...`). The result is brittle, opaque, and machine-generated.

This repository treats transcription as a **mathematical reduction into symbolic primitives ("SVG")**. Rather than hard-coding scraped floating-point timings or velocity tables, [`extraordinary_reduction.py`](extraordinary_reduction.py) constructs all 116 measures of the arrangement from **first principles of music theory, compositional form, and piano performance** in a single canonical, defensively verified pipeline with zero fallbacks:

1. **Zero Hard-Coded Timestamps**: Time is integrated naturally from section tempo markings (`BPM`), phrase-arch agogic breathing (`+4%` broadening on cadence bars), and *molto ritardando* cadences.
2. **Pure `"1 e & a"` Rhythmic Algebra**: Every note onset and duration is expressed in exact rational subdivisions of a $4/4$ measure:
   $$\text{W}=16,\quad \text{DH}=12,\quad \text{H}=8,\quad \text{DQ}=6,\quad \text{Q}=4,\quad \text{DE}=3,\quad \text{E}=2,\quad \text{S}=1,\quad \text{T}=0.5$$
   on the standard 16th-note grid (`B1, B1_E, B1_AND, B1_A, B2, ...`). The piece's signature **tresillo (`3 + 3 + 2`)** syncopation falls naturally on `(B1, B1_A, B2_AND)` and `(B3, B3_A, B4_AND)`.
3. **Zero Hard-Coded Velocities (Virtual Pianist Model)**: Expressive dynamics are derived from section markings (`pp, p, mp, mf, f, ff`), left/right-hand balance (`-12` velocity on LH accompaniment), metric accent hierarchy, soprano top-voice projection (`+4` velocity on top voice), syncopated legato sustain pedaling (`CC64` released `35 ms` before harmonic change and caught `15 ms` after), and natural bottom-to-top chord voicing micro-spread (`4.5 ms` on block chords/octaves, `20 ms` on lyrical `Roll` chords).

---

## 2. How [`extraordinary.mp3`](extraordinary.mp3) Is Rendered (96 kHz / 64-Bit Float Pipeline)

The rendered audio file [`extraordinary.mp3`](extraordinary.mp3) is produced deterministically inside the version-pinned [`Dockerfile`](Dockerfile) via [`render_in_docker.sh`](render_in_docker.sh) and [`synthesize_and_master_audio()`](extraordinary_reduction.py#L1092-L1175):

1. **Dual-Engine 96 kHz 32-Bit Float FluidSynth Synthesis (`fluidsynth=2.3.1-2`)**:
   - [`extraordinary.mid`](extraordinary.mid) is rendered at **96,000 Hz** (`float32` PCM, internal chorus/reverb disabled) through two complementary SoundFonts pinned in Debian Bookworm:
     - **Primary Body Layer (`82%`)**: `musescore-general-soundfont-lossless=0.2.1-1` (`/usr/share/sounds/sf2/MuseScore_General_Full.sf2`, 478 MB uncompressed concert grand with multi-velocity layers).
     - **Close-Mic Hammer & String Definition Layer (`18%`)**: `fluid-soundfont-gm=3.1-5.3` (`/usr/share/sounds/sf2/FluidR3_GM.sf2`), zero-phase bandpass-focused (`180 Hz – 5,800 Hz` via 4th-order Butterworth `scipy.signal.sosfiltfilt`) so it adds midrange hammer articulation without sub-bass build-up or upper-register metallic glare.
2. **24-Mode Physical Sympathetic String & Soundboard Resonance Bank (`scipy==1.13.1` at 96 kHz 64-Bit Float)**:
   - Models the undamped C-minor / $E\flat$-major harmonic overtone series of a 9-foot concert grand (`C2` through `G6`, 24 high-$Q$ parallel resonators via `scipy.signal.iirpeak` + `sosfilt` with natural bass-left / treble-right spatial panning).
3. **5-Stage Zero-Phase RBJ Biquad Mastering EQ (`sosfiltfilt` at 96 kHz)**:
   - Subsonic high-pass (`24 Hz`), wooden soundboard fundamental warmth (`+2.0 dB` at `110 Hz`), lower-mid boxiness cut (`-1.8 dB` at `320 Hz`), hammer-felt upper-mid smoothing (`-2.6 dB` at `3,150 Hz` for silky `ff` climaxes in Octaves 6–7), and silk air sheen (`+1.2 dB` at `8,500 Hz`).
4. **True-Stereo 96 kHz Concert Hall Impulse Response Synthesis & FFT Convolution (`scipy.signal.fftconvolve`)**:
   - Synthesizes a deterministic **2.8-second True-Stereo Concert Hall Impulse Response** ($268,800$ samples/channel at `96 kHz`) featuring **16 specular timber-hall early reflections** (`14 ms – 84 ms` with ITD/ILD and `3.8 kHz` wall absorption) and a **3-band frequency-dependent diffuse reverb tail** (`RT60 = 1.75s` low, `2.05s` mid, `1.10s` high air absorption) with a `22 ms` pre-delay envelope so every transient attack remains crisp before the hall blooms.
5. **Mid/Side Stereo Imaging, Soft-Knee Transformer Saturation & 48 kHz LAME `V0` Encoding (`ffmpeg=7:5.1.9-0+deb12u1`)**:
   - Applies `+10%` Mid/Side width above `220 Hz`, continuous soft-knee analog saturation (`tanh`), true-peak normalization to `-0.8 dBFS`, Kaiser-windowed polyphase anti-aliased resampling (`96 kHz → 48 kHz` via `scipy.signal.resample_poly`), and highest-precision LAME VBR `V0` encoding (`-c:a libmp3lame -q:a 0 -compression_level 0`).

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
- `lh_verse_pedal(harmony)` — Tonic `C2+C3` pedal with inner voices (`G3`, `F3+Bb3`, `Eb3+Ab3`) and the Dorian `A3 - F3 - A3` countermelody on `F/C`.
- `lh_prechorus_groove(harmony)` — Driving 8-eighth-note tonic-pedal groove (`C2+C3`) with backbeat inner-chord accents.
- `lh_chorus_drive(root_name)` — Signature rock-ballad eighth-note chorus pattern governed by the **Acoustic Register Law**:
  - When the bass root $R < \text{pitch}(\text{"C2"})$ (`Ab1`, `Bb1`), the Beat 3 tenor backbeat voices `[R + 19, R + 24]` (`Eb3+Ab3`, `F3+Bb3`).
  - When $R \ge \text{pitch}(\text{"C2"})$ (`C2`), the tenor backbeat voices `[R + 12, R + 19]` (`C3+G3`) so the left hand never crosses Middle C (`C4`).
- `lh_f_dorian_sweep()` — 2-beat `F1+F2` foundation followed by a 16th-note ascending `F2 - A2 - C3 - F3 - A3` arpeggio sweep into the right-hand `C4 - Eb4 - Ab4 - Bb4` pickup.
- `lh_breakthrough_ostinato(chord_type, driving_pulse)` — Martial eighth-note `C2+G2+C3` / `G2+C3+G3` pulse for Han Li's Nascent Soul Breakthrough (Bars 57–63).
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
| **IV. Pre-Chorus** | 25–32 | `128` | *f* | Driving `C2+C3` eighth-note groove with `-E` syncopated RH block-chord anticipations (`Cm – Bb/C – Ab/C`), culminating in the `F` Dorian 16th-note sweep |
| **V. Chorus 1** | 33–40 | `125` | *f* | First explosion of the `Ab – Bb – Cm` chorus groove with `Bb/C -> Cm` tresillo (`3+3+2`) `SixthOct` voicings |
| **VI. Post-Chorus** | 41–48 | `124` | *mp – mf* | Lyrical return of the main pentatonic theme (`Abmaj7–Bb–Cm7–Eb` then `Fm7–Gm7–Cm7–Eb`) ending with a 2-hand 32nd-note pentatonic run |
| **VIIa. Operatic Interlude** | 49–56 | `128 → 138` | *mf – f* | *Xiqing* (戲腔) lyrical interlude over 10th/12th arches (`Ab–Bb–Cm–Fm–Gm`) leading into a 2-bar `F` Dorian 16th-note trill (`D5–C5` then `C6–D6`) |
| **VIIb. Breakthrough Ostinato** | 57–64 | `132` | *f – ff* | Han Li's Nascent Soul Breakthrough: relentless two-handed martial `Cm` eighth-note chord ostinato (`C4+Eb4+G4` over `C2+G2+C3`), erupting into `F` Dorian |
| **VIIIa. Chorus 2** | 65–72 | `130` | *ff* | Full-power high-register (`C6–Bb6`) `Ab – Bb – Cm` chorus |
| **VIIIb. Chorus Extension** | 73–80 | `132` | *ff – f* | Main pentatonic motif blasted in high octaves (`F6–Eb6–C6–G6`) over the `Ab – Bb – Cm` chorus bass |
| **VIIIc. Operatic Climax** | 81–106 | `130 → 128` | *ff – mf* | High Operatic Climax (戲腔變奏高潮) reaching the 7th octave (`C7`, `Eb7`) with `Eb -> Gm` dominant turnaround, 2-bar `Fm` sweep, and final `Eb6 -> Eb4` waterfall |
| **IX. Quiet Outro** | 107–116 | `125 → 80` | *p – pp* | *Molto ritardando* (`Ab/C – Bb/C – Fm7 – Gm7 – Cm9`), closing on a softly rolled `Cm` tonic chord |

---

## 5. Repository Contents & Reproducible Execution

| File | Description |
| :--- | :--- |
| [`extraordinary.mp3`](extraordinary.mp3) | Final 96 kHz → 48 kHz LAME `V0` mastered concert-grand audio render |
| [`extraordinary.mid`](extraordinary.mid) | Playable MIDI of the complete 116-measure symphonic arrangement |
| [`CHORD_REDUCTION_SCORE.md`](CHORD_REDUCTION_SCORE.md) | Complete bar-by-bar symbolic score (Measures 1–116) with chord symbols, Roman numerals, tempos, dynamics, and exact LH/RH voicings |
| [`extraordinary_reduction.py`](extraordinary_reduction.py) | Single-mode first-principles symbolic generator, Virtual Pianist MIDI compiler, and 96 kHz / 64-bit float acoustic mastering engine |
| [`Dockerfile`](Dockerfile) | Digest- and version-pinned Debian Bookworm + Python 3.11.15 build environment |
| [`render_in_docker.sh`](render_in_docker.sh) | Defensive (`set -euo pipefail`) one-command build, offline `--network=none` render, verification, and image cleanup script |

### Reproducing Everything from Scratch
```bash
./render_in_docker.sh
```
