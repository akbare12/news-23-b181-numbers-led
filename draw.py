#!/usr/bin/env python3
"""news-23 b181 numbers-led: THE WORLD TODAY, Monday 23 November 2026.
Draws a 1024x1024 front page: big number grid first, then masthead skeleton,
3 hero scenes, 10 cards, map + pins + ALSO list, DATE CHECK red box, footer.
All facts from the verified 23 Nov 2026 brief. Run: python3 draw.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(d, text, fnt, maxw, ellipsis=True):
    """Shorten text until it fits maxw (measured), with ellipsis if needed."""
    if d.textlength(text, font=fnt) <= maxw:
        return text
    if not ellipsis:
        return text
    while text and d.textlength(text + "\u2026", font=fnt) > maxw:
        text = text[:-1]
    return text + "\u2026"


def wrap(d, text, fnt, maxw, max_lines=2):
    """Greedy wrap into at most max_lines lines, last line ellipsised if cut."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= maxw:
            cur = trial
        elif len(lines) < max_lines - 1:
            if cur:
                lines.append(cur)
            cur = w
        else:
            cur = fit(d, trial, fnt, maxw)
            break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    return lines


img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

# palette
INK = (15, 15, 15)
RED = (178, 20, 20)
DARKRED = (140, 10, 10)
GREY = (90, 90, 90)
LGREY = (230, 230, 230)
BLUE = (18, 64, 120)
GOLD = (176, 128, 0)
GREEN = (20, 110, 50)
ORANGE = (210, 90, 0)
BLACK = (0, 0, 0)

f_mast = font(SERIF, 44)
f_date = font(SANS_B, 15)
f_kick = font(SANS, 14)
f_num = font(SANS_B, 30)
f_numlab = font(SANS_B, 11)
f_reg = font(SANS_B, 12)
f_hero_h = font(SANS_B, 19)
f_hero_b = font(SANS, 13)
f_hero_src = font(SANS, 10)
f_card_h = font(SANS_B, 12)
f_card_b = font(SANS, 11)
f_chip = font(SANS_B, 9)
f_also = font(SANS, 12)
f_map = font(SANS_B, 10)
f_dc_h = font(SANS_B, 15)
f_dc = font(SANS, 12)
f_foot = font(SANS, 10)

# ---------- masthead ----------
d.text((20, 8), "THE WORLD TODAY", font=f_mast, fill=INK)
d.text((W - 20 - d.textlength("MONDAY 23 NOVEMBER 2026", font=f_date), 22),
       "MONDAY 23 NOVEMBER 2026", font=f_date, fill=RED)
d.line([(20, 62), (W - 20, 62)], fill=INK, width=2)
d.text((20, 68), "One day of world news, in one page  \u2014  every number checked against the wires.",
       font=f_kick, fill=GREY)

