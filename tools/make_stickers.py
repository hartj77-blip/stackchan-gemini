#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 JJ Hartnett <jj.hartnett777@gmail.com>
# SPDX-License-Identifier: BSL-1.0
"""Draw the photo booth's starter sticker packs (purikura style).

    tools/make_stickers.py [OUT_DIR]      (default "sdcard/photos/sticker packs")

Writes one folder per pack of RGBA PNGs:

    Kawaii/   hearts, sparkles, stars, cat ears, whiskers, blush, crown, bow ...
    Words/    かわいい, ラブ, 最高!, ずっ友, Yay!, BFF ... (fat white outline)
    Frames/   frame_*.png, 640 x 480 borders laid over the whole photo

Stickers are ~180 px on their long side: the booth shows them at ~90 px and
the saved 640 x 480 photo draws them at 2x. Push to the card with
core/tools/sd_push.py; or copy the folders into "photos/sticker packs/" on the
card from a PC. Any PNG with transparency works the same way; a file named
frame_*.png (or 300 px wide or more) is a frame.

Needs Pillow and the Noto fonts (fonts-noto-cjk, fonts-noto-core).
"""

import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

CJK_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
LATIN_BLACK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"

SS = 4  # supersample, for smooth edges
PINK = (255, 105, 170)
HOT = (240, 60, 120)
YELLOW = (255, 215, 60)
MINT = (90, 215, 180)
SKY = (110, 180, 255)
LILAC = (185, 140, 255)
WHITE = (255, 255, 255)
INK = (70, 40, 70)


def canvas(w, h):
    return Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))


