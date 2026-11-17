# Desktop Qaroshi keyboards

**Windows, macOS, and Linux (including Arch/KDE):** use the **Desktop keyboards** build. Its packages contain a compiled Keyman desktop `.kmx`, not an Android/iOS touch keyboard.

## Download

Open [Desktop keyboards Actions](https://github.com/sparklecatdev/qaroshi-keyboard/actions/workflows/desktop.yml), select the newest successful **main** run, and download `qaroshi-desktop-keyboards`. Unzip the artifact and select `qaroshi_qwerty_desktop.kmp`, `qaroshi_azerty_desktop.kmp`, or `qaroshi_dvorak_desktop.kmp`.

## Windows

Install [Keyman for Windows](https://keyman.com/windows/). Double-click the selected `.kmp` or import it from Keyman Configuration, then select it from your input method menu.

## macOS: native, no Keyman required

The **desktop artifact also includes three `.keylayout` files**, generated from the same QWERTY/AZERTY/Dvorak map as Keyman. Mac native layouts emit `ë`, `sh`, `zh`, `kh`, and `ng` on their corresponding keys, without an input-method app.

1. Unzip `qaroshi-desktop-keyboards`, find `Qaroshi-Qwerty.keylayout`, `Qaroshi-Azerty.keylayout` or `Qaroshi-Dvorak.keylayout`.
2. In Finder, choose **Go → Go to Folder** and enter `~/Library/Keyboard Layouts/`. Create that folder if missing, then copy in your chosen file.
3. Sign out and sign back in (or restart). In **System Settings → Keyboard → Text Input → Edit → +**, look under **Others** for your Qaroshi layout.
4. Switch to Qaroshi from the macOS input menu and test in TextEdit.

These XML layouts are generated and checked for mapping completeness in CI, but have **not yet been physically tested on macOS**. Option and non-US keyboard combinations may need further device validation. If you prefer Keyman, use the `_desktop.kmp` alternative and [Keyman for macOS](https://keyman.com/mac/).

## Arch Linux and KDE Wayland

Follow [Keyman's Arch installation guide](https://help.keyman.com/knowledge-base/kb0102) and [Linux guide](https://keyman.com/linux/). Install IBus/Keyman, import your `.kmp` through Keyman Configuration, and enable Keyman as the input method in KDE. You may need to log out and back in. Some Wayland apps may not support IBus properly.

## Critical layout rule

These are **physical-position** mappings. Keep the underlying operating-system keyboard set to **US QWERTY**, then choose the matching **Qaroshi QWERTY, AZERTY, or Dvorak** package *inside Keyman*. If you turn on the OS Dvorak keyboard and the Qaroshi Dvorak package together, you may double-map the keys.

## Native OS keyboards

The `.kmp` downloads remain **Keyman keyboards** (Windows, macOS and Linux). **macOS also has an experimental native `.keylayout` option** in the same desktop artifact. Native Windows drivers and full-fidelity Linux XKB layouts are not provided yet: Linux XKB ordinarily outputs one keysym per keypress and does not independently provide one-press multi-character Qaroshi digraphs.

## Build locally

```bash
npm install -g @keymanapp/kmc@18
bash scripts/build-desktop.sh
```

Packages are placed under `layouts/*/build/*_desktop.kmp`. CI validates that a desktop package has `.kmx`, **not** mobile `.js`.
