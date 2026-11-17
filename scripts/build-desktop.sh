#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
command -v kmc >/dev/null || { echo "Install @keymanapp/kmc@18 first"; exit 1; }
for layout in qwerty azerty dvorak; do
  id="qaroshi_${layout}"
  mkdir -p "layouts/${layout}/build"
  kmc build "layouts/${layout}/source/${id}.kmn" -o "layouts/${layout}/build/${id}.kmx"
  kmc build "layouts/${layout}/source/${id}_desktop.kps" -o "layouts/${layout}/build/${id}_desktop.kmp"
done
python3 -m unittest discover -s tests -v
python3 scripts/verify_platform_packages.py desktop
