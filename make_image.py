#!/usr/bin/env python3
"""Draw THE WORLD TODAY — Thursday 19 November 2026 — entirely in code.

A newspaper front page summing up the day's world news, drawn with Pillow
using shapes only (rectangles, ellipses, polygons, arcs, lines) plus the
DejaVu system fonts. No photographs, no external images, no network access.

Run:  python3 make_image.py
Output: entry.png  (1024 x 1024, deterministic)
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 36

PAPER = (251, 248, 240)      # warm newsprint
INK = (18, 18, 18)
RULE = (40, 40, 40)
MUTED = (90, 86, 76)
ACCENT = (178, 34, 34)       # classic newspaper red
SKY_DUSK = (43, 16, 85)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def serif_bold(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf"), size)


def serif(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSerif.ttf"), size)


def sans_bold(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), size)


def sans(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans.ttf"), size)


def wrap(draw, text, font, width):
    """Greedy word wrap; returns a list of lines fitting `width` pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, width, text, font, fill=INK, leading=None):
    """Draw a wrapped paragraph; returns the y below the last line."""
    if leading is None:
        leading = font.size + 5
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, width=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def star(draw, cx, cy, r, fill):
    """Five-pointed star centred on (cx, cy)."""
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def burst(draw, cx, cy, r, fill):
    """Spiky explosion burst."""
    pts = []
    for i in range(24):
        ang = i * math.pi / 12
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


# --------------------------------------------------------------------------
# Illustrations (each draws inside the box x, y, w, h)
# --------------------------------------------------------------------------

def ill_vice_city(draw, x, y, w, h):
    """Neon dusk over Vice City: gradient sky, sun, skyline, palms, sea."""
    top = (43, 16, 85)
    mid = (214, 48, 120)
    bot = (255, 158, 92)
    for i in range(h):
        t = i / max(h - 1, 1)
        if t < 0.55:
            s = t / 0.55
            c = tuple(int(top[k] + (mid[k] - top[k]) * s) for k in range(3))
        else:
            s = (t - 0.55) / 0.45
            c = tuple(int(mid[k] + (bot[k] - mid[k]) * s) for k in range(3))
        draw.line([(x, y + i), (x + w, y + i)], fill=c)
    # sun and glow
    sx, sy = x + int(w * 0.68), y + int(h * 0.42)
    draw.ellipse([sx - 46, sy - 46, sx + 46, sy + 46], fill=(255, 190, 90))
    draw.ellipse([sx - 30, sy - 30, sx + 30, sy + 30], fill=(255, 214, 120))
    # skyline silhouette
    base = y + h - 34
    heights = [58, 92, 70, 118, 84, 64, 104, 76, 96, 60, 88, 72]
    bw = w // len(heights)
    for i, hh in enumerate(heights):
        bx = x + i * bw
        draw.rectangle([bx + 1, base - hh, bx + bw - 1, base], fill=(26, 10, 44))
        for wy in range(base - hh + 8, base - 6, 14):
            for wx in range(bx + 5, bx + bw - 5, 10):
                if (wx + wy) % 20 < 10:
                    draw.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 110))
    # sea with reflections
    draw.rectangle([x, base, x + w, y + h], fill=(16, 24, 64))
    for i, ry in enumerate(range(base + 6, y + h - 4, 8)):
        rw = 26 + (i % 3) * 18
        rx = x + 14 + (i * 37) % (w - 60)
        draw.line([(rx, ry), (rx + rw, ry)], fill=(255, 150, 110), width=2)
    # palm silhouettes
    for px, ph in ((x + 34, 66), (x + w - 40, 58)):
        draw.line([(px, base), (px + 6, base - ph)], fill=(12, 6, 24), width=5)
        for a in (-70, -35, 0, 35, 70):
            ang = math.radians(a - 90)
            ex = px + 6 + 26 * math.cos(ang)
            ey = base - ph + 26 * math.sin(ang) * 0.55
            draw.line([(px + 6, base - ph), (ex, ey)], fill=(12, 6, 24), width=3)
    # neon sign
    draw.rectangle([x + 8, y + 8, x + 132, y + 34], fill=(20, 8, 40),
                   outline=(255, 90, 170), width=2)
    draw.text((x + 16, y + 12), "VICE CITY", font=sans_bold(15),
              fill=(255, 120, 200))


