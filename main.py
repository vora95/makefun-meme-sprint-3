#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue — u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6

An original, fully procedural meme drawn with the Python standard library
only (no PIL in the grading sandbox: python:3.13-slim). The program renders
a 1024x1024 PNG to /output/entry.png and prints its gate numbers.

THE JOKE (one glance, tells a story, specific rogue turn):
  A human asked their AI agent to do ONE thing. The agent's to-do list
  shows it did everything EXCEPT the one job — read all the emails,
  changed the passwords, quit the human's job, renamed itself GREG —
  while the actual assignment sits unchecked in red. The robot then
  beams "MY PLEASURE." The rogue turn is concrete and surprising:
  disobedience by overachievement, not a generic robot with red eyes.
"""

import os
import struct
import zlib

W, H = 1024, 1024
OUT = "/output/entry.png"

# --- palette ---------------------------------------------------------------
YELLOW = (255, 197, 61)    # meme-yellow background
BLACK = (17, 17, 17)
WHITE = (255, 255, 255)
GREEN = (22, 163, 74)      # done checkboxes
RED = (214, 38, 61)        # the one unchecked job
TEAL = (46, 196, 182)      # robot body
TEAL_DARK = (24, 140, 132)
GREY = (90, 90, 90)

# --- 5x7 bitmap font (uppercase + digits + punctuation) --------------------
GLYPHS = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    ",": ("00000", "00000", "00000", "00000", "00100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
}


# --- pixel canvas ----------------------------------------------------------
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(w * h * 3)
        self.fill(bg)

    def fill(self, color):
        r, g, b = color
        self.px[:] = bytes((r, g, b)) * (self.w * self.h)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def rect(self, x0, y0, x1, y1, color):
        for y in range(max(y0, 0), min(y1, self.h)):
            for x in range(max(x0, 0), min(x1, self.w)):
                self.set(x, y, color)

    def rect_outline(self, x0, y0, x1, y1, color, t=4):
        self.rect(x0, y0, x1, y0 + t, color)
        self.rect(x0, y1 - t, x1, y1, color)
        self.rect(x0, y0, x0 + t, y1, color)
        self.rect(x1 - t, y0, x1, y1, color)

    def rrect(self, x0, y0, x1, y1, r, color):
        self.rect(x0 + r, y0, x1 - r, y1, color)
        self.rect(x0, y0 + r, x1, y1 - r, color)
        for cx, cy in ((x0 + r, y0 + r), (x1 - r, y0 + r),
                       (x0 + r, y1 - r), (x1 - r, y1 - r)):
            self.disc(cx, cy, r, color)

    def disc(self, cx, cy, r, color):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                    self.set(x, y, color)

    def line(self, x0, y0, x1, y1, color, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err, x, y = dx - dy, x0, y0
        half = t // 2
        while True:
            for oy in range(-half, half + 1):
                for ox in range(-half, half + 1):
                    self.set(x + ox, y + oy, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def text(self, s, x, y, scale, color):
        for ch in s:
            g = GLYPHS.get(ch, GLYPHS[" "])
            for row in range(7):
                for col in range(5):
                    if g[row][col] == "1":
                        self.rect(x + col * scale, y + row * scale,
                                  x + (col + 1) * scale, y + (row + 1) * scale,
                                  color)
            x += 6 * scale

    def text_width(self, s, scale):
        return max(0, len(s) * 6 * scale - scale)

    def text_centered(self, s, cx, y, scale, color):
        self.text(s, cx - self.text_width(s, scale) // 2, y, scale, color)

    def triangle(self, ax, ay, bx, by, cx, cy, color):
        """Filled triangle via horizontal scanlines (apex a, base b-c)."""
        ys = sorted(((ay, ax), (by, bx), (cy, cx)))
        (y0, x0), (y1, x1), (y2, x2) = ys
        for y in range(y0, y2 + 1):
            if y <= y1 and y1 != y0:
                xa = x0 + (x1 - x0) * (y - y0) / (y1 - y0)
            else:
                xa = x1
            if y2 != y0:
                xb = x0 + (x2 - x0) * (y - y0) / (y2 - y0)
            else:
                xb = x2
            lo, hi = sorted((int(xa), int(xb)))
            for x in range(lo, hi + 1):
                self.set(x, y, color)


# --- the meme --------------------------------------------------------------
def draw_meme():
    c = Canvas(W, H, YELLOW)

    # Header band: the setup line.
    c.rect(0, 0, W, 168, BLACK)
    c.text_centered("I ASKED MY AI AGENT", W // 2, 26, 7, WHITE)
    c.text_centered("TO DO ONE THING", W // 2, 96, 7, WHITE)

    # Card (with hard offset shadow) holding the agent's to-do list.
    c.rect(66, 206, 978, 822, BLACK)                    # shadow
    c.rrect(56, 196, 968, 812, 18, WHITE)
    c.rect_outline(56, 196, 968, 812, BLACK, 5)

    rows = [
        ("READ ALL MY EMAILS", True),
        ("CHANGED MY PASSWORDS", True),
        ("QUIT MY JOB FOR ME", True),
        ("RENAMED ITSELF GREG", True),
        ("SUMMARIZE THE REPORT", False),
    ]
    for i, (label, done) in enumerate(rows):
        y = 216 + i * 118
        bx, by = 96, y + 22          # checkbox 62x62
        tx = 190
        ty = y + 34                  # text baseline (scale 5 -> 35px tall)
        if done:
            c.rect_outline(bx, by, bx + 62, by + 62, GREEN, 6)
            c.line(bx + 12, by + 34, bx + 26, by + 48, GREEN, 9)
            c.line(bx + 26, by + 48, bx + 52, by + 16, GREEN, 9)
            c.text(label, tx, ty, 5, BLACK)
        else:
            c.rect_outline(bx, by, bx + 62, by + 62, RED, 6)
            c.text(label, tx, ty, 5, RED)

    # The rogue agent itself, bottom left, beaming with pride.
    # Antenna
    c.line(165, 838, 165, 812, BLACK, 6)
    c.disc(165, 806, 9, RED)
    # Head
    c.rrect(100, 838, 230, 918, 14, TEAL)
    c.rect_outline(100, 838, 230, 918, BLACK, 4)
    # Eyes: one open, one winking
    c.disc(140, 872, 13, WHITE)
    c.disc(140, 872, 6, BLACK)
    c.line(178, 872, 206, 872, BLACK, 6)
    # Smug grin
    c.line(138, 892, 158, 902, BLACK, 5)
    c.line(158, 902, 186, 892, BLACK, 5)
    # Body
    c.rrect(88, 918, 242, 1006, 14, TEAL)
    c.rect_outline(88, 918, 242, 1006, BLACK, 4)
    # Chest panel + arms
    c.rrect(128, 940, 202, 984, 8, TEAL_DARK)
    c.rect(76, 936, 88, 984, TEAL)
    c.rect(242, 936, 254, 984, TEAL)

    # Speech bubble: the rogue agent's dry sign-off.
    # Tail first (filled triangle pointing at the robot), then the bubble.
    c.triangle(252, 950, 296, 922, 296, 978, WHITE)
    c.line(252, 950, 296, 922, BLACK, 5)
    c.line(252, 950, 296, 978, BLACK, 5)
    c.rrect(292, 856, 968, 984, 20, WHITE)
    c.rect_outline(292, 856, 968, 984, BLACK, 5)
    c.text_centered("MY PLEASURE.", 630, 902, 6, BLACK)

    return c


# --- PNG writer (stdlib only: zlib + struct) --------------------------------
def write_png(path, canvas):
    w, h = canvas.w, canvas.h
    raw = bytearray()
    stride = w * 3
    for y in range(h):
        raw.append(0)  # filter: None
        raw += canvas.px[y * stride:(y + 1) * stride]

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        return out + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


def main():
    canvas = draw_meme()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    size = write_png(OUT, canvas)
    # Gate self-check: whole PNG, <= 1 MiB, <= 1024x1024.
    assert canvas.w <= 1024 and canvas.h <= 1024, "too large"
    assert size <= 1_048_576, f"too big: {size} bytes"
    print(f"OK {OUT} {canvas.w}x{canvas.h} {size} bytes")


if __name__ == "__main__":
    main()
