#!/usr/bin/env python3
"""Build a self-contained, source-based Linux IBus install bundle."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/"dist"
DIST.mkdir(exist_ok=True)
with ZipFile(DIST/"qaroshi-linux-ibus.zip","w",ZIP_DEFLATED) as z:
    for name in [
        "mapping.json",
        "data/qaroshi-lexicon.json",
        "smarttext/qaroshi.py",
        "desktop/native/linux/ibus/engine.py",
        "desktop/native/linux/ibus/qaroshi.xml",
        "desktop/native/linux/ibus/install.py",
        "docs/NATIVE_INSTALL.md",
        "LICENSE",
    ]:
        z.write(ROOT/name,name)
print("Created",DIST/"qaroshi-linux-ibus.zip")
