#!/usr/bin/env python3
"""Flash the app over Wi-Fi via the device's /api/ota/* endpoints (no USB).

    script/ota_wifi.py <host> [image]      image defaults to build-cores3/stackchan_gemini.bin

The host can also come from $STACKCHAN_HOST. Swapping to or from the Roombot
firmware works the same way (both use the same partition table).

Keeps NVS (Wi-Fi, keys, servo calibration). The device reboots into the new image and
marks it valid on boot; the bootloader rolls back if it doesn't come up.
"""
import json
import os
import sys
import time
import urllib.request

host = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("STACKCHAN_HOST", "")
if not host:
    raise SystemExit("usage: script/ota_wifi.py <host> [image]  (or set STACKCHAN_HOST)")
image = sys.argv[2] if len(sys.argv) > 2 else "build-cores3/stackchan_gemini.bin"
CHUNK = 16384


def post(path, data, ctype):
    req = urllib.request.Request(f"http://{host}{path}", data=data, headers={"Content-Type": ctype})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.loads(r.read() or b"{}")
    if body.get("ok") is False:
        raise SystemExit(f"{path}: {body}")
    return body


blob = open(image, "rb").read()
print(f"{image}: {len(blob)} bytes -> {host}")
post("/api/ota/control", json.dumps({"op": "begin", "size": len(blob)}).encode(), "application/json")
t0 = time.time()
for off in range(0, len(blob), CHUNK):
    for attempt in range(3):
        try:
            post("/api/ota/data", blob[off:off + CHUNK], "application/octet-stream")
            break
        except Exception as e:  # a dropped request on flaky Wi-Fi: retry the same chunk
            if attempt == 2:
                post("/api/ota/control", b'{"op":"abort"}', "application/json")
                raise SystemExit(f"chunk at {off} failed: {e}")
            time.sleep(1)
    print(f"\r{min(off + CHUNK, len(blob)) * 100 // len(blob)}%", end="", flush=True)
print(f"\nsent in {time.time() - t0:.0f} s")
print(post("/api/ota/control", b'{"op":"end"}', "application/json"))
