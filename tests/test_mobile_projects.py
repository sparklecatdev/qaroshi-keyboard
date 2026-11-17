import json
import pathlib
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class MobileProjects(unittest.TestCase):
    def test_both_apps_use_shared_offline_source(self):
        assert (ROOT/"data/qaroshi-lexicon.json").exists()
        data=json.loads((ROOT/"data/qaroshi-lexicon.json").read_text())
        self.assertGreater(len(data["words"]),4000)
        self.assertEqual(len(data["words"]),len({w[0] for w in data["words"]}))
        for w,_ in data["words"]:
            self.assertEqual(w,w.lower())
        android=(ROOT/"android/app/src/main/AndroidManifest.xml").read_text()
        self.assertIn("android.permission.BIND_INPUT_METHOD",android)
        self.assertNotIn("android.permission.INTERNET",android)
        ios=(ROOT/"ios/project.yml").read_text()
        self.assertIn("RequestsOpenAccess: false",ios)
        self.assertIn("com.apple.keyboard-service",ios)
        self.assertIn("type: app-extension",ios)
    def test_platform_specific_bundling(self):
        source=(ROOT/"scripts/prepare-mobile-native.py").read_text()
        self.assertIn("android/app/src/main/assets",source)
        self.assertIn("ios/Keyboard/Resources",source)
        self.assertTrue((ROOT/".github/workflows/android-native.yml").exists())
        self.assertTrue((ROOT/".github/workflows/ios-native.yml").exists())
if __name__=="__main__":unittest.main()
