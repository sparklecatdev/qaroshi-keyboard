# Mobile Qaroshi keyboards

**Android, iPhone and iPad:** use the **Mobile keyboards** build. Its packages contain Keyman's touch keyboard `.js` (including the touch layout), not the desktop `.kmx`.

## Download

Open [Mobile keyboards Actions](https://github.com/sparklecatdev/qaroshi-keyboard/actions/workflows/mobile.yml), select the newest successful **main** run, and download `qaroshi-mobile-keyboards`. Unzip and select `qaroshi_qwerty_mobile.kmp`, `qaroshi_azerty_mobile.kmp`, or `qaroshi_dvorak_mobile.kmp`.

## Android

Install [Keyman for Android](https://keyman.com/android/). Save the `.kmp` to Downloads, import it from Keyman's keyboard installer, enable Keyman as your Android input method, and select your Qaroshi layout from its menu. Password fields may force the system keyboard.

## iPhone / iPad

Install [Keyman for iPhone and iPad](https://keyman.com/iphone-and-ipad/). Save the `.kmp` to Files, open Keyman and choose **Install From File**, and import the package. Go to **Settings → General → Keyboard → Keyboards → Add New Keyboard**, select Keyman, then switch with the globe key. Exact in-app wording may vary between Keyman versions. iOS uses the system keyboard in restricted text fields.

## Limits

These packages **do not add a layout to Apple's built-in keyboard or Gboard**. Those apps do not support arbitrary Qaroshi layout imports. A dedicated native Android IME or iOS keyboard extension would be a separate app. Keyman provides a real system-wide third-party keyboard today without publishing separate mobile apps.

## Build locally

```bash
npm install -g @keymanapp/kmc@18
bash scripts/build-mobile.sh
```

Packages are under `layouts/*/build/*_mobile.kmp`. CI checks that mobile files have `.js`, **not** `.kmx`.
