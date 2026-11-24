#!/usr/bin/env python3
"""Render the 24 November 2026 front page (1024x1024) for news-image-20261124.

Draws the newspaper front page with PIL only (no network, deterministic):
masthead, date, 3 leads with a drawn lead illustration, 12 briefs and an
8-item "Also on 24 November" strip. Stories are the verified 24 November
2026 reports (AP, Reuters, BBC, CNN, NYT, WION, SCMP live pages, checked
again on the evening of 24 November: Nepal quake, Sanofi-Insmed, Colombia
car bomb, Hanoi blast, Merz talks, Seoul jets, House majority are the
late-day additions to the earlier edition).

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


def tag(draw, x, y, label, bg, fg=(255, 255, 255)):
    f = font(F_SANS_B, 13)
    tw = draw.textlength(label, font=f)
    draw.rounded_rectangle([x, y, x + tw + 14, y + 20], radius=3, fill=bg)
    draw.text((x + 7, y + 3), label, font=f, fill=fg)
    return tw + 14  # chip width, so callers can place text after it


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
    strap = "The day's world news in one picture  ·  23 stories  ·  All stories dated 24 November 2026"
    d.text((MARGIN, y), strap, font=f_strap, fill=GREY)
    y += 24
    y = rule(d, y, 1)
    y += 10

    # ---- lead 1 ----
    tag(d, MARGIN, y, "LEAD · CONFLICT", RED)
    f_kick = font(F_SANS_B, 14)
    d.text((MARGIN + 148, y + 3), "OFF LIBYA", font=f_kick, fill=GREY)
    y += 26
    f_h1 = font(F_SERIF_B, 44)
    lines = wrap(d, "Ukraine sinks Russian warship off Libya", f_h1, CW)
    y = draw_lines(d, lines, f_h1, MARGIN, y, 50)
    y += 4
    f_dek = font(F_SERIF, 19)
    dek = ("Kyiv's sea drones struck off Benghazi — and Libya demanded an explanation — "
           "as new hacked data put Russia's death toll in Ukraine near 500,000.")
    y = draw_lines(d, wrap(d, dek, f_dek, CW), f_dek, MARGIN, y, 24)
    y += 6
    ship_scene(d, MARGIN, y, CW, 70)
    y += 70 + 8
    y = rule(d, y, 2)
    y += 10

    # ---- leads 2 and 3, side by side ----
    col_w = (CW - 24) // 2
    leads = [
        ("LEAD · CLIMATE", RED, "COP31 ends with no deal on fossil fuels",
         "After days of talks in Antalya, more than 190 countries leave the UN climate "
         "summit without agreement — the defining failure of the day."),
        ("LEAD · TECH", BLUE, "Nvidia rehires Huang after Trump push",
         "The board reinstates Jensen Huang as chief executive days after his ouster, "
         "after JD Vance lobbied it at the White House's behest."),
    ]
    f_h2 = font(F_SERIF_B, 27)
    f_dek2 = font(F_SERIF, 15)
    col_ys = []
    for i, (tg, col, head, dk) in enumerate(leads):
        x = MARGIN + i * (col_w + 24)
        yy = y
        tag(d, x, yy, tg, col)
        yy += 26
        yy = draw_lines(d, wrap(d, head, f_h2, col_w), f_h2, x, yy, 34)
        yy += 3
        yy = draw_lines(d, wrap(d, dk, f_dek2, col_w), f_dek2, x, yy, 21)
        col_ys.append(yy)
    y = max(col_ys) + 6
    y = rule(d, y, 2)
    y += 8

    # ---- 12 briefs, 2 columns x 6 rows ----
    briefs = [
        ("ASIA", BLUE, "Nepal quake shakes region",
         "Magnitude 5.3 tremor in Koshi Province, felt in India and Bhutan."),
        ("BUSINESS", OLIVE, "Sanofi buys Insmed for $41bn",
         "French drugmaker agrees a $41bn all-cash deal."),
        ("AMERICAS", RED, "Car bomb hits Colombia governor's office",
         "Blast in Villavicencio damages the Meta government headquarters."),
        ("ASIA", BLUE, "Hanoi food-shop blast kills 6",
         "Gas explosion in a crowded residential area injures 10 more."),
        ("EUROPE", GREEN, "Merz: Europe ready to talk to Russia",
         "Berlin says adviser-level talks with Moscow could resume."),
        ("KOREA", RED, "Seoul scrambles jets at Russian planes",
         "Russian warplanes enter the air defence zone over the East Sea."),
        ("USA", BLUE, "Democrats clinch biggest House majority",
         "Victory hands the party power to block Trump's agenda for two years."),
        ("KOREA", RED, "N. Korean jet enters South airspace",
         "Suspected incursion near Ulleung; residents told to shelter."),
        ("USA", BLUE, "Trump halts Iowa explosives blast",
         "Blast paused pending a court ruling."),
        ("USA", BLUE, "Trump warns Iran of 'traumatic' outcome",
         "Warning if no nuclear deal; a second US carrier considered."),
        ("USA", BLUE, "Gomez resigns after ethics findings",
         "Panel found evidence of misconduct by Rep. Gomez."),
        ("SPORT", RED, "2031 Women's Cup to US and Mexico",
         "Costa Rica and Jamaica to co-host; UK gets the 2035 edition."),
    ]
    f_bh = font(F_SERIF_B, 16)
    f_bd = font(F_SERIF, 13)
    row_h = 44
    for r in range(6):
        for c in range(2):
            tg, col, head, dk = briefs[r * 2 + c]
            x = MARGIN + c * (col_w + 24)
            yy = y + r * row_h
            # tag chip, then the headline on the same line (as the 23 Nov page)
            tw = tag(d, x, yy, tg, col)
            f_head = f_bh
            while text_w(d, head, f_head) > col_w - tw - 8 and f_head.size > 12:
                f_head = font(F_SERIF_B, f_head.size - 1)
            d.text((x + tw + 8, yy + 2), head, font=f_head, fill=INK)
            yy += 24
            dl = wrap(d, dk, f_bd, col_w)
            draw_lines(d, dl[:1], f_bd, x, yy, 16, fill=(60, 60, 60))
    y += 6 * row_h
    y = rule(d, y, 2)
    y += 8

    # ---- also strip ----
    f_also_t = font(F_SANS_B, 15)
    d.text((MARGIN, y), "ALSO ON 24 NOVEMBER", font=f_also_t, fill=RED)
    y += 22
    f_also = font(F_SERIF, 15)
    also = ("24 killed in an Indonesia factory fire · Fire engulfs six Zanzibar hotels; "
            "180 tourists evacuated · Denmark to ban school phones · States sue Musk firms "
            "over Grok images · Wars put food aid for 7.3m at risk · 360,000 displaced in "
            "Yemen since August · Hasina plans December 16 return to Bangladesh · "
            "Anthropic launches Claude Ship")
    y = draw_lines(d, wrap(d, also, f_also, CW), f_also, MARGIN, y, 19)
    y += 5
    y = rule(d, y, 1)
    y += 5
    f_foot = font(F_SANS, 12)
    d.text((MARGIN, y), "Sources: AP · Reuters · BBC · CNN · New York Times · WION · SCMP — "
           "Image: one picture of Tuesday 24 November 2026", font=f_foot, fill=GREY)
    y += 18

    print(f"layout bottom y={y} (canvas {H})")
    if y > H - 8:
        print("WARNING: content overflows the page")
    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