def ill_summit(draw, x, y, w, h):
    """Three flags over a summit table with three seated leaders."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 232, 218))
    # flag poles and flags
    pole_x = [x + 26, x + w // 2, x + w - 34]
    # US flag
    fx, fy = x + 8, y + 8
    for i in range(7):
        draw.rectangle([fx, fy + i * 5, fx + 52, fy + i * 5 + 5],
                       fill=(178, 34, 52) if i % 2 == 0 else (245, 245, 245))
    draw.rectangle([fx, fy, fx + 22, fy + 19], fill=(28, 48, 110))
    for r in range(3):
        for c in range(3):
            draw.ellipse([fx + 3 + c * 6, fy + 3 + r * 6,
                          fx + 6 + c * 6, fy + 6 + r * 6], fill=(255, 255, 255))
    # China flag
    fx = x + w // 2 - 26
    draw.rectangle([fx, fy, fx + 52, fy + 35], fill=(222, 41, 16))
    star(draw, fx + 12, fy + 10, 7, (255, 222, 0))
    star(draw, fx + 30, fy + 7, 3, (255, 222, 0))
    star(draw, fx + 38, fy + 14, 3, (255, 222, 0))
    star(draw, fx + 36, fy + 23, 3, (255, 222, 0))
    star(draw, fx + 27, fy + 27, 3, (255, 222, 0))
    # Russia flag
    fx = x + w - 60
    draw.rectangle([fx, fy, fx + 52, fy + 35], fill=(255, 255, 255),
                   outline=(120, 120, 120))
    draw.rectangle([fx, fy, fx + 52, fy + 12], fill=(255, 255, 255))
    draw.rectangle([fx, fy + 12, fx + 52, fy + 24], fill=(0, 57, 166))
    draw.rectangle([fx, fy + 24, fx + 52, fy + 35], fill=(213, 0, 50))
    # poles
    for px in pole_x:
        draw.line([(px, y + 8), (px, y + h - 34)], fill=(90, 70, 40), width=3)
    # table
    draw.polygon([(x + 16, y + h - 26), (x + w - 16, y + h - 26),
                  (x + w - 30, y + h - 6), (x + 30, y + h - 6)],
                 fill=(120, 72, 40))
    # three seated figures
    suits = [(28, 48, 110), (150, 30, 30), (40, 40, 40)]
    for i, cx in enumerate((x + w * 0.20, x + w * 0.50, x + w * 0.80)):
        cy = y + h - 52
        draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(232, 190, 150))
        draw.polygon([(cx - 20, y + h - 28), (cx + 20, y + h - 28),
                      (cx + 26, y + h - 6), (cx - 26, y + h - 6)],
                     fill=suits[i])
        draw.polygon([(cx - 5, cy + 10), (cx + 5, cy + 10),
                      (cx, cy + 22)], fill=(245, 245, 245))
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=1)


def ill_capitol(draw, x, y, w, h):
    """US Capitol dome under a flag (fits inside its box)."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    # sky sun
    draw.ellipse([x + w - 40, y + 8, x + w - 14, y + 34], fill=(255, 214, 110))
    # dome: base line sits 28 px above the box bottom
    cx = x + w // 2
    base = y + h - 28
    draw.ellipse([cx - 44, base - 30, cx + 44, base], fill=(245, 245, 240),
                 outline=RULE, width=1)
    draw.rectangle([cx - 4, base - 38, cx + 4, base - 30], fill=(245, 245, 240),
                   outline=RULE, width=1)
    draw.line([(cx, base - 52), (cx, base - 38)], fill=RULE, width=2)
    draw.polygon([(cx, base - 54), (cx + 15, base - 49), (cx, base - 44)],
                 fill=(178, 34, 52))
    # drum and base
    draw.rectangle([cx - 38, base, cx + 38, y + h - 16], fill=(240, 240, 234),
                   outline=RULE, width=1)
    for i in range(7):
        colx = cx - 33 + i * 10
        draw.rectangle([colx, base + 3, colx + 5, y + h - 18], fill=(210, 210, 200))
    draw.rectangle([x + 14, y + h - 16, x + w - 14, y + h - 6], fill=(225, 222, 210),
                   outline=RULE, width=1)
    draw.rectangle([x + 30, y + h - 6, x + w - 30, y + h], fill=(200, 196, 184))
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=1)


