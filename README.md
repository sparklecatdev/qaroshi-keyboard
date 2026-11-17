# Qaroshi Keyboard

Native Qaroshi input projects for Windows, macOS, Linux, Android and iOS, with QWERTY, AZERTY and Dvorak layouts. All output is **Unicode Qaroshi Romanization**, not experimental native-script PUA text.

## Native installs and packages

**[Full native installation guide](docs/NATIVE_INSTALL.md)** describes support levels, prerequisites and privacy.

| OS | Native method | Build/download | Status |
|---|---|---|---|
| Windows | MSKLC layout with one-key digraph ligatures | [Windows layout sources](https://github.com/sparklecatdev/qaroshi-keyboard/actions/workflows/native-desktop.yml) | Sources tested; native DLL/setup needs MSKLC compilation and device verification |
| macOS | Apple .keylayout input sources | [Native desktop artifact](https://github.com/sparklecatdev/qaroshi-keyboard/actions/workflows/native-desktop.yml) | XML generated and checked; physical hardware validation pending |
| Linux/Arch | IBus native input engine | [Linux IBus bundle](https://github.com/sparklecatdev/qaroshi-keyboard/actions/workflows/native-desktop.yml) | Per-user installer, suggestions, syntax checked; GUI/device verification pending |
| Android | Native InputMethodService | [Debug APK](https://github.com/sparklecatdev/qaroshi-keyboard/actions/workflows/android-native.yml) | APK must pass CI; enable through Android Settings |
| iOS/iPadOS | UIKit custom keyboard extension | [Xcode source / simulator build](https://github.com/sparklecatdev/qaroshi-keyboard/actions/workflows/ios-native.yml) | Xcode build needs Apple signing to install on physical iPhone |

Source-ready is not device-proven: the Windows KLC file isn't a DLL, and an unsigned iOS Simulator app cannot be installed on a normal iPhone. The compiled Keyman packages remain available as fallbacks.

## Offline suggestions and autocorrect

The native Android and iOS keyboards and Linux IBus engine use a bundled **4,395-headword canonical Qaroshi lexicon**, with source revisions in [data/qaroshi-lexicon.json](data/qaroshi-lexicon.json). Includes prefix suggestions, conservative one-edit typo correction, and basic typing helpers. Known words, hyphenated compounds, short words and proper-capitalized names are protected. Android/iOS offer correction undo, number/symbol keys, shift, caps lock, and layout choice. No user text is uploaded.

**Not yet feature-parity with Gboard or Apple Keyboard:** swipe typing, personalized learning, a full emoji keyboard, dictation, context-aware neural prediction and OS-wide desktop autocorrect are not implemented. Current lexicon is a curated subset, not the entire Qaroshi dictionary.

## Keyman fallback packages

| Platform | Build | Guide |
|---|---|---|
| Windows, macOS, Linux | [Keyman desktop](https://github.com/sparklecatdev/qaroshi-keyboard/actions/workflows/desktop.yml) | [Desktop](docs/DESKTOP.md) |
| Android, iOS | [Keyman mobile](https://github.com/sparklecatdev/qaroshi-keyboard/actions/workflows/mobile.yml) | [Mobile](docs/MOBILE.md) |

### Layout rules

Each layout preserves its 21 other Latin letter positions. The unused Latin letter slots map **C → ë**, **F → kh**, **J → zh**, **V → sh**, **X → ng** in the corresponding QWERTY, AZERTY, or Dvorak positions. Shift yields **Ë, Kh, Zh, Sh, Ng**. Four Romanized digraphs each correspond to one native Qaroshi grapheme.

## Build locally

    python3 -m unittest discover -s tests -v
    python3 scripts/build-windows-native.py
    python3 scripts/build-macos-native.py
    python3 scripts/package-native-desktop.py
    python3 scripts/prepare-mobile-native.py

    # Optional Keyman builds with kmc installed:
    bash scripts/build-desktop.sh
    bash scripts/build-mobile.sh

    # Android SDK + Gradle 8.13:
    gradle -p android :app:assembleDebug

    # macOS, Xcode and XcodeGen:
    (cd ios && xcodegen generate)
    xcodebuild -project ios/QaroshiKeyboard.xcodeproj -scheme QaroshiKeyboard -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' CODE_SIGNING_ALLOWED=NO build

Separate CI workflows validate native desktop mappings, Android, iOS and existing Keyman desktop/mobile packages. Compilation on GitHub doesn't prove end-user device compatibility.

See [Qaroshi language](https://github.com/sparklecatdev/qaroshi). MIT licensed.
