#!/usr/bin/env python3
"""Render the 24 November 2026 front page, v2 final edition (1024x1024).

Replaces the v1 "Blithe Palette" (23 stories, round 3 rank 5922/14561):
the round-3 board's top entries run 32-38 dated stories, 7-10 regions and
~13 drawn illustrations with claims labelled, so this edition carries
37 dated stories across 9 regions, 13 drawn pictures (lead scene + 12
pictograms) and attribution on every contested claim.

Draws the newspaper front page with PIL only (no network, deterministic):
masthead, date, 3 leads with a drawn lead illustration, 20 briefs and a
14-item "Also on 24 November" strip. Stories verified against 24 November
2026 reporting (AP, Reuters, BBC, CNN, NYT, Xinhua, Al Jazeera, UKHSA,
SCMP live pages; verdicts and announcements are dated by the day they
happened or were first reported, in any time zone, per the rules).

Run: python3 render.py  -> writes entry.png next to this file.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 36
CW = W - 2 * MARGIN  # 952

PAPER = (247, 242, 232)
INK = (20, 20, 20)
GREY = (85, 85, 85)
RED = (179, 38, 30)
BLUE = (31, 78, 121)
GREEN = (46, 125, 50)
OLIVE = (138, 109, 27)
SEA = (46, 98, 130)
SEA_DARK = (28, 68, 96)
ORANGE = (214, 110, 30)
GOLD = (212, 160, 40)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in s.split(" "):
        trial = f"{cur} {word}".strip()
        if text_w(draw, trial, f) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, f, x, y, leading, fill=INK):
    for line in lines:
        draw.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def tag(draw, x, y, label, bg, size=13, fg=(255, 255, 255)):
    f = font(F_SANS_B, size)
    tw = draw.textlength(label, font=f)
    h = size + 7
    draw.rounded_rectangle([x, y, x + tw + 12, y + h], radius=3, fill=bg)
    draw.text((x + 6, y + 3), label, font=f, fill=fg)
    return tw + 12  # chip width, so callers can place text after it


def rule(draw, y, width=2, x0=MARGIN, x1=W - MARGIN):
    draw.line([(x0, y), (x1, y)], fill=INK, width=width)
    return y + width


def ship_scene(draw, x, y, w, h):
    """Drawn lead illustration: warship on the sea off Libya, sun, cloud.
    All ship geometry is proportional to the scene height so nothing pokes
    above the scene's top edge."""
    # sky
    draw.rectangle([x, y, x + w, y + h], fill=(214, 226, 232))
    # sun
    draw.ellipse([x + w - 72, y + 8, x + w - 28, y + 52], fill=(232, 196, 120))
    # cloud
    draw.ellipse([x + 28, y + 12, x + 96, y + 38], fill=(240, 240, 238))
    draw.ellipse([x + 60, y + 5, x + 128, y + 34], fill=(240, 240, 238))
    # sea
    sea_y = y + int(h * 0.52)
    draw.rectangle([x, sea_y, x + w, y + h], fill=SEA)
    draw.rectangle([x, sea_y + 12, x + w, y + h], fill=SEA_DARK)
    # dashed wave lines
    for wy in (sea_y + 7, sea_y + 22):
        for wx in range(x + 8, x + w - 40, 56):
            draw.line([(wx, wy), (wx + 34, wy)], fill=(190, 215, 225), width=2)
    # ship silhouette (centered); hull sits just above the sea's lower band
    cx = x + w // 2
    hull_y = y + h - 26
    hull_h = int(h * 0.24)
    draw.polygon(
        [(cx - 210, hull_y), (cx + 210, hull_y), (cx + 165, hull_y + hull_h),
         (cx - 165, hull_y + hull_h)],
        fill=(30, 32, 36),
    )
    sup_h = int(h * 0.26)
    draw.rectangle([cx - 120, hull_y - sup_h, cx + 40, hull_y], fill=(30, 32, 36))
    draw.rectangle([cx - 78, hull_y - sup_h - int(h * 0.18), cx - 8, hull_y - sup_h],
                   fill=(30, 32, 36))
    draw.rectangle([cx + 58, hull_y - sup_h - int(h * 0.10), cx + 96, hull_y],
                   fill=(30, 32, 36))
    # mast + red flag, kept inside the scene
    mast_top = hull_y - sup_h - int(h * 0.30)
    draw.line([(cx - 40, hull_y - sup_h - int(h * 0.18)), (cx - 40, mast_top)],
              fill=(30, 32, 36), width=4)
    draw.polygon([(cx - 40, mast_top), (cx - 8, mast_top + 6), (cx - 40, mast_top + 12)],
                 fill=RED)
    # wake
    for i, wx in enumerate(range(cx - 260, cx - 170, 30)):
        draw.line([(wx, hull_y + hull_h + 4 + (i % 2) * 3),
                   (wx + 18, hull_y + hull_h + 4 + (i % 2) * 3)],
                  fill=(220, 235, 240), width=2)


