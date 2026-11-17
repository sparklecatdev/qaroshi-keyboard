#!/usr/bin/env python3
"""Copy shared offline assets into native mobile projects, deterministically."""
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[1]
for directory in (ROOT/"android/app/src/main/assets", ROOT/"ios/Keyboard/Resources"):
    directory.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT/"mapping.json",directory/"mapping.json")
    shutil.copyfile(ROOT/"data/qaroshi-lexicon.json",directory/"qaroshi-lexicon.json")
    print("Refreshed offline assets in",directory)
