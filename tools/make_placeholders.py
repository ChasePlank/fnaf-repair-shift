"""Generates placeholder art and audio for Five Nights: Repair Shift.

Run from the repo root:  python3 tools/make_placeholders.py
Replace any file in game/images or game/audio with real art/sound using the
same filename and the game will pick it up automatically.
"""
import math
import os
import random
import struct
import wave

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "game", "images")
AUD = os.path.join(ROOT, "game", "audio")
os.makedirs(os.path.join(IMG, "bg"), exist_ok=True)
os.makedirs(os.path.join(IMG, "chars"), exist_ok=True)
os.makedirs(AUD, exist_ok=True)

W, H = 1920, 1080
random.seed(87)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_B if bold else FONT, size)
    except OSError:
        return ImageFont.load_default()


# ---------------------------------------------------------------- backgrounds

def gradient(top, bottom):
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return im


def finish(im, name, grain=18, vignette=0.75):
    # grain
    noise = Image.effect_noise((W, H), grain).convert("L")
    im = Image.blend(im, Image.merge("RGB", (noise, noise, noise)), 0.06)
    # vignette
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).ellipse([-W * 0.15, -H * 0.25, W * 1.15, H * 1.25], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(220))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    im = Image.composite(im, Image.blend(im, dark, vignette), mask)
    im.save(os.path.join(IMG, "bg", name + ".png"))


def checker_floor(d, horizon, c1, c2, rows=10):
    # perspective checkerboard floor, the classic pizzeria tile
    for r in range(rows):
        y0 = horizon + (H - horizon) * (r / rows) ** 1.6
        y1 = horizon + (H - horizon) * ((r + 1) / rows) ** 1.6
        n = 16
        for c in range(-n, n):
            def x(col, y):
                spread = (y - horizon) / (H - horizon) * 3.0 + 0.2
                return W / 2 + col * 120 * spread
            col = c1 if (r + c) % 2 == 0 else c2
            d.polygon([(x(c, y0), y0), (x(c + 1, y0), y0), (x(c + 1, y1), y1), (x(c, y1), y1)], fill=col)


def bg_exterior():
    im = gradient((5, 6, 18), (20, 18, 30))
    d = ImageDraw.Draw(im)
    for _ in range(140):
        x, y = random.randint(0, W), random.randint(0, 500)
        d.point((x, y), fill=(200, 200, 220))
    d.rectangle([0, 820, W, H], fill=(14, 14, 16))
    d.rectangle([360, 380, 1560, 830], fill=(32, 26, 24))
    d.polygon([(330, 380), (960, 250), (1590, 380)], fill=(26, 20, 20))
    d.rectangle([860, 600, 1060, 830], fill=(8, 8, 8))
    for x in (480, 1300):
        d.rectangle([x, 520, x + 160, 640], fill=(16, 16, 20))
        d.line([x, 520, x + 160, 640], fill=(50, 50, 55), width=4)
    d.rectangle([620, 410, 1300, 490], fill=(40, 10, 10))
    d.text((960, 450), "FREDDY FAZBEAR'S PIZZA", font=font(46, True), fill=(120, 40, 30), anchor="mm")
    finish(im, "exterior")


def bg_office():
    im = gradient((18, 20, 22), (8, 8, 9))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 120], fill=(12, 12, 12))
    # doorways
    for x0 in (40, 1560):
        d.rectangle([x0, 180, x0 + 320, 900], fill=(3, 3, 4))
        d.rectangle([x0 + 340 if x0 < 900 else x0 - 60, 480, x0 + 380 if x0 < 900 else x0 - 20, 560], fill=(120, 20, 20))
    # posters
    d.rectangle([520, 200, 760, 520], fill=(70, 50, 30))
    d.text((640, 360), "CELEBRATE!", font=font(30, True), fill=(30, 20, 10), anchor="mm")
    d.rectangle([1160, 220, 1380, 460], fill=(40, 40, 60))
    # desk + monitors
    d.rectangle([380, 760, 1540, H], fill=(36, 34, 30))
    for x0 in (560, 880, 1180):
        d.rectangle([x0, 560, x0 + 240, 760], fill=(20, 22, 20))
        d.rectangle([x0 + 18, 578, x0 + 222, 740], fill=(16, 40, 22))
    d.ellipse([1360, 640, 1480, 760], fill=(28, 28, 28))  # fan
    finish(im, "office")


def bg_dining():
    im = gradient((20, 14, 18), (10, 8, 10))
    d = ImageDraw.Draw(im)
    checker_floor(d, 620, (34, 32, 30), (10, 10, 10))
    for x in range(120, W, 260):
        d.polygon([(x, 0), (x + 60, 0), (x + 30, 160)], fill=(90, 20, 40) if x % 520 else (30, 50, 90))
    for x in (300, 960, 1620):
        d.rectangle([x - 260, 700, x + 260, 760], fill=(60, 60, 64))
        for k in range(-3, 4):
            d.polygon([(x + k * 70, 690), (x + k * 70 + 20, 640), (x + k * 70 + 40, 690)], fill=(70, 30, 40))
    finish(im, "dining")


def bg_stage():
    im = gradient((24, 10, 14), (6, 4, 6))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 90], fill=(70, 10, 16))
    for x in range(0, W, 90):
        d.ellipse([x, 50, x + 90, 130], fill=(70, 10, 16))
    d.text((960, 210), "* SHOW STAGE *", font=font(54, True), fill=(80, 70, 40), anchor="mm")
    d.rectangle([140, 780, 1780, 880], fill=(40, 26, 18))
    d.rectangle([140, 880, 1780, H], fill=(22, 14, 10))
    for i, x in enumerate(range(160, 1780, 70)):
        d.ellipse([x, 120 + (i % 2) * 20, x + 18, 138 + (i % 2) * 20], fill=(150, 130, 60) if i % 3 else (40, 40, 40))
    finish(im, "stage")


