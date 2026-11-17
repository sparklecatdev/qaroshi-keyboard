import json
import pathlib
import unittest
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / "mapping.json").read_text(encoding="utf-8"))

class SplitPackages(unittest.TestCase):
    def test_each_layout_has_separate_desktop_and_mobile_packages(self):
        for layout in SPEC["layoutRows"]:
            for platform in ("desktop", "mobile"):
                with self.subTest(layout=layout, platform=platform):
                    path = ROOT / "layouts" / layout / "source" / f"qaroshi_{layout}_{platform}.kps"
                    xml = ET.parse(path)
                    names = [node.findtext("Name") for node in xml.findall(".//Files/File")]
                    kinds = [node.findtext("FileType") for node in xml.findall(".//Files/File")]
                    self.assertEqual(kinds.count(".kmx"), 1 if platform == "desktop" else 0)
                    self.assertEqual(kinds.count(".js"), 1 if platform == "mobile" else 0)
                    self.assertEqual(xml.find(".//Keyboard/ID").text, f"qaroshi_{layout}")
                    self.assertEqual(xml.find(".//Keyboard/Languages/Language").get("ID"), "und-Latn-x-qaroshi")
                    expected = f"qaroshi_{layout}." + ("kmx" if platform == "desktop" else "js")
                    self.assertTrue(any(s and s.endswith(expected) for s in names))
    def test_6_platform_packages_and_two_workflows(self):
        for plat in ("desktop", "mobile"):
            self.assertTrue((ROOT / ".github" / "workflows" / f"{plat}.yml").is_file())
            self.assertTrue((ROOT / "scripts" / f"build-{plat}.sh").is_file())
            self.assertTrue((ROOT / "docs" / f"{plat.upper()}.md").is_file())

if __name__ == "__main__":
    unittest.main()
