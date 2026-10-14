# syntax=docker/dockerfile:1
# Version-pinned, bit-reproducible synthesis & mastering environment for:
#   "Extraordinary (不凡)" — First-Principles Piano Reduction & 96 kHz Acoustic Mastering
FROM python:3.11.15-slim-bookworm@sha256:d29f48a31a8b408ed19272ca1e7b10ebae13b240a27e862d3d4217c528e2e0c3

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    OMP_NUM_THREADS=4 \
    OPENBLAS_NUM_THREADS=4

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg=7:5.1.9-0+deb12u1 \
    fluidsynth=2.3.1-2 \
    fluid-soundfont-gm=3.1-5.3 \
    musescore-general-soundfont-lossless=0.2.1-1 \
    libsndfile1=1.2.0-1+deb12u1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    numpy==1.26.4 \
    scipy==1.13.1 \
    pretty_midi==0.2.10 \
    soundfile==0.12.1

WORKDIR /workspace
ENTRYPOINT ["python3", "/workspace/extraordinary_reduction.py"]
