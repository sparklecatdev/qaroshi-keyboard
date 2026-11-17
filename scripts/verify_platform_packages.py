#!/usr/bin/env python3
"""Validate platform-specific compiled packages; fail on leaked wrong-target binaries."""
import json
import pathlib
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLATFORMS = {"desktop": (".kmx", ".js"), "mobile": (".js", ".kmx")}

def verify(target: str) -> None:
    if target not in PLATFORMS:
        raise SystemExit("Usage: python scripts/verify_platform_packages.py desktop|mobile")
    want, forbidden = PLATFORMS[target]
    for layout in ("qwerty", "azerty", "dvorak"):
        path = ROOT / "layouts" / layout / "build" / f"qaroshi_{layout}_{target}.kmp"
        with zipfile.ZipFile(path) as archive:
            names = {x.lower().split("/")[-1] for x in archive.namelist()}
            assert "kmp.json" in names, f"{path} missing metadata"
            assert f"qaroshi_{layout}{want}" in names, f"{path} missing {want}"
            assert f"qaroshi_{layout}{forbidden}" not in names, f"{path} contains {forbidden}"
            meta = json.loads(archive.read(next(x for x in archive.namelist() if x.lower().endswith("kmp.json"))))
            assert meta.get("keyboards"), f"{path} missing keyboard metadata"
        print(f"PASS {target}: {path}")

if __name__ == "__main__":
    verify(sys.argv[1] if len(sys.argv) == 2 else "")