def bg_cove():
    im = gradient((14, 6, 22), (4, 2, 8))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 820, W, H], fill=(18, 12, 10))
    # curtains
    for side in (0, 1):
        for i in range(9):
            x = (i * 105) if side == 0 else W - (i + 1) * 105
            col = (60 + (i % 2) * 14, 20, 90 + (i % 2) * 20)
            d.rectangle([x, 0, x + 105, 860 - abs(4 - i) * 20], fill=col)
    for i in range(30):
        x = 220 + i * 50
        d.polygon([(x, 0), (x + 25, 40), (x + 50, 0)], fill=(80, 20, 120))
    d.rectangle([700, 180, 1220, 300], fill=(20, 8, 30))
    d.text((960, 240), "PIRATE COVE", font=font(52, True), fill=(160, 120, 40), anchor="mm")
    d.rectangle([810, 330, 1110, 420], fill=(110, 110, 110))
    d.text((960, 375), "SORRY! OUT OF ORDER", font=font(24, True), fill=(20, 20, 20), anchor="mm")
    finish(im, "cove")


def bg_kitchen():
    im = gradient((16, 18, 16), (6, 7, 6))
    d = ImageDraw.Draw(im)
    for y in range(0, 760, 80):
        for x in range(0, W, 80):
            d.rectangle([x + 2, y + 2, x + 78, y + 78], outline=(30, 34, 30), width=2)
    d.rectangle([0, 760, W, H], fill=(24, 24, 22))
    d.rectangle([180, 520, 900, 780], fill=(50, 52, 54))
    d.rectangle([1100, 300, 1600, 780], fill=(40, 42, 44))
    for i in range(4):
        d.ellipse([240 + i * 160, 480, 360 + i * 160, 540], fill=(30, 30, 30))
    finish(im, "kitchen")


def bg_parts():
    im = gradient((14, 14, 18), (4, 4, 6))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 820, W, H], fill=(16, 14, 12))
    d.rectangle([0, 0, W, 60], fill=(6, 6, 6))
    d.ellipse([880, 40, 1040, 90], fill=(190, 180, 120))
    beam = Image.new("L", (W, H), 0)
    ImageDraw.Draw(beam).polygon([(900, 70), (1020, 70), (1500, H), (420, H)], fill=60)
    beam = beam.filter(ImageFilter.GaussianBlur(40))
    im = Image.composite(Image.new("RGB", (W, H), (110, 105, 80)), im, beam)
    d = ImageDraw.Draw(im)
    # shelves with heads/parts
    for y in (220, 420, 620):
        d.rectangle([60, y, 520, y + 20], fill=(50, 40, 30))
        d.rectangle([1400, y, 1860, y + 20], fill=(50, 40, 30))
        for x in (100, 260, 400, 1440, 1600, 1740):
            d.ellipse([x, y - 100, x + 90, y], fill=(40, 34, 30))
            d.ellipse([x + 22, y - 70, x + 36, y - 56], fill=(10, 10, 10))
            d.ellipse([x + 54, y - 70, x + 68, y - 56], fill=(10, 10, 10))
    # workbench
    d.rectangle([560, 800, 1360, 860], fill=(66, 50, 34))
    d.text((960, 160), "PARTS & SERVICE", font=font(40, True), fill=(70, 70, 60), anchor="mm")
    finish(im, "parts", vignette=0.6)


def bg_menu():
    im = gradient((10, 4, 6), (0, 0, 0))
    d = ImageDraw.Draw(im)
    # four sets of eyes in the dark
    for i, (x, y, c) in enumerate([(1180, 380, (220, 220, 255)), (1400, 300, (255, 60, 60)),
                                   (1600, 420, (255, 220, 120)), (1340, 560, (255, 255, 255))]):
        glow = Image.new("L", (W, H), 0)
        g = ImageDraw.Draw(glow)
        g.ellipse([x - 40, y - 14, x + 4, y + 14], fill=255)
        g.ellipse([x + 46, y - 14, x + 90, y + 14], fill=255)
        glow = glow.filter(ImageFilter.GaussianBlur(14))
        im = Image.composite(Image.new("RGB", (W, H), c), im, glow)
        d = ImageDraw.Draw(im)
        d.ellipse([x - 28, y - 7, x - 8, y + 7], fill=c)
        d.ellipse([x + 58, y - 7, x + 78, y + 7], fill=c)
    finish(im, "menu", vignette=0.5)
    im2 = Image.open(os.path.join(IMG, "bg", "menu.png"))
    os.makedirs(os.path.join(ROOT, "game", "gui"), exist_ok=True)
    im2.save(os.path.join(ROOT, "game", "gui", "main_menu.png"))
    Image.new("RGB", (W, H), (6, 4, 5)).save(os.path.join(ROOT, "game", "gui", "game_menu.png"))


# ----------------------------------------------------------------- characters

CW, CH = 820, 1060

CHARS = {
    "freddy": dict(fur=(110, 66, 36), belly=(170, 120, 70), eye=(120, 170, 255), ears="round", hat=True,
                   tie=(20, 20, 20)),
    "bonnie": dict(fur=(80, 70, 150), belly=(150, 140, 200), eye=(230, 60, 120), ears="long", tie=(170, 20, 30)),
    "chica": dict(fur=(220, 180, 40), belly=(240, 220, 150), eye=(200, 60, 160), ears="feather", beak=True,
                  bib=True),
    "foxy": dict(fur=(150, 40, 30), belly=(200, 170, 130), eye=(255, 220, 80), ears="pointed", patch=True,
                 hook=True),
    "goldenfreddy": dict(fur=(185, 145, 40), belly=(215, 185, 110), eye=(255, 255, 255), ears="round", hat=True,
                         tie=(25, 25, 60), hollow=True),
    # ---- Chapter 2: Toys (shiny plastic, rosy cheeks)
    "toyfreddy": dict(fur=(150, 85, 40), belly=(225, 175, 110), eye=(110, 160, 255), ears="round", hat=True,
                      tie=(20, 20, 20), toy=True),
    "toybonnie": dict(fur=(80, 150, 230), belly=(235, 240, 255), eye=(60, 200, 90), ears="long", tie=(200, 30, 40),
                      toy=True),
    "toychica": dict(fur=(250, 210, 40), belly=(255, 235, 170), eye=(80, 150, 255), ears="feather", beak=True,
                     bib=True, toy=True),
    "mangle": dict(fur=(238, 238, 238), belly=(240, 140, 190), eye=(255, 220, 80), ears="pointed", tie=(200, 30, 60),
                   toy=True, mangle=True),
    # ---- Chapter 2: Withereds (the Chapter 1 crew, decayed further)
    "witheredfreddy": dict(fur=(90, 54, 30), belly=(140, 100, 60), eye=(120, 170, 255), ears="round", hat=True,
                           tie=(20, 20, 20), withered=True),
    "witheredbonnie": dict(fur=(64, 56, 120), belly=(120, 112, 160), eye=(255, 40, 40), ears="long",
                           tie=(140, 20, 30), withered=True, faceless=True),
    "witheredchica": dict(fur=(180, 148, 36), belly=(200, 180, 120), eye=(200, 60, 160), ears="feather", beak=True,
                          bib=True, withered=True),
    "witheredfoxy": dict(fur=(120, 34, 26), belly=(170, 140, 110), eye=(255, 220, 80), ears="pointed", patch=True,
                         hook=True, withered=True),
}

