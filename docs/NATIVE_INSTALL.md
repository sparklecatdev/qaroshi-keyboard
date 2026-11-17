# Install native Qaroshi keyboards

These are **operating-system input sources**, not the existing Keyman packages. All variants preserve the three physical QWERTY, AZERTY and Dvorak mappings and produce standard Unicode Qaroshi Romanization.

## Downloads

[Native desktop workflow](https://github.com/sparklecatdev/qaroshi-keyboard/actions/workflows/native-desktop.yml) → latest successful `main` run → `qaroshi-native-desktop` artifact.

[Native Android APK](https://github.com/sparklecatdev/qaroshi-keyboard/actions/workflows/android-native.yml) → latest successful `main` run → `qaroshi-android-debug-apk`.

[Native iOS build check](https://github.com/sparklecatdev/qaroshi-keyboard/actions/workflows/ios-native.yml). CI publishes an **unsigned iOS Simulator app**, not an iPhone-installable IPA.

## Windows 10 / 11 (native layout DLL)

Source files: `Qaroshi-qwerty.klc`, `Qaroshi-azerty.klc`, `Qaroshi-dvorak.klc`.

1. Install [Microsoft Keyboard Layout Creator 1.4](https://www.microsoft.com/en-us/download/details.aspx?id=102134).
2. Open the desired `.klc` under **File → Load Source File**. The KLC includes multi-character ligature definitions for one-key `sh`, `zh`, `kh` and `ng`.
3. Choose **Project → Build DLL and Setup Package**, then run the generated `setup.exe` and follow the prompts.
4. Enable the new keyboard via Windows language/input settings. Switch via **Win+Space**.

**Important:** This repository builds and validates KLC *sources* only. It does **not** yet ship a tested Windows DLL or installer. MSKLC is legacy tooling and may require compatibility steps on Windows 11. If it refuses to compile a source or install the resulting layout, use the [working Keyman desktop fallback](DESKTOP.md) rather than trusting an unverified binary. Native Windows layouts by themselves do not provide autocorrect; that requires a separate Windows text input service.

## macOS (native input source)

The native desktop artifact includes `Qaroshi-Qwerty.keylayout`, `Qaroshi-Azerty.keylayout`, and `Qaroshi-Dvorak.keylayout`.

1. Copy your chosen file to `~/Library/Keyboard Layouts/`.
2. Sign out and back in, or restart.
3. Add it in **System Settings → Keyboard → Text Input → Edit → +** under **Others** if available.
4. Switch via the input menu and test in TextEdit.

No Keyman needed. macOS native text correction depends on OS dictionary support; native XML layouts alone cannot integrate the custom Qaroshi suggestion engine. These layouts are generated and structurally tested, **not device-attested**.

## Linux, including Arch KDE Wayland (native IBus input engine)

The native desktop artifact contains `qaroshi-linux-ibus.zip`. Unzip and run from the extracted folder:

```bash
# Arch: install the ibus and python-gobject packages through pacman
sudo pacman -S ibus python-gobject
python3 desktop/native/linux/ibus/install.py
ibus restart
```

Use **IBus Preferences** to select `Qaroshi QWERTY`, `Qaroshi AZERTY` or `Qaroshi Dvorak`. Set the underlying physical layout to **US QWERTY**; Qaroshi maps physical keys itself. IBus integrates with Linux desktop text input, including a native candidate panel with offline recommendations. Some Wayland apps or input contexts may not route keystrokes through IBus. See [Keyman's KDE guide](https://help.keyman.com/knowledge-base/kb0101) for IBus session issues even when using this non-Keyman engine.

To remove your per-user installation:

```bash
python3 desktop/native/linux/ibus/install.py --uninstall
ibus restart
```

This installer modifies only your home directory under `~/.local`, never system-wide XKB files.

## Android (native InputMethodService)

1. Download the **debug APK** from a successful Android build and install it (Android may ask you to allow installing from that source).
2. Open **Qaroshi Keyboard**.
3. Select a layout and choose whether to use conservative offline autocorrect.
4. Tap **Enable**, allow the Qaroshi input method, then tap **Switch to Qaroshi**.
5. You can switch from any compatible text input via Android's input-method selector.

The APK is a development artifact, not a signed Play Store production release. You should review a keyboard app before granting it text-input permissions. It has **no INTERNET permission**. Password and no-suggestions fields disable corrections.

## iPhone / iPad (native UIInputViewController keyboard extension)

1. On a Mac with a recent Xcode and XcodeGen installed, clone this repository.
2. Run `python3 scripts/prepare-mobile-native.py`, `cd ios && xcodegen generate`.
3. Open `ios/QaroshiKeyboard.xcodeproj` in Xcode. Choose your **own Apple development team and bundle identifiers** in both the app and keyboard extension targets.
4. Build and run the containing app on your iPhone/iPad using Xcode.
5. Enable **Qaroshi** via **Settings → General → Keyboard → Keyboards → Add New Keyboard**. Use the globe key to switch to it, then its layout key to cycle QWERTY/AZERTY/Dvorak.

**No pre-signed iPhone IPA is distributed.** The GitHub iOS workflow only verifies Xcode compilation and publishes a simulator artifact. For regular install distribution, an Apple-signed app and appropriate publishing method are required. iOS substitutes the system keyboard in secure fields. No Full Access is requested, and corrections run offline.

## Text-assist behavior and limitations

- 4,395 actual Qaroshi reference headwords (provenance recorded in `data/qaroshi-lexicon.json`); **not the full 30,000+ lexicon** and not empirically observed usage.
- Three prefix suggestions, typo corrections limited to one insert/delete/substitution/transposition and high-confidence tie-breaking.
- Already-known words, proper-capitalized words, short words and productive hyphenated compounds stay unchanged.
- Android and iOS expose corrections on space and a one-backspace undo; Linux uses preedit so its edits remain reversible before commit.
- No cloud, telemetry, remote language model, user keystroke collection or contact permissions.
- No swipe-to-type, full contextual neural prediction, multilingual learning, native OS-wide desktop autocorrect, dictation or emoji library yet. Those are separate substantial features and **must not be advertised as implemented**.

Please report installation/device failures with OS version, layout and a reproducible test phrase; avoid attaching private typed text.
