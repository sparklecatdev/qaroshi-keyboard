# Qaroshi Keyboard

**Three real, installable Keyman keyboard layouts for Qaroshi Romanization: QWERTY, AZERTY and Dvorak.**

All three layouts type the same 26 Qaroshi letters, including **ë, sh, zh, kh, ng**. The latter four are *one native Qaroshi letter each*, even though their portable Romanization uses two Latin characters.

> **Status:** Source implementation and automated structural tests are provided. GitHub Actions builds the downloadable `.kmp` packages; see the [Actions page](https://github.com/sparklecatdev/qaroshi-keyboard/actions/workflows/build.yml) for the real compiler result. Until a green compile and device test are recorded, do not assume that every platform has been verified on hardware. This produces **Romanized text**, not the experimental Private-Use-Area native script.

## Get a keyboard

1. Open [Build and test](https://github.com/sparklecatdev/qaroshi-keyboard/actions/workflows/build.yml), choose the latest **successful** run on `main`, and download its `qaroshi-keyman-packages` artifact. Unzip it.
2. Choose **one** file: `qaroshi_qwerty.kmp`, `qaroshi_azerty.kmp` or `qaroshi_dvorak.kmp`.
3. Install **Keyman** on your device (free and open-source): https://keyman.com/downloads/
4. Follow the device-specific steps below.

**Note:** GitHub Actions artifacts can require signing in to GitHub. Published [Releases](https://github.com/sparklecatdev/qaroshi-keyboard/releases) are the preferred permanent link when available. The release workflow uploads those same packages only on a version tag such as `v1.0.0`; no release is implied until it is actually published.

## Installation by device

### Windows 10 / 11
1. Install [Keyman for Windows](https://keyman.com/windows/).
2. Download and open the desired `.kmp` file; Keyman should offer to install it. Alternatively open Keyman Configuration, choose **Install Keyboard** and select the file.
3. Select the installed **Qaroshi QWERTY / AZERTY / Dvorak** keyboard in Keyman, then type in any normal Unicode text field.
4. If keys appear out of position, use **English (United States) / US QWERTY** as the underlying Windows hardware layout while the Qaroshi positional keyboard is active. This avoids double-mapping AZERTY or Dvorak.

### macOS
1. Install [Keyman for macOS](https://keyman.com/mac/).
2. Import the selected `.kmp` in Keyman Configuration.
3. Enable/select the keyboard from the macOS input menu; keep the underlying base layout at US English when using these positional mappings.
4. Test in TextEdit first. If the keyboard does not appear, quit and reopen the app or sign out and back in.

### Arch Linux / KDE Plasma / Wayland
1. Read Keyman's maintained [Arch + KDE/Wayland guide](https://help.keyman.com/knowledge-base/kb0102).
2. Install the required IBus/Keyman packages. With a configured AUR helper, the documented package is `keyman` from the AUR; verify the current AUR build instructions before installing.
3. Set up IBus as described in Keyman's [KDE guide](https://help.keyman.com/knowledge-base/kb0106), then log out and log back in if needed.
4. Open Keyman Configuration and install the `.kmp` file. Select the Qaroshi keyboard through the input method menu.
5. Test in a regular GTK or Qt text field. Some KDE/Wayland apps bypass IBus; if it fails in one app but works in another, check its input-method integration.

On other Linux distributions, follow https://keyman.com/linux/. Do **not** overwrite global XKB rules or run arbitrary keyboard remapping commands as root just to use Qaroshi.

### Android
1. Install [Keyman for Android](https://keyman.com/android/).
2. Download the selected `.kmp` to the device.
3. In Keyman, use its install-from-file/import option to open the package.
4. Enable Keyman as an Android input method, choose it from the keyboard selector, and select the installed Qaroshi layout.
5. Use **Shift** for uppercase; **123** for digits and symbols; the globe/menu key to change keyboards.

### iPhone / iPad
1. Install [Keyman for iPhone and iPad](https://keyman.com/iphone-and-ipad/).
2. Save the selected `.kmp` to the **Files** app.
3. In Keyman, choose **Settings → Install From File** (wording can vary by version), locate the `.kmp`, and import it.
4. In iOS **Settings → General → Keyboard → Keyboards → Add New Keyboard**, enable **Keyman**.
5. In a text field, switch to Keyman with the globe key and choose Qaroshi QWERTY, AZERTY or Dvorak.

Third-party keyboard restrictions apply in certain secure/password fields on iOS and Android. You can always switch back to your system keyboard.

## How to type

| Native Qaroshi letter | Romanized output | QWERTY key | AZERTY-labeled key | Dvorak-labeled key |
|---|---|---|---|---|
| schwa | `ë` | C | C | C |
| velar fricative | `kh` | F | F | F |
| voiced postalveolar | `zh` | J | J | J |
| voiceless postalveolar | `sh` | V | V | V |
| velar nasal | `ng` | X | X | X |

Here **labeled key** means the key that would normally type that letter in the named layout, not the printed legend on a US QWERTY keyboard. For example, Dvorak's C is at US physical `I`, whereas AZERTY's A is at US physical `Q`. The other 21 Latin letters remain on their usual QWERTY, AZERTY or Dvorak letter positions.

**Examples:** `më`, `qaroshi`, `Zha hëtiri, pingikha!`, `sh`, `zh`, `kh`, `ng`. Shift makes `Ë`, `Sh`, `Zh`, `Kh`, `Ng`; an ordinary Backspace removes one Latin codepoint at a time, including inside a digraph.

**Punctuation:** QWERTY uses ordinary US punctuation. AZERTY implements conventional French number-row punctuation and common bottom-row punctuation; Dvorak implements its usual number-adjacent, bracket, comma, period, quote, slash and semicolon positions. The mobile keyboard includes a 123/symbol layer.

### Supported layouts

| Layout | Description |
|---|---|
| QWERTY | Familiar US letter locations; C/F/J/V/X become ë/kh/zh/sh/ng |
| AZERTY | French AZERTY letter locations and major punctuation; same five substitutions |
| Dvorak | US Dvorak letter locations and major punctuation; same five substitutions |

All three keyboards are **positional** Keyman layouts, so they use the same physical-key map regardless of the user's underlying system layout. For best desktop results, enable **US QWERTY as the base input layout**, then choose the appropriate Qaroshi variant inside Keyman. Do not layer Qaroshi-Dvorak on top of an already-active OS Dvorak layout: that applies two rearrangements.

## Build from source

Requirements: Python 3.10+ (standard library only), Node.js 20+, and Keyman Developer command-line compiler `kmc` (18.x recommended).

```bash
git clone https://github.com/sparklecatdev/qaroshi-keyboard.git
cd qaroshi-keyboard
python3 -m unittest discover -s tests -v
npm install -g @keymanapp/kmc@18
bash scripts/build.sh
```

Generated packages: `layouts/qwerty/build/qaroshi_qwerty.kmp`, `layouts/azerty/build/qaroshi_azerty.kmp`, `layouts/dvorak/build/qaroshi_dvorak.kmp`. `kmc` also compiles desktop `.kmx` and web/mobile `.js` source. **Do not** distribute only `.kmx` as an iOS/Android keyboard; use `.kmp`.

The source of truth is `layouts/<layout>/source/qaroshi_<layout>.kmn` together with its paired `.keyman-touch-layout`. The tests compare desktop mappings and touch layout expectations for all 26 letters, the five special outputs, uppercase, and the language tag. CI compiles actual packages and publishes artifacts on green runs. Local structural tests are not substitutes for testing text entry on each target OS.

## Design constraints and remaining validation

* Native Nardoragon glyphs currently have an **experimental PUA font/character mapping**, not a stable Unicode encoding. Shipping PUA text without a universally available font would make chat messages unreadable. This release intentionally uses portable Romanization only.
* The 26-letter alphabet is Qaroshi's own inventory, **not** an A–Z substitution cipher. The letters C, F, J, V and X are available when the regular English keyboard is selected.
* This repo is separate from the [Qaroshi language/reference repository](https://github.com/sparklecatdev/qaroshi). Word spelling and digraph meanings come from its published orthography. Layout ergonomic placements are project choices, not language grammar amendments.
* Keyman mobile app, IBus, and macOS input permission flows vary by OS version. Treat CI success as **compiler success**, not a guarantee that every app accepts third-party input.
* Planned QA: verified Windows/macOS/Arch Wayland/iOS/Android install reports, screenshots, accessibility and physical Dvorak hardware testing, plus eventual font-safe native-script mode.

## Development

Edit the `layouts/*/source/` files. Run `python3 -m unittest discover -s tests -v` and `bash scripts/build.sh`. If you change a special character key, update both desktop `.kmn` and mobile `.keyman-touch-layout` and add a regression test.

Build reference: [Keyman Developer compiler](https://help.keyman.com/developer/current-version/reference/kmc/cli/get-started), [Keyman package format](https://help.keyman.com/developer/current-version/guides/distribute/packages), [Keyman touch schema](https://help.keyman.com/developer/current-version/reference/file-types/keyman-touch-layout).

## License

MIT, see [LICENSE](LICENSE).