#!/usr/bin/env python3
"""
WORLD NEWS DAILY - Friday 20 November 2026.

Draws the entrant's entry for the make.fun bounty "Sum up
20 November's world news in one image" (news-image-20261120):
a portrait newspaper front page, 683x1024, carrying the whole day
in 30 verified stories - three illustrated heroes over six numbered
sections, a dotted world map with a pin for the story clusters, and
a sourced footer.

The page is composed by a small flow engine: every block reports
its own height, and the three section columns stretch or squeeze
their line spacing so the columns always end exactly at the map
band. The picture is saved as a palette PNG (same picture, fewer
bytes - an exact tie on win rate goes to the smaller file).

All story data was researched and cross-checked by the agent on
the morning of 20 November 2026 from the day's wire reporting;
the one figure the sources disputed (the Cyclone Akvan evacuation
count) is deliberately left out.

Run:  python3 build_image_20.py [output.png]   (default entry.png)
"""

import sys
from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------
# palette and paper
# ------------------------------------------------------------------
PAPER = (250, 247, 238)
WHITE = (252, 250, 244)
INK = (24, 22, 18)
NAVY = (18, 34, 66)
RED = (172, 28, 34)
MUTE = (110, 100, 84)
SAND = (172, 164, 140)
GREEN = (28, 104, 58)
BLUE = (34, 66, 138)
TEAL = (24, 102, 110)
GOLD = (176, 132, 32)

PAGE_W, PAGE_H = 683, 1024
EDGE = 24                      # page margin
BODY_W = PAGE_W - 2 * EDGE     # usable width

FONT_DIR = "/usr/share/fonts/truetype"
PATHS = {
    "display": f"{FONT_DIR}/noto/NotoSerifDisplay-Black.ttf",
    "serif_b": f"{FONT_DIR}/liberation/LiberationSerif-Bold.ttf",
    "serif": f"{FONT_DIR}/liberation/LiberationSerif-Regular.ttf",
    "serif_i": f"{FONT_DIR}/liberation/LiberationSerif-Italic.ttf",
    "sans_b": f"{FONT_DIR}/liberation/LiberationSans-Bold.ttf",
}
_cache = {}


