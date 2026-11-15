# Stackchan Gemini

The base Stack-chan: an M5Stack CoreS3 Stack-chan you talk to through
Gemini Live, using everything the robot itself has, with nothing on a PC
behind it. ESP-IDF 5.4 / C++20.

It is the first of three firmwares on the same shared core
([stackchan-core](https://github.com/hartj77-blip/stackchan-core), the
`core/` submodule):

| Tier | Firmware | What it adds |
|---|---|---|
| Base | **Stackchan Gemini** (this) | The robot and Gemini: face, voice, head, light bars, senses, camera / photo booth, SD-card music and videos, NFC cards, themes |
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
  Wi-Fi setup pages, OTA updates over Wi-Fi, a remote control in the
  robot's own web page, and a LAN remote-control API (`/api/gemini/*`).
- **Photo booth:** the camera (GC0308) takes a picture of you to decorate
  with stickers; photos and sticker packs live on the microSD card.
- **Music from the SD card:** MP3, M4A / M4B, FLAC, WAV and Ogg Vorbis /
  Opus from `music/` on the card (FAT32, 32 GB or less), with a Music app, a
  themed player and "play ..." by voice. Copy songs with a card reader or
  over Wi-Fi with `core/tools/sd_push.py`.
- **Videos from the SD card:** the Videos app plays clips full screen with
  sound, and "play the Apollo video" works by voice. Any video file works:
  `core/tools/sd_push.py push holiday.mp4` converts it for the robot's
  320 x 240 screen and sends it over Wi-Fi.
- **NFC cards:** tap a card and the robot says a phrase, asks Gemini
  something, plays a song or a video, changes its lights or face, dances, or
  several of those at once. You make cards without touching code: on the
  robot (Apps > NFC cards) or from the robot's web page (see below).

The firmware image itself carries no stickers, songs or videos: they live
on the microSD card. [`sdcard/`](sdcard/) has a free starter set, and one
command puts all of it on the card over Wi-Fi (`make sdcard`, step 5
below): 26 photo booth stickers and frames, a public-domain (CC0) Bach
recording, and NASA's film of the Apollo 11 launch.

## Get it running

You need an M5Stack CoreS3 on a Stack-chan body, a USB-C cable, a 2.4 GHz
Wi-Fi network and a free Gemini API key.

### 1. Get a Gemini API key

Sign in at [Google AI Studio](https://aistudio.google.com/apikey), press
**Create API key** and copy it (it starts with `AIza`). The robot talks to
Gemini Live with it directly; there is no server in between. Keep it out
of git: it only ever goes into the gitignored file below or into the
robot's own settings.

### 2. Build

Needs [ESP-IDF 5.4](https://docs.espressif.com/projects/esp-idf/en/v5.4/esp32s3/get-started/)
(the Makefile looks for it in `~/esp/esp-idf`; set `IDF_PATH` in
`Makefile.local` if yours is elsewhere).

```sh
git clone --recursive https://github.com/hartj77-blip/stackchan-gemini.git
cd stackchan-gemini
git submodule update --init --recursive   # if you cloned without --recursive
core/tools/apply-m5-patches.sh   # M5Unified one-line fix for GCC 14
```

Then link your Wi-Fi and Gemini key. The easy way is to build them in:
create `sdkconfig.defaults.local` (gitignored, never committed) next to
the Makefile:

```
CONFIG_STACKCHAN_WIFI_SSID="your network"
CONFIG_STACKCHAN_WIFI_PASSWORD="your password"
CONFIG_STACKCHAN_GEMINI_API_KEY="AIza..."
CONFIG_STACKCHAN_TIMEZONE="EST5EDT,M3.2.0,M11.1.0"
```

The timezone is a POSIX string (that one is US Eastern; `JST-9` is Japan;
the default is UTC). You can also add `CONFIG_STACKCHAN_REMOTE_TOKEN="..."`
to put a password on the remote-control API (empty = open to your LAN).
These are fallbacks for a robot that has nothing saved yet: anything set
later in the robot's settings wins.

```sh
make set-target                  # first time only
make build
```

### 3. Flash it (first time: USB)

Plug the CoreS3 in by USB-C and:

```sh
make flash                       # or: make flash PORT=/dev/ttyACM0
```

This writes the bootloader, the partition table, the firmware and the
face assets, and keeps settings already in flash. If the port isn't found
or the upload won't start, hold the CoreS3's reset button for about three
seconds until the green light comes on (download mode), flash again, then
press reset once.

The robot boots, joins your Wi-Fi and its status line shows Gemini
connecting. Pat its head and talk.

### 4. Link Wi-Fi or Gemini without rebuilding

If you left them out of the build, or want to change them later:

- **On Wi-Fi already:** open `http://<robot-ip>/` in a browser (the
  address is in Settings on the robot, and it also answers at
  `stackchan-xxxxxx.local`). Fill in **Gemini API Key** (and the Wi-Fi
  fields, the voice or a persona if you like) and save.
- **No Wi-Fi yet:** the robot switches Bluetooth on by itself 30 seconds
  after a boot without Wi-Fi (or use the Bluetooth switch in Settings).
  Open `core/tools/settings.html` from your clone in desktop Chrome or
  Edge (133 or newer; Firefox and Safari can't do Web Bluetooth), connect
  to the robot and fill in **Wi-Fi SSID**, the Wi-Fi password and the
  **Gemini API** key. That page is still in Japanese (it comes from
  upstream stackchan-idf); the three fields are the first three on it.
  The link is encrypted per connection; no pairing is needed.

Wi-Fi, the Gemini key and the servo calibration live in the robot's
settings storage (NVS). **Don't erase flash** (`make erase-flash`) unless
you want to set them up again.

### 5. Fill the SD card (optional)

Put a microSD card (FAT32, 32 GB or less) in the robot and send the starter
set: stickers for the photo booth, a song and a video.

```sh
make sdcard HOST=<robot-ip>
```

(If you gave the robot a `CONFIG_STACKCHAN_REMOTE_TOKEN`, first
`export STACKCHAN_TOKEN=<that token>`.)

Your own things go the same way, no converting by hand (videos need
`ffmpeg` installed on the PC):

```sh
export STACKCHAN_HOST=<robot-ip>
core/tools/sd_push.py push ~/Music/"Abbey Road"     # an album folder -> the Music app
core/tools/sd_push.py push ~/Videos/holiday.mp4     # any video -> the Videos app
```

### 6. Updates over Wi-Fi

After the first flash you don't need the cable:

```sh
make update HOST=<robot-ip>
```

The robot reboots into the new firmware and keeps its settings; if the
new image doesn't come up, the bootloader rolls back to the old one.

### Control it from a browser

`http://<robot-ip>/` is also a remote control (it asks for the remote
token if you set one). Under **Remote Control** you get the robot's screen
live, and you can tap and swipe on it as if you were touching the robot.
Below it: the assistant on or off, spoken replies on or off, always
listening, "say this" and "ask it this" boxes, voice volume; the head
(mode, look up / down / left / right, exact turn and tilt), dance and
wave; the six faces; music and video from the SD card with pause, skip,
stop and volume; screen brightness; and a button for every app.

### Make NFC cards

Any NTAG213 / 215 / 216 card or sticker works. Open `http://<robot-ip>/`
on a phone or PC, open **NFC Cards**, and pick what the card should do:
say a phrase you type, ask Gemini a question, play music or a video from
the SD card, set the lights, a face, the volume, open an app. **Add as a
step** makes a card that does several things in a row. Then:

- **Try it now** makes the robot do it straight away.
- **Write to card**, then hold a card to the robot.
- **Save to My cards** keeps it on the robot: the saved ones can be tried,
  written, edited and deleted from the page, and show on the robot under
  Apps > NFC cards > More > My cards.

The same choices (with built-in phrases) are on the robot's own screen in
Apps > NFC cards.

### If Gemini doesn't answer

- "Waiting for Wi-Fi": the network name or password is wrong, or the
  network is 5 GHz only.
- Connected but silent: check the key at AI Studio. A free key has a
  quota; "You exceeded your current quota" in the log
  (`http://<robot-ip>/api/gemini/log`) means wait or use another key.

## License

Boost Software License 1.0 ([LICENSE](LICENSE)). Derived from
[stackchan-idf](https://github.com/ciniml/stackchan-idf) by Kenta IDA; see
[NOTICE](NOTICE).
