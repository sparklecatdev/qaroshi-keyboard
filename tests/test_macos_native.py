import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / "mapping.json").read_text(encoding="utf-8"))

class MacNative(unittest.TestCase):
    def test_generated_macos_maps_match_shared_source(self):
        subprocess.run([sys.executable, str(ROOT / "scripts" / "build-macos-native.py")], check=True)
        mac_codes = {"Q":12,"W":13,"E":14,"R":15,"T":17,"Y":16,"U":32,"I":34,"O":31,"P":35,
                     "A":0,"S":1,"D":2,"F":3,"G":5,"H":4,"J":38,"K":40,"L":37,"COLON":41,
                     "Z":6,"X":7,"C":8,"V":9,"B":11,"N":45,"M":46,"COMMA":43,"PERIOD":47,"SLASH":44}
        for kind, rows in SPEC["layoutRows"].items():
            with self.subTest(kind=kind):
                path=ROOT/"desktop"/"native"/"macos"/f"Qaroshi-{kind.capitalize()}.keylayout"
                root=ET.parse(path).getroot()
                self.assertEqual(root.tag,"keyboard")
                self.assertEqual(root.get("maxout"),"2")
                self.assertEqual(len(root.findall("./keyMapSet/keyMap")),4)
                layers=[{int(k.get("code")):k.get("output") for k in m.findall("key")} for m in root.findall("./keyMapSet/keyMap")]
                for i,row in enumerate(rows):
                    for j,letter in enumerate(row):
                        physical=SPEC["physicalRows"][i][j]
                        code=mac_codes[physical]
                        val=SPEC["specialLetterReplacements"].get(letter,letter)
                        shifted=SPEC["shiftPunctuation"].get(kind,{}).get(physical,val[:1].upper()+val[1:])
                        self.assertEqual(layers[0][code],val)
                        self.assertEqual(layers[1][code],shifted)
                        self.assertNotEqual(layers[0][code],"\ue000")
                self.assertEqual(layers[0][49]," ")
                self.assertEqual(layers[0][18],"1")

if __name__=="__main__":
    unittest.main()
