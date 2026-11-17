import json
import pathlib
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT=pathlib.Path(__file__).resolve().parents[1]
SPEC=json.loads((ROOT/"mapping.json").read_text(encoding="utf-8"))
MAC={
    "1":18,"2":19,"3":20,"4":21,"5":23,"6":22,"7":26,"8":28,"9":25,"0":29,
    "HYPHEN":27,"EQUAL":24,"LBRKT":33,"RBRKT":30,"BKSLASH":42,"QUOTE":39,"BKQUOTE":50
}
WIN={
    "1":"02","2":"03","3":"04","4":"05","5":"06","6":"07","7":"08","8":"09",
    "9":"0a","0":"0b","HYPHEN":"0c","EQUAL":"0d","LBRKT":"1a",
    "RBRKT":"1b","QUOTE":"28","BKSLASH":"2b","BKQUOTE":"29"
}
class PunctuationParity(unittest.TestCase):
    def test_windows_macos_and_keyman_special_keys_match(self):
        subprocess.run([sys.executable,str(ROOT/"scripts/build-windows-native.py")],check=True)
        subprocess.run([sys.executable,str(ROOT/"scripts/build-macos-native.py")],check=True)
        for layout,mapping in SPEC["extraKeys"].items():
            with self.subTest(layout=layout):
                mac=ET.parse(ROOT/"desktop/native/macos"/f"Qaroshi-{layout.capitalize()}.keylayout").getroot()
                layers=[{int(k.get("code")):k.get("output") for k in layer.findall("key")}
                        for layer in mac.findall("./keyMapSet/keyMap")]
                klc=(ROOT/"desktop/native/windows"/f"Qaroshi-{layout}.klc").read_text(encoding="utf-16")
                scan={}
                for line in klc.splitlines():
                    parts=line.split()
                    if len(parts)>=6 and parts[0].lower() in set(WIN.values()):
                        scan[parts[0].lower()]=(parts[3],parts[4])
                keyman=(ROOT/"layouts"/layout/"source"/f"qaroshi_{layout}.kmn").read_text()
                for key,(low,high) in mapping.items():
                    self.assertEqual(layers[0][MAC[key]],low)
                    self.assertEqual(layers[1][MAC[key]],high)
                    for value,winhex in zip((low,high),scan[WIN[key]]):
                        self.assertEqual(winhex.upper(),f"{ord(value):04X}")
                    # Keyman already has a matching explicit rule for each extra key.
                    self.assertIn(f"+ [K_{key}]",keyman)
                    self.assertIn(f"+ [SHIFT K_{key}]",keyman)
if __name__=="__main__":unittest.main()
