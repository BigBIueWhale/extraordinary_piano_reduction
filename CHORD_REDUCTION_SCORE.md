# First-Principles Mathematical & Musical Reduction: *Extraordinary (不凡)*

- **Piece**: *A Mortal's Journey「不凡 Extraordinary」— Ru's Piano Cover*
- **Source Performance**: [https://youtu.be/JB31Aq_5Slw](https://youtu.be/JB31Aq_5Slw)
- **Created With**: **Gemini 4 Argon high in Antigravity CLI**
- **Key**: **C Natural Minor** (`C, D, Eb, F, G, Ab, Bb`) with **C Dorian** (`A` natural on the `F` major IV chord) & **G Dominant** (`Gm/G5` at the climax)
- **Meter**: **4/4** on a pure rational 16th-note grid (`0` = Beat 1, `4` = Beat 2, `8` = Beat 3, `12` = Beat 4; `~` denotes an upward rolled chord)

## 1. First-Principles Architecture ("PNG to SVG")

| Domain | First-Principles Generator | Musical Meaning |
| :--- | :--- | :--- |
| **Tonal Basis** | C Minor + Dorian $\natural\hat{6}$ + Pentatonic $\{C, E\flat, F, G, B\flat\}$ | Modal Gufeng (古風) harmonic & ornamental space |
| **Rhythmic Algebra** | Pure rational subdivisions (`W=16, H=8, Q=4, DE=3, E=2, S=1, T=0.5`) | Zero hard-coded timestamps; exact metric & tresillo (`3+3+2`) geometry |
| **Left-Hand Functors** | `lh_verse_pedal`, `lh_prechorus_groove`, `lh_chorus_drive`, `lh_f_dorian_sweep`, `lh_breakthrough_ostinato`, `lh_climax_arpeggio` | 6 accompaniment archetypes spanning all 116 measures |
| **Right-Hand Operators** | `N`, `Oct`, `SixthOct`, `FourthOct`, `Roll`, `pentatonic_cascade` | Idiomatic solo-piano voicings & pentatonic waterfalls |
| **Virtual Pianist** | Section BPM + Dynamic markings (`pp`–`ff`) + Metric/Soprano voicing model | Natural expressive dynamics, top-note projection, and chord rolls |

## 2. Complete Bar-by-Bar Symbolic Score (Measures 1–116)

### I. Intro

| Bar | Tempo | Dyn | Chord | Roman | Left Hand (`step`:voicing) | Right Hand (`step`:voicing) |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **1** | `120` | *mp* | **Abmaj7** | `VI` | `0`:Ab1+Ab2  `12`:G3 | `-2`:Eb6  `-1.5`:C6  `-1`:Bb5  `-0.5`:G5  `0`:F5  `2`:Eb5  `4`:C5  `6`:G5  `8`:F5  `10`:Eb5  `12`:C5  `14`:Bb4 |
| **2** | `120` | *mp* | **Bb -> Eb/G -> Bb/D** | `VII -> III6 -> VII6` | `0`:Bb2+F3+Bb3  `8`:Eb3+Bb3  `12`:D3+Bb3 | `2`:F4  `6`:G4  `12`:Bb4  `15`:F4 |
| **3** | `120` | *p* | **Cm9** | `i9` | `0`:~C3+G3+D4+Eb4 | `0`:~G4+C5  `10`:Bb4  `12`:Bb4  `14`:C5 |
| **4** | `116` | *p* | **Cm -> G(half)** | `i -> V` | *(tacet)* | `0`:Eb4  `8`:D4  `14`:Eb6  `14.5`:C6  `15`:Bb5  `15.5`:G5 |
| **5** | `120` | *mp* | **Abmaj7** | `VI` | `0`:Ab1+Ab2  `12`:G3 | `0`:F5  `2`:Eb5  `4`:C5  `6`:G5  `8`:F5  `10`:Eb5  `12`:C5  `14`:Bb4 |
| **6** | `120` | *mp* | **Bb -> Eb/G -> Bb/D** | `VII -> III6 -> VII6` | `0`:Bb2+F3+Bb3  `8`:Eb3+Bb3  `12`:D3+Bb3 | `2`:F4  `6`:G4  `12`:Bb4  `15`:F4 |
| **7** | `118` | *p* | **Cm9** | `i9` | `0`:~C3+G3+D4+Eb4 | `0`:~G4+C5  `10`:G5  `10.5`:F5  `11`:Eb5  `11.5`:C5  `12`:Bb4  `12.5`:G4  `13`:F4  `13.5`:Eb4 |
| **8** | `108` | *p* | **Cm (Fermata)** | `i` | `0`:C2+G2+C3 | `0`:~G3+C4+Eb4 |

### II. Verse 1

| Bar | Tempo | Dyn | Chord | Roman | Left Hand (`step`:voicing) | Right Hand (`step`:voicing) |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **9** | `124` | *mp* | **Cm** | `i` | `0`:C2+C3  `8`:G3 | `2`:Eb4+Eb5  `4`:D4+D5  `6`:C5  `8`:C4+Eb4  `10`:C5  `12`:Bb4  `14`:G4 |
| **10** | `124` | *mp* | **Bb/C** | `VII/1` | `0`:C2+C3+F3+Bb3  `8`:F3+Bb3 | `0`:D4  `2`:G4  `4`:F4  `6`:Eb4  `8`:D4+F4  `11`:G4  `14`:C4 |
| **11** | `124` | *p* | **Ab/C** | `VI/1` | `0`:C2+Eb3+Ab3  `8`:Eb3+Ab3  `14`:Eb3+Bb3 | `4`:C4+Eb4  `8`:C4+Eb4 |
| **12** | `124` | *mp* | **Ab/C -> Bb** | `VI/1 -> VII` | `0`:Ab3  `8`:Bb2+F3+Bb3 | `0`:C4  `2`:F4  `4`:G4  `6`:Bb4  `8`:D4+F4+C5  `11`:Bb4  `14`:G4 |
| **13** | `124` | *mp* | **Cm** | `i` | `0`:C2+C3  `8`:G3 | `2`:Eb4+Eb5  `4`:D4+D5  `6`:C5  `8`:C4+Eb4  `10`:C5  `12`:Bb4  `14`:G4 |
| **14** | `124` | *mp* | **Bb/C** | `VII/1` | `0`:C2+C3+F3+Bb3  `8`:F3+Bb3 | `0`:D4  `2`:F4  `4`:Eb4  `6`:F4  `8`:D4+G4  `11`:Bb4  `14`:C5 |
| **15** | `124` | *mp* | **F/C (Dorian IV)** | `IV/1` | `0`:C2+C3  `8`:A3  `10`:F3  `12`:A3 | `0`:~C4+F4+A4  `13`:C5  `14`:C4+G4  `15`:F4 |
| **16** | `122` | *mp* | **Cm -> Bb** | `i -> VII` | `0`:C3+G3  `6`:G2  `8`:Bb2+Bb3 | `0`:C4+Eb4  `8`:D4+G4  `12`:D4+G4+D5 |

### III. Verse 2

| Bar | Tempo | Dyn | Chord | Roman | Left Hand (`step`:voicing) | Right Hand (`step`:voicing) |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **17** | `124` | *mf* | **Cm** | `i` | `0`:C2+C3  `8`:G3 | `2`:Eb4+Eb5  `4`:D4+D5  `6`:C5  `8`:C4+Eb4  `10`:C5  `12`:Bb4  `14`:G4 |
| **18** | `124` | *mf* | **Bb/C** | `VII/1` | `0`:C2+C3+F3+Bb3  `8`:F3+Bb3 | `0`:D4  `2`:G4  `4`:F4  `6`:Eb4  `8`:D4+F4  `11`:G4  `14`:C4 |
| **19** | `124` | *p* | **Ab/C** | `VI/1` | `0`:C2+Eb3+Ab3  `8`:Eb3+Ab3  `14`:Eb3+Bb3 | `4`:C4+Eb4  `8`:C4+Eb4 |
| **20** | `124` | *mf* | **Ab/C -> Bb** | `VI/1 -> VII` | `0`:Ab3  `8`:Bb2+F3+Bb3 | `0`:C4  `2`:F4  `4`:G4  `6`:Bb4  `8`:D4+F4+C5  `11`:D5  `14`:G4 |
| **21** | `124` | *mf* | **Cm** | `i` | `0`:C2+C3  `8`:G3 | `2`:Eb4+Eb5  `4`:D4+D5  `6`:C5  `8`:C4+Eb4  `10`:C5  `12`:Bb4  `14`:G4 |
| **22** | `124` | *mf* | **Bb/C** | `VII/1` | `0`:C2+C3+F3+Bb3  `8`:F3+Bb3 | `0`:D4  `2`:F4  `4`:Eb4  `6`:F4  `8`:D4+G4  `11`:Bb4  `14`:C5 |
| **23** | `124` | *mf* | **F/C (Dorian IV)** | `IV/1` | `0`:C2+C3  `8`:A3  `10`:F3  `12`:A3 | `0`:~C4+F4+A4  `14`:D4+F4+A4 |
| **24** | `126` | *f* | **Cm -> Gm -> Bb** | `i -> v -> VII` | `0`:C3  `6`:G2+G3  `8`:Bb2+Bb3 | `0`:Eb4+Eb5  `2`:Eb4+Eb5  `4`:Eb4+Eb5  `6`:C4+C5  `8`:Eb4+Eb5  `12`:F4+F5 |

### IV. Pre-Chorus

| Bar | Tempo | Dyn | Chord | Roman | Left Hand (`step`:voicing) | Right Hand (`step`:voicing) |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **25** | `128` | *f* | **Cm** | `i` | `0`:C2+C3  `2`:G2  `4`:C3  `6`:C3  `8`:G3+C4  `10`:C3  `12`:C3  `14`:G2 | `-2`:G4+C5+Eb5+G5  `12`:G4+G5 |
| **26** | `128` | *f* | **Bb/C** | `VII/1` | `0`:C2+C3  `2`:Bb2  `4`:D3  `6`:D3  `8`:D3  `10`:Bb3+D4  `12`:D3  `14`:D3 | `-2`:F4+Bb4+D5+F5  `10`:G4+G5  `12`:F4+F5 |
| **27** | `128` | *f* | **Ab/C** | `VI/1` | `0`:C2+C3  `2`:Ab2  `4`:C3  `6`:C3  `8`:Ab3+C4  `10`:C3  `12`:C3  `14`:Ab2 | `-2`:Eb4+Ab4+C5+Eb5  `10`:D4+D5  `12`:Eb4+Eb5 |
| **28** | `128` | *f* | **Bb/C** | `VII/1` | `0`:C2+C3  `2`:Bb2  `4`:D3  `6`:D3  `8`:D3  `10`:Bb3+D4  `12`:D3  `14`:D3 | `-2`:F4+Bb4+D5+F5  `8`:D4+F4+Bb4+D5  `12`:F4+A4+D5 |
| **29** | `128` | *f* | **Cm -> Eb/G** | `i -> III6` | `0`:C2+C3  `2`:G2  `4`:C3  `6`:C3  `8`:G3+C4  `10`:C3  `12`:C3  `14`:G2 | `0`:G4+C5+Eb5+G5  `6`:Bb4+Eb5+G5+Bb5  `12`:C5+C6  `14`:Eb5 |
| **30** | `128` | *f* | **Bb/C** | `VII/1` | `0`:C2+C3  `2`:Bb2  `4`:D3  `6`:D3  `8`:D3  `10`:Bb3+D4  `12`:D3  `14`:D3 | `0`:F4+Bb4+D5+F5  `10`:G4+G5  `12`:F4+F5 |
| **31** | `128` | *f* | **Ab/C** | `VI/1` | `0`:C2+C3  `2`:Ab2  `4`:C3  `6`:C3  `8`:Ab3+C4  `10`:C3  `12`:C3  `14`:Ab2 | `0`:Eb4+Ab4+C5+Eb5  `2`:D4+D5  `4`:Eb4+Eb5  `6`:C4+C5 |
| **32** | `128` | *f* | **F (Dorian IV)** | `IV` | `0`:F1+F2  `2`:C2  `4`:F2  `6`:A2+C3  `8`:F2  `9`:A2  `10`:C3  `11`:F3  `12`:A3 | `0`:C4+F4+A4+C5  `12`:C4  `13`:Eb4  `14`:Ab4  `15`:Bb4 |

### V. Chorus 1

| Bar | Tempo | Dyn | Chord | Roman | Left Hand (`step`:voicing) | Right Hand (`step`:voicing) |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **33** | `125` | *f* | **Ab** | `VI` | `0`:Ab1+Ab2  `2`:Eb2  `4`:Ab2  `6`:Ab2  `8`:Eb3+Ab3  `10`:Ab2  `12`:Ab2  `14`:Eb2 | `0`:Eb4+Ab4+C5  `4`:C4+C5  `6`:Bb3+Bb4  `8`:C4+C5  `11`:Eb4+Eb5  `14`:C4+C5 |
| **34** | `125` | *f* | **Bb** | `VII` | `0`:Bb1+Bb2  `2`:F2  `4`:Bb2  `6`:Bb2  `8`:F3+Bb3  `10`:Bb2  `12`:Bb2  `14`:F2 | `4`:C4+C5  `6`:Bb3+Bb4  `8`:C4+C5  `11`:F4+F5  `14`:Eb4+Eb5 |
| **35** | `125` | *f* | **Bb/C -> Cm** | `VII/1 -> i` | `0`:C2+C3  `2`:G2  `4`:C3  `6`:G2  `8`:C3+G3  `10`:C3  `12`:C3  `14`:G2 | `0`:F4+Bb4+D5+F5  `3`:G4+C5+Eb5+G5  `6`:G4+C5+Eb5+G5  `14`:Eb5+C6+Eb6 |
| **36** | `125` | *f* | **Cm** | `i` | `0`:C2+C3  `2`:G2  `4`:C3  `6`:G2  `8`:C3+G3  `10`:C3  `12`:C3  `14`:G2 | `0`:F5+D6+F6  `3`:G5+Eb6+G6  `6`:G5+Eb6+G6  `8`:G5+Eb6+G6  `11`:F5+D6+F6  `14`:Eb5+C6+Eb6 |
| **37** | `125` | *f* | **Ab** | `VI` | `0`:Ab1+Ab2  `2`:Eb2  `4`:Ab2  `6`:Ab2  `8`:Eb3+Ab3  `10`:Ab2  `12`:Ab2  `14`:Eb2 | `4`:C4+C5  `6`:Bb3+Bb4  `8`:C4+C5  `11`:Eb4+Eb5  `14`:C4+C5 |
| **38** | `125` | *f* | **Bb** | `VII` | `0`:Bb1+Bb2  `2`:F2  `4`:Bb2  `6`:Bb2  `8`:F3+Bb3  `10`:Bb2  `12`:Bb2  `14`:F2 | `4`:C4+C5  `6`:Bb3+Bb4  `8`:C4+C5  `11`:F4+F5  `14`:Eb4+Eb5 |
| **39** | `125` | *f* | **Bb/C -> Cm** | `VII/1 -> i` | `0`:C2+C3  `2`:G2  `4`:C3  `6`:G2  `8`:C3+G3  `10`:C3  `12`:C3  `14`:G2 | `0`:F4+Bb4+D5+F5  `3`:G4+C5+Eb5+G5  `6`:G4+C5+Eb5+G5  `14`:Eb5+C6+Eb6 |
| **40** | `125` | *f* | **Cm** | `i` | `0`:C2+C3  `2`:G2  `4`:C3  `6`:G2  `8`:C3+G3  `10`:C3  `12`:C3 | `0`:F5+D6+F6  `3`:G5+Eb6+G6  `6`:Bb5+Bb6  `8`:G5+Eb6+G6  `11`:F5+D6+F6  `14`:Eb5+C6+Eb6 |

### VI. Post-Chorus

| Bar | Tempo | Dyn | Chord | Roman | Left Hand (`step`:voicing) | Right Hand (`step`:voicing) |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **41** | `124` | *mp* | **Abmaj7 -> Bb** | `VI -> VII` | `0`:Ab3  `8`:F3+Bb3 | `0`:Eb4+F5  `2`:Eb5  `4`:C5  `6`:G5  `8`:D4+F5  `10`:Eb5  `12`:C5  `14`:Bb4 |
| **42** | `124` | *mp* | **Cm7 -> Eb** | `i7 -> III` | `0`:C3+G3+Bb3  `8`:Eb3 | `2`:F4  `6`:G4  `10`:Bb4  `15`:Ab4 |
| **43** | `124` | *mp* | **Ab -> Bb** | `VI -> VII` | `0`:Ab2+Eb3  `8`:Bb2+F3+Bb3 | `0`:C5+F5  `2`:Eb5  `4`:C5  `6`:G5  `8`:F5  `10`:Eb5  `12`:Bb4  `14`:C5 |
| **44** | `124` | *mp* | **Cm** | `i` | `0`:C3+G3 | `0`:C4  `6`:Eb5  `6.5`:C5  `7`:Bb4  `7.5`:G4  `8`:C4+F4  `10`:Eb4+G4  `12`:F4+Bb4  `14`:G4+C5  `15`:Ab4 |
| **45** | `124` | *mp* | **Fm7 -> Gm7** | `iv7 -> v7` | `0`:F2+C3  `8`:G2+D3+G3 | `0`:C5+F5  `2`:Eb5  `4`:C5  `6`:G5  `8`:F5  `10`:Eb5  `12`:C5  `14`:Bb4 |
| **46** | `124` | *mp* | **Cm7 -> Eb** | `i7 -> III` | `0`:C3+G3+Bb3  `8`:Eb3 | `2`:F4  `6`:G4  `10`:Bb4  `15`:Ab4 |
| **47** | `124` | *mp* | **Ab -> Bb** | `VI -> VII` | `0`:Ab2+Eb3+Ab3  `8`:Bb2+F3+Bb3 | `0`:C5+F5  `2`:Eb5  `4`:C5  `6`:G5  `8`:F5  `10`:Eb5  `12`:Bb4  `14`:C5 |
| **48** | `124` | *mf* | **Cm (Pentatonic Run)** | `i` | `0`:C2+C3  `4`:C3  `4.5`:Eb3  `5`:F3  `5.5`:G3  `6`:Bb3 | `8`:C4  `8.5`:Eb4  `9`:F4  `9.5`:G4  `10`:Bb4  `11`:Eb6  `11.5`:C6  `12`:Bb5  `12.5`:G5  `13`:F5  `13.5`:Eb5 |

### VIIa. Operatic Interlude

| Bar | Tempo | Dyn | Chord | Roman | Left Hand (`step`:voicing) | Right Hand (`step`:voicing) |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **49** | `128` | *mf* | **Ab** | `VI` | `0`:Ab1+Ab2  `6`:Eb3  `8`:Ab3  `12`:Ab2 | `0`:C5  `4`:G4  `12`:F4+Bb4  `14`:Eb4 |
| **50** | `128` | *mf* | **Bb** | `VII` | `0`:Bb1+Bb2  `6`:F3  `8`:Bb3  `12`:Bb2 | `0`:F4  `6`:Eb5  `6.5`:C5  `7`:Bb4  `7.5`:G4  `8`:F4  `12`:Eb4  `14`:C4 |
| **51** | `128` | *mp* | **Cm -> Gm** | `i -> v` | `0`:C2+C3  `4`:G3  `6`:C2  `8`:G2+C3  `12`:G2+Bb3 | `0`:Eb4  `4`:C4  `12`:D4 |
| **52** | `128` | *mp* | **Cm** | `i` | `0`:C3  `8`:C2+C3 | `0`:C4+Eb4  `11`:Eb6  `11.5`:C6  `12`:Bb5  `12.5`:G5  `13`:F5  `13.5`:Eb5  `14`:C5 |
| **53** | `128` | *mf* | **Fm** | `iv` | `0`:F1+F2  `6`:C3  `8`:F3  `12`:F2 | `0`:G4+Bb4  `8`:G4  `12`:Bb4  `14`:F4 |
| **54** | `128` | *mf* | **Gm** | `v` | `0`:G1+G2  `6`:D3  `8`:G3  `12`:G2 | `6`:Eb5  `6.5`:C5  `7`:Bb4  `7.5`:G4  `8`:F4  `10`:G4  `12`:Bb4  `14`:C5 |
| **55** | `136` | *mf* | **F (Dorian Trill I)** | `IV` | `0`:F1+F2  `2`:C2  `4`:F2  `6`:A2+C3  `8`:F2  `10`:A2+C3  `12`:F3  `14`:A3 | `0`:D5  `1`:C5  `2`:D5  `3`:C5  `4`:D5  `5`:C5  `6`:D5  `7`:C5  `8`:D5  `9`:C5  `10`:D5  `11`:Eb5  `12`:F5  `13`:G5  `14`:C4+A5  `15`:Bb5 |
| **56** | `138` | *f* | **F (Dorian Trill II)** | `IV` | `2`:A3  `4`:F3  `6`:C3  `8`:A2  `10`:F3  `12`:C3  `14`:F2+A2 | `0`:F4+C6  `1`:C4+D6  `2`:C6  `3`:D6  `4`:C6  `5`:D6  `6`:C6  `7`:D6  `8`:C6  `9`:D6  `10`:C6  `11`:D6  `12`:C6  `13`:D6  `14`:C6  `15`:D6 |

### VIIb. Breakthrough Ostinato

| Bar | Tempo | Dyn | Chord | Roman | Left Hand (`step`:voicing) | Right Hand (`step`:voicing) |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **57** | `132` | *f* | **Cm** | `i` | `0`:C2+G2+C3  `2`:G2+G3  `4`:G2+G3  `6`:G2+G3  `8`:G2+C3+G3  `10`:G2+G3  `12`:G2+C3+G3  `14`:G2+G3 | `0`:C4+Eb4+G4  `2`:C4+Eb4+G4  `4`:C4+Eb4+G4  `6`:C4+Eb4+G4  `8`:C4+Eb4+G4  `10`:C4+Eb4+G4  `12`:C4+Eb4+G4  `14`:C4+Eb4+G4 |
| **58** | `132` | *f* | **Bb/C -> Cm** | `VII/1 -> i` | `0`:C2+G2+C3+Bb3  `2`:G2+G3  `4`:G2+G3  `6`:G2+G3  `8`:G2+C3+G3  `10`:G2+G3  `12`:G2+C3+G3  `14`:G2+G3 | `0`:D4+F4+D5  `2`:C4+G4  `4`:C4+G4  `6`:C4+G4  `8`:C4+G4  `10`:C4+G4  `12`:F4+G4  `14`:G4 |
| **59** | `132` | *f* | **Ab/C -> Cm** | `VI/1 -> i` | `0`:C2+G2+C3+Eb3+Ab3  `2`:G2+G3  `4`:G2+G3  `6`:G2+G3  `8`:G2+C3+G3  `10`:G2+G3  `12`:G2+C3+G3  `14`:G2+G3 | `0`:C4+Eb4+G4+Ab4  `2`:C4+Eb4+G4+Ab4  `4`:C4+Eb4+G4+Ab4  `6`:C4+Eb4+G4  `8`:C4+Eb4+G4  `10`:C4+Eb4+G4  `12`:C4+Eb4+G4  `14`:C4+Eb4+G4 |
| **60** | `132` | *ff* | **Cm** | `i` | `0`:C2+G2+C3  `4`:G2+G3  `6`:G2+G3  `8`:G2+C3+G3  `10`:G2+G3  `12`:G2+C3+G3  `14`:G2+G3 | `0`:C4+F4  `2`:F4  `4`:G4  `6`:G4+Bb4  `8`:G4+C5  `11`:G4+Bb4  `14`:G4 |
| **61** | `132` | *f* | **Cm** | `i` | `0`:C2+G2+C3  `2`:G2+G3  `4`:G2+G3  `6`:G2+G3  `8`:G2+C3+G3  `10`:G2+G3  `12`:G2+C3+G3  `14`:G2+G3 | `0`:C4+Eb4+G4  `2`:C4+Eb4+G4  `4`:C4+Eb4+G4  `6`:C4+Eb4+G4  `8`:C4+Eb4+G4  `10`:C4+Eb4+G4  `12`:C4+Eb4+G4  `14`:C4+Eb4+G4 |
| **62** | `132` | *f* | **Bb/C -> Cm** | `VII/1 -> i` | `0`:C2+G2+C3+Bb3  `2`:G2+G3  `4`:G2+G3  `6`:G2+G3  `8`:G2+C3+G3  `10`:G2+G3  `12`:G2+C3+G3  `14`:G2+G3 | `0`:D4+F4+D5  `2`:C4+G4  `4`:C4+G4  `6`:C4+G4  `8`:C4+G4  `10`:C4+G4  `12`:C4+G4  `14`:C4+G4 |
| **63** | `132` | *ff* | **Ab/C -> Cm** | `VI/1 -> i` | `0`:C2+G2+C3+Eb3+Ab3  `4`:G2+G3  `6`:G2+G3  `8`:G2+C3+G3  `10`:G2+G3  `12`:G2+C3+G3  `14`:G2+G3 | `0`:C4+Ab4  `2`:C4+G4  `4`:C4+F4  `6`:F4  `8`:F4+G4  `11`:F4+G4+Bb4  `14`:G4 |
| **64** | `132` | *ff* | **F (Dorian IV)** | `IV` | `0`:F1+F2  `2`:C2  `4`:F2  `6`:A2+C3  `8`:F2  `9`:A2  `10`:C3  `11`:F3  `12`:A3 | `0`:F4+A4+C5+F5  `12`:C4  `13`:Eb4  `14`:Ab4  `15`:Bb4 |

### VIIIa. Chorus 2

| Bar | Tempo | Dyn | Chord | Roman | Left Hand (`step`:voicing) | Right Hand (`step`:voicing) |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **65** | `130` | *ff* | **Ab** | `VI` | `0`:Ab1+Ab2  `2`:Eb2  `4`:Ab2  `6`:Ab2  `8`:Eb3+Ab3  `10`:Ab2  `12`:Ab2  `14`:Eb2 | `0`:Eb4+Ab4+C5  `4`:C5+C6  `6`:Bb4+Bb5  `8`:C5+C6  `11`:Eb5+Eb6  `14`:C5+C6 |
| **66** | `130` | *ff* | **Bb** | `VII` | `0`:Bb1+Bb2  `2`:F2  `4`:Bb2  `6`:Bb2  `8`:F3+Bb3  `10`:Bb2  `12`:Bb2  `14`:F2 | `4`:C5+C6  `6`:Bb4+Bb5  `8`:C5+C6  `11`:F5+F6  `14`:Eb5+Eb6 |
| **67** | `130` | *ff* | **Bb/C -> Cm** | `VII/1 -> i` | `0`:C2+C3  `2`:G2  `4`:C3  `6`:G2  `8`:C3+G3  `10`:C3  `12`:C3  `14`:G2 | `0`:F5+D6+F6  `3`:G5+Eb6+G6  `6`:G5+Eb6+G6  `14`:Eb5+C6+Eb6 |
| **68** | `130` | *ff* | **Cm** | `i` | `0`:C2+C3  `2`:G2  `4`:C3  `6`:G2  `8`:C3+G3  `10`:C3  `12`:C3  `14`:G2 | `0`:F5+D6+F6  `3`:G5+Eb6+G6  `6`:G5+Eb6+G6  `8`:G5+Eb6+G6  `11`:F5+D6+F6  `14`:Eb5+C6+Eb6 |
| **69** | `130` | *ff* | **Ab** | `VI` | `0`:Ab1+Ab2  `2`:Eb2  `4`:Ab2  `6`:Ab2  `8`:Eb3+Ab3  `10`:Ab2  `12`:Ab2  `14`:Eb2 | `4`:C5+C6  `6`:Bb4+Bb5  `8`:C5+C6  `11`:Eb5+Eb6  `14`:C5+C6 |
| **70** | `130` | *ff* | **Bb** | `VII` | `0`:Bb1+Bb2  `2`:F2  `4`:Bb2  `6`:Bb2  `8`:F3+Bb3  `10`:Bb2  `12`:Bb2  `14`:F2 | `4`:C5+C6  `6`:Bb4+Bb5  `8`:C5+C6  `11`:F5+F6  `14`:Eb5+Eb6 |
| **71** | `130` | *ff* | **Bb/C -> Cm** | `VII/1 -> i` | `0`:C2+C3  `2`:G2  `4`:C3  `6`:G2  `8`:C3+G3  `10`:C3  `12`:C3  `14`:G2 | `0`:F5+D6+F6  `3`:G5+Eb6+G6  `6`:G5+Eb6+G6  `14`:Eb5+C6+Eb6 |
| **72** | `130` | *ff* | **Cm** | `i` | `0`:C2+C3  `2`:G2  `4`:C3  `6`:G2  `8`:C3+G3  `10`:C3  `12`:C3  `14`:G2 | `0`:F5+D6+F6  `3`:G5+Eb6+G6  `6`:Bb5+G6+Bb6  `8`:G5+Eb6+G6  `11`:F5+D6+F6  `14`:Eb5+C6+Eb6 |

### VIIIb. Chorus Ext

| Bar | Tempo | Dyn | Chord | Roman | Left Hand (`step`:voicing) | Right Hand (`step`:voicing) |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **73** | `132` | *ff* | **Ab** | `VI` | `0`:Ab1+Ab2  `2`:Eb2  `4`:Ab2  `6`:Ab2  `8`:Eb3+Ab3  `10`:Ab2  `12`:Ab2 | `0`:F5+F6  `2`:Eb5+Eb6  `4`:C5+C6  `6`:G5+G6  `8`:F5+F6  `10`:Eb5+Eb6  `12`:C5+C6  `14`:Bb4+Bb5 |
| **74** | `132` | *ff* | **Bb** | `VII` | `0`:Bb1+Bb2  `2`:F2  `4`:Bb2  `6`:Bb2  `8`:F3+Bb3  `10`:Bb2  `12`:Bb2  `14`:F2 | `2`:F4+F5  `6`:G4+G5  `10`:Bb4+Bb5 |
| **75** | `132` | *ff* | **Cm** | `i` | `0`:C2+C3  `2`:G2  `4`:C3  `6`:G2  `8`:C3+G3  `10`:C3  `12`:C3  `14`:G2 | `0`:F5+F6  `2`:Eb5+Eb6  `4`:C5+C6  `6`:G5+G6  `8`:F5+F6  `10`:Eb5+Eb6  `12`:Bb4+Bb5  `14`:C5+C6 |
| **76** | `132` | *f* | **Cm** | `i` | `0`:C2+C3  `2`:G2  `4`:C3  `6`:G2  `8`:C3+G3  `10`:C3  `12`:C3  `14`:G2 | `0`:C4+F5  `6`:C4+G4+G5  `12`:Eb5 |
| **77** | `132` | *ff* | **Ab** | `VI` | `0`:Ab1+Ab2  `2`:Eb2  `4`:Ab2  `6`:Ab2  `8`:Eb3+Ab3  `10`:Ab2  `12`:Ab2 | `0`:F5+F6  `2`:Eb5+Eb6  `4`:C5+C6  `6`:G5+G6  `8`:F5+F6  `10`:Eb5+Eb6  `12`:C5+C6  `14`:Bb4+Bb5 |
| **78** | `132` | *ff* | **Bb** | `VII` | `0`:Bb1+Bb2  `2`:F2  `4`:Bb2  `6`:Bb2  `8`:F3+Bb3  `10`:Bb2  `12`:Bb2  `14`:F2 | `2`:F4+F5  `6`:G4+G5  `12`:Bb4+Bb5 |
| **79** | `132` | *f* | **Cm** | `i` | `0`:C2+C3  `2`:G2  `4`:C3  `6`:G2  `8`:C3+G3  `10`:C3  `12`:C3  `14`:G2 | `0`:C6+F6  `2`:Bb5+Eb6  `4`:G5+C6  `12`:C6+F6  `14`:Bb5+Eb6 |
| **80** | `132` | *f* | **Cm** | `i` | `0`:C2+C3  `2`:G2  `4`:C3  `6`:G2  `8`:C3+G3  `10`:C3  `12`:C3  `14`:G2 | `0`:C4+Eb4+G4+G5+C6 |

### VIIIc. Operatic Climax

| Bar | Tempo | Dyn | Chord | Roman | Left Hand (`step`:voicing) | Right Hand (`step`:voicing) |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **81** | `130` | *ff* | **Ab** | `VI` | `0`:Ab1+Ab2  `6`:Eb3+Ab3  `8`:Eb3+Ab3  `10`:Eb3+Ab3  `12`:Ab2+Eb3+Ab3  `14`:Eb3 | `4`:C4+C5  `8`:D4+D5  `12`:Eb4+Eb5 |
| **82** | `130` | *ff* | **Bb** | `VII` | `0`:Bb1+Bb2  `3`:Bb2+Bb3  `6`:F3+Bb3  `8`:F3+Bb3  `10`:F3+Bb3  `12`:Bb2+F3+Bb3  `14`:F3 | `0`:F4+D5+F5  `6`:Eb4+Eb5 |
| **83** | `130` | *ff* | **Cm** | `i` | `0`:C2+C3  `6`:G2+G3  `8`:C3+G3  `10`:G2+G3  `12`:C3+G3  `14`:G2 | `4`:C4+G4+C5  `6`:C4+G4+C5  `8`:D4+D5  `12`:Eb4+Eb5 |
| **84** | `130` | *ff* | **Cm** | `i` | `0`:C2+C3  `3`:C3+G3  `6`:G2+G3  `8`:C3+G3  `10`:G2+G3  `12`:C3+G3  `14`:G2 | `0`:F4+D5+F5  `6`:G4+Eb5+G5  `12`:Eb4+C5+Eb5 |
| **85** | `130` | *ff* | **Ab** | `VI` | `0`:Ab1+Ab2  `6`:Eb3+Ab3  `8`:Eb3+Ab3  `10`:Eb3+Ab3  `12`:Ab2+Eb3+Ab3  `14`:Eb3 | `4`:C4+C5  `8`:D4+D5  `12`:Eb4+Eb5 |
| **86** | `130` | *ff* | **Bb** | `VII` | `0`:Bb1+Bb2  `3`:Bb2+Bb3  `6`:F3+Bb3  `8`:F3+Bb3  `10`:F3+Bb3  `12`:Bb2+F3+Bb3  `14`:F3 | `0`:F4+D5+F5  `6`:Eb4+Eb5  `12`:G4+Eb5+G5 |
| **87** | `130` | *ff* | **Cm** | `i` | `0`:C2+C3  `6`:G2+G3  `8`:C3+G3  `10`:G2+G3  `12`:C3+G3  `14`:G2 | `4`:C4+G4+C5  `6`:C4+G4+C5  `8`:D4+D5  `12`:Eb4+Eb5 |
| **88** | `130` | *ff* | **Cm** | `i` | `0`:C2+C3  `6`:G2+G3  `8`:C3+G3  `10`:G2+G3  `12`:C3+G3  `14`:G2 | `0`:F4+D5+F5  `6`:G4+Eb5+G5  `12`:G4+Eb5+G5 |
| **89** | `132` | *ff* | **Ab** | `VI` | `0`:Ab1+Ab2  `6`:Eb3+Ab3  `8`:Eb3+Ab3+Eb4  `10`:Eb3+Ab3  `12`:Ab2+Eb3+Ab3  `14`:Eb3 | `0`:C6+C7  `3`:Bb5+Bb6  `4`:C6+C7  `8`:Bb5+Bb6 |
| **90** | `132` | *ff* | **Bb** | `VII` | `0`:Bb1+Bb2  `3`:Bb2+Bb3  `6`:F3+Bb3  `8`:F3+Bb3+F4  `10`:F3+Bb3  `12`:Bb2+F3+Bb3  `14`:F3 | `0`:G5+G6  `6`:C6+C7  `8`:Bb5+Bb6 |
| **91** | `132` | *ff* | **Cm** | `i` | `0`:C2+C3  `2`:G2  `4`:C3  `6`:G2  `8`:C3+G3  `10`:C3  `12`:C3  `14`:G2 | `0`:G5+Eb6+G6  `6`:Bb5+Bb6  `8`:G5+G6  `12`:F5+F6 |
| **92** | `132` | *ff* | **Cm** | `i` | `0`:C2+C3  `2`:G2  `4`:C3  `6`:G2  `8`:C3+G3  `10`:C3  `12`:C3  `14`:G2 | `0`:Eb5+C6+Eb6  `8`:Eb4+G4+C5+Eb5+G5+C6 |
| **93** | `132` | *ff* | **Ab** | `VI` | `0`:Ab1+Ab2  `6`:Eb3+Ab3  `8`:Eb3+Ab3+Eb4  `10`:Eb3+Ab3  `12`:Ab2+Eb3+Ab3  `14`:Eb3 | `0`:C6+C7  `3`:Bb5+Bb6  `4`:C6+C7  `8`:Bb5+Bb6 |
| **94** | `132` | *ff* | **Bb** | `VII` | `0`:Bb1+Bb2  `3`:Bb2+Bb3  `6`:F3+Bb3  `8`:F3+Bb3+F4  `10`:F3+Bb3  `12`:Bb2+F3+Bb3  `14`:F3 | `0`:G5+G6  `6`:Bb5+Bb6  `8`:F5+F6 |
| **95** | `132` | *ff* | **Eb** | `III` | `0`:Eb2+Eb3  `6`:Bb2+Bb3  `8`:Eb3+Bb3  `10`:Bb2+Bb3  `12`:Eb3+Bb3  `14`:Bb2 | `0`:Eb6+Bb6+Eb7  `8`:Bb5+Bb6  `10`:C6+C7  `11`:Bb5+Bb6  `12`:G5+G6  `14`:F5+F6 |
| **96** | `132` | *ff* | **Gm (Dominant v)** | `v` | `0`:G1+G2  `2`:D2  `4`:G2  `6`:D3  `8`:G3+D4  `10`:D3  `12`:G2+D3 | `0`:G4+G5+D6+G6 |
| **97** | `132` | *ff* | **Ab** | `VI` | `0`:Ab1+Ab2  `6`:Eb3+Ab3  `8`:Eb3+Ab3+Eb4  `10`:Eb3+Ab3  `12`:Ab2+Eb3+Ab3  `14`:Eb3 | `0`:C6+C7  `3`:Bb5+Bb6  `4`:C6+C7  `8`:Eb5+Eb6+Eb7 |
| **98** | `132` | *ff* | **Bb** | `VII` | `0`:Bb1+Bb2  `3`:Bb2+Bb3  `6`:F3+Bb3  `8`:F3+Bb3+F4  `10`:F3+Bb3  `12`:Bb2+F3+Bb3  `14`:F3 | `0`:G5+G6  `6`:C6+C7  `8`:Bb5+Bb6 |
| **99** | `132` | *ff* | **Cm** | `i` | `0`:C2+C3  `2`:G2  `4`:C3  `6`:G2  `8`:C3+G3  `10`:C3  `12`:C3  `14`:G2 | `0`:G5+G6  `6`:Eb6+Eb7  `8`:C6+C7  `12`:Bb5+Bb6 |
| **100** | `132` | *ff* | **Ab -> Gm** | `VI -> v` | `0`:Ab1+Ab2  `2`:Eb2  `4`:Ab2  `6`:Eb3  `8`:Ab3+Eb4  `10`:Eb3  `12`:G1+G2 | `0`:C6+C7  `12`:G5+G6  `14`:Bb5+Bb6  `15`:G5+G6 |
| **101** | `132` | *ff* | **Fm** | `iv` | `0`:F1+F2  `2`:C2  `4`:F2  `6`:C3  `8`:F3+C4  `10`:C3  `12`:F3+Ab3+F4 | `0`:F4+F5+F6 |
| **102** | `132` | *ff* | **Fm** | `iv` | `0`:F4  `2`:F3+Ab3  `4`:F3  `6`:C3  `8`:F3  `10`:C3  `12`:F2+F3 | `8`:F4+Eb5+Eb6  `12`:F4+F5+F6 |
| **103** | `132` | *ff* | **Ab** | `VI` | `0`:Ab1+Ab2  `2`:Eb2  `4`:Ab2  `6`:Eb3  `8`:Ab3+Eb4  `10`:Eb3  `12`:Ab2+Eb3 | `0`:G5+G6  `12`:Bb5+Bb6 |
| **104** | `132` | *ff* | **Bb** | `VII` | `0`:Bb1+Bb2  `3`:Bb2+Bb3  `6`:F3+Bb3  `8`:F3+Bb3+F4  `10`:F3+Bb3  `12`:Bb2+F3+Bb3  `14`:F3 | `0`:F5+F6  `3`:Eb5+Eb6  `4`:F5+F6  `8`:G5+G6  `12`:Bb5+Bb6 |
| **105** | `130` | *ff* | **Cm** | `i` | `0`:C2+C3 | `0`:Eb6+C7+Eb7  `6`:C4+G4+C6+G6+C7 |
| **106** | `128` | *mf* | **Cm (Waterfall)** | `i` | `0`:C3 | `0`:Eb4+G4+Eb5  `8`:Eb6  `8.5`:C6  `9`:Bb5  `9.5`:G5  `10`:F5  `10.5`:Eb5  `11`:C5  `11.5`:Bb4  `12`:G4  `12.5`:F4  `13`:Eb4 |

### IX. Outro

| Bar | Tempo | Dyn | Chord | Roman | Left Hand (`step`:voicing) | Right Hand (`step`:voicing) |
| :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **107** | `125` | *p* | **Ab/C** | `VI/1` | `0`:C2+C3  `12`:C3 | `0`:~C4+Eb4+Ab4  `8`:~C4+Eb4+Ab4 |
| **108** | `125` | *p* | **Bb/C** | `VII/1` | `0`:C3 | `0`:~F4+Ab4+Bb4  `8`:F4  `14`:Eb6  `14.5`:C6  `15`:Bb5  `15.5`:G5 |
| **109** | `122` | *p* | **Fm7** | `iv7` | `0`:F2+C3+F3 | `0`:F5  `2`:Eb5  `4`:C5  `6`:G5  `8`:F5  `10`:Eb5  `12`:C5  `14`:Bb4 |
| **110** | `122` | *p* | **Gm7** | `v7` | `0`:G2+D3 | `2`:F4  `6`:G4  `12`:Bb4  `15`:F4 |
| **111** | `118` | *p* | **Cm9** | `i9` | `0`:~C3+G3+D4+Eb4 | `0`:~G4+C5  `12`:Bb4  `14`:C5 |
| **112** | `122` | *p* | **Cm -> G(half)** | `i -> V` | *(tacet)* | `0`:Eb4  `8`:D4  `14`:Eb6  `14.5`:C6  `15`:Bb5  `15.5`:G5 |
| **113** | `118` | *p* | **Fm7** | `iv7` | `0`:F2+C3+F3 | `0`:F5  `2`:Eb5  `4`:C5  `6`:G5  `8`:F5  `10`:Eb5  `12`:C5  `14`:Bb4 |
| **114** | `118` | *p* | **Gm7** | `v7` | `0`:G2+D3 | `2`:F4  `6`:G4  `12`:Bb4  `15`:F4 |
| **115** | `104` | *pp* | **Cm9** | `i9` | `0`:~C3+G3+Eb4+F4 | `0`:~C5  `8`:Eb6  `8.5`:C6  `9`:Bb5  `9.5`:G5  `10`:F5  `10.5`:Eb5  `11`:C5  `11.5`:Bb4  `12`:G4  `12.5`:F4  `13`:Eb4 |
| **116** | ` 80` | *pp* | **Cm (Final Tonic)** | `i` | `0`:C2+G2+C3 | `0`:~G3+C4+Eb4 |

