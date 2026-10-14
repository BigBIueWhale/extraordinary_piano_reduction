#!/usr/bin/env bash
# Reproducible, isolated Docker build & render pipeline (single mode, zero fallbacks).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_TAG="extraordinary-piano-render-tmp:pinned"

cleanup() {
    docker rmi -f "${IMAGE_TAG}" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "[1/3] Building version-pinned Docker image (${IMAGE_TAG})..."
docker build -t "${IMAGE_TAG}" "${SCRIPT_DIR}"

echo "[2/3] Running first-principles symbolic compilation & 96 kHz physical/acoustic mastering..."
docker run --rm --network=none \
    -u "$(id -u):$(id -g)" \
    -v "${SCRIPT_DIR}:/workspace" \
    "${IMAGE_TAG}"

echo "[3/3] Verifying generated artifacts..."
test -s "${SCRIPT_DIR}/extraordinary.mid"
test -s "${SCRIPT_DIR}/extraordinary.mp3"
test -s "${SCRIPT_DIR}/CHORD_REDUCTION_SCORE.md"
ls -lh "${SCRIPT_DIR}/extraordinary.mid" "${SCRIPT_DIR}/extraordinary.mp3" "${SCRIPT_DIR}/CHORD_REDUCTION_SCORE.md"
echo "Done."
