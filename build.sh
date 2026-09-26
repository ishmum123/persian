#!/bin/sh
# Builds the self-contained Persian trainer and writes it to index.html at
# the repo root, so GitHub Pages serves it at https://bannerless-studio.github.io/persian/
# Usage: ./build.sh   (or: sh build.sh)
set -e
cd "$(dirname "$0")"

OUT="${1:-index.html}"
engine/build.sh pack "$OUT"
