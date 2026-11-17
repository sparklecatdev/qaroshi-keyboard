#!/usr/bin/env python3
"""Verify compiled packages contain installable desktop and mobile keyboard files."""
import pathlib
import zipfile

root = pathlib.Path(__file__).resolve().parents[1]
for kind in ("qwerty", "azerty", "dvorak"):
    path = root / "layouts" / kind / "build" / f"qaroshi_{kind}.kmp"
    with zipfile.ZipFile(path) as archive:
        names = {name.lower().rsplit("/", 1)[-1] for name in archive.namelist()}
        expected = {"kmp.json", f"qaroshi_{kind}.kmx", f"qaroshi_{kind}.js"}
        missing = expected - names
        assert not missing, f"{path} missing {sorted(missing)}"
    print(f"Package validated: {path}")