# ---------- BIG NUMBER GRID (2 rows x 5) ----------
NUMBERS = [
    ("-3.3%", "KOSPI"),
    ("5.3", "US-CHINA GAP"),
    ("11,762", "EBOLA CASES, DRC"),
    ("10T won", "SEOUL FUND"),
    ("2%", "BILLIONAIRE TAX"),
    ("$450M", "SKUBAL, METS"),
    ("165", "MISSILES / WEEK"),
    ("12,000", "MANCHESTER"),
    ("264 kg", "LEBANON"),
    ("$107.3B", "ANTHROPIC IPO"),
]
gx, gy, cw, ch = 20, 92, 193, 52
for i, (num, lab) in enumerate(NUMBERS):
    x = gx + (i % 5) * (cw + 4)
    y = gy + (i // 5) * (ch + 4)
    d.rectangle([x, y, x + cw, y + ch], outline=LGREY, width=1)
    d.rectangle([x, y, x + cw, y + 3], fill=RED)
    d.text((x + 8, y + 7), num, font=f_num, fill=INK)
    d.text((x + 8, y + 34), lab, font=f_numlab, fill=GREY)
grid_bottom = gy + 2 * ch + 4

# ---------- region bar ----------
d.rectangle([20, grid_bottom + 6, W - 20, grid_bottom + 32], fill=INK)
regions = [("ASIA-PACIFIC", 7), ("AMERICAS", 8), ("MIDDLE EAST", 6),
           ("EUROPE", 5), ("AFRICA", 3), ("WORLD", 2)]
rx = 34
for name, n in regions:
    t = f"{name} {n}"
    d.text((rx, grid_bottom + 13), t, font=f_reg, fill="white")
    rx += d.textlength(t, font=f_reg) + 26
d.text((W - 20 - d.textlength("31 STORIES", font=f_reg), grid_bottom + 13),
       "31 STORIES", font=f_reg, fill=(255, 210, 0))
hero_top = grid_bottom + 40

# ---------- 3 hero scenes ----------
HEROES = [
    {
        "tag": "AI ROUT HITS ASIA",
        "body": "Kospi -3.3% closes 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
        "src": "SEOUL \u00b7 MARKETS",
        "kind": "kospi",
    },
    {
        "tag": "GUTERRES: REGULATE AI",
        "body": "Bridgetown summit, Barbados: 150 delegates back a risk framework. A blueprint, not a treaty.",
        "src": "BRIDGETOWN \u00b7 UNITED NATIONS",
        "kind": "guterres",
    },
    {
        "tag": "US LEAD AT RECORD LOW",
        "body": "US 78.9, China 73.6, gap 5.3 — narrowest since 2018. India 3rd, 40.5.",
        "src": "ASIA POWER INDEX 2026",
        "kind": "power",
    },
]
hw = 322
hx0 = 20
hy0 = hero_top
hh = 218
for i, hero in enumerate(HEROES):
    x = hx0 + i * (hw + 8)
    # scene area
    d.rectangle([x, hy0, x + hw, hy0 + 118], fill=(235, 238, 242))
    d.rectangle([x, hy0, x + hw, hy0 + 118], outline=LGREY, width=1)
    if hero["kind"] == "kospi":
        # skyline bars + falling chart line
        import random
        random.seed(7)
        bx = x + 14
        for _ in range(9):
            bh = random.randint(18, 52)
            d.rectangle([bx, hy0 + 108 - bh, bx + 22, hy0 + 108], fill=(150, 170, 195))
            bx += 30
        pts = [(x + 110, hy0 + 24), (x + 160, hy0 + 34), (x + 210, hy0 + 44),
               (x + 260, hy0 + 62), (x + 308, hy0 + 88)]
        d.line(pts, fill=ORANGE, width=4)
        d.text((x + 14, hy0 + 8), "-3.3%", font=font(SANS_B, 26), fill=RED)
    elif hero["kind"] == "guterres":
        # globe + flags
        cx, cy, r = x + hw // 2, hy0 + 52, 40
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 170, 210), outline=BLUE, width=2)
        d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=BLUE, width=1)
        d.line([(cx - r, cy), (cx + r, cy)], fill=BLUE, width=1)
        d.line([(cx - r + 8, cy - 22), (cx + r - 8, cy - 22)], fill=BLUE, width=1)
        d.line([(cx - r + 8, cy + 22), (cx + r - 8, cy + 22)], fill=BLUE, width=1)
        for j, col in enumerate([(0, 90, 160), (200, 40, 40), (20, 120, 60), (220, 160, 0)]):
            fx = x + 30 + j * 76
            d.rectangle([fx, hy0 + 100, fx + 34, hy0 + 112], fill=col)
    else:
        # power bars
        bars = [("US", 78.9, BLUE), ("CHINA", 73.6, RED), ("INDIA", 40.5, GREEN)]
        by = hy0 + 12
        for name, val, col in bars:
            bw = int(val / 100.0 * 190)
            d.text((x + 12, by), name, font=f_numlab, fill=INK)
            d.rectangle([x + 66, by + 1, x + 66 + bw, by + 15], fill=col)
            d.text((x + 66 + bw + 6, by), f"{val}", font=f_numlab, fill=INK)
            by += 28
        d.text((x + 12, by + 2), "GAP 5.3 \u2014 NARROWEST SINCE 2018", font=f_numlab, fill=RED)
    # headline + body + source below scene
    ty = hy0 + 126
    d.text((x, ty), hero["tag"], font=f_hero_h, fill=INK)
    blines = wrap(d, hero["body"], f_hero_b, hw, max_lines=2)
    byy = ty + 24
    for ln in blines:
        d.text((x, byy), ln, font=f_hero_b, fill=(40, 40, 40))
        byy += 16
    d.text((x, byy + 2), hero["src"], font=f_hero_src, fill=GREY)