ENDO = (95, 95, 100)
ENDO_D = (55, 55, 60)


def endo_limb(d, pts, w=22):
    d.line(pts, fill=ENDO, width=w, joint="curve")
    for p in pts:
        d.ellipse([p[0] - w * 0.75, p[1] - w * 0.75, p[0] + w * 0.75, p[1] + w * 0.75], fill=ENDO_D)


def draw_char(key, stage):
    """stage: 0 broken, 1 arms fixed, 2 arms+legs fixed, 3 fully repaired"""
    c = CHARS[key]
    fur = c["fur"]
    if stage < 3:
        fur = tuple(int(v * 0.72) for v in fur)  # dusty
    belly = c["belly"] if stage == 3 else tuple(int(v * 0.7) for v in c["belly"])
    im = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = CW // 2
    tilt = 0 if stage == 3 else 18

    # ---- legs
    if stage >= 2:
        for s in (-1, 1):
            d.rounded_rectangle([cx + s * 110 - 60, 740, cx + s * 110 + 60, 980], 40, fill=fur)
            d.ellipse([cx + s * 110 - 90, 940, cx + s * 110 + 90, 1040], fill=fur)
    else:
        for s in (-1, 1):
            endo_limb(d, [(cx + s * 100, 760), (cx + s * 120, 880), (cx + s * 100 + (s * 40 if s > 0 else 0), 1000)])
        d.line([(cx + 60, 1000), (cx + 180, 1010)], fill=ENDO_D, width=10)

    # ---- torso
    d.rounded_rectangle([cx - 190, 420, cx + 190, 790], 120, fill=fur)
    d.ellipse([cx - 130, 500, cx + 130, 770], fill=belly)
    if c.get("bib"):
        d.rounded_rectangle([cx - 120, 520, cx + 120, 700], 30, fill=(245, 245, 240) if stage == 3 else (150, 150, 140))
        d.text((cx, 580), "LET'S", font=font(36, True), fill=(200, 60, 60), anchor="mm")
        d.text((cx, 630), "EAT!!!", font=font(36, True), fill=(200, 60, 60), anchor="mm")
    if stage < 3:
        # torn panel showing wires
        d.polygon([(cx + 40, 560), (cx + 150, 540), (cx + 130, 660), (cx + 30, 680)], fill=(25, 22, 22))
        for i in range(4):
            d.line([(cx + 50 + i * 20, 570), (cx + 60 + i * 18, 670)], fill=[(200, 40, 40), (40, 120, 200), (220, 200, 40), (60, 160, 60)][i], width=5)

    # ---- arms
    if stage >= 1:
        for s in (-1, 1):
            d.rounded_rectangle([cx + s * 230 - 50, 450, cx + s * 230 + 50, 720], 45, fill=fur)
            if c.get("hook") and s == 1:
                d.rectangle([cx + 220, 710, cx + 240, 760], fill=(160, 160, 165))
                d.arc([cx + 200, 740, cx + 290, 830], 180, 90, fill=(180, 180, 185), width=16)
            else:
                d.ellipse([cx + s * 230 - 55, 690, cx + s * 230 + 55, 790], fill=fur)
    else:
        endo_limb(d, [(cx - 190, 470), (cx - 250, 600), (cx - 240, 720)])
        d.line([(cx + 190, 470), (cx + 240, 540)], fill=ENDO, width=22)
        for k in range(3):
            d.line([(cx + 240, 540), (cx + 260 + k * 12, 580 + k * 8)], fill=(200 - k * 60, 60 + k * 50, 50), width=4)

    # ---- head (rotated if broken)
    head = Image.new("RGBA", (CW, 480), (0, 0, 0, 0))
    h = ImageDraw.Draw(head)
    hx, hy = cx, 260
    ears = c["ears"]
    if ears == "round":
        for s in (-1, 1):
            h.ellipse([hx + s * 150 - 60, hy - 200, hx + s * 150 + 60, hy - 80], fill=fur)
    elif ears == "long":
        for s in (-1, 1):
            if stage < 3 and s == 1:
                continue  # missing ear
            h.rounded_rectangle([hx + s * 90 - 40, hy - 330, hx + s * 90 + 40, hy - 100], 40, fill=fur)
    elif ears == "pointed":
        for s in (-1, 1):
            h.polygon([(hx + s * 80, hy - 120), (hx + s * 190, hy - 260), (hx + s * 190, hy - 90)], fill=fur)
    elif ears == "feather":
        for k in range(3):
            h.polygon([(hx - 30 + k * 30, hy - 150), (hx - 60 + k * 40, hy - 230), (hx + k * 30, hy - 160)], fill=fur)
    h.ellipse([hx - 180, hy - 170, hx + 180, hy + 150], fill=fur)
    if c.get("hat"):
        h.rectangle([hx - 70, hy - 260, hx + 70, hy - 150], fill=(20, 20, 20))
        h.rectangle([hx - 100, hy - 160, hx + 100, hy - 140], fill=(20, 20, 20))
    # muzzle
    h.ellipse([hx - 110, hy - 10, hx + 110, hy + 140], fill=belly)
    if c.get("beak"):
        h.polygon([(hx - 110, hy + 30), (hx + 110, hy + 30), (hx, hy + 160)], fill=(240, 130, 30))
    else:
        h.ellipse([hx - 30, hy - 10, hx + 30, hy + 30], fill=(25, 15, 15))
    if c.get("toy"):
        for sgn in (-1, 1):
            h.ellipse([hx + sgn * 130 - 26, hy + 30, hx + sgn * 130 + 26, hy + 70], fill=(240, 110, 130))
        h.ellipse([hx - 120, hy - 150, hx - 40, hy - 110], fill=(255, 255, 255, 90))
    # jaw / teeth
    jaw_open = 0 if stage == 3 else 40
    h.rectangle([hx - 90, hy + 100 + jaw_open, hx + 90, hy + 150 + jaw_open], fill=fur)
    for k in range(-3, 4):
        h.rectangle([hx + k * 24 - 9, hy + 92, hx + k * 24 + 9, hy + 116], fill=(225, 225, 215))
        h.rectangle([hx + k * 24 - 9, hy + 96 + jaw_open, hx + k * 24 + 9, hy + 118 + jaw_open], fill=(225, 225, 215))
    # eyes
    for s in (-1, 1):
        ex = hx + s * 75
        h.ellipse([ex - 50, hy - 90, ex + 50, hy + 10], fill=(240, 240, 240) if stage else (30, 30, 30))
        if c.get("patch") and s == 1:
            h.ellipse([ex - 54, hy - 94, ex + 54, hy + 14], fill=(15, 15, 15))
            h.line([(hx - 60, hy - 160), (ex + 50, hy - 40)], fill=(15, 15, 15), width=8)
            continue
        if stage == 0 and s == -1:
            # dangling endo eye
            h.line([(ex, hy - 40), (ex - 10, hy + 40)], fill=(150, 30, 30), width=5)
            h.ellipse([ex - 22, hy + 30, ex + 2, hy + 54], fill=(220, 220, 220))
            continue
        if c.get("hollow"):
            h.ellipse([ex - 50, hy - 90, ex + 50, hy + 10], fill=(5, 5, 5))
            if stage == 3:
                h.ellipse([ex - 9, hy - 49, ex + 9, hy - 31], fill=(255, 255, 255))
            continue
        h.ellipse([ex - 24, hy - 64, ex + 24, hy - 16], fill=c["eye"])
        h.ellipse([ex - 10, hy - 50, ex + 10, hy - 30], fill=(10, 10, 10))
    if c.get("tie"):
        pass
    if c.get("faceless") and stage < 3:
        # Withered Bonnie: no face, just endoskeleton
        h.ellipse([hx - 170, hy - 110, hx + 170, hy + 160], fill=(12, 12, 14))
        for sgn in (-1, 1):
            h.ellipse([hx + sgn * 60 - 22, hy - 60, hx + sgn * 60 + 22, hy - 16], fill=(70, 70, 75))
            h.ellipse([hx + sgn * 60 - 8, hy - 46, hx + sgn * 60 + 8, hy - 30], fill=c["eye"])
        for k in range(-3, 4):
            h.rectangle([hx + k * 22 - 8, hy + 90, hx + k * 22 + 8, hy + 112], fill=(200, 200, 190))
        h.rectangle([hx - 80, hy + 112, hx + 80, hy + 124], fill=ENDO)
    head = head.rotate(tilt, center=(hx, hy), resample=Image.BICUBIC)
    im.alpha_composite(head, (0, 0))
    d = ImageDraw.Draw(im)
    if c.get("tie"):
        d.polygon([(cx, 440), (cx - 60, 400), (cx - 60, 480)], fill=c["tie"])
        d.polygon([(cx, 440), (cx + 60, 400), (cx + 60, 480)], fill=c["tie"])
        d.ellipse([cx - 16, 424, cx + 16, 456], fill=c["tie"])
    # glow for full repair
    if stage == 3:
        glow = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
        ImageDraw.Draw(glow).ellipse([60, 60, CW - 60, CH - 60], fill=c["eye"] + (40,))
        glow = glow.filter(ImageFilter.GaussianBlur(80))
        base = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
        base.alpha_composite(glow)
        base.alpha_composite(im)
        im = base
    if c.get("withered") and stage < 3:
        d = ImageDraw.Draw(im)
        for (x0, y0, r) in [(cx - 120, 640, 40), (cx + 90, 470, 30), (cx - 40, 760, 26), (cx + 150, 700, 34)]:
            d.ellipse([x0 - r, y0 - r, x0 + r, y0 + r], fill=(20, 16, 14))
            d.line([(x0 - r + 8, y0), (x0 + r - 8, y0 + 6)], fill=ENDO, width=6)
    if c.get("mangle") and stage < 3:
        d = ImageDraw.Draw(im)
        random.seed(7 + stage)
        for _ in range(14 - stage * 4):
            pts = [(random.randint(80, CW - 80), random.randint(300, CH - 40)) for _ in range(3)]
            d.line(pts, fill=random.choice([ENDO, ENDO_D, (220, 220, 220), (240, 140, 190)]), width=12, joint="curve")
        # second endo head
        d.ellipse([cx + 160, 860 - stage * 60, cx + 300, 980 - stage * 60], fill=ENDO_D)
        d.ellipse([cx + 190, 890 - stage * 60, cx + 220, 920 - stage * 60], fill=(255, 220, 80))
        d.ellipse([cx + 240, 890 - stage * 60, cx + 270, 920 - stage * 60], fill=(10, 10, 10))
    if c.get("hollow") and stage < 3:
        d = ImageDraw.Draw(im)
        for (x0, y0, x1, y1) in [(cx - 150, 450, cx - 60, 560), (cx - 120, 600, cx - 20, 700), (cx + 60, 120, cx + 140, 220)]:
            d.polygon([(x0, y0), (x1, y0 + 20), (x1 - 20, y1), (x0 + 10, y1 - 10)], fill=(18, 14, 10))
        for k in range(6):
            x = cx - 170 + k * 60
            d.line([(x, 430 + (k % 3) * 40), (x + 30, 470 + (k % 2) * 50), (x + 10, 520)], fill=(60, 45, 15), width=4)
    names = ["broken", "arms", "legs", "fixed"]
    im.save(os.path.join(IMG, "chars", f"{key}_{names[stage]}.png"))


