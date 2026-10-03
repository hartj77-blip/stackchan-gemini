# stackchan-gemini — working conventions

The base tier of three Stack-chan firmwares (Gemini → Roombot → Server Bot)
for the same M5Stack CoreS3 robot. Almost everything lives in the shared
core, the `core/` submodule (`~/stackchan-core`): **read `core/CLAUDE.md`
first** — code style, hardware, RAM budget, screens, head, LEDs, senses,
themes, tools and the remote API are all documented there.

## What's here

- `main/app_main.cpp`: the tier's hooks (`tier::Hooks`, name `gemini`, so
  the remote API is `/api/gemini/*`), the photo booth (the core's opt-in
  `stackchan_photo`; its camera / FATFS lines are in `sdkconfig.defaults.cores3`)
  and its launcher places. Nothing else.
- `partitions.csv` is a symlink to `core/partitions.csv`.
- `sdkconfig.defaults.local` / `Makefile.local` (gitignored): timezone,
  `CONFIG_STACKCHAN_REMOTE_TOKEN`, IDF path, port.

## Rules

- **A feature that every Stack-chan should have goes in the core**, not
  here: change `~/stackchan-core` first, then bump the submodule here and in
  the other tiers (`~/stackchan-roombot`, `~/stackchan-serverbot/firmware`)
  and build each. Gemini-only things go in `main/` through the core's hooks.
- **Same robot, swapped by OTA:** never change the partition table or the
  shared NVS keys here; **never erase flash** (Wi-Fi, the Gemini key and
  servo calibration live in NVS).
- **This repo will be public:** no IPs, hostnames, keys or tokens in
  committed files.
- Build: `make build`; flash over Wi-Fi with `script/ota_wifi.py <ip>`
  (check which firmware the robot runs first: `GET /api/<tier>/diag`).
