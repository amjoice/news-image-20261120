#!/usr/bin/env python3
"""Draw the news-image-20261120 front page with PIL and save entry.png.

A newspaper front page summing up Friday 20 November 2026: Cyclone Akvan's
landfall in Odisha, COP31's final day in Antalya, the Gulf radar claim,
New Zealand's Test fightback in Wellington, and the Senegal boat search.
Every story was checked against reporting of that day before drawing.

Run:  python3 draw.py            (writes entry.png beside this file)
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (248, 244, 233)
INK = (20, 38, 74)
RED = (166, 30, 34)
GOLD = (192, 138, 43)
SLATE = (90, 107, 124)
PALE = (226, 232, 238)
WHITE = (255, 255, 255)
CREAM = (250, 247, 238)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, lines, fnt, max_w):
    """Shrink font until every line fits; returns (font, lines)."""
    size = fnt.size
    while size > 10 and any(d.textlength(t, font=fnt) > max_w for t in lines):
        size -= 1
        fnt = ImageFont.truetype(fnt.path, size)
    return fnt


def text_block(d, x, y, lines, fnt, fill, leading=None):
    lead = leading if leading is not None else int(fnt.size * 1.18)
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += lead
    return y


def kicker(d, x, y, label, color=RED, size=19):
    f = font(SANS_B, size)
    d.text((x, y), label, font=f, fill=color)
    return y + size + 6


def spiral(d, cx, cy, r_max, color, width=7):
    """Archimedean spiral made of short line segments."""
    pts = []
    steps = 260
    for i in range(steps + 1):
        t = i / steps * 3.6 * math.pi
        r = r_max * i / steps
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    d.line(pts, fill=color, width=width, joint="curve")


def cyclone_art(d, x0, y0, x1, y1):
    """Storm spiral over a stylised coastline, with a landfall marker."""
    d.rectangle([x0, y0, x1, y1], fill=(214, 226, 235))
    # rain streaks
    for i in range(14):
        rx = x0 + 14 + i * 24
        d.line([(rx, y0 + 8), (rx - 10, y0 + 44)], fill=(150, 170, 190), width=3)
    # coastline: a curved shore along the bottom-left
    shore = []
    for i in range(41):
        t = i / 40
        shore.append((x0 + 8 + t * (x1 - x0 - 16),
                      y1 - 26 - 34 * math.sin(t * math.pi * 0.85)))
    d.line(shore, fill=(120, 140, 160), width=4, joint="curve")
    d.line([(x0 + 8, y1 - 8)] + shore, fill=(120, 140, 160), width=2)
    # the storm itself
    cx, cy = (x0 + x1) // 2 + 18, (y0 + y1) // 2 - 6
    spiral(d, cx, cy, 92, INK, 7)
    spiral(d, cx, cy, 62, RED, 5)
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=RED)
    # landfall marker on the shore
    mx, my = x0 + 118, y1 - 52
    d.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=RED,
              outline=WHITE, width=2)
    d.text((mx + 12, my - 9), "GOPALPUR", font=font(SANS_B, 15), fill=INK)


def globe_art(d, x0, y0, x1, y1):
    """A globe with a red 1.5C tag."""
    d.rectangle([x0, y0, x1, y1], fill=(222, 235, 228))
    cx, cy, r = (x0 + x1) // 2, (y0 + y1) // 2, 62
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(38, 92, 110))
    for k in (-1, 0, 1):
        d.ellipse([cx - r + 26 * abs(k), cy - r, cx + r - 26 * abs(k),
                   cy + r], outline=(222, 235, 228), width=3)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(222, 235, 228), width=3)
    d.arc([cx - r, cy - r + 26, cx + r, cy + r - 26], 200, 340,
          fill=(222, 235, 228), width=3)
    d.arc([cx - r, cy - r + 26, cx + r, cy + r - 26], 20, 160,
          fill=(222, 235, 228), width=3)
    d.rounded_rectangle([x1 - 92, y1 - 34, x1 - 8, y1 - 8], radius=6,
                        fill=RED)
    d.text((x1 - 84, y1 - 29), "1.5°C", font=font(SANS_B, 17), fill=WHITE)


def radar_art(d, x0, y0, x1, y1):
    """Radar dish sweeping over a tanker on waves."""
    d.rectangle([x0, y0, x1, y1], fill=(232, 226, 214))
    cx, cy = (x0 + x1) // 2, y0 + 78
    for r in (26, 48, 70):
        d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360,
              fill=INK, width=4)
    d.line([(cx, cy), (cx + 62, cy - 46)], fill=RED, width=5)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=INK)
    # tanker hull, kept inside the panel
    hy = y1 - 46
    d.polygon([(x0 + 14, hy), (x1 - 14, hy), (x1 - 28, hy + 22),
               (x0 + 28, hy + 22)], fill=INK)
    bw = (x1 - x0 - 44) // 3
    for i in range(3):
        bx = x0 + 22 + i * bw
        d.rectangle([bx, hy - 18, bx + bw - 8, hy], fill=RED)
    # waves
    for wy in (y1 - 14, y1 - 6):
        pts = []
        for i in range(41):
            t = i / 40
            pts.append((x0 + 8 + t * (x1 - x0 - 16),
                        wy + 4 * math.sin(t * math.pi * 5)))
        d.line(pts, fill=SLATE, width=3, joint="curve")


def cricket_art(d, x0, y0, x1, y1):
    """Stumps, a red ball and the lunch score."""
    d.rectangle([x0, y0, x1, y1], fill=(226, 234, 222))
    sx = x0 + 30
    for i in range(3):
        d.rectangle([sx + i * 16, y0 + 30, sx + i * 16 + 9, y0 + 96],
                    fill=GOLD)
    d.rectangle([sx + 2, y0 + 23, sx + 40, y0 + 29], fill=GOLD)
    d.ellipse([x1 - 78, y0 + 26, x1 - 30, y0 + 74], fill=RED)
    d.arc([x1 - 78, y0 + 26, x1 - 30, y0 + 74], 250, 110,
          fill=WHITE, width=3)
    d.text((x0 + 14, y1 - 56), "317/6", font=font(SERIF, 38), fill=INK)
    d.text((x0 + 14, y1 - 20), "AT LUNCH, DAY 2",
           font=font(SANS_B, 13), fill=RED)


def boat_art(d, x0, y0, x1, y1):
    """A small boat on heavy waves with a life ring."""
    d.rectangle([x0, y0, x1, y1], fill=(214, 228, 236))
    # boat hull tilted on a wave, mast and flag top-left
    d.polygon([(x0 + 16, y0 + 62), (x1 - 24, y0 + 50), (x1 - 12, y0 + 70),
               (x0 + 30, y0 + 80)], fill=INK)
    d.line([(x0 + 62, y0 + 56), (x0 + 62, y0 + 22)], fill=INK, width=4)
    d.polygon([(x0 + 62, y0 + 22), (x0 + 94, y0 + 46), (x0 + 62, y0 + 46)],
              fill=RED)
    # life ring, bottom-right, clear of the mast
    rx, ry = x1 - 36, y1 - 40
    d.ellipse([rx - 22, ry - 22, rx + 22, ry + 22], outline=RED, width=8)
    d.ellipse([rx - 10, ry - 10, rx + 10, ry + 10], outline=RED, width=3)
    # waves
    for wy in (y0 + 104, y0 + 124, y0 + 144):
        pts = []
        for i in range(41):
            t = i / 40
            pts.append((x0 + 6 + t * (x1 - x0 - 12),
                        wy + 5 * math.sin(t * math.pi * 4)))
        d.line(pts, fill=SLATE, width=3, joint="curve")


def card(d, x0, y0, x1, y1, fill=WHITE):
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=INK, width=2)
    return x0 + 16, y0 + 14, x1 - 16, y1 - 14


def story_card(d, x0, y0, x1, y1, kicker_text, headline, deck, art=None):
    ix0, iy0, ix1, iy1 = card(d, x0, y0, x1, y1)
    ax0, ay0 = ix0, iy0
    text_x = ix0
    if art is not None:
        aw = 150
        art(d, ix0, iy0, ix0 + aw, iy1)
        text_x = ix0 + aw + 14
    y = kicker(d, text_x, iy0, kicker_text, size=15)
    hf = font(SERIF, 24)
    lines = wrap(d, headline, hf, ix1 - text_x)
    hf = fit_lines(d, lines, hf, ix1 - text_x)
    y = text_block(d, text_x, y, lines, hf, INK, leading=28)
    y += 6
    df = font(SANS, 16)
    dlines = wrap(d, deck, df, ix1 - text_x)
    text_block(d, text_x, y, dlines, df, (58, 66, 80), leading=20)


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 26  # margin

    # top rule + masthead
    d.rectangle([0, 0, W, 7], fill=RED)
    mf = font(SERIF, 84)
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=mf)) / 2, 16), title,
           font=mf, fill=INK)
    df = font(SANS_B, 24)
    date = "F R I D A Y ,  2 0  N O V E M B E R  2 0 2 6"
    d.text(((W - d.textlength(date, font=df)) / 2, 112), date,
           font=df, fill=RED)
    d.line([(m, 146), (W - m, 146)], fill=INK, width=2)

    # ---- lead story: Cyclone Akvan ----
    lx0, ly0, lx1, ly1 = m, 158, W - m, 428
    d.rectangle([lx0, ly0, lx1, ly1], fill=WHITE, outline=INK, width=2)
    cyclone_art(d, lx0 + 2, ly0 + 2, lx0 + 372, ly1 - 2)
    tx = lx0 + 392
    y = kicker(d, tx, ly0 + 16, "INDIA  •  CYCLONE AKVAN  —  LANDFALL TODAY",
               size=19)
    hf = font(SERIF, 47)
    head = ["AKVAN SLAMS INTO", "THE ODISHA COAST"]
    hf = fit_lines(d, head, hf, lx1 - 16 - tx)
    y = text_block(d, tx, y, head, hf, INK, leading=52)
    y += 8
    df2 = font(SANS, 20)
    deck = ("Severe Cyclonic Storm Akvan crosses the coast near "
            "Gopalpur around noon, with winds of 90–100 km/h gusting "
            "to 110. More than 105,000 people have been moved to "
            "shelters.")
    y = text_block(d, tx, y, wrap(d, deck, df2, lx1 - 16 - tx),
                   df2, (58, 66, 80), leading=25)
    # fact chips
    chips = ["105,304 EVACUATED", "110 KM/H GUSTS", "11 DISTRICTS ON RED ALERT"]
    cy = ly1 - 46
    cx = tx
    cf = font(SANS_B, 15)
    for chip in chips:
        wch = d.textlength(chip, font=cf) + 18
        d.rounded_rectangle([cx, cy, cx + wch, cy + 30], radius=5,
                            fill=INK)
        d.text((cx + 9, cy + 7), chip, font=cf, fill=WHITE)
        cx += wch + 10

    # ---- row 2: COP31 + Gulf ----
    ry0, ry1 = 442, 668
    cw = (W - 2 * m - 14) // 2
    story_card(d, m, ry0, m + cw, ry1,
               "CLIMATE  •  COP31, ANTALYA",
               "COP31'S FINAL DAY: NO FOSSIL FUELS IN THE DRAFT",
               "Negotiators race the Friday deadline after the new text "
               "drops every mention of coal, oil and gas.",
               art=globe_art)
    story_card(d, m + cw + 14, ry0, W - m, ry1,
               "THE GULF  •  IRAN–U.S.",
               "IRAN CLAIMS U.S. RADAR HIT IN BAHRAIN",
               "Tehran says it destroyed an early-warning radar; the U.S. "
               "says its drones were shot down. Fourteen Hormuz shipping "
               "attacks this month.",
               art=radar_art)

    # ---- row 3: cricket + Senegal ----
    ry0, ry1 = 682, 908
    story_card(d, m, ry0, m + cw, ry1,
               "SPORT  •  WELLINGTON",
               "NICHOLLS 146* AS NEW ZEALAND REACH 317–6",
               "Glenn Phillips makes 118 in a 216-run stand — the first "
               "man to score centuries in all formats against India in a "
               "calendar year.",
               art=cricket_art)
    story_card(d, m + cw + 14, ry0, W - m, ry1,
               "AFRICA  •  THE ATLANTIC ROUTE",
               "DOZENS STILL MISSING OFF SENEGAL",
               "Boat with about 100 migrants capsized off Yenne; four "
               "bodies found. The second wreck there in two weeks.",
               art=boat_art)

    # ---- numbers strip ----
    ny0, ny1 = 922, 978
    d.rectangle([m, ny0, W - m, ny1], fill=INK)
    stats = [("105,304", "evacuated in Odisha"),
             ("110 km/h", "Akvan's gusts"),
             ("317–6", "New Zealand at lunch"),
             ("14", "Hormuz attacks in Nov")]
    seg = (W - 2 * m) / 4
    nf = font(SERIF, 26)
    lf = font(SANS, 14)
    for i, (num, label) in enumerate(stats):
        cx = m + seg * i + seg / 2
        d.text((cx - d.textlength(num, font=nf) / 2, ny0 + 6), num,
               font=nf, fill=WHITE)
        d.text((cx - d.textlength(label, font=lf) / 2, ny0 + 38), label,
               font=lf, fill=(200, 210, 222))

    # ---- footer ----
    d.rectangle([0, 986, W, H], fill=RED)
    ff = font(SANS_B, 17)
    foot = "WORLD  •  POLITICS  •  CLIMATE  •  SPORT   —   FRIDAY 20 NOVEMBER 2026"
    d.text(((W - d.textlength(foot, font=ff)) / 2, 999), foot,
           font=ff, fill=WHITE)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print(out, os.path.getsize(out), "bytes", img.size)


if __name__ == "__main__":
    draw()