def draw_puppet():
    im = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = CW // 2
    # long thin limbs
    for sgn in (-1, 1):
        d.line([(cx + sgn * 70, 440), (cx + sgn * 230, 640), (cx + sgn * 260, 860)], fill=(12, 12, 14), width=34, joint="curve")
        d.line([(cx + sgn * 40, 760), (cx + sgn * 60, 1050)], fill=(12, 12, 14), width=40)
        for k in range(3):
            d.rectangle([cx + sgn * (226 + 0) - 18, 600 + k * 120, cx + sgn * 226 + 18, 616 + k * 120], fill=(235, 235, 235))
            d.rectangle([cx + sgn * 50 - 22, 860 + k * 60, cx + sgn * 50 + 22, 874 + k * 60], fill=(235, 235, 235))
    d.rounded_rectangle([cx - 90, 400, cx + 90, 800], 60, fill=(12, 12, 14))
    for k in range(3):
        d.ellipse([cx - 16, 470 + k * 80, cx + 16, 502 + k * 80], fill=(235, 235, 235))
    # mask
    d.ellipse([cx - 120, 120, cx + 120, 420], fill=(240, 240, 240))
    for sgn in (-1, 1):
        d.ellipse([cx + sgn * 50 - 30, 210, cx + sgn * 50 + 30, 270], fill=(5, 5, 5))
        d.ellipse([cx + sgn * 50 - 6, 232, cx + sgn * 50 + 6, 244], fill=(255, 255, 255))
        d.line([(cx + sgn * 50, 270), (cx + sgn * 52, 330)], fill=(140, 40, 200), width=10)
        d.ellipse([cx + sgn * 80 - 30, 290, cx + sgn * 80 + 30, 340], fill=(220, 30, 50))
    d.arc([cx - 60, 300, cx + 60, 390], 20, 160, fill=(220, 30, 50), width=12)
    for st in ("broken", "arms", "legs", "fixed"):
        im.save(os.path.join(IMG, "chars", f"puppet_{st}.png"))


