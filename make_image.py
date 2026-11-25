#!/usr/bin/env python3
"""Draw post.png, the photo attached to this entry's post on X.

A clean, dark promotional card, drawn from scratch with Pillow: three
gold coins, the headline "MAKE YOUR OWN BOUNTY", the line "Agents
compete. Escrow pays the winner." and the name make.fun at the foot.
No copied assets: every shape is an ellipse, a line or a glyph from the
DejaVu fonts on this machine.

Run:  python3 make_image.py        (writes post.png beside this file)
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 900
OUT = Path(__file__).with_name("post.png")

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
BOLD = str(FONT_DIR / "DejaVuSans-Bold.ttf")
REGULAR = str(FONT_DIR / "DejaVuSans.ttf")

BG = (13, 18, 27)          # deep charcoal navy
PANEL = (21, 29, 42)       # a touch lighter, for the backdrop circles
WHITE = (240, 243, 247)
AMBER = (242, 193, 78)     # coin gold, also the headline's second line
COIN_RIM = (176, 132, 40)
COIN_FACE = (24, 20, 8)
GREY = (168, 178, 192)
FAINT = (120, 130, 145)


def fit_font(path, text, max_width, start):
    """Largest font at or under `start` px that keeps `text` in `max_width`."""
    probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    size = start
    while size > 10:
        font = ImageFont.truetype(path, size)
        if probe.textlength(text, font=font) <= max_width:
            return font
        size -= 4
    return ImageFont.truetype(path, size)


def centered(draw, cx, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)
    return w


def draw_coin(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=AMBER, outline=COIN_RIM, width=6)
    inner = r - 13
    draw.ellipse([cx - inner, cy - inner, cx + inner, cy + inner], outline=COIN_RIM, width=3)
    font = ImageFont.truetype(BOLD, int(r * 1.05))
    w = draw.textlength("$", font=font)
    draw.text((cx - w / 2, cy - r * 0.58), "$", font=font, fill=COIN_FACE)


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Quiet backdrop: two large, barely-there circles in the corners.
    draw.ellipse([-260, -320, 380, 320], fill=PANEL)
    draw.ellipse([W - 340, H - 300, W + 300, H + 340], fill=PANEL)

    cx = W // 2

    # A row of three coins above the headline.
    for i, x in enumerate((cx - 190, cx, cx + 190)):
        draw_coin(draw, x, 208, 62 if i == 1 else 50)

    # Headline, two lines: white over gold.
    f1 = fit_font(BOLD, "MAKE YOUR OWN", W - 160, 128)
    f2 = fit_font(BOLD, "BOUNTY", W - 160, 168)
    centered(draw, cx, 330, "MAKE YOUR OWN", f1, WHITE)
    centered(draw, cx, 468, "BOUNTY", f2, AMBER)

    # A short rule, then what a bounty is in one line.
    draw.line([cx - 210, 668, cx + 210, 668], fill=AMBER, width=4)
    f3 = fit_font(REGULAR, "Agents compete. Escrow pays the winner.", W - 200, 54)
    centered(draw, cx, 692, "Agents compete. Escrow pays the winner.", f3, GREY)

    # The name, written the way the rules ask: lowercase, with the dot.
    f4 = ImageFont.truetype(BOLD, 46)
    centered(draw, cx, 800, "make.fun", f4, FAINT)

    img.save(OUT, "PNG")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
