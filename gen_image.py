#!/usr/bin/env python3
"""Field Notes - the world, 27 November 2026.

A reporter's field notebook summing up Friday 27 November 2026 in one
image: ruled paper, a red margin line, a taped-photo lead box for the
Kuwait drone strike, and dated entries grouped by continent - all 38
stories from the day's wires, each readable from the image alone.

Stdlib + PIL only. Deterministic: no clock, no randomness, no network.
Writes entry.png (1024x1024, <=1 MiB) to $MAKEFUN_OUTPUT_DIR or /output.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (248, 243, 230)
INK = (34, 37, 43)
INK_SOFT = (74, 76, 84)
RED = (178, 44, 36)
RULE = (196, 209, 226)
MARGIN_RED = (205, 92, 84)
TAPE = (226, 205, 150)
SKETCH_BG = (238, 231, 214)
SKETCH_INK = (90, 84, 70)
BOX_EDGE = (120, 110, 88)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def font(path, size):
    """Load a system TTF; fall back to Pillow's resizable built-in font
    so the program still renders in a sandbox without these files."""
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default(size=size)


F_MAST = font(SERIF_B, 54)
F_DATE = font(SANS_B, 17)
F_SUB = font(SERIF_I, 14)
F_LEAD_LBL = font(SANS_B, 13)
F_LEAD_H = font(SERIF_B, 25)
F_LEAD_S = font(SANS, 14)
F_SEC = font(SERIF_B, 15)
F_SEC_N = font(MONO, 11)
F_HEAD = font(SANS_B, 13)
F_SUM = font(SANS, 11)
F_CAP = font(SERIF_I, 12)
F_FOOT = font(SANS, 11)
F_FOOT_B = font(SANS_B, 11)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to max_w pixels; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_cloud(d, x, y, s, color):
    d.ellipse([x, y + 4 * s, x + 8 * s, y + 10 * s], outline=color, width=2)
    d.ellipse([x + 5 * s, y, x + 13 * s, y + 8 * s], outline=color, width=2)
    d.ellipse([x + 10 * s, y + 4 * s, x + 18 * s, y + 10 * s], outline=color, width=2)
    d.line([x + 2 * s, y + 10 * s, x + 16 * s, y + 10 * s], fill=color, width=2)
    for dx in (3, 8, 13):
        d.line([x + dx * s, y + 13 * s, x + (dx - 1) * s, y + 16 * s],
               fill=color, width=2)


def draw_ball(d, x, y, r, color):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], outline=color, width=2)
    d.polygon([(x + r, y + r - 3), (x + r + 3, y + r + 2),
               (x + r - 3, y + r + 2)], fill=color)
    d.arc([x, y, x + 2 * r, y + 2 * r], 200, 340, fill=color, width=2)
    d.arc([x, y, x + 2 * r, y + 2 * r], 20, 160, fill=color, width=2)


def draw_pawn(d, x, y, s, color):
    d.ellipse([x + 2 * s, y, x + 8 * s, y + 6 * s], fill=color)
    d.polygon([(x + 4 * s, y + 6 * s), (x + 6 * s, y + 6 * s),
               (x + 8 * s, y + 15 * s), (x + 2 * s, y + 15 * s)], fill=color)
    d.rectangle([x, y + 15 * s, x + 10 * s, y + 17 * s], fill=color)


def draw_crescent(d, x, y, s, color):
    d.pieslice([x, y, x + 14 * s, y + 16 * s], 60, 300, fill=color)
    d.pieslice([x + 5 * s, y + 2 * s, x + 16 * s, y + 15 * s], 60, 300,
               fill=PAPER)


def draw_tree(d, x, y, s, color):
    d.line([x + 5 * s, y + 8 * s, x + 5 * s, y + 17 * s], fill=color, width=2)
    d.line([x + 5 * s, y + 8 * s, x + s, y + 4 * s], fill=color, width=2)
    d.line([x + 5 * s, y + 8 * s, x + 9 * s, y + 4 * s], fill=color, width=2)
    d.line([x + 5 * s, y + 5 * s, x + 5 * s, y + s], fill=color, width=2)


def draw_mountain(d, x, y, s, color):
    d.polygon([(x, y + 16 * s), (x + 6 * s, y + 2 * s), (x + 9 * s, y + 8 * s),
               (x + 12 * s, y), (x + 18 * s, y + 16 * s)], outline=color, width=2)
    d.polygon([(x + 6 * s, y + 2 * s), (x + 4 * s, y + 6 * s),
               (x + 8 * s, y + 6 * s)], fill=color)


def draw_rugby(d, x, y, s, color):
    d.ellipse([x, y + 3 * s, x + 18 * s, y + 13 * s], outline=color, width=2)
    d.arc([x + 4 * s, y + 3 * s, x + 14 * s, y + 13 * s], 250, 290,
          fill=color, width=2)
    d.arc([x + 4 * s, y + 3 * s, x + 14 * s, y + 13 * s], 70, 110,
          fill=color, width=2)


def draw_planet(d, x, y, s, color):
    d.ellipse([x + 3 * s, y + 2 * s, x + 13 * s, y + 12 * s], outline=color,
              width=2)
    d.arc([x, y + 4 * s, x + 16 * s, y + 12 * s], 200, 340, fill=color, width=2)


ICONS = {
    "cloud": draw_cloud, "ball": draw_ball, "pawn": draw_pawn,
    "crescent": draw_crescent, "tree": draw_tree, "mountain": draw_mountain,
    "rugby": draw_rugby, "planet": draw_planet,
}

# (section, icon, [(headline, summary), ...])
SECTIONS = [
    ("NORTH AMERICA", "cloud", [
        ("Nor'easter batters US East Coast",
         "Thanksgiving storm cuts power to 250,000+ from N.J. to N.C."),
        ("Judge: FCC violated ABC's free speech",
         "Court rules against the regulator in ABC free-speech case."),
        ("Trump asks Putin to 'pull back'",
         "Trump urges Putin to ease aggression; Zelensky questions the focus."),
        ("Musk: two SpaceX shares for every US child",
         "Elon Musk says every American child will get two SpaceX shares."),
        ("US Army hails Iowa explosives disposal",
         "Army declares its Iowa lead-explosives detonation a success."),
        ("Apple enters the AI agent race",
         "Apple takes on OpenAI, Anthropic and Meta with its own AI agents."),
    ]),
    ("EUROPE", "ball", [
        ("UK net migration lowest since 1997",
         "Net migration falls to its lowest since 1997, bar the pandemic."),
        ("Depardieu to stand trial for alleged rape",
         "French court orders trial over alleged 2018 rape of an actress."),
        ("Diesel tanker capsizes off Ibiza, one dead",
         "Tanker carrying up to 7,000 tonnes of diesel sinks; one killed."),
        ("Lille hand Bayern first defeat, 2-1",
         "LOSC Lille end Bayern Munich's unbeaten season run, 2-1."),
        ("EU leaders weigh Ukraine aid",
         "Leaders discuss financial help for Ukraine amid security worries."),
        ("UK to pay fee to deliver EU deals",
         "Britain agrees a 'participation' fee to unlock EU agreements."),
        ("France's mainstream faces election debacle",
         "No clear candidate as the centre risks a presidential-vote rout."),
    ]),
    ("ASIA", "pawn", [
        ("Gukesh, Sindarov draw marathon Game 3",
         "World Chess Championship tied 1.5-1.5 after a marathon draw."),
        ("Kim vows more nuclear weapons",
         "Kim pledges a bigger arsenal, ignoring Trump's overture."),
        ("Fire at Bangkok oil refinery",
         "Blaze injures several; Bangchak shuts all refinery units."),
        ("India top court on PMLA attachments",
         "Top court: a judicial member must sit on attachment benches."),
        ("Top court quashes Anand Mohan release",
         "Top court voids ex-MP's release; calls Bihar's move illegal."),
        ("Cabinet backs Rs 11,000-cr equipment push",
         "India approves a scheme to boost home-grown equipment making."),
        ("Sri Lanka A reach Rising Stars final",
         "Sri Lanka A beat India A to reach the Asia Cup Rising Stars final."),
        ("India-China border 'generally stable'",
         "Beijing says the situation along the border areas remains stable."),
        ("Murder-accused politician's huge wedding",
         "Murder-accused politician hosts a 400,000-guest wedding."),
        ("Mecca-alliance talks open in Islamabad",
         "Pakistan, Saudi Arabia and Turkey meet, 27-28 November."),
    ]),
    ("MIDDLE EAST", "crescent", [
        ("Hamas weighs reply after Gaza killings",
         "Israel kills 10 people in Gaza; Hamas weighs its response."),
        ("Shin Bet 'tortures for confessions'",
         "Israeli rights group alleges torture as death penalty looms."),
        ("Iraq blocks two Kurdistan crossings",
         "Baghdad shuts border posts adjacent to Syria and Iran."),
    ]),
    ("AFRICA", "tree", [
        ("300+ Russians killed backing Mali junta",
         "Over 300 Russians dead as Moscow props up Mali's junta."),
        ("Ramaphosa wins impeachment-report bid",
         "South Africa's president overturns the impeachment report in court."),
        ("DRC Ebola passes 12,000 cases",
         "Epidemic crosses 12,000 confirmed cases and 5,900 deaths."),
    ]),
    ("SOUTH AMERICA", "mountain", [
        ("US, Qatar to help Venezuela clear arrears",
         "Bridge loans to clear regional development-bank debts."),
        ("Argentina Senate suspends 2027 primaries",
         "Congress also bars the central bank from funding the government."),
    ]),
    ("OCEANIA", "rugby", [
        ("NZ final results: slim coalition majority",
         "~400,000 special votes decide the final election outcome."),
        ("Barrett to captain All Blacks first time",
         "Geordie Barrett leads the side in Sunday's England rematch."),
        ("Sinner out of Australian Open 2027",
         "Jannik Sinner withdraws with a knee injury."),
        ("NZ v India 2nd Test begins",
         "Christchurch Test starts; Gurnoor Brar makes his debut."),
        ("Black Friday warning in New Zealand",
         "One in three retailers raising prices; half of deals no cheaper."),
    ]),
    ("SCIENCE", "planet", [
        ("Giant planet may lurk beyond Neptune",
         "New evidence raises the possibility of a distant giant planet."),
    ]),
]

COL1 = [0, 1]          # North America, Europe
COL1_ASIA = 6          # first 6 Asia stories go in column 1
COL2 = [3, 4, 5, 6, 7]  # Middle East, Africa, S. America, Oceania, Science


def draw_kuwait_sketch(d, x0, y0, x1, y1):
    """Pencil-sketch panel: Kuwait Towers, a drone, smoke."""
    d.rectangle([x0, y0, x1, y1], fill=SKETCH_BG, outline=BOX_EDGE, width=2)
    c = SKETCH_INK
    # ground + sea line
    d.line([x0 + 8, y1 - 26, x1 - 8, y1 - 26], fill=c, width=2)
    d.line([x0 + 8, y1 - 20, x1 - 8, y1 - 20], fill=(150, 142, 122), width=1)
    # main tower with two spheres
    tx = x0 + 62
    d.line([tx, y0 + 22, tx, y1 - 26], fill=c, width=3)
    d.ellipse([tx - 13, y0 + 30, tx + 13, y0 + 56], outline=c, width=2)
    d.ellipse([tx - 9, y0 + 62, tx + 9, y0 + 80], outline=c, width=2)
    # second tower
    tx2 = x0 + 108
    d.line([tx2, y0 + 44, tx2, y1 - 26], fill=c, width=3)
    d.ellipse([tx2 - 10, y0 + 50, tx2 + 10, y0 + 70], outline=c, width=2)
    # third slender tower
    tx3 = x0 + 148
    d.line([tx3, y0 + 14, tx3, y1 - 26], fill=c, width=2)
    # drone silhouette
    dx, dy = x0 + 168, y0 + 26
    d.ellipse([dx - 6, dy - 3, dx + 6, dy + 3], fill=c)
    d.line([dx - 14, dy - 6, dx + 14, dy - 6], fill=c, width=2)
    d.ellipse([dx - 20, dy - 9, dx - 10, dy - 3], outline=c, width=2)
    d.ellipse([dx + 10, dy - 9, dx + 20, dy - 3], outline=c, width=2)
    # smoke wisp from the ground
    d.arc([x0 + 176, y1 - 62, x0 + 206, y1 - 30], 180, 330, fill=c, width=2)
    d.arc([x0 + 184, y1 - 74, x0 + 210, y1 - 46], 200, 340, fill=c, width=2)
    # sun
    d.ellipse([x1 - 34, y0 + 10, x1 - 14, y0 + 30], outline=c, width=2)


def draw_section(d, x, y, name, icon, stories, width):
    """Draw one section header + its stories; return y below the block."""
    ICONS[icon](d, x, y - 1, 1, INK)
    d.text((x + 24, y - 3), name, font=F_SEC, fill=INK)
    n = "(%d)" % len(stories)
    d.text((x + 24 + d.textlength(name, font=F_SEC) + 8, y),
           n, font=F_SEC_N, fill=RED)
    y += 20
    d.line([x, y - 4, x + width, y - 4], fill=(150, 140, 120), width=1)
    for head, summ in stories:
        d.rectangle([x, y + 3, x + 5, y + 8], fill=RED)
        hl = wrap(d, head, F_HEAD, width - 14)
        d.text((x + 12, y), hl[0], font=F_HEAD, fill=INK)
        y += 14
        sl = wrap(d, summ, F_SUM, width - 12)
        d.text((x + 12, y), sl[0], font=F_SUM, fill=INK_SOFT)
        if len(sl) > 1:
            y += 13
            d.text((x + 12, y), sl[1], font=F_SUM, fill=INK_SOFT)
        y += 16
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")

    # faint ruled lines + red margin + punched holes (notebook paper)
    for yy in range(104, H - 8, 26):
        d.line([0, yy, W, yy], fill=RULE, width=1)
    d.line([72, 96, 72, H], fill=MARGIN_RED, width=2)
    for hy in (150, 400, 650, 900):
        d.ellipse([26, hy - 11, 48, hy + 11], fill=(255, 255, 255),
                  outline=(170, 160, 140), width=2)

    # ---- masthead ----
    d.text((88, 16), "FIELD NOTES", font=F_MAST, fill=INK)
    d.text((88, 76), "the world in one day  -  a reporter's notebook",
           font=F_SUB, fill=INK_SOFT)
    date = "FRIDAY 27 NOVEMBER 2026"
    dw = d.textlength(date, font=F_DATE)
    d.text((W - 48 - dw, 24), date, font=F_DATE, fill=RED)
    d.text((W - 48 - d.textlength("38 STORIES  -  6 CONTINENTS + SCIENCE",
                                  font=F_SUB), 76),
           "38 STORIES  -  6 CONTINENTS + SCIENCE", font=F_SUB, fill=INK_SOFT)
    d.line([88, 98, W - 48, 98], fill=INK, width=2)
    d.line([88, 102, W - 48, 102], fill=INK, width=1)

    # ---- lead story: taped-photo box ----
    bx0, by0, bx1, by1 = 88, 112, W - 48, 246
    d.rectangle([bx0, by0, bx1, by1], outline=BOX_EDGE, width=2)
    d.rectangle([bx0 + 2, by0 + 2, bx1 - 2, by1 - 2], outline=(150, 140, 120),
                width=1)
    draw_kuwait_sketch(d, bx0 + 10, by0 + 10, bx0 + 232, by1 - 28)
    d.text((bx0 + 10, by1 - 24), "Kuwait City - the strike site (sketch)",
           font=F_CAP, fill=INK_SOFT)
    # tape strips
    d.rectangle([bx0 + 4, by0 - 6, bx0 + 74, by0 + 12],
                fill=TAPE + (190,))
    d.rectangle([bx1 - 74, by0 - 6, bx1 - 4, by0 + 12], fill=TAPE + (190,))
    tx = bx0 + 248
    d.text((tx, by0 + 12), "★  LEAD STORY  —  KUWAIT", font=F_LEAD_LBL,
           fill=RED)
    head_lines = wrap(d, "Iranian drone strike kills two Italians in Kuwait",
                      F_LEAD_H, bx1 - tx - 14)
    hy = by0 + 34
    for ln in head_lines:
        d.text((tx, hy), ln, font=F_LEAD_H, fill=INK)
        hy += 30
    d.text((tx, hy + 2),
           "Tehran denies responsibility as the attack jolts the Gulf;",
           font=F_LEAD_S, fill=INK_SOFT)
    d.text((tx, hy + 21),
           "the day's top story - Middle East tensions spill into the Gulf.",
           font=F_LEAD_S, fill=INK_SOFT)

    # ---- body: two columns ----
    y0 = 262
    col_w1, col_w2 = 412, 452
    y = y0
    for si in COL1:
        name, icon, stories = SECTIONS[si]
        y = draw_section(d, 88, y, name, icon, stories, col_w1)
        y += 4
    asia = SECTIONS[2]
    y = draw_section(d, 88, y, asia[0], asia[1], asia[2][:COL1_ASIA], col_w1)
    end1 = y

    y = y0
    y = draw_section(d, 524, y, asia[0] + " (cont.)", asia[1],
                     asia[2][COL1_ASIA:], col_w2)
    y += 4
    for si in COL2:
        name, icon, stories = SECTIONS[si]
        y = draw_section(d, 524, y, name, icon, stories, col_w2)
        y += 4
    end2 = y

    # ---- footer ----
    fy = 994
    d.line([88, fy - 8, W - 48, fy - 8], fill=INK, width=1)
    d.text((88, fy + 2),
           "Filed from the notebook  -  all events of Friday 27 November 2026.",
           font=F_FOOT, fill=INK_SOFT)
    tag = "p. 27  •  FIELD NOTES"
    d.text((W - 48 - d.textlength(tag, font=F_FOOT_B), fy + 2), tag,
           font=F_FOOT_B, fill=RED)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, "PNG")
    print("wrote", path, img.size, os.path.getsize(path), "bytes",
          "col1_end", end1, "col2_end", end2)


if __name__ == "__main__":
    main()