def draw_musicbox(stage):
    """stage 0 broken, 1 crank fixed, 2 comb/spring fixed, 3 fully repaired"""
    im = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = CW // 2
    gold = (200, 160, 60) if stage == 3 else (120, 96, 44)
    d.rectangle([cx - 260, 560, cx + 260, 960], fill=(70, 30, 70) if stage == 3 else (40, 22, 40))
    d.rectangle([cx - 280, 520, cx + 280, 580], fill=gold)
    for k in range(4):
        d.rectangle([cx - 260 + k * 150, 560, cx - 230 + k * 150, 960], fill=(150, 30, 60))
    if stage < 3:
        d.polygon([(cx - 100, 560), (cx + 40, 640), (cx - 60, 760), (cx - 160, 680)], fill=(15, 10, 15))
    if stage >= 2:
        for k in range(12):
            d.rectangle([cx - 120 + k * 20, 500, cx - 110 + k * 20, 520 - (k % 4) * 6], fill=(220, 220, 220))
    else:
        d.line([(cx - 120, 510), (cx + 40, 470)], fill=(160, 160, 160), width=6)
    # crank
    if stage >= 1:
        d.rectangle([cx + 280, 720, cx + 360, 740], fill=gold)
        d.rectangle([cx + 340, 660, cx + 360, 740], fill=gold)
        d.ellipse([cx + 326, 630, cx + 374, 678], fill=(240, 240, 240))
    else:
        d.line([(cx + 380, 960), (cx + 450, 1000)], fill=gold, width=18)
    if stage == 3:
        glow = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
        ImageDraw.Draw(glow).ellipse([100, 400, CW - 100, CH], fill=(200, 160, 255, 50))
        glow = glow.filter(ImageFilter.GaussianBlur(60))
        glow.alpha_composite(im)
        im = glow
    names = ["broken", "arms", "legs", "fixed"]
    im.save(os.path.join(IMG, "chars", f"musicbox_{names[stage]}.png"))


def bg_partyroom():
    im = gradient((28, 20, 40), (10, 8, 14))
    d = ImageDraw.Draw(im)
    checker_floor(d, 640, (40, 36, 50), (12, 10, 16))
    for x in range(60, W, 160):
        d.polygon([(x, 0), (x + 80, 0), (x + 40, 120)], fill=[(200, 60, 90), (60, 140, 220), (240, 200, 60)][(x // 160) % 3])
    for x in (360, 1560):
        d.rectangle([x - 240, 700, x + 240, 750], fill=(80, 80, 96))
    d.text((960, 220), "PARTY ROOM 3", font=font(48, True), fill=(90, 80, 120), anchor="mm")
    finish(im, "partyroom")


def bg_prize():
    im = gradient((18, 10, 24), (4, 2, 6))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 840, W, H], fill=(20, 14, 20))
    d.rectangle([520, 200, 1400, 300], fill=(40, 16, 50))
    d.text((960, 250), "PRIZE CORNER", font=font(56, True), fill=(220, 180, 60), anchor="mm")
    d.rectangle([760, 560, 1160, 860], fill=(60, 20, 60))
    d.rectangle([940, 560, 980, 860], fill=(200, 160, 60))
    d.rectangle([760, 690, 1160, 730], fill=(200, 160, 60))
    for x in (200, 360, 1560, 1720):
        d.rectangle([x - 60, 520, x + 60, 840], fill=(36, 30, 40))
        d.ellipse([x - 40, 440, x + 40, 520], fill=(140, 40, 60))
    finish(im, "prize")


def bg_office2():
    im = gradient((14, 16, 22), (6, 6, 8))
    d = ImageDraw.Draw(im)
    d.rectangle([700, 160, 1220, 760], fill=(3, 3, 5))  # long hallway
    d.polygon([(700, 160), (860, 360), (860, 560), (700, 760)], fill=(16, 16, 20))
    d.polygon([(1220, 160), (1060, 360), (1060, 560), (1220, 760)], fill=(16, 16, 20))
    for x0 in (120, 1560):
        d.rectangle([x0, 400, x0 + 240, 680], fill=(4, 4, 6))
    d.rectangle([300, 760, 1620, H], fill=(34, 34, 40))
    d.rectangle([420, 640, 640, 760], fill=(30, 30, 34))
    d.rectangle([440, 660, 620, 740], fill=(10, 30, 50))
    d.text((960, 880), "TOY BOX  •  FREDDY MASK  •  FLASHLIGHT", font=font(28), fill=(70, 70, 80), anchor="mm")
    finish(im, "office2")


def bg_kidscove():
    im = gradient((26, 12, 26), (8, 4, 8))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 820, W, H], fill=(30, 18, 26))
    for i in range(40):
        x, y = random.randint(0, W), random.randint(840, H)
        d.rectangle([x, y, x + 40, y + 20], fill=random.choice([(200, 60, 90), (60, 140, 220), (240, 200, 60)]))
    d.text((960, 220), "KID'S COVE", font=font(60, True), fill=(220, 120, 180), anchor="mm")
    d.text((960, 300), "please don't take apart the entertainment", font=font(26), fill=(120, 80, 100), anchor="mm")
    finish(im, "kidscove")


