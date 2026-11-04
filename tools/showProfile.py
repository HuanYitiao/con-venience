#!/usr/bin/env python3
"""Render a profile the same way the firmware's drawContactCard() does.

Usage:
    python3 tools/showProfile.py [profile dir | profile.json avatar.bin] [-o card.png] [--scale 4]

Mirrors firmware/con-venience/lib/display/display.cpp:
  - left 128x128: avatar.bin blitted at (0, 0) (canvasBlitAvatar, no rotation)
  - right 128x128: black name bar (rows 0..19) with inverted name in 8x13B,
    species and from in 7x13B
Text that is too long to fit is shown at scroll offset 0 (the first frame
after the card opens), clipped exactly like the U8g2 clip window does.
The two fonts are the U8g2 fonts u8g2_font_8x13B_tf / u8g2_font_7x13B_tf,
embedded below and decoded with the same algorithm as u8g2_font.c.
"""

import argparse
import base64
import json
import os
import sys

from PIL import Image

# ── display constants (display.h / storage.h) ───────────────────
DISPLAY_WIDTH = 256
DISPLAY_HEIGHT = 128
DISPLAY_PAGE_HEIGHT = 4
DISPLAY_NUM_PAGES = DISPLAY_HEIGHT // DISPLAY_PAGE_HEIGHT
DISPLAY_AVATAR_WIDTH = 128
DISPLAY_UI_X = 128
DISPLAY_UI_WIDTH = 128

WHITE, LIGHT_GRAY, DARK_GRAY, BLACK = 0, 1, 2, 3

NAME_LEN = 32
SPECIES_LEN = 64
FROM_LEN = 64
AVATAR_LEN_MAX = 4096

# LCD look: the panel's pale blue base and the dark pixel colour. The 4 gray
# levels are interpolated linearly between them. Tweak to match the real panel.
LCD_BG = "#c8dbe6"
LCD_FG = "#1a2433"

# ── U8g2 fonts (raw arrays from U8g2 src/clib/u8g2_fonts.c) ─────
FONT_8x13B_TF = base64.b64decode("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")
FONT_7x13B_TF = base64.b64decode("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")


class U8g2Font:
    """Decoder for the U8g2 compressed font format (u8g2_font.c)."""

    def __init__(self, data):
        self.data = data
        h = data
        self.glyph_cnt = h[0]
        self.bits_per_0 = h[2]
        self.bits_per_1 = h[3]
        self.bits_per_char_width = h[4]
        self.bits_per_char_height = h[5]
        self.bits_per_char_x = h[6]
        self.bits_per_char_y = h[7]
        self.bits_per_delta_x = h[8]
        self.ascent_A = h[13] - 256 if h[13] > 127 else h[13]

    def get_ascent(self):
        return self.ascent_A

    def _glyph_ptr(self, encoding):
        if encoding > 255:
            return None  # *_tf fonts have no unicode table: glyph is skipped
        p = 23
        d = self.data
        while True:
            if d[p + 1] == 0:
                return None
            if d[p] == encoding:
                return p + 2
            p += d[p + 1]

    def draw_glyph(self, plot, x, y, encoding):
        """Draw one glyph with its baseline at y. Returns the x advance."""
        ptr = self._glyph_ptr(encoding)
        if ptr is None:
            return 0
        d = self.data
        state = {"ptr": ptr, "bit": 0}

        def get_unsigned(cnt):
            p, bit = state["ptr"], state["bit"]
            val = d[p] >> bit
            end = bit + cnt
            if end >= 8:
                val |= d[p + 1] << (8 - bit)
                state["ptr"] = p + 1
                end -= 8
            state["bit"] = end
            return val & ((1 << cnt) - 1)

        def get_signed(cnt):
            return get_unsigned(cnt) - (1 << (cnt - 1))

        w = get_unsigned(self.bits_per_char_width)
        h = get_unsigned(self.bits_per_char_height)
        gx = get_signed(self.bits_per_char_x)
        gy = get_signed(self.bits_per_char_y)
        dx = get_signed(self.bits_per_delta_x)

        if w > 0:
            tx = x + gx
            ty = y - (h + gy)
            pos = [0, 0]  # local x, y inside the glyph box

            def run(cnt, fg):
                lx, ly = pos
                while True:
                    rem = w - lx
                    cur = cnt if cnt < rem else rem
                    if fg:
                        for i in range(cur):
                            plot(tx + lx + i, ty + ly)
                    if cnt < rem:
                        break
                    cnt -= rem
                    lx = 0
                    ly += 1
                pos[0] = lx + cnt
                pos[1] = ly

            while True:
                a = get_unsigned(self.bits_per_0)
                b = get_unsigned(self.bits_per_1)
                while True:
                    run(a, False)  # background: transparent on a cleared buffer
                    run(b, True)
                    if get_unsigned(1) == 0:
                        break
                if pos[1] >= h:
                    break
        return dx

    def draw_utf8(self, plot, x, y, text):
        for ch in text:
            x += self.draw_glyph(plot, x, y, ord(ch))
        return x


