#!/usr/bin/env python3
"""Per-user IBus install; never modifies /usr or global XKB."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
dest = Path.home() / ".local/share/qaroshi-ibus"
component = Path.home() / ".local/share/ibus/component/qaroshi.xml"
if len(sys.argv) == 2 and sys.argv[1] == "--uninstall":
    component.unlink(missing_ok=True)
    if dest.is_dir():
        shutil.rmtree(dest)
    print("Qaroshi IBus removed. Run ibus restart and sign out/in if necessary.")
    sys.exit(0)
if len(sys.argv) != 1:
    raise SystemExit("Usage: python3 install.py [--uninstall]")
if not shutil.which("ibus"):
    raise SystemExit("Install the ibus and python-gobject/python3-gi packages first.")
dest.mkdir(parents=True, exist_ok=True)
component.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(Path(__file__).with_name("engine.py"), dest / "engine.py")
shutil.copyfile(ROOT / "mapping.json", dest / "mapping.json")
shutil.copyfile(ROOT / "data/qaroshi-lexicon.json", dest / "qaroshi-lexicon.json")
shutil.copyfile(ROOT / "smarttext/qaroshi.py", dest / "qaroshi.py")
# Engine expects the installed bundle's parent for Python resources:
engine = (dest / "engine.py").read_text()
engine = engine.replace('ROOT = pathlib.Path(__file__).resolve().parents[3]', 'ROOT = pathlib.Path(__file__).resolve().parent')
engine = engine.replace('sys.path.insert(0, str(ROOT / "smarttext"))', 'sys.path.insert(0, str(ROOT))')
engine = engine.replace('ROOT / "mapping.json"', 'ROOT / "mapping.json"')
(dest / "engine.py").write_text(engine)
assist = (dest / "qaroshi.py").read_text().replace('pathlib.Path(__file__).resolve().parents[1] / "data" / "qaroshi-lexicon.json"','pathlib.Path(__file__).resolve().parent / "qaroshi-lexicon.json"')
(dest / "qaroshi.py").write_text(assist)
component.write_text(Path(__file__).with_name("qaroshi.xml").read_text().replace("@INSTALL_DIR@", str(dest)))
print("Installed Qaroshi IBus source in",dest)
print("Run 'ibus restart', then add Qaroshi in IBus Preferences. KDE Wayland may require configuring IBus session integration.")
