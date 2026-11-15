# Stackchan Gemini

The base Stack-chan: an M5Stack CoreS3 Stack-chan you talk to through
Gemini Live, using everything the robot itself has, with nothing on a PC
behind it. ESP-IDF 5.4 / C++20.

It is the first of three firmwares on the same shared core
([stackchan-core](https://github.com/hartj77-blip/stackchan-core), the
`core/` submodule):

| Tier | Firmware | What it adds |
|---|---|---|
| Base | **Stackchan Gemini** (this) | The robot and Gemini: face, voice, head, light bars, senses, camera / photo booth, SD-card music, NFC cards, themes |
| Mid | Stackchan Roombot | Bedroom apps: clock, alarms, calendar, lights, media, photo booth (a PC hub) |
| Top | Stackchan Server Bot | A home-server coworker: dashboards, ring language, ID cards (a server desk) |

All three use the same partition table and settings, so one robot can switch
between them over Wi-Fi and keep its Wi-Fi, Gemini key and calibration.

## What it does

- **Talk to it.** Gemini Live, with a pat on the head to talk (or always
  listening). It changes its face, moves its head, and drives its own body
  by voice: light bars, dance / wave, screen brightness and sleep, volume,
  opening its screens, the time, and web search.
- **A face with an inner life:** it breathes, blinks, looks around, gets
  sleepy at night and lonely when left alone, and blushes when petted.
- **Senses:** room light (auto brightness), someone near, picked up,
  shaken, laid on its side, a double knock.
- **Head:** Off, Random (it looks around) or Locked; calibration and home
  poses in the Head app.
- **Light bars:** Alive (breathes with its inner life) and manual effects
  with colour themes.
- **Four UI themes:** Default, Aqua (Mac OS X), Luna (Windows XP) and
  Terminal (btop on a CRT). Settings > Display > Theme.
- **Settings** on the robot, a quick panel (top-right corner), Bluetooth and
  Wi-Fi setup pages, OTA updates over Wi-Fi, and a LAN remote-control API
  (`/api/gemini/*`) for testing.
- **Photo booth:** the camera (GC0308) takes a picture of you to decorate
  with stickers; photos and sticker packs live on the microSD card.
- **Music from the SD card:** MP3, M4A / M4B, FLAC, WAV and Ogg Vorbis /
  Opus from `music/` on the card (FAT32, 32 GB or less), with a Music app, a
  themed player and "play ..." by voice. Copy songs with a card reader or
  over Wi-Fi with `core/tools/sd_push.py`.
- **NFC cards:** tap a card and the robot plays music, dances, opens an app
  or says something; the NFC cards app writes them.

## Build

Needs [ESP-IDF 5.4](https://docs.espressif.com/projects/esp-idf/en/v5.4/esp32s3/get-started/)
(the Makefile looks for it in `~/esp/esp-idf`; set `IDF_PATH` in
`Makefile.local` if yours is elsewhere).

```sh
git clone --recursive https://github.com/hartj77-blip/stackchan-gemini.git
cd stackchan-gemini
git submodule update --init --recursive   # if you cloned without --recursive
core/tools/apply-m5-patches.sh   # M5Unified one-line fix for GCC 14
make set-target                  # first time only
make build
```

Optional machine-only settings go in `sdkconfig.defaults.local`
(gitignored), e.g. `CONFIG_STACKCHAN_TIMEZONE` and
`CONFIG_STACKCHAN_REMOTE_TOKEN` (a token for the remote API; empty = open
to your LAN).

## Install

First time, over USB (keeps settings already in flash):

```sh
make flash PORT=/dev/ttyACM0
```

After that, over Wi-Fi:

```sh
script/ota_wifi.py <robot-ip>
```

Wi-Fi and the Gemini API key are set from the robot's Bluetooth or web
settings page and live in NVS. **Don't erase flash** unless you want to set
them up again.

## License

Boost Software License 1.0 ([LICENSE](LICENSE)). Derived from
[stackchan-idf](https://github.com/ciniml/stackchan-idf) by Kenta IDA; see
[NOTICE](NOTICE).
