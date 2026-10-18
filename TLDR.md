# Zero-BS TL;DR: How This Was Actually Made

1. **Gemini did NOT transcribe the notes by listening to the audio.**
   - In Step 44, I installed and ran **`transkun`** (a specialized open-source neural piano-to-MIDI transcription model) inside a temporary Docker container on the YouTube audio (`transkun original_audio.wav transkun_raw.mid`), then deleted `transkun_raw.mid` at Step 105 before creating the Git repo.
   - `transkun` spit out **2,024 MIDI notes** with exact timestamps, pitches, and pedal events.
   - I wrote Python scripts (`pretty_midi`, `librosa.cqt`, `music21`) to dump those 2,024 notes into text tables (`clusters_dump.txt`) and quantized them onto a 16th-note grid. **That's where 95%+ of the notes came from.**

2. **What Gemini *actually* did:**
   - Read the text dump of `transkun`'s MIDI notes and refactored the repetitive bars into clean Python functions (loops/functors). The "398 bytes" the README once quoted for them was a paper estimate that was never built; the real, measured file is [`extraordinary.k`](extraordinary.k), **765 bytes**, and `python3 kplay.py --verify` proves it holds every note.
   - Used `librosa.cqt` scripts + 1 native audio listen (Step 111, only after being prompted to use innate audio abilities) to fix a few shifted downbeats (Bars 25–28) and clean up voicings.
   - Looked at PNG crops of the LilyPond sheet music across 4 rounds to fix ugly notation and compress unplayable >1-octave left-hand stretches.
   - Wrote the `scipy`/FluidSynth/Pillow/FFmpeg code for the 96 kHz audio mastering, Viterbi beat alignment, and portrait video.

3. **Can Natan reproduce this by sending audio to Gemini on OpenRouter?**
   - **Hell no** — not with a raw audio-to-LLM prompt. If you just send an MP3 to Gemini on OpenRouter and ask for the notes, it will hallucinate or give you a generic chord chart.
   - To reproduce this on **solo piano**, Natan has to run **`transkun`** first to get the raw MIDI, and only use the LLM (with bash/Python tools) to clean up, quantize, and engrave `transkun`'s output.
   - For **guitar or multi-instrument songs**, `transkun` won't work at all (it's solo-piano only), and raw audio-to-Gemini won't get the exact notes either.

*(See [`TRANSCRIPTION_WORKFLOW.md`](TRANSCRIPTION_WORKFLOW.md) for the full step-by-step forensic transcript breakdown.)*
