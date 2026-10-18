#!/usr/bin/env bash
# Reproducible, isolated Docker build & render pipeline (single mode, zero fallbacks).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_TAG="extraordinary-piano-render-tmp:pinned"

cleanup() {
    docker rmi -f "${IMAGE_TAG}" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "[1/4] Building version-pinned Docker image (${IMAGE_TAG})..."
docker build -t "${IMAGE_TAG}" "${SCRIPT_DIR}"

echo "[2/4] Running first-principles symbolic compilation, dynamic rubato alignment, LilyPond engraving, 96 kHz mastering & portrait showcase video render (pinned to <= 50% physical cores: 4 P-cores + 8 E-cores)..."
docker run --rm --network=none \
    --cpuset-cpus="4-7,16-23" \
    --cpus="12" \
    -u "$(id -u):$(id -g)" \
    -v "${SCRIPT_DIR}:/workspace" \
    "${IMAGE_TAG}"

echo "[3/4] Verifying the 765-byte extraordinary.k against the score and rendering it on its own tempo marks..."
for kplay_args in "--verify" "/workspace/extraordinary.k"; do
    docker run --rm --network=none \
        --cpuset-cpus="4-7,16-23" \
        --cpus="12" \
        -u "$(id -u):$(id -g)" \
        -v "${SCRIPT_DIR}:/workspace" \
        --entrypoint python3 \
        "${IMAGE_TAG}" /workspace/kplay.py ${kplay_args}
done

echo "[4/4] Verifying generated artifacts..."
test -s "${SCRIPT_DIR}/extraordinary.mid"
test -s "${SCRIPT_DIR}/extraordinary.mp3"
test -s "${SCRIPT_DIR}/extraordinary_sheet_music.png"
test -s "${SCRIPT_DIR}/CHORD_REDUCTION_SCORE.md"
test -s "${SCRIPT_DIR}/extraordinary_showcase.mp4"
test -s "${SCRIPT_DIR}/extraordinary_k.mid"
test -s "${SCRIPT_DIR}/extraordinary_k.mp3"
ls -lh \
    "${SCRIPT_DIR}/extraordinary.mid" \
    "${SCRIPT_DIR}/extraordinary.mp3" \
    "${SCRIPT_DIR}/extraordinary_sheet_music.png" \
    "${SCRIPT_DIR}/CHORD_REDUCTION_SCORE.md" \
    "${SCRIPT_DIR}/extraordinary_showcase.mp4" \
    "${SCRIPT_DIR}/extraordinary.k" \
    "${SCRIPT_DIR}/extraordinary_k.mid" \
    "${SCRIPT_DIR}/extraordinary_k.mp3"
echo "Done."

