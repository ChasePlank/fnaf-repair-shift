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
    if c.get("hollow") and stage < 3:
        d = ImageDraw.Draw(im)
        for (x0, y0, x1, y1) in [(cx - 150, 450, cx - 60, 560), (cx - 120, 600, cx - 20, 700), (cx + 60, 120, cx + 140, 220)]:
            d.polygon([(x0, y0), (x1, y0 + 20), (x1 - 20, y1), (x0 + 10, y1 - 10)], fill=(18, 14, 10))
        for k in range(6):
            x = cx - 170 + k * 60
            d.line([(x, 430 + (k % 3) * 40), (x + 30, 470 + (k % 2) * 50), (x + 10, 520)], fill=(60, 45, 15), width=4)
    names = ["broken", "arms", "legs", "fixed"]
    im.save(os.path.join(IMG, "chars", f"{key}_{names[stage]}.png"))


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


if __name__ == "__main__":
    bg_exterior(); bg_office(); bg_dining(); bg_stage(); bg_cove(); bg_kitchen(); bg_parts(); bg_menu()
    for k in CHARS:
        for st in range(4):
            draw_char(k, st)
    audio()
    print("placeholders written")
