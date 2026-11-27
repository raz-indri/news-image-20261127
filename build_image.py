#!/usr/bin/env python3
"""Build the front page of The Meridian Herald for Friday 27 November 2026.

Draws a 1024x1024 newspaper front page with Pillow only (no network).
Run:  python3 build_image.py   -> writes news.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "news.png")

W, H = 1024, 1024
PAPER = (253, 250, 243)
INK = (17, 17, 17)
GREY = (90, 86, 78)
RED = (178, 34, 34)
BLUE = (30, 64, 110)
SKY = (214, 230, 242)
SEA = (46, 105, 150)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK, justify=False):
    """Draw a wrapped paragraph; return y below it."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, x0, y, x1, weight=2, color=INK):
    draw.line([(x0, y), (x1, y)], fill=color, width=weight)


def headline_block(draw, x, y, w, kick, title, title_size, deck, body):
    """A story: kicker, bold title, deck, body paragraphs. Returns y."""
    f_kick = font(SANS_B, 15)
    f_title = font(SERIF_B, title_size)
    f_deck = font(SERIF, 16)
    f_body = font(SERIF, 14)
    if kick:
        draw.text((x, y), kick.upper(), font=f_kick, fill=RED)
        y += 22
    for line in wrap(draw, title, f_title, w):
        draw.text((x, y), line, font=f_title, fill=INK)
        y += title_size + 6
    y += 2
    if deck:
        y = para(draw, x, y, deck, f_deck, w, 20, color=(40, 40, 40))
        y += 4
    for p in body:
        y = para(draw, x, y, p, f_body, w, 17)
        y += 5
    return y