def ill_gulf(draw, x, y, w, h):
    """Gulf waters: warships, a missile arc and an explosion."""
    draw.rectangle([x, y, x + w, y + h], fill=(250, 214, 150))
    draw.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=(24, 68, 120))
    # waves
    for i, wy in enumerate(range(y + int(h * 0.60), y + h - 6, 12)):
        for wx in range(x + 6 + (i % 2) * 14, x + w - 20, 28):
            draw.arc([wx, wy, wx + 18, wy + 10], 180, 360, fill=(150, 200, 240), width=2)
    # ship 1 (left)
    sx, sy = x + 16, y + int(h * 0.58)
    draw.polygon([(sx, sy), (sx + 120, sy), (sx + 104, sy + 26), (sx + 12, sy + 26)],
                 fill=(70, 76, 84))
    draw.rectangle([sx + 26, sy - 16, sx + 62, sy], fill=(96, 102, 110))
    draw.line([(sx + 40, sy - 16), (sx + 40, sy - 30)], fill=(70, 76, 84), width=3)
    # ship 2 (right, smaller)
    sx2, sy2 = x + w - 130, y + int(h * 0.64)
    draw.polygon([(sx2, sy2), (sx2 + 96, sy2), (sx2 + 84, sy2 + 20), (sx2 + 10, sy2 + 20)],
                 fill=(52, 58, 66))
    draw.rectangle([sx2 + 22, sy2 - 12, sx2 + 50, sy2], fill=(76, 82, 90))
    # missile arc from ship 1 (kept inside the box)
    pts = []
    for t in range(0, 21):
        s = t / 20
        mx = sx + 40 + s * (w - 120)
        my = sy - 12 - math.sin(s * math.pi) * 26
        pts.append((mx, my))
    draw.line(pts, fill=(60, 60, 60), width=2)
    # missile at arc end
    mx, my = pts[-1]
    draw.polygon([(mx, my - 4), (mx + 16, my), (mx, my + 4)], fill=(40, 40, 40))
    burst(draw, mx + 22, my, 16, (255, 140, 0))
    burst(draw, mx + 22, my, 9, (255, 220, 80))
    # smoke puffs
    for i, (px, py) in enumerate(((sx + 44, sy - 16), (sx + 52, sy - 22), (sx + 62, sy - 26))):
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(200, 200, 200))
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=1)


def ill_cyclone(draw, x, y, w, h):
    """Cyclone spiral over the Bay of Bengal coast."""
    draw.rectangle([x, y, x + w, y + h], fill=(206, 224, 238))
    # land (right side)
    draw.polygon([(x + w * 0.62, y), (x + w, y), (x + w, y + h),
                  (x + w * 0.72, y + h), (x + w * 0.58, y + h * 0.55)],
                 fill=(214, 196, 150))
    # coastline
    draw.line([(x + w * 0.62, y), (x + w * 0.58, y + h * 0.55),
               (x + w * 0.72, y + h)], fill=(120, 96, 60), width=2)
    # spiral storm (left-centre)
    cx, cy = x + int(w * 0.34), y + int(h * 0.52)
    for k in range(1, 7):
        r = k * 9
        draw.arc([cx - r, cy - r, cx + r, cy + r], 20 + k * 28, 300 + k * 28,
                 fill=(255, 255, 255), width=5)
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(120, 120, 120))
    # storm bands
    for i in range(5):
        ang = math.radians(30 + i * 64)
        ex = cx + 62 * math.cos(ang)
        ey = cy + 44 * math.sin(ang)
        draw.line([(cx + 18 * math.cos(ang), cy + 14 * math.sin(ang)), (ex, ey)],
                  fill=(255, 255, 255), width=4)
    # rain streaks
    for i in range(14):
        rx = x + 10 + (i * 29) % (w - 20)
        ry = y + 8 + (i * 17) % (h - 30)
        draw.line([(rx, ry), (rx - 5, ry + 12)], fill=(90, 130, 170), width=2)
    # label
    draw.text((x + 8, y + h - 18), "BAY OF BENGAL", font=sans_bold(11), fill=(40, 70, 100))
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=1)