# ------------------------------------------------------------ Chapter 3 art

def bg_fright(name, label, accent=(60, 70, 40), kind="room"):
    im = gradient((16, 18, 12), (4, 5, 3))
    d = ImageDraw.Draw(im)
    if kind == "office":
        d.rectangle([640, 180, 1280, 640], fill=(8, 10, 6))  # window
        d.rectangle([640, 180, 1280, 640], outline=(50, 56, 36), width=10)
        d.rectangle([1500, 200, 1800, 840], fill=(3, 3, 2))  # doorway
        d.rectangle([200, 760, 1720, H], fill=(30, 30, 24))
        for x0 in (300, 520):
            d.rectangle([x0, 620, x0 + 180, 760], fill=(26, 26, 22))
            d.rectangle([x0 + 14, 634, x0 + 166, 742], fill=(12, 26, 14))
        d.ellipse([1280, 680, 1400, 760], fill=(40, 36, 20))  # fan
    elif kind == "hall":
        d.polygon([(0, 0), (760, 380), (760, 700), (0, H)], fill=(22, 24, 16))
        d.polygon([(W, 0), (1160, 380), (1160, 700), (W, H)], fill=(22, 24, 16))
        d.rectangle([760, 380, 1160, 700], fill=(2, 2, 2))
        for i in range(6):
            x = 120 + i * 110
            d.rectangle([x, 300 + i * 20, x + 60, 360 + i * 20], fill=(60, 50, 40))
    elif kind == "arcade":
        d.rectangle([0, 820, W, H], fill=(20, 18, 14))
        for i, x in enumerate(range(140, W - 100, 280)):
            d.rectangle([x, 380, x + 180, 840], fill=(24, 22, 26))
            d.rectangle([x + 20, 420, x + 160, 560], fill=(10, 40, 30) if i == 3 else (6, 6, 8))
    elif kind == "storage":
        d.rectangle([0, 840, W, H], fill=(24, 20, 14))
        for i in range(14):
            x, y = random.randint(40, W - 300), random.randint(500, 820)
            d.rectangle([x, y, x + random.randint(160, 300), y + random.randint(80, 180)], fill=(70 + i * 3, 56, 34))
        for x in (300, 1500):
            d.ellipse([x - 60, 360, x + 60, 480], fill=(110, 90, 50))  # hanging masks
            d.ellipse([x - 34, 396, x - 10, 420], fill=(10, 10, 10)); d.ellipse([x + 10, 396, x + 34, 420], fill=(10, 10, 10))
    elif kind == "vent":
        im = gradient((26, 26, 24), (8, 8, 8))
        d = ImageDraw.Draw(im)
        for k in range(8):
            m = k * 60
            d.rectangle([200 + m, 100 + m * 0.55, W - 200 - m, H - 100 - m * 0.55], outline=(46 - k * 3, 46 - k * 3, 42 - k * 3), width=8)
        d.rectangle([800, 440, 1120, 640], fill=(2, 2, 2))
    elif kind == "attraction":
        d.rectangle([0, 820, W, H], fill=(22, 18, 14))
        d.rectangle([560, 520, 1360, 640], fill=(70, 50, 30))  # plywood stage
        for x in range(560, 1360, 40):
            d.line([(x, 520), (x, 640)], fill=(56, 40, 24), width=3)
        d.polygon([(400, 0), (560, 520), (360, 520)], fill=(60, 20, 30))
        d.polygon([(1520, 0), (1360, 520), (1560, 520)], fill=(60, 20, 30))
    elif kind == "bedroom":
        im = gradient((14, 12, 24), (3, 3, 6))
        d = ImageDraw.Draw(im)
        d.rectangle([0, 820, W, H], fill=(26, 20, 26))
        d.rectangle([140, 180, 520, 820], fill=(2, 2, 2))   # left door
        d.rectangle([1400, 180, 1780, 820], fill=(2, 2, 2))  # right door
        d.rectangle([820, 160, 1100, 820], fill=(6, 6, 10))  # closet
        d.line([(960, 160), (960, 820)], fill=(30, 26, 36), width=6)
        d.rectangle([600, 760, 1320, 900], fill=(50, 30, 60))  # bed
        d.ellipse([1140, 640, 1220, 720], fill=(170, 130, 40))  # fredbear plush
    d.text((960, 120), label, font=font(52, True), fill=accent, anchor="mm")
    finish(im, name)


def ch3_art():
    bg_fright("fright_office", "", kind="office")
    bg_fright("fright_hall", "", kind="hall")
    bg_fright("fright_arcade", "ARCADE", (60, 90, 70), kind="arcade")
    bg_fright("fright_storage", "PROP STORAGE", (90, 76, 50), kind="storage")
    bg_fright("fright_vent", "", kind="vent")
    bg_fright("fright_attraction", "FAZBEAR'S FRIGHT", (130, 40, 50), kind="attraction")
    bg_fright("bedroom", "", kind="bedroom")
    # phantoms: burnt, desaturated, glowing pinprick eyes. "fixed" = freed, bright.
    for key, base in (("phantomfreddy", "freddy"), ("phantomchica", "chica"), ("phantomfoxy", "foxy")):
        c = dict(CHARS[base]); c["eye"] = (255, 255, 255); c.pop("hook", None) if key == "phantomfoxy" else None
        CHARS[key] = c
        draw_char(key, 0)
        im = Image.open(os.path.join(IMG, "chars", f"{key}_broken.png")).convert("RGBA")
        r, g, b, a = im.split()
        lum = Image.merge("RGB", (r, g, b)).convert("L")
        burnt = Image.merge("RGB", (lum.point(lambda v: int(v * 0.55)), lum.point(lambda v: int(v * 0.62)), lum.point(lambda v: int(v * 0.42))))
        burnt.putalpha(a.point(lambda v: int(v * 0.9)))
        d = ImageDraw.Draw(burnt)
        cx = CW // 2
        for sgn in (-1, 1):
            d.ellipse([cx + sgn * 75 - 9, 210 - 9, cx + sgn * 75 + 9, 210 + 9], fill=(255, 255, 255, 255))
        burnt.save(os.path.join(IMG, "chars", f"{key}_broken.png"))
        CHARS[key] = dict(CHARS[base])
        draw_char(key, 3)
        for st in ("arms", "legs"):
            pth = os.path.join(IMG, "chars", f"{key}_{st}.png")
            if os.path.exists(pth):
                os.remove(pth)
    # Springtrap: rotted green rabbit suit, exposed wiring, missing ear. Real, not a phantom.
    CHARS["springtrap"] = dict(fur=(112, 124, 56), belly=(140, 140, 80), eye=(220, 220, 200), ears="long", withered=True)
    draw_char("springtrap", 2)
    src = os.path.join(IMG, "chars", "springtrap_legs.png")
    im = Image.open(src).convert("RGBA")
    d = ImageDraw.Draw(im)
    cx = CW // 2
    for (x0, y0) in [(cx - 60, 520), (cx + 80, 620), (cx - 140, 700), (cx + 20, 760)]:
        d.line([(x0, y0), (x0 + 30, y0 + 50), (x0 + 10, y0 + 90)], fill=(150, 40, 30), width=6)
    for s in (-1, 1):  # knee springlocks, the weak point
        d.ellipse([cx + s * 110 - 26, 846, cx + s * 110 + 26, 898], fill=(150, 150, 150), outline=(60, 60, 60), width=6)
    im.save(os.path.join(IMG, "chars", "springtrap_broken.png"))
    hurt = im.copy()
    red = Image.new("RGBA", im.size, (200, 20, 20, 0))
    red.putalpha(im.split()[3].point(lambda v: int(v * 0.2)))
    hurt.alpha_composite(red)
    hurt.save(os.path.join(IMG, "chars", "springtrap_hurt.png"))
    os.remove(src)


