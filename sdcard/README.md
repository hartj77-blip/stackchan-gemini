# Starter microSD card

Free things to put on the robot's card (FAT32, 32 GB or less). The folders
here mirror the card: copy what's inside `sdcard/` to the top of the card
with a card reader, or push it over Wi-Fi:

```sh
export STACKCHAN_HOST=<robot-ip>
core/tools/sd_push.py push "sdcard/photos/sticker packs" "/sd/photos/sticker packs"
core/tools/sd_push.py push sdcard/music/Samples
```

| What | Where | Licence |
|---|---|---|
| Photo booth stickers: Kawaii (hearts, sparkles, cat ears...), Words, and three full-picture Frames | `photos/sticker packs/` | Drawn by `tools/make_stickers.py` for this project; Boost Software License 1.0 like the rest of the repo |
| J.S. Bach, Goldberg Variations BWV 988, Variatio 1, played by Kimiko Ishizaka (1:55, Ogg Vorbis) | `music/Samples/` | Public domain, CC0 1.0: from the [Open Goldberg Variations](https://www.opengoldbergvariations.org/), file from [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Kimiko_Ishizaka_-_02_-_Variatio_1_a_1_Clav.ogg) |

Your own stickers: any PNG with transparency in a folder under
`photos/sticker packs/` (one folder per pack; a file named `frame_*.png`,
or 300 px wide or more, is laid over the whole photo as a frame).
`tools/make_stickers.py` redraws these packs (needs Pillow and the Noto
fonts).

Your own music: MP3, M4A / M4B, FLAC, WAV or Ogg anywhere under `music/`.
