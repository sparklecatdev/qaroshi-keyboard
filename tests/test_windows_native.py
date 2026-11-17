import json
import pathlib
import subprocess
import sys
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
class WindowsNative(unittest.TestCase):
    def test_windows_klc_sources_have_all_letters_and_ligatures(self):
        subprocess.run([sys.executable,str(ROOT/"scripts/build-windows-native.py")],check=True)
        spec=json.loads((ROOT/"mapping.json").read_text())
        for layout in spec["layoutRows"]:
            path=ROOT/"desktop/native/windows"/f"Qaroshi-{layout}.klc"
            content=path.read_text(encoding="utf-16")
            self.assertIn("SHIFTSTATE",content)
            self.assertIn("LAYOUT",content)
            self.assertIn("ENDKBD",content)
            self.assertIn("LIGATURE",content)
            self.assertEqual(sum(1 for x in content.splitlines() if x.strip().startswith("%%")),0)
            self.assertGreaterEqual(content.count("%%"),8)
            self.assertGreaterEqual(content.count("00EB"),1)
            for key in ("F","J","V","X"):
                self.assertIn(f"{key}\t0\t",content)
                self.assertIn(f"{key}\t1\t",content)
if __name__=="__main__":unittest.main()
