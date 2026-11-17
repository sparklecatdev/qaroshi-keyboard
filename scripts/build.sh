#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
command -v kmc >/dev/null || { echo "Keyman Developer compiler 'kmc' is required"; exit 1; }
for layout in qwerty azerty dvorak; do
  id="qaroshi_${layout}"
  mkdir -p "layouts/${layout}/build"
  kmc build "layouts/${layout}/source/${id}.kmn" -o "layouts/${layout}/build/${id}.kmx"
  test -s "layouts/${layout}/build/${id}.kmx"
  test -s "layouts/${layout}/build/${id}.js"
  kmc build "layouts/${layout}/source/${id}.kps" -o "layouts/${layout}/build/${id}.kmp"
  test -s "layouts/${layout}/build/${id}.kmp"
done
python3 -m unittest discover -s tests -v
python3 scripts/verify_packages.py
echo "Built 3 Keyman .kmp packages under layouts/*/build/"