def finish(img, outline=10, shadow=True):
    """Fat white outline + soft drop shadow around whatever is drawn, then downsample."""
    a = img.getchannel("A")
    ring = a.filter(ImageFilter.MaxFilter(outline * SS // 2 * 2 + 1))
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", img.size, (60, 20, 60, 0))
        sh.putalpha(ring.point(lambda v: v * 70 // 255))
        out.alpha_composite(sh, (SS * 3, SS * 4))
    white = Image.new("RGBA", img.size, WHITE + (0,))
    white.putalpha(ring)
    out.alpha_composite(white)
    out.alpha_composite(img)
    w, h = img.size
    out = out.resize((w // SS, h // SS), Image.LANCZOS)
    return out.crop(out.getbbox())


def heart_poly(cx, cy, r, n=120):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * r / 17, cy + y * r / 17))
    return pts


def star_poly(cx, cy, r_out, r_in, points=5, rot=-90):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + 180 * i / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def s(v):
    return v * SS


# ---- Kawaii -------------------------------------------------------------------------


def heart(color):
    img = canvas(180, 170)
    d = ImageDraw.Draw(img)
    d.polygon(heart_poly(s(90), s(88), s(78)), fill=color)
    d.ellipse([s(40), s(40), s(70), s(62)], fill=(255, 255, 255, 170))  # shine
    return finish(img)


def hearts_trio():
    img = canvas(200, 170)
    d = ImageDraw.Draw(img)
    for cx, cy, r, c in [(60, 110, 48, PINK), (140, 95, 56, HOT), (100, 45, 30, LILAC)]:
        d.polygon(heart_poly(s(cx), s(cy), s(r)), fill=c)
    return finish(img)


def sparkle(color):
    img = canvas(180, 180)
    d = ImageDraw.Draw(img)
    d.polygon(star_poly(s(90), s(90), s(84), s(18), 4), fill=color)
    d.polygon(star_poly(s(150), s(40), s(22), s(5), 4), fill=color)
    d.polygon(star_poly(s(35), s(145), s(16), s(4), 4), fill=color)
    return finish(img, outline=8)


def star(color):
    img = canvas(180, 175)
    d = ImageDraw.Draw(img)
    d.polygon(star_poly(s(90), s(95), s(86), s(40)), fill=color)
    d.ellipse([s(68), s(82), s(80), s(98)], fill=INK)  # a face
    d.ellipse([s(100), s(82), s(112), s(98)], fill=INK)
    d.arc([s(78), s(96), s(102), s(116)], 20, 160, fill=INK, width=s(4))
    d.ellipse([s(56), s(104), s(70), s(112)], fill=(255, 150, 170))
    d.ellipse([s(110), s(104), s(124), s(112)], fill=(255, 150, 170))
    return finish(img)


def cat_ears():
    img = canvas(240, 120)
    d = ImageDraw.Draw(img)
    for x0, flip in [(10, False), (140, True)]:
        outer = [(s(x0), s(115)), (s(x0 + 45), s(5)), (s(x0 + 90), s(115))]
        inner = [(s(x0 + 20), s(108)), (s(x0 + 45), s(35)), (s(x0 + 70), s(108))]
        d.polygon(outer, fill=(60, 50, 60))
        d.polygon(inner, fill=PINK)
    return finish(img, outline=8)


def whiskers_blush():
    img = canvas(240, 90)
    d = ImageDraw.Draw(img)
    for cx in (50, 190):
        d.ellipse([s(cx - 36), s(28), s(cx + 36), s(62)], fill=(255, 120, 160, 200))
    for side in (-1, 1):
        cx = 120 + side * 110
        for dy in (-14, 0, 14):
            d.line([(s(120 + side * 40), s(45 + dy / 2)), (s(cx), s(45 + dy))], fill=INK, width=s(4))
    return finish(img, outline=6, shadow=False)


def crown():
    img = canvas(200, 140)
    d = ImageDraw.Draw(img)
    pts = [(s(15), s(130)), (s(15), s(40)), (s(60), s(85)), (s(100), s(20)), (s(140), s(85)), (s(185), s(40)),
           (s(185), s(130))]
    d.polygon(pts, fill=YELLOW)
    for cx, c in [(55, PINK), (100, SKY), (145, MINT)]:
        d.ellipse([s(cx - 11), s(100), s(cx + 11), s(122)], fill=c)
    for cx, cy in [(15, 40), (100, 20), (185, 40)]:
        d.ellipse([s(cx - 10), s(cy - 10), s(cx + 10), s(cy + 10)], fill=YELLOW)
    return finish(img)


def bow():
    img = canvas(200, 130)
    d = ImageDraw.Draw(img)
    d.polygon([(s(100), s(65)), (s(10), s(10)), (s(20), s(120))], fill=HOT)
    d.polygon([(s(100), s(65)), (s(190), s(10)), (s(180), s(120))], fill=HOT)
    d.ellipse([s(78), s(42), s(122), s(88)], fill=PINK)
    for x in (40, 160):
        d.ellipse([s(x - 6), s(55), s(x + 6), s(67)], fill=WHITE)
    return finish(img)


def flower(petal):
    img = canvas(170, 170)
    d = ImageDraw.Draw(img)
    for i in range(5):
        a = math.radians(i * 72 - 90)
        cx, cy = 85 + 45 * math.cos(a), 85 + 45 * math.sin(a)
        d.ellipse([s(cx - 36), s(cy - 36), s(cx + 36), s(cy + 36)], fill=petal)
    d.ellipse([s(60), s(60), s(110), s(110)], fill=YELLOW)
    return finish(img)


def note():
    img = canvas(150, 180)
    d = ImageDraw.Draw(img)
    d.ellipse([s(10), s(120), s(65), s(165)], fill=LILAC)
    d.ellipse([s(85), s(100), s(140), s(145)], fill=LILAC)
    d.rectangle([s(55), s(20), s(67), s(145)], fill=LILAC)
    d.rectangle([s(130), s(5), s(142), s(125)], fill=LILAC)
    d.polygon([(s(55), s(20)), (s(142), s(5)), (s(142), s(35)), (s(55), s(50))], fill=LILAC)
    return finish(img)


def bubble(text):
    img = canvas(200, 150)
    d = ImageDraw.Draw(img)
    d.ellipse([s(5), s(5), s(195), s(115)], fill=WHITE)
    d.polygon([(s(50), s(100)), (s(30), s(145)), (s(90), s(108))], fill=WHITE)
    f = ImageFont.truetype(CJK_BOLD, s(44), index=0)
    d.text((s(100), s(60)), text, font=f, fill=HOT, anchor="mm")
    img2 = finish(img, outline=6)
    return img2


# ---- Words ----------------------------------------------------------------------------


def word(text, color, size=64, cjk=True, tilt=-6):
    font = ImageFont.truetype(CJK_BOLD if cjk else LATIN_BLACK, s(size), index=0) if cjk else \
        ImageFont.truetype(LATIN_BLACK, s(size))
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    l, t, r, b = tmp.textbbox((0, 0), text, font=font)
    pad = s(12)
    img = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Coloured fill with a darker rim, like a purikura stamp.
    d.text((pad - l, pad - t), text, font=font, fill=color, stroke_width=s(3),
           stroke_fill=tuple(max(0, c - 70) for c in color))
    img = img.rotate(tilt, resample=Image.BICUBIC, expand=True)
    # Cap the long side at ~200 px after the outline.
    out = finish(img, outline=11)
    if max(out.size) > 210:
        k = 210 / max(out.size)
        out = out.resize((round(out.width * k), round(out.height * k)), Image.LANCZOS)
    return out


# ---- Frames (640 x 480) ------------------------------------------------------------------

FW, FH = 640, 480


def frame_hearts():
    img = Image.new("RGBA", (FW * 2, FH * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    b = 44
    d.rectangle([0, 0, FW * 2, b * 2], fill=(255, 190, 215, 255))
    d.rectangle([0, FH * 2 - b * 2, FW * 2, FH * 2], fill=(255, 190, 215, 255))
    d.rectangle([0, 0, b * 2, FH * 2], fill=(255, 190, 215, 255))
    d.rectangle([FW * 2 - b * 2, 0, FW * 2, FH * 2], fill=(255, 190, 215, 255))
    d.rounded_rectangle([b * 2 - 8, b * 2 - 8, FW * 2 - b * 2 + 8, FH * 2 - b * 2 + 8], radius=40, outline=WHITE,
                        width=12)
    rnd = random.Random(7)
    step = 110
    along = [(x, b) for x in range(b, FW * 2, step)] + [(x, FH * 2 - b) for x in range(b, FW * 2, step)] + \
            [(b, y) for y in range(b + step, FH * 2 - b, step)] + [(FW * 2 - b, y) for y in range(b + step, FH * 2 - b, step)]
    for (x, y) in along:
        c = rnd.choice([PINK, HOT, LILAC, (255, 255, 255)])
        d.polygon(heart_poly(x, y, 30), fill=c)
    f = ImageFont.truetype(LATIN_BLACK, 64)
    d.text((FW, FH * 2 - 50), "Stack-chan Photo Booth", font=f, fill=HOT, anchor="mm", stroke_width=8,
           stroke_fill=WHITE)
    return img.resize((FW, FH), Image.LANCZOS)


def frame_polaroid():
    img = Image.new("RGBA", (FW * 2, FH * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cream = (252, 250, 244, 255)
    top, side, bottom = 40, 40, 150
    d.rectangle([0, 0, FW * 2, top], fill=cream)
    d.rectangle([0, 0, side, FH * 2], fill=cream)
    d.rectangle([FW * 2 - side, 0, FW * 2, FH * 2], fill=cream)
    d.rectangle([0, FH * 2 - bottom, FW * 2, FH * 2], fill=cream)
    f = ImageFont.truetype(CJK_BOLD, 76, index=0)
    d.text((FW, FH * 2 - bottom / 2), "ずっと友だち ♡", font=f, fill=(90, 90, 110), anchor="mm")
    return img.resize((FW, FH), Image.LANCZOS)


def frame_sparkle():
    img = Image.new("RGBA", (FW * 2, FH * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Pastel rainbow border.
    band = 56
    cols = [(255, 170, 200), (255, 220, 150), (170, 235, 200), (170, 205, 255), (215, 180, 255)]
    for i in range(band):
        c = cols[i * len(cols) // band] + (255,)
        d.rectangle([i, i, FW * 2 - 1 - i, FH * 2 - 1 - i], outline=c)
    rnd = random.Random(3)
    for _ in range(26):
        edge = rnd.choice("tblr")
        x = rnd.randrange(40, FW * 2 - 40) if edge in "tb" else (rnd.randrange(10, 110) if edge == "l" else
                                                                     rnd.randrange(FW * 2 - 110, FW * 2 - 10))
        y = rnd.randrange(40, FH * 2 - 40) if edge in "lr" else (rnd.randrange(10, 110) if edge == "t" else
                                                                     rnd.randrange(FH * 2 - 110, FH * 2 - 10))
        r = rnd.randrange(14, 38)
        d.polygon(star_poly(x, y, r, r / 4.5, 4, 0), fill=(255, 255, 255, 255))
    return img.resize((FW, FH), Image.LANCZOS)


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "sdcard/photos/sticker packs")
    packs = {
        "Kawaii": {
            "heart_pink": heart(PINK), "heart_red": heart(HOT), "hearts": hearts_trio(),
            "sparkle_gold": sparkle(YELLOW), "sparkle_blue": sparkle(SKY), "star_face": star(YELLOW),
            "cat_ears": cat_ears(), "whiskers": whiskers_blush(), "crown": crown(), "bow": bow(),
            "flower_pink": flower(PINK), "flower_mint": flower(MINT), "note": note(), "bubble_love": bubble("♡"),
        },
        "Words": {
            "kawaii": word("かわいい", PINK), "love": word("ラブ♡", HOT, 72), "saikou": word("最高!", YELLOW, 70, tilt=5),
            "zuttomo": word("ずっ友", LILAC, 70), "kirakira": word("キラキラ", SKY, 58, tilt=4),
            "peace": word("ピース", MINT, 64), "yay": word("Yay!", HOT, 72, cjk=False, tilt=8),
            "bff": word("BFF", SKY, 80, cjk=False), "cute": word("so cute", PINK, 56, cjk=False),
        },
        "Frames": {
            "frame_hearts": frame_hearts(), "frame_polaroid": frame_polaroid(), "frame_sparkle": frame_sparkle(),
        },
    }
    for pack, items in packs.items():
        d = out / pack
        d.mkdir(parents=True, exist_ok=True)
        for name, img in items.items():
            p = d / f"{name}.png"
            img.save(p, optimize=True)
            print(f"{p}  {img.width}x{img.height}  {p.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
