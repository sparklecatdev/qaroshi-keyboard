import json
import pathlib
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / "mapping.json").read_text(encoding="utf-8"))
KEYS = SPEC["physicalRows"]
SPECIAL = SPEC["specialLetterReplacements"]
VALID = set("abcdefghijklmnopqrstuvwxyz")
RULE = re.compile(r"^\+ \[(SHIFT )?K_([A-Z0-9]+)\] > (?:'((?:[^']|'')*)'|(U\+[0-9A-F]{4,6}))$", re.M)

class QaroshiLayouts(unittest.TestCase):
    def test_26_letters_and_desktop_touch_parity(self):
        for layout, rows in SPEC["layoutRows"].items():
            with self.subTest(layout=layout):
                self.assertEqual([len(row) for row in rows], [10, 10, 10])
                pairs = [(KEYS[i][j], rows[i][j]) for i in range(3) for j in range(10)]
                letters = [letter for _, letter in pairs if letter in VALID]
                self.assertEqual(set(letters), VALID)
                self.assertEqual(len(letters), 26)
                name = f"qaroshi_{layout}"
                folder = ROOT / "layouts" / layout / "source"
                kmn = (folder / f"{name}.kmn").read_text(encoding="utf-8")
                rules = {(bool(m.group(1)), m.group(2)): (m.group(3).replace("''", "'") if m.group(3) is not None else chr(int(m.group(4)[2:], 16))) for m in RULE.finditer(kmn)}
                self.assertEqual(len(rules), len(set(rules)))
                touch = json.loads((folder / f"{name}.keyman-touch-layout").read_text(encoding="utf-8"))
                for device in ("phone", "tablet"):
                    layers = {layer["id"]:layer["row"] for layer in touch[device]["layer"]}
                    self.assertEqual(set(layers), {"default", "shift", "numeric"})
                    for shifted, lname in ((False, "default"), (True, "shift")):
                        for rowindex in range(3):
                            bykey = {k["id"]:k for k in layers[lname][rowindex]["key"]}
                            for physical, ordinary in pairs:
                                if physical not in KEYS[rowindex]:
                                    continue
                                out = SPECIAL.get(ordinary,ordinary)
                                out = ((SPEC["shiftPunctuation"].get(layout, {}).get(physical) or (out[:1].upper() + out[1:])) if shifted else out)
                                self.assertEqual(rules[(shifted, physical)], out)
                                self.assertEqual(bykey["K_"+physical]["text"], out)
                    for switch in ("K_NUMERALS", "K_SPACE", "K_ENTER"):
                        self.assertIn(switch, {key["id"] for row in layers["default"] for key in row["key"]})
                self.assertEqual({SPECIAL[k] for k in SPECIAL}, {"ë", "sh", "zh", "kh", "ng"})

    def test_package_contents_and_language(self):
        for layout in SPEC["layoutRows"]:
            folder = ROOT / "layouts" / layout / "source"
            for platform, wanted in (("desktop", ".kmx"), ("mobile", ".js")):
                kps = ET.parse(folder / f"qaroshi_{layout}_{platform}.kps")
                ns = {file.findtext("FileType") for file in kps.findall(".//Files/File")}
                self.assertIn(wanted, ns)
                self.assertNotIn(".js" if platform == "desktop" else ".kmx", ns)
                self.assertEqual(kps.find(".//Keyboard/Languages/Language").attrib["ID"], "und-Latn-x-qaroshi")

    def test_no_native_pua_output(self):
        for path in ROOT.glob("layouts/*/source/*.kmn"):
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, r"U\+[eE][0-9a-fA-F]{3}")

if __name__ == "__main__":
    unittest.main()
