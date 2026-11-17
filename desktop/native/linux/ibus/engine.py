#!/usr/bin/env python3
"""Native IBus Qaroshi input-method engine, uses the desktop's input framework.

Requires /usr/bin/python3 GI+IBus 1.0. No shell command execution or network.
"""
import json
import pathlib
import sys

import gi
gi.require_version("IBus", "1.0")
from gi.repository import IBus, GLib

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "smarttext"))
from qaroshi import autocorrect, suggestions

SPEC = json.loads((ROOT / "mapping.json").read_text(encoding="utf-8"))
# IBus sends the US physical key's keysym when a US base layout is selected.
ORDINARY = {}
for variant, rows in SPEC["layoutRows"].items():
    table = {}
    for i, row in enumerate(rows):
        for j, symbol in enumerate(row):
            keyname = SPEC["physicalRows"][i][j]
            low = SPEC["specialLetterReplacements"].get(symbol, symbol)
            high = SPEC["shiftPunctuation"].get(variant, {}).get(keyname, low[:1].upper()+low[1:])
            keyval = {"COLON": ";", "COMMA": ",", "PERIOD": ".", "SLASH": "/"}.get(keyname, keyname.lower())
            table[keyval] = (low, high)
    ORDINARY[variant] = table

class QaroshiEngine(IBus.Engine):
    __gtype_name__ = "QaroshiIBusEngine"

    def __init__(self, connection, object_path, layout):
        super().__init__(connection=connection, object_path=object_path)
        self.layout = layout
        self.preedit = ""
        self.assist = True

    def _show(self):
        if self.preedit:
            self.update_preedit_text(IBus.Text.new_from_string(self.preedit), len(self.preedit), True)
            table = IBus.LookupTable.new(3, 0, True, True)
            for item in suggestions(self.preedit, 3):
                table.append_candidate(IBus.Text.new_from_string(item))
            self.update_lookup_table(table, table.get_number_of_candidates()>0)
        else:
            self.hide_preedit_text()
            self.hide_lookup_table()

    def _flush(self, suffix=""):
        if self.preedit:
            word = autocorrect(self.preedit) if self.assist else self.preedit
            self.commit_text(IBus.Text.new_from_string(word + suffix))
            self.preedit = ""
            self._show()
        elif suffix:
            self.commit_text(IBus.Text.new_from_string(suffix))

    def do_candidate_clicked(self, index, button, state):
        options = suggestions(self.preedit, 3)
        if index < len(options):
            self.commit_text(IBus.Text.new_from_string(options[index]))
            self.preedit = ""
            self._show()

    def do_reset(self):
        self._flush()

    def do_focus_out(self):
        self._flush()

    def do_process_key_event(self, keyval, keycode, state):
        mods = IBus.ModifierType
        if state & (mods.RELEASE_MASK | mods.CONTROL_MASK | mods.MOD1_MASK | mods.SUPER_MASK):
            return False
        if keyval == IBus.KEY_BackSpace:
            if self.preedit:
                self.preedit = self.preedit[:-1]
                self._show()
                return True
            return False
        if keyval == IBus.KEY_Escape and self.preedit:
            self.preedit = ""
            self._show()
            return True
        if keyval in (IBus.KEY_space, IBus.KEY_Return, IBus.KEY_KP_Enter, IBus.KEY_Tab):
            if keyval == IBus.KEY_space:
                self._flush(" ")
                return True
            self._flush()
            return False
        # Non-text navigation, app shortcuts, system key sequences pass through.
        physical = IBus.keyval_to_unicode(keyval)
        if not physical:
            self._flush()
            return False
        char = chr(physical).lower()
        shifted = bool(state & mods.SHIFT_MASK)
        row = ORDINARY[self.layout].get(char)
        if row:
            output = row[1 if shifted else 0]
            if all(c.isalpha() or c in "ë-" for c in output):
                self.preedit += output
                self._show()
            else:
                self._flush(output)
            return True
        if char in ".,!?;:'\"-/":
            self._flush(char)
            return True
        self._flush()
        return False

class QaroshiFactory(IBus.Factory):
    def __init__(self, bus):
        super().__init__(connection=bus.get_connection())
        self.bus = bus
        self.count = 0

    def do_create_engine(self, engine_name):
        self.count += 1
        kind = engine_name.rsplit("-", 1)[-1]
        if kind not in ORDINARY:
            raise ValueError("Unknown Qaroshi layout: " + kind)
        return QaroshiEngine(self.bus.get_connection(), f"/org/freedesktop/IBus/engine/Qaroshi{self.count}", kind)

def main():
    IBus.init()
    bus = IBus.Bus()
    bus.connect("disconnected", lambda *args: loop.quit())
    factory = QaroshiFactory(bus)
    bus.request_name("org.freedesktop.IBus.Qaroshi", 0)
    global loop
    loop = GLib.MainLoop()
    loop.run()

if __name__ == "__main__":
    main()
