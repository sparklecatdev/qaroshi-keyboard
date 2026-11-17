import pathlib
import unittest
import xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1]
class IBusNative(unittest.TestCase):
    def test_component_declares_three_engines(self):
        tree=ET.parse(ROOT/"desktop/native/linux/ibus/qaroshi.xml")
        engines=tree.findall(".//engine")
        self.assertEqual({x.findtext("name") for x in engines},{"qaroshi-qwerty","qaroshi-azerty","qaroshi-dvorak"})
        self.assertTrue(all(x.findtext("layout")=="us" for x in engines))
    def test_engine_does_not_require_keyman_or_network(self):
        text=(ROOT/"desktop/native/linux/ibus/engine.py").read_text()
        self.assertIn("IBus.Engine",text)
        self.assertIn("autocorrect",text)
        self.assertNotIn("requests.",text)
        self.assertNotIn("subprocess.",text)
if __name__=="__main__":unittest.main()
