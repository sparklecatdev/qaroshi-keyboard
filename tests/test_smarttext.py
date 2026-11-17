import json
import pathlib
import sys
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"smarttext"))
import qaroshi

class Suggestions(unittest.TestCase):
    def test_canonical_lexicon(self):
        words=qaroshi.load()
        self.assertGreater(len(words),4000)
        for word in ("më","zha","hëtiri","pingikha","rakuzhi","qaroshi"):
            if word == "qaroshi": continue
            self.assertIn(word, words)
        self.assertEqual(qaroshi.autocorrect("hëtiri"),"hëtiri")
        self.assertEqual(qaroshi.autocorrect("rakuzhi"),"rakuzhi")
    def test_conservative_correction(self):
        self.assertEqual(qaroshi.autocorrect("shiri"),"shiri")
        self.assertEqual(qaroshi.autocorrect("Shiri"),"Shiri")
        self.assertEqual(qaroshi.autocorrect("mi"),"mi")
        self.assertEqual(qaroshi.autocorrect("mi-na"),"mi-na")
        self.assertEqual(qaroshi.autocorrect("mailto@example.com"),"mailto@example.com")
        self.assertTrue(qaroshi.distance_one("shiri","shiri"))
        self.assertTrue(qaroshi.distance_one("shiri","sihri"))
        self.assertTrue(qaroshi.distance_one("shiri","shri"))
        self.assertFalse(qaroshi.distance_one("shiri","qxiro"))
        self.assertTrue(qaroshi.suggestions("shi"))
    def test_no_english_prediction_and_unicode(self):
        self.assertEqual(qaroshi.autocorrect("hello"),"hello")
        self.assertEqual(qaroshi.suggestions("SHI"),qaroshi.suggestions("shi"))
        self.assertEqual(qaroshi.autocorrect("më"),"më")

if __name__=="__main__":unittest.main()
