# Desktop Qaroshi keyboards

**Windows, macOS, and Linux (including Arch/KDE):** use the **Desktop keyboards** build. Its packages contain a compiled Keyman desktop `.kmx`, not an Android/iOS touch keyboard.

## Download

Open [Desktop keyboards Actions](https://github.com/sparklecatdev/qaroshi-keyboard/actions/workflows/desktop.yml), select the newest successful **main** run, and download `qaroshi-desktop-keyboards`. Unzip the artifact and select `qaroshi_qwerty_desktop.kmp`, `qaroshi_azerty_desktop.kmp`, or `qaroshi_dvorak_desktop.kmp`.

## Windows

Install [Keyman for Windows](https://keyman.com/windows/). Double-click the selected `.kmp` or import it from Keyman Configuration, then select it from your input method menu.

## macOS

Install [Keyman for macOS](https://keyman.com/mac/). Import your `.kmp` from Keyman Configuration, then enable it in the macOS input menu.

## Arch Linux and KDE Wayland

Follow [Keyman's Arch installation guide](https://help.keyman.com/knowledge-base/kb0102) and [Linux guide](https://keyman.com/linux/). Install IBus/Keyman, import your `.kmp` through Keyman Configuration, and enable Keyman as the input method in KDE. You may need to log out and back in. Some Wayland apps may not support IBus properly.

## Critical layout rule

These are **physical-position** mappings. Keep the underlying operating-system keyboard set to **US QWERTY**, then choose the matching **Qaroshi QWERTY, AZERTY, or Dvorak** package *inside Keyman*. If you turn on the OS Dvorak keyboard and the Qaroshi Dvorak package together, you may double-map the keys.

## Native OS keyboards

These desktop packages are **Keyman keyboards**, not Windows `.dll`, macOS `.keylayout`, or Linux XKB layouts. They still require Keyman. Independent native OS integration is a distinct workstream and must not be advertised as built until platform-specific installers are created and tested. The Mac and Linux native keyboards have tradeoffs around digraph output, and Windows native layouts require a tested layout compiler.

## Build locally

```bash
npm install -g @keymanapp/kmc@18
bash scripts/build-desktop.sh
```

Packages are placed under `layouts/*/build/*_desktop.kmp`. CI validates that a desktop package has `.kmx`, **not** mobile `.js`.