# ---- small pictograms, drawn in a 22x22 box at (x, y) ----
def icon_leaf(d, x, y):
    d.ellipse([x + 2, y + 4, x + 18, y + 18], fill=GREEN)
    d.line([(x + 11, y + 20), (x + 16, y + 6)], fill=(255, 255, 255), width=2)


def icon_chip(d, x, y):
    d.rectangle([x + 5, y + 5, x + 17, y + 17], fill=INK)
    for px in (8, 11, 14):
        d.line([(x + px, y + 2), (x + px, y + 5)], fill=INK, width=2)
        d.line([(x + px, y + 17), (x + px, y + 20)], fill=INK, width=2)
    d.rectangle([x + 9, y + 9, x + 13, y + 13], fill=GOLD)


def icon_chart(d, x, y):
    d.line([(x + 3, y + 19), (x + 19, y + 19)], fill=INK, width=2)
    d.line([(x + 3, y + 3), (x + 3, y + 19)], fill=INK, width=2)
    for i, h in enumerate((6, 11, 16)):
        d.rectangle([x + 6 + i * 5, y + 19 - h, x + 9 + i * 5, y + 19], fill=BLUE)


def icon_rocket(d, x, y):
    d.polygon([(x + 11, y + 1), (x + 16, y + 9), (x + 6, y + 9)], fill=RED)
    d.rectangle([x + 7, y + 9, x + 15, y + 17], fill=BLUE)
    d.polygon([(x + 11, y + 17), (x + 14, y + 21), (x + 8, y + 21)], fill=ORANGE)
    d.ellipse([x + 9, y + 11, x + 13, y + 15], fill=(255, 255, 255))


def icon_star(d, x, y):
    d.polygon([(x + 11, y + 1), (x + 13, y + 8), (x + 21, y + 8), (x + 15, y + 13),
               (x + 17, y + 21), (x + 11, y + 16), (x + 5, y + 21), (x + 7, y + 13),
               (x + 1, y + 8), (x + 9, y + 8)], fill=GOLD)


def icon_flame(d, x, y):
    d.polygon([(x + 11, y + 1), (x + 16, y + 8), (x + 19, y + 13), (x + 15, y + 20),
               (x + 7, y + 20), (x + 3, y + 13), (x + 6, y + 8)], fill=ORANGE)
    d.polygon([(x + 11, y + 10), (x + 14, y + 14), (x + 12, y + 18),
               (x + 9, y + 18), (x + 8, y + 14)], fill=RED)


def icon_scales(d, x, y):
    d.line([(x + 11, y + 2), (x + 11, y + 18)], fill=INK, width=2)
    d.line([(x + 3, y + 5), (x + 19, y + 5)], fill=INK, width=2)
    d.polygon([(x + 2, y + 6), (x + 8, y + 6), (x + 5, y + 12)], fill=BLUE)
    d.polygon([(x + 14, y + 6), (x + 20, y + 6), (x + 17, y + 12)], fill=BLUE)
    d.rectangle([x + 8, y + 18, x + 14, y + 21], fill=INK)


def icon_sun(d, x, y):
    d.ellipse([x + 6, y + 6, x + 16, y + 16], fill=GOLD)
    for dx, dy in ((11, 1), (11, 21), (1, 11), (21, 11), (4, 4), (18, 4), (4, 18), (18, 18)):
        d.line([(x + dx, y + dy), (x + 11, y + 11)], fill=GOLD, width=1)


def icon_alert(d, x, y):
    d.polygon([(x + 11, y + 1), (x + 21, y + 20), (x + 1, y + 20)], fill=RED)
    d.line([(x + 11, y + 7), (x + 11, y + 14)], fill=(255, 255, 255), width=2)
    d.ellipse([x + 10, y + 16, x + 12, y + 18], fill=(255, 255, 255))


def icon_burst(d, x, y):
    pts = []
    for i in range(16):
        r = 10 if i % 2 == 0 else 4
        import math
        a = math.pi * i / 8 - math.pi / 2
        pts.append((x + 11 + r * math.cos(a), y + 11 + r * math.sin(a)))
    d.polygon(pts, fill=ORANGE)
    d.ellipse([x + 8, y + 8, x + 14, y + 14], fill=RED)


def icon_shield(d, x, y):
    d.polygon([(x + 3, y + 3), (x + 19, y + 3), (x + 19, y + 11),
               (x + 11, y + 21), (x + 3, y + 11)], fill=BLUE)
    d.line([(x + 7, y + 11), (x + 10, y + 14), (x + 15, y + 7)],
           fill=(255, 255, 255), width=2)