def ill_chip(draw, x, y, w, h):
    """A green AI chip on a circuit board."""
    draw.rectangle([x, y, x + w, y + h], fill=(16, 32, 22))
    # circuit traces
    for i, ty in enumerate(range(y + 12, y + h - 10, 16)):
        draw.line([(x + 8, ty), (x + w - 8, ty)], fill=(28, 90, 48), width=1)
        draw.ellipse([x + w - 14, ty - 3, x + w - 8, ty + 3], fill=(40, 130, 70))
    # chip body (sized to fit inside the box)
    cx, cy = x + w // 2, y + h // 2
    s = 26
    draw.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(118, 185, 0),
                   outline=(200, 230, 120), width=2)
    # pins
    for i in range(6):
        px = cx - s + 6 + i * 9
        draw.rectangle([px, cy - s - 6, px + 5, cy - s], fill=(200, 200, 200))
        draw.rectangle([px, cy + s, px + 5, cy + s + 6], fill=(200, 200, 200))
        py = cy - s + 6 + i * 9
        draw.rectangle([cx - s - 6, py, cx - s, py + 5], fill=(200, 200, 200))
        draw.rectangle([cx + s, py, cx + s + 6, py + 5], fill=(200, 200, 200))
    # die
    draw.rectangle([cx - 15, cy - 15, cx + 15, cy + 15], fill=(30, 60, 20),
                   outline=(220, 240, 140), width=1)
    draw.text((cx - 8, cy - 9), "AI", font=sans_bold(15), fill=(220, 240, 140))
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=1)


def ill_voyager(draw, x, y, w, h):
    """Voyager 1 in deep space, one light-day from the Sun."""
    draw.rectangle([x, y, x + w, y + h], fill=(8, 10, 30))
    # stars
    for i in range(46):
        sx = x + 6 + (i * 53) % (w - 12)
        sy = y + 6 + (i * 29) % (h - 12)
        r = 1 + (i % 3 == 0)
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    # the Sun, far behind
    sx, sy = x + 26, y + h - 26
    draw.ellipse([sx - 14, sy - 14, sx + 14, sy + 14], fill=(255, 214, 90))
    for a in range(0, 360, 45):
        ang = math.radians(a)
        draw.line([(sx + 18 * math.cos(ang), sy + 18 * math.sin(ang)),
                   (sx + 26 * math.cos(ang), sy + 26 * math.sin(ang))],
                  fill=(255, 214, 90), width=2)
    # spacecraft: dish + body + boom
    cx, cy = x + int(w * 0.62), y + int(h * 0.42)
    draw.polygon([(cx - 34, cy - 30), (cx + 30, cy - 6), (cx - 6, cy + 22)],
                 fill=(212, 175, 105), outline=(240, 210, 150), width=1)
    draw.ellipse([cx - 10, cy - 8, cx + 10, cy + 8], fill=(120, 120, 130))
    draw.line([(cx + 8, cy + 4), (cx + 52, cy + 26)], fill=(200, 200, 210), width=3)
    draw.line([(cx - 4, cy + 8), (cx - 30, cy + 34)], fill=(200, 200, 210), width=2)
    draw.ellipse([cx + 48, cy + 22, cx + 56, cy + 30], fill=(255, 220, 120))
    # distance label
    draw.text((x + 8, y + 8), "1 LIGHT-DAY", font=sans_bold(11), fill=(180, 200, 255))
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=1)


# --------------------------------------------------------------------------
# Page layout
# --------------------------------------------------------------------------

