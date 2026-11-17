# Qaroshi Keyboard

Type **Qaroshi Romanization** on Windows, macOS, Linux, Android, iPhone and iPad. Supports **QWERTY, AZERTY, and Dvorak**.

**Choose your device first.** Desktop and mobile now have **separate builds, packages, CI checks, and installation guides**, while sharing the same canonical Qaroshi letter mapping.

| Device | Download | Installation guide | Engine |
|---|---|---|---|
| Windows, macOS, Linux | [Desktop build](https://github.com/sparklecatdev/qaroshi-keyboard/actions/workflows/desktop.yml) → `qaroshi-desktop-keyboards` | [Desktop instructions](docs/DESKTOP.md) | Keyman desktop |
| Android, iPhone, iPad | [Mobile build](https://github.com/sparklecatdev/qaroshi-keyboard/actions/workflows/mobile.yml) → `qaroshi-mobile-keyboards` | [Mobile instructions](docs/MOBILE.md) | Keyman mobile |

Open the latest successful `main` workflow run, download and unzip the named artifact, then select a QWERTY, AZERTY, or Dvorak `.kmp`. Install [Keyman](https://keyman.com/downloads/) and import that package.

## Why separate?

Desktop Keyman installs a **`.kmx`** keyboard, while phone and tablet Keyman installs a **`.js`** touch keyboard. The packages are now independently built and validated. The user does not have to download both targets inside one package. [Keyman package documentation](https://help.keyman.com/developer/current-version/guides/distribute/packages).

## Typing behavior

* Qaroshi uses 26 native letters. This release produces portable Unicode Latin Romanization, not the experimental native-glyph PUA encoding.
* Each layout preserves 21 other Latin letters. The five unused Latin letter positions become **C → ë**, **F → kh**, **J → zh**, **V → sh**, **X → ng**, positioned according to the *selected* QWERTY/AZERTY/Dvorak mapping.
* Shift produces **Ë**, **Kh**, **Zh**, **Sh**, **Ng**.
* The four digraphs each represent one native Qaroshi grapheme but output two Latin Unicode characters.
* On desktop these are **positional** Keyman layouts. Set the base OS layout to **US QWERTY**, then choose the desired Qaroshi QWERTY/AZERTY/Dvorak variant inside Keyman to avoid double remapping.

## Native macOS option

The **desktop build** additionally exports `Qaroshi-Qwerty.keylayout`, `Qaroshi-Azerty.keylayout` and `Qaroshi-Dvorak.keylayout` for direct macOS input-source installation **without Keyman**. See [macOS steps](docs/DESKTOP.md#macos-native-no-keyman-required). These are structurally tested but haven't yet been verified on physical Mac hardware. Windows and Linux retain the Keyman desktop packages for full digraph behavior.

## Build and test

```bash
git clone https://github.com/sparklecatdev/qaroshi-keyboard.git
cd qaroshi-keyboard
npm install -g @keymanapp/kmc@18
python3 -m unittest discover -s tests -v
bash scripts/build-desktop.sh
bash scripts/build-mobile.sh
```

Build outputs are at `layouts/*/build/*_desktop.kmp` and `layouts/*/build/*_mobile.kmp`. Each script builds **only its own platform packages** and checks the ZIP contents. GitHub Actions runs them in separate workflows.

## Current scope

The builds compile the Keyman keyboard source and verify expected package contents. **They are not native Windows DLL or Linux XKB layouts**, and mobile packages do not modify Apple's built-in keyboard or Gboard. Producing native OS layouts and dedicated mobile keyboard apps requires separate platform-specific implementations and testing. CI compilation is not a substitute for real on-device text-entry tests.

## Repository organization

```text
mapping.json                        Canonical QWERTY/AZERTY/Dvorak mapping
layouts/{qwerty,azerty,dvorak}/     Shared KMN and touch source
  source/*_desktop.kps              Desktop .kmx package manifests
  source/*_mobile.kps               Mobile .js package manifests
scripts/build-desktop.sh            Desktop-only package builder
scripts/build-mobile.sh             Mobile-only package builder
.github/workflows/desktop.yml       Desktop CI + download artifact
.github/workflows/mobile.yml        Mobile CI + download artifact
docs/DESKTOP.md                     Windows/macOS/Linux installation
docs/MOBILE.md                      Android/iOS installation
tests/                              Letter/output parity and package checks
```

See the [Qaroshi language reference](https://github.com/sparklecatdev/qaroshi). Licensed under [MIT](LICENSE).