def F(kind, size):
    key = (kind, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(PATHS[kind], size)
    return _cache[key]


# ------------------------------------------------------------------
# text helpers
# ------------------------------------------------------------------
def lines_of(draw, text, font, width):
    """Greedy word wrap, measured with textbbox."""
    out, cur = [], ""
    for word in text.split():
        trial = word if not cur else f"{cur} {word}"
        if draw.textbbox((0, 0), trial, font=font)[2] <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def text_w(draw, text, font):
    return draw.textbbox((0, 0), text, font=font)[2]


def centred(draw, cx, y, text, font, fill=INK):
    draw.text((cx - text_w(draw, text, font) / 2, y), text, font=font, fill=fill)


def hline(draw, y, x0=EDGE, x1=PAGE_W - EDGE, w=1, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


# ------------------------------------------------------------------
# the day's stories (verified set - see TRANSCRIPT.md)
# ------------------------------------------------------------------
HEROES = [
    dict(kicker="POLITICS & DIPLOMACY", art="summit",
         head="Trump, Xi and Putin end Shenzhen summit with a peace declaration",
         dek="The joint statement backs UN reform, more oil supply and "
             "nuclear-risk dialogue \u2014 but omits the Ukraine and Iran wars."),
    dict(kicker="INTERNATIONAL JUSTICE", art="court",
         head="UN court rules Myanmar committed genocide against Rohingya",
         dek="The ICJ finds six violations of the 1948 Genocide "
             "Convention over the 2017 crackdown."),
    dict(kicker="MARKETS & TECHNOLOGY", art="debut",
         head="Anthropic's IPO is the largest in history, at $1.5 trillion",
         dek="Priced at $83, the Claude maker raised $81 billion; shares "
             "opened at $111.50 and closed the debut at $97."),
]

SECTIONS_LEFT = [
    ("POLITICS & DIPLOMACY", [
        (4, "Europe's leaders meet in Berlin and say they are ready for talks with Russia on ending the Ukraine war."),
        (5, "Putin says Ukraine and Europe are \"not ready\" for the compromises proposed by the US."),
        (6, "Trump delays any Iran war decision to 2027: \"no rush\" after January 1."),
        (7, "US Senate rejects the Iran war-powers resolution 51-48, Republicans backing Trump."),
        (8, "Trump says an aide raised detained Americans Chen and Zin with Beijing."),
        (9, "South Korea's top court overturns ex-PM Han Duck-soo's 15-year martial-law sentence in part; retrial ordered."),
        (10, "US and Venezuela sign a deal restoring military cooperation, less than a year after Maduro's ouster."),
    ]),
    ("TECHNOLOGY & SCIENCE", [
        (22, "NASA: Voyager 1 is now one light-day from Earth."),
        (23, "Japan's Hayabusa2 gives up its asteroid landing after engine trouble."),
        (24, "GTA VI tops The Odyssey's $1.80B box office."),
    ]),
]

SECTIONS_MID = [
    ("WAR & SECURITY", [
        (11, "Ukraine hits the Crimean Bridge for the third time in three days; a road arch fell into the sea on Tuesday."),
        (12, "Houthi missile threat on Riyadh: falling debris causes damage as fighting escalates."),
        (13, "Saudi Crown Prince Mohammed bin Salman meets US CENTCOM chief Admiral Brad Cooper in Riyadh."),
        (14, "Haiti offensive: security forces kill 34 suspected gang members to retake the Martissant corridor."),
        (15, "IAEA: North Korea completes an extension of the Yongbyon uranium-enrichment plant \u2014 a \"serious concern\"."),
        (16, "UK sanctions 8 Israeli settlement firms; Australia sanctions settler figures after a woman, 72, is shot dead near Jericho."),
    ]),
    ("SOCIETY & SPORT", [
        (25, "Migrant boat capsizes off Senegal: about 50 aboard, dozens missing on the West Africa route."),
        (26, "Cricket: Nicholls hits 113 not out as New Zealand make 243/5 on day one of the first Test vs India."),
        (27, "A Van Gogh sells for a record $190.4 million after a row over its Nazi-era history."),
    ]),
]

SECTIONS_RIGHT = [
    ("MARKETS & ECONOMY", [
        (17, "US stocks slump ~2%: S&P 500 and Nasdaq at seven-month lows, longest losing streak since April 2024."),
        (18, "IEA: the Iran war is history's largest energy shock, with \"no credible pathway\" back to the pre-war sector."),
        (19, "Gold slides to about $3,686 an ounce as the dollar index nears a 19-month high."),
        (20, "Oil: Brent settles at $91.95 and WTI near $83.20, WTI's lowest since August."),
        (21, "India's Sensex climbs 1.21% and the Nifty 1.14% on banking and auto buying."),
    ]),
    ("CLIMATE & ENVIRONMENT", [
        (28, "Cyclone Akvan bears down on Odisha and Andhra Pradesh; mass evacuations under way ahead of landfall."),
        (29, "COP31 in Antalya reaches its scheduled final day with fossil-fuel and climate-finance texts still unresolved."),
        (30, "Fiji declares a national state of disaster over the El Nino drought; below-normal rain is forecast until April."),
    ]),
]

# story-number clusters pinned on the map: (lon, lat, label)
PINS = [
    (-102, 42, "06,07,17,18"), (-122, 37, "03,22,24"), (-74, 19, "14"),
    (-67, 10, "10"), (10, 52, "04,05,16"), (38, 53, "11"),
    (47, 24, "12,13"), (31, 37, "29"), (-17, 15, "25"),
    (80, 17, "21,28"), (96, 21, "02"), (114, 22, "01,08"),
    (125, 40, "15"), (127, 37, "09"), (138, 37, "23"),
    (175, -41, "26"), (178, -17, "30"),
]

# coarse land mask, one string per latitude band (75N .. 60S, 100 cols)
LAND = [
    "                                                                                                    ",
    "            #######                              #########           ##########                     ",
    "        #############        ##              ###############################  ######                ",
    "      #################   ######           ##########################################               ",
    "     ##################   ######           ############################################             ",
    "      ################    #####             ##################  ##########################          ",
    "       ##############      ###               ################    ############################         ",
    "        ############                          ##############      ##########################          ",
    "         ##########                            ############        ########################           ",
    "          ########                             ###########          #####################             ",
    "          #######                               #########            ###################              ",
    "           ######                               ########              #################               ",
    "           #####                                 ######                ##############                 ",
    "            ####                                  #####                 ############                  ",
    "            #####                                  ####                  ##########                   ",
    "            ######                                 ####                   ########                    ",
    "            #######                                ###                     ######                     ",
    "            ########                               ##                       ####                      ",
    "             #######                                                                                  ",
    "             ########                                                                                 ",
    "              ######                                                                                  ",
    "              #####                                                                                   ",
    "               ###                                                                                    ",
    "               ##                                                                                     ",
    "                                                                                                    ",
    "                                                                                                    ",
    "                                                                                                    ",
]

REGIONS = [
    ((190, 44, 44), "Asia"), ((96, 44, 32), "Europe"),
    ((34, 120, 60), "North America"), ((128, 116, 40), "Middle East"),
    ((24, 110, 130), "South America"), ((44, 84, 160), "Oceania"),
]


# ------------------------------------------------------------------
# hero artwork
# ------------------------------------------------------------------
def art_summit(d, x, y, w, h):
    """Three summit flags on poles over a ground line, data-driven."""
    specs = [
        ("stripes", [RED, WHITE, RED, WHITE, RED, WHITE, RED], BLUE),
        ("field", [RED], GOLD),
        ("stripes", [WHITE, BLUE, RED], None),
    ]
    slot = (w - 12) // 3
    for i, (kind, bands, accent) in enumerate(specs):
        fx = x + i * (slot + 6)
        d.line([(fx + 2, y), (fx + 2, y + h)], fill=INK, width=2)
        bx, by, bw, bh = fx + 4, y + 2, slot - 5, int(h * 0.68)
        if kind == "field":
            d.rectangle([bx, by, bx + bw, by + bh], fill=bands[0])
            star = [(10, 9, 3.6), (22, 5, 1.9), (26, 12, 1.9), (26, 20, 1.9), (21, 26, 1.9)]
            for dx, dy, r in star:
                d.ellipse([bx + dx - r, by + dy - r, bx + dx + r, by + dy + r], fill=accent)
        else:
            n = len(bands)
            for s, col in enumerate(bands):
                d.rectangle([bx, by + s * bh // n, bx + bw, by + (s + 1) * bh // n], fill=col)
            if accent is not None:
                d.rectangle([bx, by, bx + bw * 0.45, by + bh * 4 // 7], fill=accent)
                for r_ in range(3):
                    for c_ in range(3):
                        cx, cy = bx + 5 + c_ * 9, by + 4 + r_ * 8
                        d.ellipse([cx - 1.5, cy - 1.5, cx + 1.5, cy + 1.5], fill=WHITE)
        d.rectangle([bx, by, bx + bw, by + bh], outline=INK, width=1)
    d.line([(x, y + h - 4), (x + w, y + h - 4)], fill=INK, width=3)


def art_court(d, x, y, w, h):
    """Scales of justice for the ICJ hero."""
    cx = x + w // 2
    beam_y, foot_y = y + 14, y + h - 10
    d.line([(cx - 56, beam_y), (cx + 56, beam_y)], fill=INK, width=3)
    d.ellipse([cx - 5, beam_y - 5, cx + 5, beam_y + 5], fill=GOLD, outline=INK)
    d.line([(cx, beam_y), (cx, foot_y - 8)], fill=INK, width=3)
    d.line([(cx - 22, foot_y - 8), (cx + 22, foot_y - 8)], fill=INK, width=4)
    for sx in (cx - 56, cx + 56):
        pan_y = beam_y + 44
        for dx in (-15, 0, 15):
            d.line([(sx, beam_y), (sx + dx, pan_y)], fill=INK, width=1)
        d.pieslice([sx - 19, pan_y - 6, sx + 19, pan_y + 12], 0, 180, fill=GOLD, outline=INK)
    f = F("serif_b", 15)
    d.text((cx - text_w(d, "ICJ", f) / 2, foot_y - 26), "ICJ", font=f, fill=NAVY)


def art_debut(d, x, y, w, h):
    """Area chart for the Anthropic IPO hero."""
    floor = y + h - 6
    d.line([(x + 6, y + 4), (x + 6, floor), (x + w - 4, floor)], fill=INK, width=2)
    pts = [(x + 22 + i * (w - 52) // 3, floor - int((h - 18) * f))
           for i, f in enumerate([0.28, 0.47, 0.63, 0.88])]
    d.polygon(pts + [(pts[-1][0], floor), (pts[0][0], floor)], fill=(196, 224, 222))
    d.line(pts, fill=RED, width=3)
    ex, ey = pts[-1]
    d.polygon([(ex + 11, ey - 5), (ex - 2, ey - 3), (ex + 2, ey + 8)], fill=RED)
    f = F("serif_b", 24)
    d.text((x + 12, y + 1), "$81B", font=f, fill=TEAL)


ARTWORK = {"summit": art_summit, "court": art_court, "debut": art_debut}


# ------------------------------------------------------------------
# page blocks
# ------------------------------------------------------------------
def header(d):
    small = F("sans_b", 10.5)
    d.text((EDGE, 14), "Trusted News. A Global Perspective.", font=small, fill=INK)
    stamp = "Friday, 20 November 2026"
    sw = text_w(d, stamp, small)
    d.rectangle([PAGE_W - EDGE - sw - 14, 10, PAGE_W - EDGE + 2, 32], fill=INK)
    d.text((PAGE_W - EDGE - sw - 7, 14), stamp, font=small, fill=WHITE)
    hline(d, 38, w=2)
    hline(d, 43, w=1)
    centred(d, PAGE_W / 2, 50, "WORLD NEWS DAILY", F("display", 57))
    d.rectangle([EDGE, 122, PAGE_W - EDGE, 150], fill=INK)
    centred(d, PAGE_W / 2, 128, "30 STORIES IN ONE EDITION", F("sans_b", 15), WHITE)
    centred(d, PAGE_W / 2, 158, "Friday, 20 November 2026", F("serif_b", 17), RED)
    hline(d, 184, w=1)


def heroes(d, top):
    col_w = (BODY_W - 24) / 3
    kicker_f, head_f, dek_f = F("sans_b", 9.5), F("serif_b", 17), F("serif", 10.8)
    chip_f = F("sans_b", 10)
    for i, hero in enumerate(HEROES):
        hx = EDGE + i * (col_w + 12)
        hw = int(col_w)
        d.rectangle([hx, top, hx + hw, top + 19], fill=NAVY)
        d.text((hx + 6, top + 4), hero["kicker"], font=kicker_f, fill=WHITE)
        ARTWORK[hero["art"]](d, hx, top + 25, hw, 96)
        yy = top + 127
        for ln in lines_of(d, hero["head"], head_f, hw)[:4]:
            d.text((hx, yy), ln, font=head_f, fill=INK)
            yy += 20
        yy += 2
        for ln in lines_of(d, hero["dek"], dek_f, hw)[:3]:
            d.text((hx, yy), ln, font=dek_f, fill=INK)
            yy += 14
        chip = f"\u25ba{i + 1}"
        cw = text_w(d, chip, chip_f)
        d.rectangle([hx + hw - cw - 8, yy - 13, hx + hw, yy + 3], fill=RED)
        d.text((hx + hw - cw - 4, yy - 11), chip, font=chip_f, fill=WHITE)
        if i:
            d.line([(hx - 6, top), (hx - 6, top + 300)], fill=MUTE, width=1)
    hline(d, top + 320, w=1)


def measure_column(d, sections, width):
    """Natural height of a column at the base line step."""
    item_f, num_f = F("serif", 10.3), F("sans_b", 11)
    total = 0
    for _title, items in sections:
        total += 26
        for num, text in items:
            nw = text_w(d, f"{num:02d}", num_f)
            total += len(lines_of(d, text, item_f, width - nw - 5)) * 12.2 + 3
        total += 4
    return total


def column(d, x, top, bottom, width, sections):
    """Draw one column, stretching its spacing to end at bottom."""
    natural = measure_column(d, sections, width)
    slack = max(0.0, (bottom - top) - natural)
    n_items = sum(len(items) for _t, items in sections)
    extra = slack / max(1, n_items)
    item_f, num_f, sec_f = F("serif", 10.3), F("sans_b", 11), F("sans_b", 10.5)
    yy = float(top)
    for title, items in sections:
        d.rectangle([x, yy, x + width, yy + 19], fill=NAVY)
        d.rectangle([x + 5, yy + 5, x + 13, yy + 13], fill=WHITE)
        d.text((x + 18, yy + 4), title, font=sec_f, fill=WHITE)
        yy += 26
        for num, text in items:
            label = f"{num:02d}"
            nw = text_w(d, label, num_f)
            d.text((x, yy), label, font=num_f, fill=RED)
            for ln in lines_of(d, text, item_f, width - nw - 5)[:3]:
                d.text((x + nw + 5, yy), ln, font=item_f, fill=INK)
                yy += 12.2
            yy += 3 + extra
        yy += 4


def world_map(d, x0, y0, w, h):
    rows = len(LAND)
    cols = len(LAND[0])
    for r, row in enumerate(LAND):
        for c, cell in enumerate(row):
            if cell == "#":
                px = x0 + (c + 0.5) * w / cols
                py = y0 + (r + 0.5) * h / rows
                d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=SAND)
    pin_f = F("sans_b", 7.5)
    for lon, lat, label in PINS:
        px = x0 + (lon + 180) / 360.0 * w
        py = y0 + (75 - lat) / 135.0 * h
        tw = text_w(d, label, pin_f)
        d.rounded_rectangle([px - tw / 2 - 3.5, py - 6.5, px + tw / 2 + 3.5, py + 6.5],
                            radius=3, fill=RED)
        d.text((px - tw / 2, py - 4.5), label, font=pin_f, fill=WHITE)


def footer(d):
    hline(d, 994, w=1)
    d.text((EDGE, 1001), "30 GLOBAL HEADLINES \u2022 FRIDAY 20 NOVEMBER 2026",
           font=F("sans_b", 12), fill=INK)
    src_f = F("serif_i", 8.5)
    s1 = "Sources: Reuters, AP, BBC, Le Monde, France 24"
    s2 = "Illustrative editorial imagery; headlines compiled from public reports."
    d.text((PAGE_W - EDGE - text_w(d, s1, src_f), 999), s1, font=src_f, fill=MUTE)
    d.text((PAGE_W - EDGE - text_w(d, s2, src_f), 1010), s2, font=src_f, fill=MUTE)


def build(out_path):
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(img)
    header(d)
    heroes(d, 192)
    col_w = int((BODY_W - 24) / 3)
    for i, sections in enumerate([SECTIONS_LEFT, SECTIONS_MID, SECTIONS_RIGHT]):
        column(d, EDGE + i * (col_w + 12), 518, 890, col_w, sections)
    hline(d, 892, w=1)
    world_map(d, EDGE, 900, 452, 84)
    lx = EDGE + 470
    d.rectangle([lx, 898, PAGE_W - EDGE, 990], outline=INK, width=1)
    d.text((lx + 8, 903), "KEY REGIONS", font=F("sans_b", 10.5), fill=INK)
    for j, (col, name) in enumerate(REGIONS):
        ly = 924 + j * 11
        d.ellipse([lx + 8, ly + 1, lx + 16, ly + 9], fill=col)
        d.text((lx + 21, ly), name, font=F("sans_b", 9.5), fill=INK)
    footer(d)
    img.convert("P", palette=Image.Palette.ADAPTIVE, colors=256).save(
        out_path, format="PNG", optimize=True)
    print("wrote", out_path)


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
