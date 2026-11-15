# Starter microSD card

Free things to put on the robot's card (FAT32, 32 GB or less). One command
sends all of it over Wi-Fi:

```sh
make sdcard HOST=<robot-ip>
```

Or with a card reader: the folders here mirror the card, so copy `music`,
`videos` and `photos` to the top of the card.

| What | Where | Licence |
|---|---|---|
| Photo booth stickers: Kawaii (hearts, sparkles, cat ears...), Words, and three full-picture Frames | `photos/sticker packs/` | Drawn by `tools/make_stickers.py` for this project; Boost Software License 1.0 like the rest of the repo |
| J.S. Bach, Goldberg Variations BWV 988, Variatio 1, played by Kimiko Ishizaka (1:55, Ogg Vorbis) | `music/Samples/` | Public domain, CC0 1.0: from the [Open Goldberg Variations](https://www.opengoldbergvariations.org/), file from [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Kimiko_Ishizaka_-_02_-_Variatio_1_a_1_Clav.ogg) |
| The launch of Apollo 11 with Jack King's countdown commentary, 16 July 1969 (0:21, already in the robot's video format) | `videos/` | Public domain: a NASA film, from [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Jack_King%27s_Apollo_11_Launch_Commentary_o4OBKOlgmfo.webm); cropped, resized and made louder for the robot |

Your own stickers: any PNG with transparency in a folder under
`photos/sticker packs/` (one folder per pack; a file named `frame_*.png`,
or 300 px wide or more, is laid over the whole photo as a frame).
`tools/make_stickers.py` redraws these packs (needs Pillow and the Noto
fonts).

Your own music: MP3, M4A / M4B, FLAC, WAV or Ogg anywhere under `music/`
(`core/tools/sd_push.py push <folder>`).

Your own videos: `core/tools/sd_push.py push <video file or folder>` converts
any video for the robot and puts it in `videos/`. For a long film, make the
file on the PC (`core/tools/sd_push.py convert film.mkv`) and copy it with a
card reader: Wi-Fi to the card is slow.