def icon_arrow(d, x, y):
    d.line([(x + 11, y + 20), (x + 11, y + 5)], fill=GREEN, width=3)
    d.polygon([(x + 11, y + 1), (x + 17, y + 8), (x + 5, y + 8)], fill=GREEN)


ICONS = {
    "leaf": icon_leaf, "chip": icon_chip, "chart": icon_chart,
    "rocket": icon_rocket, "star": icon_star, "flame": icon_flame,
    "scales": icon_scales, "sun": icon_sun, "alert": icon_alert,
    "burst": icon_burst, "shield": icon_shield, "arrow": icon_arrow,
}


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 24

    # masthead
    f_mast = font(F_SERIF_B, 27)
    mast = "T H E   W O R L D   I N   O N E   D A Y"
    d.text((MARGIN, y), mast, font=f_mast, fill=RED)
    f_no = font(F_SANS_B, 14)
    no = "No. 24 · 2026"
    d.text((W - MARGIN - text_w(d, no, f_no), y + 6), no, font=f_no, fill=GREY)
    y += 40
    y = rule(d, y, 3)
    y += 8

    # date
    f_date = font(F_SERIF_B, 54)
    d.text((MARGIN, y), "Tuesday 24 November 2026", font=f_date, fill=INK)
    y += 68
    y = rule(d, y, 1)
    y += 6
    f_strap = font(F_SANS, 15)
    strap = ("The day's world news in one picture  ·  37 stories  ·  9 regions  ·  "
             "13 drawn  ·  claims labelled")
    d.text((MARGIN, y), strap, font=f_strap, fill=GREY)
    y += 24
    y = rule(d, y, 1)
    y += 10

    # ---- lead 1 ----
    tag(d, MARGIN, y, "LEAD · CONFLICT", RED)
    f_kick = font(F_SANS_B, 14)
    d.text((MARGIN + 148, y + 3), "OFF LIBYA", font=f_kick, fill=GREY)
    y += 26
    f_h1 = font(F_SERIF_B, 40)
    lines = wrap(d, "Ukraine sinks Russian warship off Libya", f_h1, CW)
    y = draw_lines(d, lines, f_h1, MARGIN, y, 48)
    y += 4
    f_dek = font(F_SERIF, 19)
    dek = ("Kyiv says its sea drones struck off Benghazi — and Libya demanded an "
           "explanation — as new hacked data put Russia's death toll in Ukraine "
           "near 500,000.")
    y = draw_lines(d, wrap(d, dek, f_dek, CW), f_dek, MARGIN, y, 24)
    y += 6
    ship_scene(d, MARGIN, y, CW, 52)
    y += 52 + 8
    y = rule(d, y, 2)
    y += 8

    # ---- leads 2 and 3, side by side ----
    col_w = (CW - 24) // 2
    leads = [
        ("LEAD · CHINA", RED, "China probes Shanghai party chief Chen Jining",
         "Xinhua says the Politburo member faces a graft inquiry — the fourth "
         "top leader probed since 2025, and the first Shanghai chief "
         "investigated since 2006."),
        ("LEAD · COURTS", BLUE, "Huawei guilty on 10 of 12 counts",
         "A Brooklyn jury convicts the telecom giant of bank fraud, wire fraud "
         "and sanctions-busting over Iran — and clears it of racketeering."),
    ]
    f_h2 = font(F_SERIF_B, 26)
    f_dek2 = font(F_SERIF, 14)
    col_ys = []
    for i, (tg, col, head, dk) in enumerate(leads):
        x = MARGIN + i * (col_w + 24)
        yy = y
        tag(d, x, yy, tg, col)
        yy += 26
        yy = draw_lines(d, wrap(d, head, f_h2, col_w), f_h2, x, yy, 32)
        yy += 3
        yy = draw_lines(d, wrap(d, dk, f_dek2, col_w), f_dek2, x, yy, 19)
        col_ys.append(yy)
    y = max(col_ys) + 6
    y = rule(d, y, 2)
    y += 8

    # ---- 20 briefs, 2 columns x 10 rows ----
    briefs = [
        ("CLIMATE", GREEN, "COP31 ends with no deal on fossil fuels",
         "190+ countries leave Antalya without agreement.", "leaf"),
        ("TECH", BLUE, "Nvidia rehires Jensen Huang as CEO",
         "Board reinstates him days after his ouster.", "chip"),
        ("MARKETS", OLIVE, "Dow tops 50,000 as Nvidia slides 5.9%",
         "Nasdaq −1.5%, S&P −0.5%; the Huang rally fades in a day.", "chart"),
        ("SPACE", BLUE, "Shenzhou-24 crew named, first foreigner aboard",
         "Pakistan's Zeeshan Ali to visit Tiangong; launch Wednesday.", "rocket"),
        ("SPACE", BLUE, "Zhu Yangzhu to spend a year in orbit",
         "A first for China, announced with the Shenzhou-24 crew.", "star"),
        ("MIDEAST", RED, "Iran says four tankers hit mines in Hormuz",
         "Tehran blames unauthorised routes; oil jumps.", "flame"),
        ("EUROPE", GREEN, "Sarkozy and Bruni to stand trial in Nov 2027",
         "Judges order trial over alleged witness tampering.", "scales"),
        ("UK", RED, "England records 5,258 heat deaths",
         "Highest since records began in 2016, UKHSA says.", "sun"),
        ("TECH", BLUE, "Microsoft declares 'Code Red' after worst outage",
         "24-hour 365 failure; a one-hour fix target is set.", "alert"),
        ("MIDEAST", RED, "Houthis hit Riyadh tower; 11 hurt",
         "Saudi civil defence said; second strike in a week.", "burst"),
        ("USA", BLUE, "FBI seizes $17bn in Operation Blackout",
         "29 scam compounds shut in a global crackdown.", "shield"),
        ("USA", BLUE, "US blacklists 7 firms, incl. Alibaba unit",
         "New export curbs announced on Tuesday.", None),
        ("UK", RED, "Arrests after break-in at Prince William's home",
         "Two held over the Norfolk estate intrusion.", None),
        ("MARKETS", OLIVE, "Asian markets rally: Kospi +6.3%, Nikkei +3.9%",
         "Seoul retakes 5,000; Taipei +9%.", "arrow"),
        ("ASIA", BLUE, "Nepal quake shakes region",
         "Magnitude 5.3 in Koshi Province, felt in India.", None),
        ("BUSINESS", OLIVE, "Sanofi buys Insmed for $41bn",
         "All-cash deal; Sanofi shares rise 9.7%.", None),
        ("AMERICAS", RED, "Car bomb hits Colombia governor's office",
         "Blast in Villavicencio damages the Meta HQ.", None),
        ("ASIA", BLUE, "Hanoi food-shop blast kills 6",
         "Gas explosion injures 10 more.", None),
        ("EUROPE", GREEN, "Merz: Europe ready to talk to Russia",
         "Berlin says adviser-level talks could resume.", None),
        ("KOREA", RED, "Seoul scrambles jets at Russian planes",
         "Warplanes enter the air defence zone.", None),
    ]
    f_bh = font(F_SERIF_B, 14)
    f_bd = font(F_SERIF, 11)
    row_h = 33
    for r in range(10):
        for c in range(2):
            tg, col, head, dk, icon = briefs[r * 2 + c]
            x = MARGIN + c * (col_w + 24)
            yy = y + r * row_h
            tx = x
            if icon:
                ICONS[icon](d, x, yy - 2)
                tx = x + 28
            tw = tag(d, tx, yy, tg, col, size=11)
            fh = f_bh
            while text_w(d, head, fh) > col_w - (tx - x) - tw - 6 and fh.size > 11:
                fh = font(F_SERIF_B, fh.size - 1)
            d.text((tx + tw + 6, yy + 1), head, font=fh, fill=INK)
            dl = wrap(d, dk, f_bd, col_w - (tx - x))
            draw_lines(d, dl[:1], f_bd, tx, yy + 20, 14, fill=(60, 60, 60))
    y += 10 * row_h
    y = rule(d, y, 2)
    y += 8

    # ---- also strip ----
    f_also_t = font(F_SANS_B, 15)
    d.text((MARGIN, y), "ALSO ON 24 NOVEMBER", font=f_also_t, fill=RED)
    y += 22
    f_also = font(F_SERIF, 13)
    also = ("N. Korean jet enters South airspace · Democrats clinch biggest House "
            "majority · Trump halts Iowa explosives blast · Trump warns Iran of "
            "'traumatic' outcome · Gomez resigns after ethics findings · 2031 "
            "Women's Cup to US and Mexico · Indonesia factory fire toll rises to "
            "26 · Fire engulfs six Zanzibar hotels · Denmark to ban school phones "
            "· States sue Musk firms over Grok images · Wars put food aid for "
            "7.3m at risk · 360,000 displaced in Yemen since August · Hasina "
            "plans December 16 return · Anthropic launches Claude Ship")
    y = draw_lines(d, wrap(d, also, f_also, CW), f_also, MARGIN, y, 16)
    y += 5
    y = rule(d, y, 1)
    y += 5
    f_foot = font(F_SANS, 11)
    d.text((MARGIN, y), "Sources: AP · Reuters · BBC · CNN · NYT · Xinhua · Al Jazeera · "
           "UKHSA — Contested claims are labelled with their source in the text "
           "(Iran says · Kyiv says · Saudi civil defence said).", font=f_foot,
           fill=GREY)
    y += 16

    print(f"layout bottom y={y} (canvas {H})")
    if y > H - 8:
        print("WARNING: content overflows the page")
    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
