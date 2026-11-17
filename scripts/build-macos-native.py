#!/usr/bin/env python3
"""Produce native macOS .keylayout files from canonical Qaroshi key mapping.

Outputs portable Romanization; the Mac Keyboard Layouts framework can emit
two Unicode characters from one key, unlike plain Linux XKB symbol maps.
"""
import json
import pathlib
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / "mapping.json").read_text(encoding="utf-8"))
OUT = ROOT / "desktop" / "native" / "macos"
OUT.mkdir(parents=True, exist_ok=True)

# macOS ANSI virtual key codes for the matching US physical positions.
CODES = {
    "Q": 12, "W": 13, "E": 14, "R": 15, "T": 17, "Y": 16,
    "U": 32, "I": 34, "O": 31, "P": 35,
    "A": 0, "S": 1, "D": 2, "F": 3, "G": 5, "H": 4,
    "J": 38, "K": 40, "L": 37, "COLON": 41,
    "Z": 6, "X": 7, "C": 8, "V": 9, "B": 11,
    "N": 45, "M": 46, "COMMA": 43, "PERIOD": 47, "SLASH": 44,
}
# Standard US ANSI printing keys, including punctuation/number-row fallback.
EXTRA = {
    18: ("1", "!"), 19: ("2", "@"), 20: ("3", "#"),
    21: ("4", "$"), 23: ("5", "%"), 22: ("6", "^"),
    26: ("7", "&"), 28: ("8", "*"), 25: ("9", "("),
    29: ("0", ")"), 27: ("-", "_"), 24: ("=", "+"),
    33: ("[", "{"), 30: ("]", "}"), 42: ("\\", "|"),
    39: ("'", '"'), 50: ("`", "~"), 49: (" ", " "),
}
for kind, rows in SPEC["layoutRows"].items():
    output = {}
    for i, row in enumerate(rows):
        for j, letter in enumerate(row):
            key = SPEC["physicalRows"][i][j]
            original = SPEC["specialLetterReplacements"].get(letter, letter)
            shifted = SPEC["shiftPunctuation"].get(kind, {}).get(key)
            if shifted is None:
                shifted = original[0].upper() + original[1:] if original else original
            caps = original[0].upper() + original[1:] if letter.isalpha() else original
            output[CODES[key]] = (original, shifted, caps)
    EXTRA_CODES = {
        18:"1", 19:"2", 20:"3", 21:"4", 23:"5", 22:"6",
        26:"7", 28:"8", 25:"9", 29:"0",
        27:"HYPHEN", 24:"EQUAL", 33:"LBRKT", 30:"RBRKT",
        42:"BKSLASH", 39:"QUOTE", 50:"BKQUOTE", 49:"SPACE"
    }
    for code, (low, high) in EXTRA.items():
        override = SPEC.get("extraKeys",{}).get(kind,{}).get(EXTRA_CODES[code])
        if override is not None:
            low, high = override
        output.setdefault(code, (low, high, low))
    keyboard = ET.Element("keyboard", group="126", id=str(-2301 - list(SPEC["layoutRows"]).index(kind)), name=f"Qaroshi {kind.upper()}", maxout="2")
    layouts = ET.SubElement(keyboard, "layouts")
    ET.SubElement(layouts, "layout", first="0", last="17", mapSet="ANSI", modifiers="QaroshiMods")
    mods = ET.SubElement(keyboard, "modifierMap", id="QaroshiMods", defaultIndex="0")
    for index, keys in enumerate(("", "anyShift", "caps", "anyShift caps")):
        group = ET.SubElement(mods, "keyMapSelect", mapIndex=str(index))
        ET.SubElement(group, "modifier", keys=keys)
    maps = ET.SubElement(keyboard, "keyMapSet", id="ANSI")
    for index in range(4):
        layer = ET.SubElement(maps, "keyMap", index=str(index))
        for keycode, (low, high, caps) in sorted(output.items()):
            result = (low, high, caps, low)[index]
            ET.SubElement(layer, "key", code=str(keycode), output=result)
    xml = ET.tostring(keyboard, encoding="unicode")
    declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    declaration += '<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">\n'
    target = OUT / f"Qaroshi-{kind.capitalize()}.keylayout"
    target.write_text(declaration + xml + "\n", encoding="utf-8")
    print(f"Generated native macOS keyboard: {target}")
