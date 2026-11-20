#!/usr/bin/env python3
"""Render entry.png: THE DAILY ORBIT front page for Thursday 19 November 2026.

A single-image broadsheet summary of that day's world news, drawn entirely
with Pillow primitives (rules, columns, type and small line illustrations).
Run:  python3 draw.py   ->  writes entry.png beside this file (1024x1024).
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

W, H = 1024, 1024
PAPER = (249, 245, 234)
INK = (26, 26, 26)
GREY = (92, 88, 80)
LIGHT = (214, 206, 188)
NAVY = (31, 58, 95)
RED = (139, 30, 30)
TEAL = (24, 92, 88)
GOLD = (150, 118, 52)
WHITE = (255, 255, 255)
DARKBAR = (28, 30, 34)

FDIR = "/usr/share/fonts/truetype/noto"
def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)

SERIF_BLACK = "NotoSerif-Black.ttf"
SERIF_BOLD = "NotoSerif-Bold.ttf"
SERIF_REG = "NotoSerif-Regular.ttf"
SERIF_IT = "NotoSerif-Italic.ttf"
SANS_BOLD = "NotoSans-Bold.ttf"
SANS_REG = "NotoSans-Regular.ttf"
SANS_COND = "NotoSans-Condensed.ttf"
SANS_CONDB = "NotoSans-CondensedBold.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def tw(text, fnt):
    b = d.textbbox((0, 0), text, font=fnt)
    return b[2] - b[0]

def wrap(text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def para(x, y, text, fnt, maxw, leading, fill=INK):
    for ln in wrap(text, fnt, maxw):
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

def dropcap_para(x, y, text, fnt, maxw, leading):
    """Body copy with a broadsheet drop cap: the first letter is set large
    in navy and the first three lines wrap around it."""
    cap, rest = text[0], text[1:]
    cap_f = font(SERIF_BLACK, 34)
    cap_w = tw(cap, cap_f) + 7
    d.text((x, y - 3), cap, font=cap_f, fill=NAVY)
    lines, cur = [], ""
    for w_ in rest.split():
        limit = maxw - cap_w if len(lines) < 3 else maxw
        t = (cur + " " + w_).strip()
        if tw(t, fnt) <= limit:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    for i, ln in enumerate(lines):
        d.text((x + cap_w if i < 3 else x, y), ln, font=fnt, fill=INK)
        y += leading
    return y

def centered(y, text, fnt, fill=INK):
    d.text(((W - tw(text, fnt)) / 2, y), text, font=fnt, fill=fill)

def hline(x0, x1, y, fill=INK, wd=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=wd)

def kicker(x, y, text, fill=RED):
    d.text((x, y), text, font=font(SANS_CONDB, 12), fill=fill)

# ---------------------------------------------------------------- folio bar
MX = 30
f_small = font(SANS_REG, 11)
d.text((MX, 14), "Vol. CCXXVI  ·  No. 321", font=f_small, fill=GREY)
centered(14, "Independent · World Edition · Late City Final", f_small)
r = "Price: One Day's News"
d.text((W - MX - tw(r, f_small), 14), r, font=f_small, fill=GREY)
hline(MX, W - MX, 34, INK, 1)

# ---------------------------------------------------------------- masthead
centered(42, "THE DAILY ORBIT", font(SERIF_BLACK, 74))
hline(MX, W - MX, 128, INK, 4)
hline(MX, W - MX, 134, INK, 1)

# ---------------------------------------------------------------- date line
f_date = font(SERIF_BOLD, 17)
d.text((MX, 142), "Thursday, 19 November 2026", font=f_date, fill=INK)
mid = "THE WORLD IN ONE PAGE"
centered(144, mid, font(SANS_CONDB, 12))
wt = "Weather: Antalya 19°C · Shenzhen 24°C · New York 9°C"
d.text((W - MX - tw(wt, f_small), 144), wt, font=f_small, fill=GREY)
hline(MX, W - MX, 166, INK, 1)

# ---------------------------------------------------------------- ticker
d.rectangle([MX, 172, W - MX, 200], fill=DARKBAR)
ticker_a = "MARKETS   "
ticker_b = ("S&P 500  -2.0%  ·  NIKKEI  -4.7%  ·  OIL JUMPS ON HORMUZ NEWS"
            "   ·   ANTHROPIC IN RECORD MARKET DEBUT   ·   VAN GOGH  $190.4M")
f_tick = font(SANS_CONDB, 13)
tx = (W - tw(ticker_a + ticker_b, f_tick)) / 2
d.text((tx, 179), ticker_a, font=f_tick, fill=(232, 197, 120))
d.text((tx + tw(ticker_a, f_tick), 179), ticker_b, font=f_tick, fill=(245, 240, 225))

# ---------------------------------------------------------------- main story
y = 210
centered(y, "INTERNATIONAL COURT OF JUSTICE  ·  THE HAGUE", font(SANS_CONDB, 13))
# bump fill for kicker centered in red
d.rectangle([0, y, W, y + 16], fill=PAPER)
c = "INTERNATIONAL COURT OF JUSTICE  ·  THE HAGUE"
d.text(((W - tw(c, font(SANS_CONDB, 13))) / 2, y), c, font=font(SANS_CONDB, 13), fill=RED)
y += 22
f_main = font(SERIF_BLACK, 41)
for ln in ["World court finds Myanmar guilty",
           "of genocide against Rohingya"]:
    centered(y, ln, f_main)
    y += 46
y += 5
centered(y, "First genocide judgment against a State — refugees cheer the verdict",
         font(SERIF_IT, 16))
y += 24
centered(y, "By our Legal Correspondent, The Hague  ·  Photographs inside", font(SANS_REG, 11))
y += 18

# courthouse illustration: pediment, columns, scales (centred banner)
ix0, ix1 = MX + 330, W - MX - 330
# simple pediment + columns
d.ellipse([(ix0 + ix1) // 2 - 4, y + 6, (ix0 + ix1) // 2 + 4, y + 14], outline=GOLD, width=2)
d.polygon([(ix0, y + 18), (ix1, y + 18), ((ix0 + ix1) // 2, y)], fill=None, outline=NAVY)
d.line([(ix0, y + 18), (ix1, y + 18), ((ix0 + ix1) // 2, y), (ix0, y + 18)], fill=NAVY, width=2)
for i in range(5):
    cx = ix0 + 14 + i * ((ix1 - ix0 - 28) // 4)
    d.line([(cx, y + 23), (cx, y + 42)], fill=NAVY, width=3)
hline(ix0 - 6, ix1 + 6, y + 47, NAVY, 2)
# cheering figures either side (heads + raised arms)
for fx in (MX + 120, MX + 190, W - MX - 190, W - MX - 120):
    d.ellipse([fx - 5, y + 20, fx + 5, y + 30], outline=TEAL, width=2)
    d.line([(fx, y + 30), (fx, y + 44)], fill=TEAL, width=2)
    d.line([(fx, y + 34), (fx - 9, y + 22)], fill=TEAL, width=2)
    d.line([(fx, y + 34), (fx + 9, y + 22)], fill=TEAL, width=2)
y += 54

f_body = font(SERIF_REG, 13)
colw = (W - 2 * MX - 24) // 2
main_text = ("The International Court of Justice ruled that Myanmar committed genocide "
             "against the Rohingya — the first such judgment ever delivered against a State. "
             "The violence, judges found, met the legal test for genocide.")
main_text2 = ("In Cox's Bazar and in refugee communities worldwide, Rohingya families "
              "cheered a verdict awaited for years. Myanmar must now report to the court "
              "on reparations and guarantees against repetition.")
y1 = dropcap_para(MX, y, main_text, f_body, colw, 17)
y2 = dropcap_para(MX + colw + 24, y, main_text2, f_body, colw, 17)
y = max(y1, y2) + 6
hline(MX, W - MX, y, INK, 2)
y += 10

# ---------------------------------------------------------------- 3-col rows
COLW = (W - 2 * MX - 2 * 18) // 3
XS = [MX, MX + COLW + 18, MX + 2 * (COLW + 18)]

def article(idx, ytop, kick, head, head_size, body, icon=None):
    x = XS[idx]
    # short red accent tick above the kicker, a classic section marker
    d.rectangle([x, ytop - 6, x + 30, ytop - 3], fill=RED)
    kicker(x, ytop, kick)
    yy = ytop + 17
    for ln in wrap(head, font(SERIF_BOLD, head_size), COLW):
        d.text((x, yy), ln, font=font(SERIF_BOLD, head_size), fill=INK)
        yy += head_size + 2
    yy += 1
    if icon == "bridge":
        d.arc([x + 6, yy, x + 120, yy + 34], 180, 360, fill=NAVY, width=2)
        d.line([(x, yy + 24), (x + 126, yy + 24)], fill=NAVY, width=2)
        yy += 32
    elif icon == "ship":
        d.polygon([(x + 8, yy + 14), (x + 110, yy + 14), (x + 96, yy + 24), (x + 20, yy + 24)], outline=RED)
        d.rectangle([x + 44, yy + 2, x + 74, yy + 14], outline=RED)
        for wx in range(x + 2, x + 120, 16):
            d.arc([wx, yy + 26, wx + 12, yy + 33], 0, 180, fill=TEAL, width=2)
        yy += 36
    elif icon == "flags":
        for i, col in enumerate((RED, NAVY, TEAL)):
            fx = x + 10 + i * 42
            d.line([(fx, yy), (fx, yy + 24)], fill=INK, width=2)
            d.rectangle([fx, yy, fx + 26, yy + 12], outline=col, width=2)
            d.ellipse([fx + 9, yy + 3, fx + 17, yy + 11], fill=col)
        yy += 30
    yy = para(x, yy, body, font(SERIF_REG, 13), COLW, 17)
    return yy

row_top = y
ends = []
ends.append(article(0, row_top, "DIPLOMACY · SHENZHEN",
    "Trump, Xi and Putin hold first trilateral summit in Shenzhen", 18,
    "The three leaders signed a peace declaration and opened nuclear-risk talks. "
    "APEC adopted the Shenzhen Outlook, pledging calmer trade.",
    icon="flags"))
ends.append(article(1, row_top, "WAR IN UKRAINE",
    "Ukraine strikes Crimean Bridge for third time in four days", 18,
    "Kyiv struck the bridge for the third time in four days, tightening pressure "
    "on Russia's supply line. Putin vowed a harsher response.",
    icon="bridge"))
ends.append(article(2, row_top, "ENERGY · STRAIT OF HORMUZ",
    "Hormuz shock: tankers hit mines east of the strait", 18,
    "Tankers struck mines east of the Strait of Hormuz, jolting oil markets. The IEA "
    "called it the greatest threat ever to energy security.",
    icon="ship"))
y = max(ends) + 6
# vertical column rules for the row just drawn
for vx in (XS[1] - 9, XS[2] - 9):
    d.line([(vx, row_top), (vx, y - 6)], fill=LIGHT, width=1)
hline(MX, W - MX, y, INK, 1)
y += 8

row_top = y
ends = []
ends.append(article(0, row_top, "MARKETS",
    "Wall Street slides for fifth day on AI worries", 18,
    "The S&P 500 fell 2.0% in a fifth straight slide on AI worries, despite "
    "Anthropic's record debut. Tokyo's Nikkei plunged 4.7%."))
ends.append(article(1, row_top, "CLIMATE · COP31, ANTALYA",
    "COP31 deadlocked as draft drops fossil-fuel phase-out", 18,
    "Talks in Antalya stalled after the draft climate deal dropped any fossil-fuel "
    "phase-out. Negotiators worked into the night to save a text."))
ends.append(article(2, row_top, "SPACE",
    "Voyager 1 is now one light-day from Earth", 18,
    "NASA's Voyager 1 is now one light-day from Earth: its signal takes a full day to "
    "arrive. BepiColombo reached Mercury orbit the same day."))
y = max(ends) + 6
for vx in (XS[1] - 9, XS[2] - 9):
    d.line([(vx, row_top), (vx, y - 6)], fill=LIGHT, width=1)
hline(MX, W - MX, y, INK, 1)
y += 8

# chart + globe + star mini-icons row (thin decorative strip)
d.line([(MX + 30, y + 13), (MX + 80, y + 5), (MX + 130, y + 16), (MX + 180, y + 2)],
       fill=RED, width=2)
d.text((MX + 196, y + 3), "THE CHART: FIVE DAYS DOWN", font=font(SANS_CONDB, 11), fill=GREY)
d.ellipse([470, y, 496, y + 26], outline=TEAL, width=2)
d.arc([470, y + 6, 496, y + 20], 0, 360, fill=TEAL, width=1)
d.text((506, y + 6), "ANTALYA: NO DEAL YET", font=font(SANS_CONDB, 11), fill=GREY)
for sx, sy in ((770, y + 5), (800, y + 15), (835, y + 3), (868, y + 13), (905, y + 6)):
    d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)
y += 26
hline(MX, W - MX, y, INK, 1)
y += 8

row_top = y
ends = []
ends.append(article(0, row_top, "CULTURE · GAMES",
    "GTA VI launches to rave reviews after 13-year wait", 18,
    "Grand Theft Auto VI launched to rave reviews after a 13-year wait, with midnight "
    "queues worldwide. Critics praised its scale and story."))
ends.append(article(1, row_top, "WASHINGTON",
    "Democrats nominate Jeffries, set to be first Black Speaker", 18,
    "Democrats nominated Hakeem Jeffries, set to become the first Black Speaker of the "
    "US House. A historic changing of the guard."))
# briefs box in third column (box height measured from the wrapped text)
bx = XS[2]
briefs = [
    "Nearly 1 in 4 children live in conflict zones, Save the Children reports.",
    "Denmark approves the US Greenland defence deal 109-0 in parliament.",
    "Van Gogh sells for a record $190.4M at auction.",
    'Cambridge Word of the Year is "Human".',
]
f_brief = font(SERIF_REG, 11)
box_h = 24 + sum(len(wrap(b, f_brief, COLW - 18)) * 13 + 4 for b in briefs) + 4
d.rectangle([bx - 6, row_top - 4, bx + COLW + 6, row_top - 4 + box_h], fill=(238, 232, 214), outline=INK)
bh = "AROUND THE WORLD — IN BRIEF"
d.text((bx + (COLW - tw(bh, font(SANS_CONDB, 12))) / 2, row_top + 2), bh,
       font=font(SANS_CONDB, 12), fill=NAVY)
hline(bx + 2, bx + COLW - 2, row_top + 19, NAVY, 1)
by = row_top + 24
for b in briefs:
    d.text((bx + 2, by), "•", font=font(SERIF_BOLD, 12), fill=RED)
    by = para(bx + 16, by, b, f_brief, COLW - 18, 13) + 4
ends.append(by)
y = max(ends) + 6
for vx in (XS[1] - 9,):
    d.line([(vx, row_top), (vx, y - 6)], fill=LIGHT, width=1)

# ---------------------------------------------------------------- footer
hline(MX, W - MX, 972, INK, 3)
hline(MX, W - MX, 978, INK, 1)
f_foot = font(SANS_REG, 11)
d.text((MX, 986), "Continued inside: Summit text p.4 · Markets p.18 · Sport p.24", font=f_foot, fill=GREY)
pg = "Page 1 of 1 — The whole day, on one page"
d.text((W - MX - tw(pg, f_foot), 986), pg, font=f_foot, fill=GREY)
d.text((MX, 1002), "THE DAILY ORBIT — Thursday, 19 November 2026", font=font(SANS_CONDB, 11), fill=INK)

print("content ends at y =", y, "(footer rule at 972)")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("wrote", out, os.path.getsize(out), "bytes")