def draw_skyline_scene(draw, x0, y0, x1, y1):
    """Illustration for the lead story: Gulf skyline, drones, smoke, sea."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # sun / haze
    draw.ellipse([x1 - 110, y0 + 14, x1 - 40, y0 + 84], fill=(246, 214, 130))
    # distant skyline silhouettes (heights capped to the panel)
    import random
    rnd = random.Random(20261127)
    ph = y1 - y0
    base = y1 - 45
    maxh = max(30, ph - 75)
    bx = x0 + 8
    while bx < x1 - 60:
        bw = rnd.randint(28, 52)
        bh = rnd.randint(25, maxh)
        draw.rectangle([bx, base - bh, bx + bw, base], fill=(120, 138, 158))
        for wy in range(base - bh + 10, base - 8, 16):
            for wx in range(bx + 6, bx + bw - 6, 12):
                if rnd.random() < 0.5:
                    draw.rectangle([wx, wy, wx + 5, wy + 7], fill=(240, 220, 140))
        bx += bw + 6
    # Kuwait Towers-like trio (three slender towers with spheres)
    for tx, th in ((x0 + 150, 55), (x0 + 205, 65), (x0 + 258, 45)):
        draw.rectangle([tx, base - th, tx + 14, base], fill=(70, 84, 104))
        draw.ellipse([tx - 8, base - th - 22, tx + 22, base - th + 8], fill=(70, 84, 104))
    # smoke plume rising from the right
    for i, (sx, sy, sr) in enumerate(((x1 - 190, y0 + 95, 20), (x1 - 208, y0 + 72, 26),
                                      (x1 - 186, y0 + 45, 30), (x1 - 210, y0 + 22, 22))):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(110, 108, 104))
    # two drone silhouettes
    for dx, dy, s in ((x0 + 330, y0 + 48, 1.0), (x0 + 470, y0 + 76, 0.7)):
        draw.ellipse([dx - 26 * s, dy - 7 * s, dx + 26 * s, dy + 7 * s], fill=INK)
        draw.line([(dx - 34 * s, dy - 10 * s), (dx - 14 * s, dy - 4 * s)], fill=INK, width=2)
        draw.line([(dx + 14 * s, dy - 4 * s), (dx + 34 * s, dy - 10 * s)], fill=INK, width=2)
        draw.ellipse([dx - 4 * s, dy + 6 * s, dx + 4 * s, dy + 12 * s], fill=INK)
    # sea strip
    draw.rectangle([x0, base, x1, y1], fill=SEA)
    for wx in range(x0 + 20, x1 - 20, 70):
        draw.line([(wx, base + 14), (wx + 34, base + 14)], fill=(200, 225, 240), width=3)
        draw.line([(wx + 12, base + 30), (wx + 46, base + 30)], fill=(200, 225, 240), width=3)
    # caption bar
    draw.rectangle([x0, y1 - 26, x1, y1], fill=(17, 17, 17))
    draw.text((x0 + 10, y1 - 22),
              "Kuwait City skyline after the drone strike that killed two Italian workers.  Illustration: Herald Graphics",
              font=font(SANS, 13), fill=(240, 240, 235))


def draw_chess_mini(draw, x0, y0, size):
    """Small chess board illustration for the chess story."""
    cell = size // 8
    for r in range(8):
        for c in range(8):
            col = (240, 235, 220) if (r + c) % 2 == 0 else (60, 55, 50)
            draw.rectangle([x0 + c * cell, y0 + r * cell,
                            x0 + (c + 1) * cell, y0 + (r + 1) * cell], fill=col)
    # a few pieces as simple circles with letters
    pieces = {(3, 4): ("K", (20, 20, 20)), (4, 3): ("Q", (245, 245, 240)),
              (2, 5): ("N", (20, 20, 20)), (5, 2): ("R", (245, 245, 240))}
    f_p = font(SERIF_B, cell)
    for (r, c), (ch, col) in pieces.items():
        cx, cy = x0 + c * cell + cell // 2, y0 + r * cell + cell // 2
        draw.ellipse([cx - cell // 2 + 1, cy - cell // 2 + 1,
                      cx + cell // 2 - 1, cy + cell // 2 - 1],
                     fill=(200, 40, 40) if col == (20, 20, 20) else (240, 235, 220),
                     outline=INK, width=1)
        tw = draw.textlength(ch, font=f_p)
        draw.text((cx - tw / 2, cy - cell // 2 + 1), ch, font=f_p, fill=col)
    draw.rectangle([x0, y0, x0 + size, y0 + size], outline=INK, width=2)


def draw_storm_mini(draw, x0, y0, w, h):
    """Storm cloud + rain over a parade balloon, for the parade story."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(226, 234, 240))
    s = h / 110.0
    # balloon
    draw.ellipse([x0 + 18, y0 + 30 * s, x0 + 78, y0 + 74 * s], fill=(196, 52, 52))
    draw.ellipse([x0 + 34, y0 + 16 * s, x0 + 62, y0 + 40 * s], fill=(196, 52, 52))
    draw.polygon([(x0 + 44, y0 + 74 * s), (x0 + 52, y0 + 74 * s), (x0 + 48, y0 + 92 * s)], fill=(150, 30, 30))
    # cloud
    for cx, cy, cr in ((x0 + 110, y0 + 28 * s, 24), (x0 + 140, y0 + 20 * s, 30),
                       (x0 + 172, y0 + 30 * s, 22), (x0 + 140, y0 + 42 * s, 28)):
        draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(96, 104, 116))
    for rx in range(x0 + 105, x0 + 185, 14):
        draw.line([(rx, y0 + 58 * s), (rx - 4, y0 + 78 * s)], fill=(60, 90, 130), width=3)
    # ground
    draw.rectangle([x0, y0 + h - 10, x0 + w, y0 + h], fill=(90, 110, 90))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 30  # margin
    X1 = W - M

    # --- top strip ---
    f_small = font(SANS, 14)
    f_small_b = font(SANS_B, 14)
    d.text((M, 16), "FRIDAY, 27 NOVEMBER 2026", font=f_small_b, fill=INK)
    t = "VOL. XII  —  No. 331"
    d.text(((W - d.textlength(t, font=f_small)) / 2, 16), t, font=f_small, fill=GREY)
    t = "PRICE $2.50"
    d.text((X1 - d.textlength(t, font=f_small_b), 16), t, font=f_small_b, fill=INK)
    rule(d, M, 40, X1, 3)

    # --- masthead ---
    f_mast = font(SERIF_B, 58)
    name = "The Meridian Herald"
    d.text(((W - d.textlength(name, font=f_mast)) / 2, 44), name, font=f_mast, fill=INK)
    f_tag = font(SANS, 15)
    tag = "INDEPENDENT  •  WORLD NEWS  •  EST. 2014"
    d.text(((W - d.textlength(tag, font=f_tag)) / 2, 112), tag, font=f_tag, fill=GREY)
    rule(d, M, 134, X1, 2)
    rule(d, M, 139, X1, 5)

    # --- lead headline ---
    y = 152
    f_head = font(SERIF_B, 40)
    for line in ("DRONE STRIKE IN KUWAIT", "KILLS TWO ITALIANS"):
        d.text((M, y), line, font=f_head, fill=INK)
        y += 46
    f_deck = font(SERIF, 18)
    y = para(d, M, y + 2,
             "Tehran denies any role; Rome demands answers and an urgent inquiry.",
             f_deck, X1 - M, 22, color=(40, 40, 40))
    y += 6

    # --- main illustration ---
    img_y0, img_y1 = y, y + 130
    draw_skyline_scene(d, M, img_y0, X1, img_y1)
    y = img_y1 + 12

    # --- three columns ---
    col_w = (X1 - M - 2 * 22) // 3
    cx = [M, M + col_w + 22, M + 2 * (col_w + 22)]
    rule(d, M, y, X1, 1)
    y += 10
    top_y = y

    # Column 1: lead continued + migration
    cy = headline_block(
        d, cx[0], top_y, col_w, "Middle East",
        "Gulf on edge after deadly strike",
        22,
        "Officials say the drone hit a work site; two Italian "
        "nationals were killed. Iran denies responsibility.",
        ["Kuwait said the strike hit a civilian work site early "
         "on Friday; Italy demanded a full inquiry. Gulf "
         "governments urged restraint to prevent wider escalation."])
    cy += 6
    rule(d, cx[0], cy, cx[0] + col_w, 1)
    cy += 10
    cy = headline_block(
        d, cx[0], cy, col_w, "Britain",
        "UK net migration falls to lowest since 1997",
        20,
        "The sharpest drop in nearly three decades.",
        ["Official figures show net migration fell to its lowest "
         "since 1997. Ministers credited tighter visa rules."])
    # Column 2: Gaza + chess
    cy2 = headline_block(
        d, cx[1], top_y, col_w, "Gaza",
        "Israeli strikes kill 10 as Hamas weighs reply",
        22,
        "A day of deadly strikes deepens fears for the fragile "
        "ceasefire in Gaza.",
        ["Israeli strikes killed 10 people in Gaza on Friday, "
         "officials said, as Hamas weighed its response. "
         "Diplomats pressed both sides to hold the ceasefire."])
    cy2 += 6
    rule(d, cx[1], cy2, cx[1] + col_w, 1)
    cy2 += 10
    draw_chess_mini(d, cx[1], cy2, 72)
    d.text((cx[1] + 84, cy2 + 4), "SPORT", font=font(SANS_B, 14), fill=RED)
    cy2 = headline_block(
        d, cx[1] + 84, cy2 + 24, col_w - 84, "",
        "Gukesh, Sindarov draw Game 3",
        18,
        "Nothing separates the pair after three games.",
        ["The title match stayed dead level after a long draw."])
    # Column 3: parade + tanker
    cy3 = headline_block(
        d, cx[2], top_y, col_w, "United States",
        "Storm postpones Macy's 100th parade",
        22,
        "New York delays its centenary Thanksgiving parade for "
        "the first time ever.",
        ["A storm forced New York to postpone the 100th Macy's "
         "parade — a first. Half a million homes lost power; "
         "flights were cancelled."])
    cy3 += 6
    draw_storm_mini(d, cx[2], cy3, col_w, 76)
    cy3 += 86
    cy3 = headline_block(
        d, cx[2], cy3, col_w, "Mediterranean",
        "Tanker capsizes off Ibiza, one dead",
        20,
        "",
        ["Rescue teams searched off Ibiza after the tanker "
         "capsized, killing one. Officials watch for a fuel spill."])

    # --- bottom strip: in brief (two columns) + weather/markets line ---
    by = max(cy, cy2, cy3) + 12
    rule(d, M, by, X1, 2)
    by += 10
    f_sec = font(SANS_B, 15)
    d.text((M, by), "IN BRIEF", font=f_sec, fill=RED)
    by += 22
    f_brief = font(SERIF, 13)
    briefs_l = [
        "Trump asked Putin to “pull back” aggression in Europe.",
        "EU split over $49bn Ukraine loan; new ECB chief named.",
        "Depardieu to stand trial over alleged 2018 rape of actress.",
    ]
    briefs_r = [
        "Guinea-Bissau's junta postpones elections until 2028.",
        "Ebola in Congo passes 12,000 cases as unrest drives responders out.",
        "Black Friday: shoppers hunt deals as AI reshapes spending.",
    ]
    half_w = (X1 - M - 24) // 2
    ly = by
    for b in briefs_l:
        ly = para(d, M + 12, ly, "•  " + b, f_brief, half_w - 12, 16)
        ly += 2
    ry = by
    for b in briefs_r:
        ry = para(d, M + half_w + 24 + 12, ry, "•  " + b, f_brief, half_w - 12, 16)
        ry += 2
    by = max(ly, ry) + 6
    rule(d, M, by, X1, 1)
    by += 8
    d.text((M, by), "WEATHER:  New York 9°C rain  •  London 11°C cloudy  •  Kuwait City 24°C hazy      MARKETS:  Oil steadies; stocks mixed      •      Page 1",
           font=font(SANS, 13), fill=INK)

    img.save(OUT, "PNG", optimize=True)
    print("saved", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