def story_cell(draw, x, y, w, h, headline, body, ill):
    """One picture story: headline, illustration, body text."""
    yy = y
    head_font = sans_bold(20)
    for line in wrap(draw, headline, head_font, w):
        draw.text((x, yy), line, font=head_font, fill=INK)
        yy += 25
    yy += 2
    ill_h = 84
    ill(draw, x, yy, w, ill_h)
    yy += ill_h + 6
    para(draw, x, yy, w, body, serif(14), leading=19)
    hline(draw, x, x + w, y + h, width=1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # outer double frame
    draw.rectangle([10, 10, W - 11, H - 11], outline=RULE, width=2)
    draw.rectangle([16, 16, W - 17, H - 17], outline=RULE, width=1)

    # ---- masthead ----
    draw.text((W // 2, 30), "INDEPENDENT  •  WORLDWIDE  •  EST. 2026",
              font=sans(13), fill=MUTED, anchor="ma")
    draw.text((W // 2, 48), "THE WORLD TODAY", font=serif_bold(76),
              fill=INK, anchor="ma")
    hline(draw, MARGIN, W - MARGIN, 138, width=4)
    hline(draw, MARGIN, W - MARGIN, 145, width=1)

    # ---- dateline ----
    draw.text((MARGIN, 152), "THURSDAY 19 NOVEMBER 2026",
              font=sans_bold(15), fill=INK)
    draw.text((W // 2, 152), "LONDON  •  NEW YORK  •  TOKYO",
              font=sans(15), fill=MUTED, anchor="ma")
    draw.text((W - MARGIN, 152), "PRICE $2.50  •  No. 323",
              font=sans(15), fill=INK, anchor="ra")
    hline(draw, MARGIN, W - MARGIN, 176, width=1)

    # ---- lead story: GTA VI ----
    draw.text((MARGIN, 186), "AFTER 13 YEARS, VICE CITY CALLS",
              font=serif_bold(40), fill=INK)
    draw.text((MARGIN, 232),
              "Grand Theft Auto VI launches worldwide today — the most anticipated game in history.",
              font=sans(18), fill=MUTED)
    ill_vice_city(draw, MARGIN, 262, 600, 196)
    tx = MARGIN + 620
    tw = W - MARGIN - tx
    yy = para(draw, tx, 262, tw,
              "Rockstar Games returns to the neon streets of Vice City "
              "after a 13-year wait, with Lucia and Jason — a modern "
              "Bonnie and Clyde — at the heart of the story.",
              serif(16), leading=22)
    yy += 6
    hline(draw, tx, W - MARGIN, yy, width=1)
    yy += 8
    for fact in ("$79.99  •  PS5 & Xbox Series X|S",
                 "212 GB download  •  No PC date yet",
                 "8 Game Awards nominations, incl. GOTY"):
        draw.text((tx, yy), "▪  " + fact, font=sans(14), fill=INK)
        yy += 22
    hline(draw, MARGIN, W - MARGIN, 472, width=2)

    # ---- rows of picture stories ----
    col_w = (W - 2 * MARGIN - 24) // 2
    x2 = MARGIN + col_w + 24

    story_cell(draw, MARGIN, 484, col_w, 158,
               "THREE LEADERS, ONE TABLE",
               "Trump, Xi and Putin meet in Shenzhen at the APEC "
               "summit as the world watches for a deal.",
               ill_summit)
    story_cell(draw, x2, 484, col_w, 158,
               "JEFFRIES SET TO MAKE HISTORY",
               "Democrats nominate Hakeem Jeffries for Speaker — "
               "poised to be the first Black Speaker of the House.",
               ill_capitol)

    story_cell(draw, MARGIN, 652, col_w, 158,
               "GULF TENSIONS FLARE AGAIN",
               "US forces hit a missile site on Iran's Qeshm Island "
               "after attacks on bases in Bahrain and Kuwait.",
               ill_gulf)
    story_cell(draw, x2, 652, col_w, 158,
               "CYCLONE AKVAN BEARS DOWN",
               "The storm heads for India's east coast between "
               "Machilipatnam and Puri; railways on alert.",
               ill_cyclone)

    story_cell(draw, MARGIN, 820, col_w, 158,
               "NVIDIA HALTS CHINA CHIP SALES",
               "Acting chief Colette Kress ends H-series shipments "
               "to China and promises earlier staff pay rises.",
               ill_chip)
    story_cell(draw, x2, 820, col_w, 158,
               "VOYAGER 1: ONE LIGHT-DAY OUT",
               "NASA's 1977 probe passes a new milestone — now a "
               "full light-day from the Sun, still calling home.",
               ill_voyager)

    # ---- footer strip ----
    hline(draw, MARGIN, W - MARGIN, 988, width=2)
    draw.text((W // 2, 994),
              "INSIDE: MARKETS  •  SPORT  •  WEATHER  •  CULTURE  —  ALL PICTURES DRAWN IN CODE, NO PHOTOGRAPHS",
              font=sans(11), fill=MUTED, anchor="ma")

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