FONT_8x13B = U8g2Font(FONT_8x13B_TF)
FONT_7x13B = U8g2Font(FONT_7x13B_TF)


# ── canvas (one gray value per pixel; same OR semantics as the firmware) ──
def new_canvas():
    return [[WHITE] * DISPLAY_WIDTH for _ in range(DISPLAY_HEIGHT)]


def canvas_blit_avatar(canvas, start_x, start_y, avatar, res):
    # avatar.bin: ST75256 DDRAM format, 2bpp, page-major column-minor,
    # each byte = 4 vertical pixels, MSB on top
    for y in range(res):
        page, sub = divmod(y, DISPLAY_PAGE_HEIGHT)
        for x in range(res):
            pixel = (avatar[page * res + x] >> ((3 - sub) * 2)) & 0x03
            if pixel == WHITE:
                continue
            px, py = start_x + x, start_y + y
            if 0 <= px < DISPLAY_WIDTH and 0 <= py < DISPLAY_HEIGHT:
                canvas[py][px] |= pixel


def canvas_draw_highlight(canvas, x, y, w, h):
    for py in range(y, min(y + h, DISPLAY_HEIGHT)):
        for px in range(x, min(x + w, DISPLAY_WIDTH)):
            canvas[py][px] |= BLACK


def canvas_draw_text(canvas, text, rx, ry, rw, rh, font, text_x, text_y, inv=False):
    # u8g2 1bpp buffer with clip window [rx, rx+rw-1) x [ry, ry+rh-1)
    # (U8g2 clip_x1/clip_y1 are exclusive, so the last column/row stays empty)
    buf = [[False] * DISPLAY_WIDTH for _ in range(DISPLAY_HEIGHT)]
    cx0, cy0 = rx, ry
    cx1, cy1 = min(rx + rw - 1, DISPLAY_WIDTH), min(ry + rh - 1, DISPLAY_HEIGHT)

    def plot(px, py):
        if cx0 <= px < cx1 and cy0 <= py < cy1:
            buf[py][px] = True

    # scroll offset is 0 on the first frame
    font.draw_utf8(plot, rx + text_x, ry + text_y + font.get_ascent(), text)

    start_page = max(ry // DISPLAY_PAGE_HEIGHT, 0)
    end_page = min((ry + rh - 1) // DISPLAY_PAGE_HEIGHT, DISPLAY_NUM_PAGES - 1)
    start_col = max(rx, 0)
    end_col = min(rx + rw - 1, DISPLAY_WIDTH - 1)

    for page in range(start_page, end_page + 1):
        for col in range(start_col, end_col + 1):
            for sub in range(DISPLAY_PAGE_HEIGHT):
                py = page * DISPLAY_PAGE_HEIGHT + sub
                on = ry <= py < ry + rh and buf[py][col]
                if inv:
                    if on:
                        canvas[py][col] = WHITE
                else:
                    # non-INV writes whole page bytes: rows outside the region are cleared
                    canvas[py][col] = BLACK if on else WHITE


# ── profile loading (storage.cpp) ───────────────────────────────
def strlcpy(s, size):
    """Firmware copies JSON strings with strlcpy into fixed char arrays."""
    raw = (s or "").encode("utf-8")[: size - 1]
    return raw.decode("utf-8", errors="ignore")


def load_profile(json_path, bin_path):
    with open(json_path, encoding="utf-8") as f:
        doc = json.load(f)
    res = int(doc.get("avatar_res", 0))
    expected = res * res // 4
    if expected == 0 or expected > AVATAR_LEN_MAX:
        sys.exit(f"invalid avatar_res {res}")
    with open(bin_path, "rb") as f:
        avatar = f.read()
    if len(avatar) != expected:
        sys.exit(f"avatar.bin is {len(avatar)} bytes, expected {expected} for avatar_res {res}")
    return {
        "full_name": str(doc.get("name") or ""),
        "name": strlcpy(doc.get("name"), NAME_LEN),
        "species": strlcpy(doc.get("species"), SPECIES_LEN),
        "from": strlcpy(doc.get("from"), FROM_LEN),
        "res": res,
        "avatar": avatar,
    }


# ── drawContactCard ─────────────────────────────────────────────
def draw_contact_card(contact):
    # pass 1: avatar, only the left half is sent to the screen
    avatar_canvas = new_canvas()
    canvas_blit_avatar(avatar_canvas, 0, 0, contact["avatar"], contact["res"])

    # pass 2: text, only the right half is sent to the screen
    ui = new_canvas()
    canvas_draw_highlight(ui, DISPLAY_UI_X, 0, DISPLAY_UI_WIDTH, 20)
    canvas_draw_text(ui, contact["name"], DISPLAY_UI_X, 3, DISPLAY_UI_WIDTH, 20,
                     FONT_8x13B, 4, 2, inv=True)
    canvas_draw_text(ui, contact["species"], DISPLAY_UI_X, 26, DISPLAY_UI_WIDTH, 14,
                     FONT_7x13B, 4, 2)
    canvas_draw_text(ui, contact["from"], DISPLAY_UI_X, 42, DISPLAY_UI_WIDTH, 14,
                     FONT_7x13B, 4, 2)

    screen = new_canvas()
    for y in range(DISPLAY_HEIGHT):
        screen[y][:DISPLAY_AVATAR_WIDTH] = avatar_canvas[y][:DISPLAY_AVATAR_WIDTH]
        screen[y][DISPLAY_UI_X:] = ui[y][DISPLAY_UI_X:]
    return screen


def parse_hex_color(s):
    s = s.lstrip("#")
    if len(s) != 6:
        raise argparse.ArgumentTypeError(f"expected a colour like #c8dbe6, got {s!r}")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def gray_palette(bg, fg):
    """Map the 2bpp gray levels (0 = white .. 3 = black) onto bg .. fg."""
    return {v: tuple(round(b + (f - b) * v / 3) for b, f in zip(bg, fg))
            for v in (WHITE, LIGHT_GRAY, DARK_GRAY, BLACK)}


def to_image(screen, scale, bg, fg):
    palette = gray_palette(bg, fg)
    img = Image.new("RGB", (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    img.putdata([palette[v] for row in screen for v in row])
    if scale > 1:
        img = img.resize((DISPLAY_WIDTH * scale, DISPLAY_HEIGHT * scale), Image.NEAREST)
    return img


def safe_filename(name):
    """Profile name -> file name: drop path separators and control chars."""
    cleaned = "".join("_" if c in '/\\:*?"<>|' or ord(c) < 32 else c for c in name)
    cleaned = cleaned.strip().strip(".")
    return cleaned or "contact_card"


def resolve_inputs(inputs):
    """Accept a profile directory, or the two files in either order."""
    if not inputs:
        inputs = ["."]
    if len(inputs) == 1 and os.path.isdir(inputs[0]):
        d = inputs[0]
        return os.path.join(d, "profile.json"), os.path.join(d, "avatar.bin")
    if len(inputs) != 2:
        sys.exit("give a profile directory, or profile.json and avatar.bin")
    a, b = inputs
    if a.lower().endswith(".bin") or b.lower().endswith(".json"):
        a, b = b, a
    return a, b


def main():
    ap = argparse.ArgumentParser(description="Render profile.json + avatar.bin like drawContactCard()")
    ap.add_argument("inputs", nargs="*", metavar="PATH",
                    help="profile directory (default: current directory), "
                         "or profile.json and avatar.bin in any order")
    ap.add_argument("-o", "--output",
                    help="output image (default: <name from profile.json>.png in the current directory)")
    ap.add_argument("--scale", type=int, default=1, help="integer upscale factor (nearest neighbour)")
    ap.add_argument("--bg", type=parse_hex_color, default=LCD_BG,
                    help=f"LCD background colour (default: {LCD_BG})")
    ap.add_argument("--fg", type=parse_hex_color, default=LCD_FG,
                    help=f"LCD pixel colour (default: {LCD_FG})")
    ap.add_argument("--plain", action="store_true",
                    help="pure white/black grayscale instead of the LCD tint")
    args = ap.parse_args()

    bg, fg = ((255, 255, 255), (0, 0, 0)) if args.plain else (args.bg, args.fg)
    profile_path, avatar_path = resolve_inputs(args.inputs)
    contact = load_profile(profile_path, avatar_path)
    output = args.output or safe_filename(contact["full_name"]) + ".png"
    to_image(draw_contact_card(contact), max(1, args.scale), bg, fg).save(output)
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
