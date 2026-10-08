from PIL import Image, ImageDraw, ImageFont
import math
from pathlib import Path

W, H = 1000, 371
FRAMES = 16
DURATION_MS = 150

# Palette sampled conceptually from the supplied profile-photo background:
# deep charcoal, warm grey, dark brown, copper/amber highlights.
BG = (20, 20, 24)
CHARCOAL = (43, 42, 42)
WARM_GREY = (92, 84, 79)
COPPER = (217, 138, 95)
COPPER_LIGHT = (229, 174, 150)
COPPER_DARK = (136, 82, 67)
TEXT = (238, 230, 224)
MUTED = (168, 151, 141)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "profile-hud.gif"
OUT.parent.mkdir(parents=True, exist_ok=True)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, size)

frames = []

for i in range(FRAMES):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")
    t = i / FRAMES

    # Industrial background texture.
    for x in range(24, 625, 30):
        d.line((x, 38, x, 338), fill=WARM_GREY + (18,), width=1)
    for y in range(46, 340, 30):
        d.line((24, y, 625, y), fill=WARM_GREY + (18,), width=1)
    d.line((0, 344, 500, 24), fill=COPPER + (28,), width=2)
    d.line((420, 371, 760, 30), fill=COPPER_DARK + (24,), width=2)

    # Identity block.
    d.text((34, 38), "AZARMI // ENGINEERING INTELLIGENCE",
           font=font(11, True), fill=COPPER)
    d.text((34, 78), "MOHAMMADREZA",
           font=font(31, True), fill=TEXT)
    d.text((34, 118), "AZARMI",
           font=font(37, True), fill=COPPER_LIGHT)
    d.text((36, 151),
           "CIVIL ENGINEER · CONCRETE QC · AI SYSTEMS BUILDER",
           font=font(9, True), fill=MUTED)
    d.line((35, 168, 330, 168), fill=COPPER, width=2)

    for j, label in enumerate([
        "ENGINEERING REALITY",
        "→ TRACEABLE EVIDENCE",
        "→ CONTROLLED INTELLIGENCE",
    ]):
        d.text((35, 188 + j * 23), label, font=font(10, j == 0), fill=TEXT)

    # Status module.
    d.rounded_rectangle((34, 282, 330, 333), radius=9,
                        fill=(20, 20, 24, 225),
                        outline=COPPER + (85,), width=1)
    d.text((48, 294), "SYSTEM STATUS", font=font(8, True), fill=MUTED)
    d.ellipse((48, 314, 55, 321), fill=COPPER)
    d.text((64, 310), "BUILD / RESEARCH / IMPROVE",
           font=font(9, True), fill=TEXT)

    # Animated command HUD.
    cx, cy = 814, 185
    for radius, width, color, span, rotation in [
        (142, 2, COPPER, 95, i * 22),
        (116, 2, COPPER_LIGHT, 70, -i * 30),
        (94, 2, COPPER_DARK, 48, i * 45),
    ]:
        for k in range(5):
            start = (rotation + k * 72) % 360
            d.arc(
                (cx - radius, cy - radius, cx + radius, cy + radius),
                start=start, end=start + span,
                fill=color, width=width
            )

    d.ellipse((cx - 149, cy - 149, cx + 149, cy + 149),
              outline=TEXT + (55,), width=1)

    for deg in range(0, 360, 30):
        a = math.radians(deg)
        r1, r2 = 154, 159
        d.line(
            (
                cx + math.cos(a) * r1,
                cy + math.sin(a) * r1,
                cx + math.cos(a) * r2,
                cy + math.sin(a) * r2,
            ),
            fill=COPPER + (90,),
            width=1,
        )

    # Moving scan line.
    scan_y = 50 + ((i * 23) % 270)
    d.line((cx - 160, scan_y, cx + 160, scan_y),
           fill=COPPER_LIGHT + (45,), width=1)

    # Pulse core.
    pulse = (math.sin(2 * math.pi * t) + 1) / 2
    r = 5 + int(3 * pulse)
    alpha = 120 + int(100 * pulse)
    d.ellipse((cx - r, cy - r, cx + r, cy + r),
               fill=COPPER + (alpha,))
    d.ellipse((cx - 15, cy - 15, cx + 15, cy + 15),
              outline=COPPER_LIGHT + (65,), width=1)

    # Command panel.
    d.rounded_rectangle((742, 20, 972, 57), radius=8,
                        fill=(20, 20, 24, 235),
                        outline=COPPER + (80,), width=1)
    d.text((758, 29), "COMMAND INTERFACE",
           font=font(8, True), fill=MUTED)
    d.text((758, 43), "EVIDENCE / CONTROL / DELIVERY",
           font=font(7), fill=TEXT)

    d.text((653, 342), "CONCRETE × DATA × AI × ENGINEERING",
           font=font(8, True), fill=COPPER)
    d.text((790, 353), "NO FAKE TELEMETRY",
           font=font(7), fill=MUTED)

    # 128-color palette keeps GitHub payload compact.
    frames.append(img.quantize(colors=128, method=Image.Quantize.MEDIANCUT))

frames[0].save(
    OUT,
    save_all=True,
    append_images=frames[1:],
    duration=DURATION_MS,
    loop=0,
    optimize=True,
    disposal=2,
)

print(f"generated {OUT} ({OUT.stat().st_size} bytes, {FRAMES} frames)")