hero_bottom = hy0 + hh

# ---------- 10 cards (2 rows x 5) ----------
CARDS = [
    ("Bessent demands Nvidia answers", "Treasury chief presses chipmaker.", "REPORTED"),
    ("FBI probes NCIC hack", "Police-database breach probed.", "REPORTED"),
    ("Trump: Iran strikes may resume", "Strikes may resume in New Year.", "REPORTED"),
    ("Nasdaq futures +3%", "Holiday week opens higher.", "REPORTED"),
    ("Skubal $450M to the Mets", "Nine years, largest pitcher deal ever.", "REPORTED"),
    ("Tom Jackson dies at 75", "NFL star and broadcaster.", "REPORTED"),
    ("States sue SpaceX", "AI safety claims challenged.", "REPORTED"),
    ("Anthropic IPO $107.3B", "Priced $83; debut close $97.17.", "REPORTED"),
    ("Poland: 3 Kh-101 crossed airspace", "Warsaw: missiles entered airspace.", "CLAIM"),
    ("Intel warns of nuclear satellite", "Russia said to plan orbital weapon.", "CLAIM"),
]
cy0 = hero_bottom + 8
cw2, ch2 = 193, 84
for i, (h, b, chip) in enumerate(CARDS):
    x = 20 + (i % 5) * (cw2 + 4)
    y = cy0 + (i // 5) * (ch2 + 4)
    d.rectangle([x, y, x + cw2, y + ch2], outline=LGREY, width=1)
    hl = wrap(d, h, f_card_h, cw2 - 12, max_lines=2)
    yy = y + 6
    for ln in hl:
        d.text((x + 6, yy), ln, font=f_card_h, fill=INK)
        yy += 14
    bl = wrap(d, b, f_card_b, cw2 - 12, max_lines=1)
    if bl:
        d.text((x + 6, yy + 1), bl[0], font=f_card_b, fill=(60, 60, 60))
        yy += 15
    chip_col = RED if chip == "CLAIM" else GREEN
    d.rectangle([x + 6, y + ch2 - 16, x + 6 + d.textlength(chip, font=f_chip) + 10,
                 y + ch2 - 5], fill=chip_col)
    d.text((x + 11, y + ch2 - 15), chip, font=f_chip, fill="white")
cards_bottom = cy0 + 2 * ch2 + 4

# ---------- map + ALSO ----------
my0 = cards_bottom + 8
map_w = 400
d.rectangle([20, my0, 20 + map_w, my0 + 196], fill=(222, 232, 240))
d.rectangle([20, my0, 20 + map_w, my0 + 196], outline=LGREY, width=1)
d.text((30, my0 + 6), "WORLD MAP \u2014 WHERE THE NEWS IS", font=f_map, fill=INK)
# stylised blobs
d.ellipse([40, my0 + 40, 190, my0 + 130], fill=(200, 215, 190))   # Americas
d.ellipse([215, my0 + 28, 405, my0 + 128], fill=(200, 215, 190))  # Eurasia
d.ellipse([255, my0 + 118, 345, my0 + 172], fill=(200, 215, 190))  # Africa
PINS = [
    (1, "Seoul", 345, 70), (2, "Bridgetown", 110, 118), (3, "Beijing", 365, 82),
    (4, "Paris", 255, 66), (5, "Manchester", 240, 50), (6, "Kyiv", 300, 58),
    (7, "Warsaw", 280, 44), (8, "Gaza", 298, 100), (9, "Beirut", 320, 84),
    (10, "Manama", 326, 106), (11, "Khartoum", 300, 132), (12, "Kinshasa", 284, 152),
    (13, "Dhaka", 372, 96),
]
for n, name, px, py in PINS:
    ax, ay = 20 + px, my0 + py
    d.ellipse([ax - 8, ay - 8, ax + 8, ay + 8], fill=RED, outline="white", width=1)
    d.text((ax - 3, ay - 7), str(n), font=font(SANS_B, 9), fill="white")
d.text((30, my0 + 170), "1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing \u00b7 4 Paris \u00b7 5 Manchester \u00b7 6 Kyiv",
       font=font(SANS, 10), fill=GREY)
d.text((30, my0 + 183), "7 Warsaw \u00b7 8 Gaza \u00b7 9 Beirut \u00b7 10 Manama \u00b7 11 Khartoum \u00b7 12 Kinshasa \u00b7 13 Dhaka",
       font=font(SANS, 10), fill=GREY)

# ALSO list (right of map)
ax0 = 20 + map_w + 16
d.text((ax0, my0), "ALSO ON MONDAY", font=font(SANS_B, 15), fill=INK)
d.line([(ax0, my0 + 20), (W - 20, my0 + 20)], fill=INK, width=1)
ALSO = [
    ("Paris: 100+ back 2% billionaire tax", False),
    ("Manchester: 12,000 cleared", False),
    ("Zelenskyy: 165 Russian missiles in a week", False),
    ("COP31: day after, Antalya pact out", False),
    ("Israel unity talks resume", False),
    ("Gaza: two killed in Israeli strike", False),
    ("West Bank settler attacks", False),
    ("Iran war: no deal in sight", False),
    ("Lebanon seizes 264 kg explosives", False),
    ("Bahrain: strike hits plant, 2 hurt", False),
    ("Benghazi: UN demands probe of attacks", True),
    ("Sudan: air defences down drones", True),
    ("DRC: fighting traps Ebola teams", False),
    ("Bangladesh: Hasina jailed if she returns", False),
    ("Seoul minister quits over AI exam chaos", False),
    ("SK Telecom -7.3%", False),
    ("China eases margin rules to 80%", False),
    ("Seoul readies 10T-won fund", False),
]
ay = my0 + 26
col_w = (W - 20 - ax0)
for text, claim in ALSO:
    line = fit(d, text, f_also, col_w - (58 if claim else 0))
    d.text((ax0, ay), "\u2022  " + line, font=f_also, fill=INK)
    if claim:
        tx = ax0 + 14 + d.textlength(line, font=f_also) + 4
        d.text((tx, ay), "[CLAIM]", font=f_chip, fill=RED)
    ay += 12
also_bottom = ay

# ---------- DATE CHECK ----------
dc_y = max(my0 + 200, also_bottom + 6)
d.rectangle([20, dc_y, W - 20, dc_y + 74], outline=RED, width=2)
d.rectangle([20, dc_y, W - 20, dc_y + 22], fill=RED)
d.text((30, dc_y + 3), "DATE CHECK \u2014 LEFT OUT: NOT 23 NOVEMBER", font=f_dc_h, fill="white")
d.text((30, dc_y + 28), "Democrats reach 258 (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo Isidro captured (22 Nov)",
       font=f_dc, fill=INK)
d.text((30, dc_y + 44), "EU\u2013Indonesia pact (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar ruling (19 Nov)",
       font=f_dc, fill=INK)
d.text((30, dc_y + 60), "NOT YET: Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating Ebola staff",
       font=f_dc, fill=GREY)

# ---------- footer ----------
fy = dc_y + 82
d.line([(20, fy), (W - 20, fy)], fill=LGREY, width=1)
d.text((20, fy + 6),
       "Sources: wires and official statements, 23 November 2026.  REPORTED = confirmed by wires.  CLAIM = one side's claim, not verified.",
       font=f_foot, fill=GREY)
d.text((20, fy + 20), "THE WORLD TODAY \u00b7 Monday 23 November 2026 \u00b7 31 stories, checked.",
       font=f_foot, fill=GREY)

img.save(OUT, "PNG")
print("saved", OUT, os.path.getsize(OUT), "bytes")
