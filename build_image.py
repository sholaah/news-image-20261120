"""Cover renderer for the 20 November 2026 news-image entry.

Draws one square front page, Economist-style: a red masthead, the date
as the title, a courthouse scene for the day's lead story (the ICJ
genocide verdict on Myanmar), two smaller panels (the Shenzhen
three-leader summit and Anthropic's record stock-market debut), and a
bottom strip with three more of the day's stories. Everything is drawn
with PIL primitives so the output bytes are fully deterministic.
"""

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024

CREAM = (247, 242, 227)
INK = (24, 24, 24)
RED = (224, 18, 11)
RED_DARK = (168, 10, 5)
NAVY = (30, 45, 74)
SKY = (208, 220, 232)
STONE = (196, 190, 172)
GOLD = (196, 152, 40)
GREEN = (18, 118, 60)
GREY_LINE = (120, 116, 104)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def kicker(draw, x, y, text):
    """Small red section label with a short rule under it."""
    f = font(SANS_BOLD, 24)
    draw.text((x, y), text, font=f, fill=RED_DARK)
    draw.line([(x, y + 34), (x + 52, y + 34)], fill=RED, width=5)
    return y + 44


def courthouse(draw, box):
    """Flat courthouse facade sized to its box: pediment, columns, steps."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SKY)
    cx = (x0 + x1) // 2
    ped_base = y0 + 62
    draw.polygon([(x0 + 56, ped_base), (x1 - 56, ped_base), (cx, y0 + 12)], fill=NAVY)
    draw.polygon([(x0 + 88, ped_base - 4), (x1 - 88, ped_base - 4), (cx, y0 + 26)],
                 outline=GOLD, width=3)
    draw.rectangle([x0 + 56, ped_base, x1 - 56, ped_base + 16], fill=STONE)
    col_top, col_bot = ped_base + 16, y1 - 30
    span = (x1 - 56) - (x0 + 56)
    for i in range(6):
        cx_i = x0 + 56 + span * (i + 0.5) / 6
        draw.rectangle([cx_i - 15, col_top, cx_i + 15, col_bot], fill=(238, 234, 222))
        draw.rectangle([cx_i - 20, col_top, cx_i + 20, col_top + 8], fill=STONE)
        draw.rectangle([cx_i - 20, col_bot - 8, cx_i + 20, col_bot], fill=STONE)
    for s in range(3):
        draw.rectangle([x0 + 40 - s * 8, col_bot + s * 10, x1 - 40 + s * 8,
                        col_bot + s * 10 + 9], fill=STONE)
    # scales of justice between the middle columns
    top = col_top + 8
    draw.line([(cx, top), (cx, top + 34)], fill=GOLD, width=4)
    draw.line([(cx - 40, top + 6), (cx + 40, top + 6)], fill=GOLD, width=4)
    for sx in (cx - 40, cx + 40):
        draw.line([(sx, top + 6), (sx - 12, top + 30)], fill=GOLD, width=3)
        draw.line([(sx, top + 6), (sx + 12, top + 30)], fill=GOLD, width=3)
        draw.arc([sx - 17, top + 24, sx + 17, top + 42], 0, 180, fill=GOLD, width=3)


def flags_panel(draw, box):
    """Three national flags on poles over a summit table line."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(233, 228, 210))
    top = y0 + 14
    pole_bot = y1 - 46
    fw, fh = 118, 70
    xs = [x0 + 38, (x0 + x1) // 2 - fw // 2, x1 - 38 - fw]
    for fx in xs:
        draw.line([(fx + 5, top - 8), (fx + 5, pole_bot)], fill=INK, width=4)
    # United States: stripes + blue canton
    fx = xs[0] + 10
    for i in range(7):
        col = (178, 34, 52) if i % 2 == 0 else (244, 244, 240)
        draw.rectangle([fx, top + i * 10, fx + fw, top + (i + 1) * 10], fill=col)
    draw.rectangle([fx, top, fx + 48, top + 40], fill=(60, 59, 110))
    for r in range(3):
        for c in range(4):
            draw.ellipse([fx + 5 + c * 11, top + 5 + r * 12, fx + 9 + c * 11,
                          top + 9 + r * 12], fill=(244, 244, 240))
    # China: red field, one large gold star and three small
    fx = xs[1] + 10
    draw.rectangle([fx, top, fx + fw, top + fh], fill=(222, 41, 16))
    draw.polygon([(fx + 26, top + 10), (fx + 31, top + 23), (fx + 45, top + 23),
                  (fx + 34, top + 31), (fx + 38, top + 45), (fx + 26, top + 37),
                  (fx + 14, top + 45), (fx + 18, top + 31), (fx + 7, top + 23),
                  (fx + 21, top + 23)], fill=(255, 222, 0))
    for dy in (6, 22, 38):
        draw.ellipse([fx + 56, top + dy, fx + 63, top + dy + 7], fill=(255, 222, 0))
    # Russia: white, blue, red bands
    fx = xs[2] + 10
    for i, col in enumerate([(244, 244, 240), (0, 57, 166), (213, 43, 30)]):
        draw.rectangle([fx, top + i * 23, fx + fw, top + (i + 1) * 23 + (1 if i == 2 else 0)],
                       fill=col)
    # summit table
    draw.rectangle([x0 + 26, pole_bot, x1 - 26, pole_bot + 12], fill=NAVY)
    draw.rectangle([x0 + 52, pole_bot + 12, x0 + 64, y1 - 16], fill=NAVY)
    draw.rectangle([x1 - 64, pole_bot + 12, x1 - 52, y1 - 16], fill=NAVY)


def chart_panel(draw, box):
    """Rising market chart with gridlines and an arrowhead."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(240, 244, 238))
    gx0, gy0, gx1, gy1 = x0 + 34, y0 + 18, x1 - 28, y1 - 48
    for i in range(4):
        yy = gy0 + (gy1 - gy0) * i // 3
        draw.line([(gx0, yy), (gx1, yy)], fill=(196, 205, 196), width=2)
    pts = [(gx0, gy1 - 10), (gx0 + 62, gy1 - 22), (gx0 + 116, gy1 - 16),
           (gx0 + 178, gy1 - 48), (gx0 + 238, gy1 - 62), (gx0 + 300, gy1 - 98),
           (gx1 - 6, gy1 - 128)]
    draw.line(pts, fill=GREEN, width=8, joint="curve")
    hx, hy = pts[-1]
    draw.polygon([(hx, hy), (hx - 26, hy + 5), (hx - 7, hy + 24)], fill=GREEN)
    for px, py in pts[::2]:
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=GREEN)
    draw.text((gx0, gy1 + 10), "DAY ONE  +17%", font=font(SANS_BOLD, 26), fill=GREEN)


def render(path):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 110], fill=RED)
    centered(d, W // 2, 20, "THE WORLD TODAY", font(SERIF_BOLD, 60), (255, 250, 238))
    d.line([(36, 130), (W - 36, 130)], fill=INK, width=3)
    centered(d, W // 2, 142, "FRIDAY  ·  20 NOVEMBER 2026", font(SANS_BOLD, 38), INK)
    d.line([(36, 196), (W - 36, 196)], fill=INK, width=3)

    # --- hero: the ICJ verdict ---
    hy = 210
    kicker(d, 36, hy, "THE HAGUE  ·  JUSTICE")
    courthouse(d, (36, hy + 48, W - 36, hy + 208))
    d.rectangle([36, hy + 48, W - 36, hy + 208], outline=INK, width=3)
    yy = hy + 222
    hf = font(SERIF_BOLD, 52)
    for line in wrap(d, "GENOCIDE, THE COURT FINDS", hf, W - 72):
        centered(d, W // 2, yy, line, hf, INK)
        yy += 60
    sub = ("UN judges rule that Myanmar's army committed genocide against "
           "the Rohingya — the court's first verdict of its kind against a state.")
    sf = font(SANS, 25)
    for line in wrap(d, sub, sf, W - 120):
        centered(d, W // 2, yy + 2, line, sf, (52, 52, 52))
        yy += 32

    # --- middle panels ---
    py = yy + 14
    half = (W - 72 - 24) // 2
    lx, rx = 36, 36 + half + 24
    kicker(d, lx, py, "SHENZHEN  ·  SUMMIT")
    kicker(d, rx, py, "NEW YORK  ·  MARKETS")
    flags_panel(d, (lx, py + 48, lx + half, py + 198))
    d.rectangle([lx, py + 48, lx + half, py + 198], outline=INK, width=3)
    chart_panel(d, (rx, py + 48, rx + half, py + 198))
    d.rectangle([rx, py + 48, rx + half, py + 198], outline=INK, width=3)
    pf = font(SERIF_BOLD, 27)
    for j, line in enumerate(wrap(d, "THREE LEADERS, ONE PEACE DECLARATION", pf, half)):
        d.text((lx, py + 208 + j * 33), line, font=pf, fill=INK)
    for j, line in enumerate(wrap(d, "ANTHROPIC'S RECORD MARKET DEBUT", pf, half)):
        d.text((rx, py + 208 + j * 33), line, font=pf, fill=INK)
    panel_text_end = py + 208 + 2 * 33

    # --- bottom strip ---
    by = panel_text_end + 12
    d.line([(36, by), (W - 36, by)], fill=INK, width=3)
    items = [
        "EUROPE READY FOR TALKS WITH RUSSIA ON ENDING THE UKRAINE WAR",
        "COP31 DRAFT DROPS FOSSIL FUELS — OUTCRY AT THE ANTALYA SUMMIT",
        "HOUTHI MISSILE HITS RIYADH'S TALLEST TOWER; TANKER AFIRE AT HORMUZ",
    ]
    iy = by + 12
    col_w = (W - 72 - 2 * 24) // 3
    bf = font(SANS_BOLD, 19)
    for i, item in enumerate(items):
        x = 36 + i * (col_w + 24)
        if i:
            d.line([(x - 12, iy + 2), (x - 12, iy + 58)], fill=GREY_LINE, width=2)
        for j, line in enumerate(wrap(d, item, bf, col_w)):
            d.text((x, iy + j * 24), line, font=bf, fill=INK)
    d.line([(36, H - 42), (W - 36, H - 42)], fill=INK, width=3)
    centered(d, W // 2, H - 34, "AND FAREWELL TO FIONA, CINCINNATI'S BELOVED HIPPO",
             font(SANS, 18), (70, 66, 58))

    img.save(path, format="PNG", optimize=True)
    return path