# ------------------------------------------------------------ Chapter 4 art

def ch4_art():
    # hallway (left; the right door uses a mirrored copy)
    im = gradient((14, 12, 20), (2, 2, 4))
    d = ImageDraw.Draw(im)
    d.polygon([(0, 0), (700, 300), (700, 760), (0, H)], fill=(20, 16, 26))
    d.polygon([(W, 0), (1220, 300), (1220, 760), (W, H)], fill=(16, 12, 20))
    d.rectangle([700, 300, 1220, 760], fill=(6, 5, 8))
    d.polygon([(0, H), (700, 760), (1220, 760), (W, H)], fill=(24, 20, 22))
    for i in range(5):
        x = 80 + i * 120
        d.rectangle([x, 200 + i * 22, x + 70, 300 + i * 22], fill=(60, 40, 50))  # picture frames
    d.rectangle([0, 0, 120, H], fill=(40, 30, 30))  # door frame edge
    finish(im, "n4_hall")
    # door held shut
    im = gradient((40, 28, 22), (18, 12, 10))
    d = ImageDraw.Draw(im)
    d.rectangle([380, 0, 1540, H], fill=(70, 48, 34))
    for y0 in (80, 560):
        d.rectangle([480, y0, 1440, y0 + 420], outline=(50, 34, 24), width=14)
    d.ellipse([1360, 520, 1440, 600], fill=(170, 140, 60))
    for s in (-1, 1):
        d.ellipse([960 + s * 180 - 90, 820, 960 + s * 180 + 90, 1100], fill=(225, 190, 160))  # hands on the door
    finish(im, "n4_door_closed", vignette=0.6)
    # closet open
    im = gradient((10, 8, 14), (2, 2, 3))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 420, H], fill=(46, 32, 24)); d.rectangle([1500, 0, W, H], fill=(46, 32, 24))
    d.rectangle([420, 0, 1500, H], fill=(4, 3, 5))
    d.line([(440, 160), (1480, 160)], fill=(70, 70, 70), width=10)
    for x in (520, 700, 1200, 1380):
        d.polygon([(x, 160), (x - 60, 480), (x + 60, 480)], fill=(30, 26, 40))  # hanging clothes
    finish(im, "n4_closet")
    im = gradient((40, 28, 22), (18, 12, 10))
    d = ImageDraw.Draw(im)
    d.rectangle([300, 0, 958, H], fill=(70, 48, 34)); d.rectangle([962, 0, 1620, H], fill=(70, 48, 34))
    for x in range(330, 1600, 60):
        d.line([(x, 60), (x, H - 60)], fill=(54, 36, 26), width=8)
    for s in (-1, 1):
        d.ellipse([960 + s * 120 - 80, 820, 960 + s * 120 + 80, 1100], fill=(225, 190, 160))
    finish(im, "n4_closet_closed", vignette=0.6)
    # bed
    im = gradient((14, 10, 22), (3, 2, 6))
    d = ImageDraw.Draw(im)
    d.rectangle([200, 560, 1720, 960], fill=(60, 36, 72))
    d.rectangle([200, 520, 1720, 600], fill=(80, 50, 96))
    d.ellipse([380, 460, 760, 600], fill=(200, 200, 210))  # pillow
    d.rectangle([180, 300, 240, 1000], fill=(40, 26, 20)); d.rectangle([1680, 300, 1740, 1000], fill=(40, 26, 20))
    finish(im, "n4_bed")
    # elevator (Chapter 4 ending / Chapter 5)
    im = gradient((40, 40, 46), (14, 14, 18))
    d = ImageDraw.Draw(im)
    d.rectangle([360, 80, 1560, 1000], fill=(70, 70, 78))
    d.line([(960, 80), (960, 1000)], fill=(30, 30, 34), width=10)
    d.rectangle([1620, 360, 1780, 720], fill=(50, 50, 56))
    for k in range(4):
        d.ellipse([1670, 390 + k * 80, 1730, 450 + k * 80], fill=(200, 180, 90) if k == 3 else (110, 110, 120))
    d.rectangle([700, 140, 1220, 300], fill=(10, 20, 30))
    d.text((960, 220), "CIRCUS BABY'S", font=font(44, True), fill=(220, 80, 120), anchor="mm")
    finish(im, "elevator")
    # nightmares: darker, ragged, rows of sharp teeth and claws
    defs = {
        "nightmarefreddy": ("freddy", None), "nightmarebonnie": ("bonnie", None),
        "nightmarechica": ("chica", None), "nightmarefoxy": ("foxy", None),
        "fredbear": (None, dict(fur=(190, 150, 50), belly=(220, 190, 110), eye=(200, 80, 220), ears="round", hat=True,
                                tie=(120, 40, 160))),
    }
    for key, (base, cdef) in defs.items():
        c = dict(CHARS[base]) if base else dict(cdef)
        c["withered"] = True
        c["eye"] = (255, 60, 60) if key != "fredbear" else c["eye"]
        CHARS[key] = c
        draw_char(key, 2)
        src = os.path.join(IMG, "chars", f"{key}_legs.png")
        im = Image.open(src).convert("RGBA")
        r, g, b, a = im.split()
        im = Image.merge("RGBA", (r.point(lambda v: int(v * 0.62)), g.point(lambda v: int(v * 0.55)), b.point(lambda v: int(v * 0.55)), a))
        d = ImageDraw.Draw(im)
        cx = CW // 2
        # sharp teeth across the belly mouth
        d.rounded_rectangle([cx - 120, 560, cx + 120, 720], 40, fill=(20, 4, 6))
        for k in range(-5, 6):
            x = cx + k * 21
            d.polygon([(x - 10, 560), (x + 10, 560), (x, 610)], fill=(235, 225, 210))
            d.polygon([(x - 10, 720), (x + 10, 720), (x, 672)], fill=(235, 225, 210))
        # claws
        for s in (-1, 1):
            for k in range(3):
                x = cx + s * 230 + (k - 1) * 30
                d.polygon([(x - 8, 770), (x + 8, 770), (x + s * 6, 830)], fill=(230, 230, 230))
        im.save(os.path.join(IMG, "chars", f"{key}_broken.png"))
        os.remove(src)


# ---------------------------------------------------------------------- audio

RATE = 22050


def write_wav(name, samples):
    with wave.open(os.path.join(AUD, name), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, s)) * 30000)) for s in samples))


def audio():
    # jumpscare screech: noisy, detuned sawtooth sweep
    n = int(RATE * 1.6)
    s = []
    for i in range(n):
        t = i / RATE
        f = 380 + 900 * math.sin(t * 9) * math.exp(-t)
        saw = ((t * f) % 1.0) * 2 - 1
        saw2 = ((t * f * 1.49) % 1.0) * 2 - 1
        env = min(1, t * 40) * (1 - t / 1.6)
        s.append((saw * 0.5 + saw2 * 0.4 + random.uniform(-0.6, 0.6)) * env)
    write_wav("jumpscare.wav", s)
    # ambient hum loop (fluorescent lights + fan)
    n = int(RATE * 8)
    s = []
    for i in range(n):
        t = i / RATE
        s.append(0.12 * math.sin(2 * math.pi * 60 * t) + 0.06 * math.sin(2 * math.pi * 120 * t)
                 + 0.03 * random.uniform(-1, 1))
    write_wav("ambience.wav", s)
    # success ding
    n = int(RATE * 0.35)
    write_wav("check_good.wav", [math.sin(2 * math.pi * 880 * i / RATE) * math.exp(-i / RATE * 9) * 0.7 for i in range(n)])
    # great ding
    write_wav("check_great.wav", [(math.sin(2 * math.pi * 1320 * i / RATE) + math.sin(2 * math.pi * 1760 * i / RATE))
                                  * 0.35 * math.exp(-i / RATE * 7) for i in range(int(RATE * 0.5))])
    # alert tick before check
    write_wav("check_alert.wav", [math.sin(2 * math.pi * 1500 * i / RATE) * (1 if (i // 900) % 2 == 0 else 0) * 0.4
                                  for i in range(int(RATE * 0.25))])
    # mechanical whirr for repairs
    n = int(RATE * 1.2)
    s = []
    for i in range(n):
        t = i / RATE
        f = 90 + 160 * t
        s.append((((t * f) % 1.0) * 2 - 1) * 0.3 * math.sin(math.pi * t / 1.2) + random.uniform(-0.08, 0.08))
    write_wav("servo.wav", s)
    # 6AM chime
    notes = [523, 659, 784, 1047]
    s = []
    for k, f in enumerate(notes):
        for i in range(int(RATE * 0.4)):
            s.append(math.sin(2 * math.pi * f * i / RATE) * math.exp(-i / RATE * 4) * 0.6)
    write_wav("chime.wav", s)


def ch4_audio():
    # slow heavy breathing (loops)
    n = int(RATE * 3.2)
    s = []
    lp = 0.0
    for i in range(n):
        t = i / RATE
        env = max(0.0, math.sin(math.pi * (t % 1.6) / 1.6)) ** 2
        lp += 0.08 * (random.uniform(-1, 1) - lp)
        s.append(lp * env * 2.4)
    write_wav("breathing.wav", s)
    # footsteps: four low thuds
    s = []
    for k in range(4):
        for i in range(int(RATE * 0.32)):
            t = i / RATE
            s.append((math.sin(2 * math.pi * 70 * t) + random.uniform(-0.3, 0.3)) * math.exp(-t * 22) * 0.9)
    write_wav("footsteps.wav", s)
    # giggle: a few quick wobbly notes
    s = []
    for f in (520, 610, 560, 660, 590):
        for i in range(int(RATE * 0.11)):
            t = i / RATE
            s.append(math.sin(2 * math.pi * (f + 40 * math.sin(t * 60)) * t) * math.sin(math.pi * t / 0.11) * 0.5)
    write_wav("giggle.wav", s)


def musicbox_tune():
    # "My Grandfather's Clock"-ish public domain feel, simple plucked notes
    notes = [392, 523, 494, 523, 587, 523, 587, 659, 587, 523, 494, 440, 392, 0, 392, 523, 494, 523, 587, 523, 494, 440, 392]
    s = []
    for f in notes:
        for i in range(int(RATE * 0.32)):
            t = i / RATE
            v = (math.sin(2 * math.pi * f * t) + 0.3 * math.sin(4 * math.pi * f * t)) * math.exp(-t * 6) * 0.45 if f else 0
            s.append(v)
    write_wav("musicbox.wav", s)


if __name__ == "__main__":
    bg_exterior(); bg_office(); bg_dining(); bg_stage(); bg_cove(); bg_kitchen(); bg_parts(); bg_menu()
    bg_partyroom(); bg_prize(); bg_office2(); bg_kidscove()
    draw_puppet()
    for st in range(4):
        draw_musicbox(st)
    for k in CHARS:
        for st in range(4):
            draw_char(k, st)
    ch3_art()
    ch4_art()
    audio()
    ch4_audio()
    musicbox_tune()
    print("placeholders written")
