from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1200, 430
FRAMES = 16
BG = (24, 23, 24)
BG2 = (42, 40, 40)
COPPER = (173, 123, 96)
COPPER_LIGHT = (213, 169, 142)
COPPER_DARK = (110, 78, 64)
WARM_GRAY = (105, 99, 96)
WHITE = (238, 231, 226)
MUTED = (169, 159, 152)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FMB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def font(size, bold=False, mono=False):
    path = FMB if mono and bold else FM if mono else FB if bold else F
    return ImageFont.truetype(path, size)

frames = []
for i in range(FRAMES):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")

    for y in range(H):
        q = y / (H - 1)
        col = tuple(int(BG[k] * (1 - q) + BG2[k] * q * 0.30) for k in range(3))
        d.line((0, y, W, y), fill=col + (255,))

    # Warm diagonal light borrowed from the profile-photo atmosphere.
    d.polygon([(770, 0), (1200, 0), (1200, 80), (930, 430), (735, 430)],
              fill=COPPER_DARK + (30,))
    d.line((760, 430, 1200, 80), fill=COPPER + (120,), width=2)
    d.line((800, 430, 1200, 112), fill=COPPER_LIGHT + (34,), width=1)

    # Fine graphite grid.
    for x in range(24, W, 32):
        d.line((x, 22, x, H - 22), fill=WARM_GRAY + (13,), width=1)
    for y in range(24, H, 32):
        d.line((22, y, W - 22, y), fill=WARM_GRAY + (11,), width=1)

    d.rounded_rectangle((8, 8, W - 8, H - 8), radius=20,
                         outline=WARM_GRAY + (52,), width=1)
    d.line((34, 64, W - 34, 64), fill=COPPER + (72,), width=1)

    # Identity.
    d.text((40, 30), "AZARMI // ENGINEERING INTELLIGENCE",
           font=font(9, True, True), fill=COPPER_LIGHT + (255,))
    d.text((40, 96), "MOHAMMADREZA", font=font(37, True), fill=WHITE + (255,))
    d.text((40, 145), "AZARMI", font=font(48, True), fill=COPPER_LIGHT + (255,))
    d.text((43, 205),
           "CIVIL ENGINEER  ·  CONCRETE QC  ·  AI SYSTEMS BUILDER",
           font=font(9, True, True), fill=MUTED + (255,))

    # Engineering doctrine.
    d.text((43, 250), "ENGINEERING REALITY",
           font=font(9, True, True), fill=WHITE + (235,))
    d.text((43, 271), "→ TRACEABLE EVIDENCE",
           font=font(9, True, True), fill=COPPER_LIGHT + (245,))
    d.text((43, 292), "→ CONTROLLED INTELLIGENCE",
           font=font(9, True, True), fill=WHITE + (220,))
    d.text((43, 333), "Engineering first. Intelligence second.",
           font=font(13, True), fill=WHITE + (245,))

    # Process strip — descriptive, not telemetry.
    d.rounded_rectangle((39, 350, 500, 400), radius=9,
                         fill=BG + (175,), outline=WARM_GRAY + (55,), width=1)
    d.text((57, 365), "WORKING PRINCIPLE",
           font=font(7, True, True), fill=MUTED + (255,))
    pulse = (math.sin(2 * math.pi * i / FRAMES) + 1) / 2
    d.ellipse((154, 364, 161, 371),
              fill=COPPER + (130 + int(80 * pulse),))
    d.text((174, 362), "BUILD  /  RESEARCH  /  VERIFY",
           font=font(8, True, True), fill=WHITE + (235,))

    # JARVIS-like command reactor.
    cx, cy = 900, 218
    for r, a in [(150, 10), (128, 18), (106, 28)]:
        d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=COPPER + (a,))
    for r, w, a in [(146, 1, 55), (123, 1, 75), (98, 2, 105), (70, 1, 65)]:
        d.ellipse((cx-r, cy-r, cx+r, cy+r),
                  outline=COPPER + (a,), width=w)
    for rad, w, span, start, color in [
        (140, 3, 68, i * 15, COPPER_LIGHT),
        (118, 2, 92, -i * 22, COPPER),
        (94, 2, 50, i * 30, COPPER_DARK),
    ]:
        d.arc((cx-rad, cy-rad, cx+rad, cy+rad),
              start=start % 360, end=(start + span) % 360,
              fill=color + (205,), width=w)
    for deg in range(0, 360, 20):
        a = math.radians(deg)
        r1, r2 = 150, 156
        d.line((cx + math.cos(a)*r1, cy + math.sin(a)*r1,
                cx + math.cos(a)*r2, cy + math.sin(a)*r2),
               fill=MUTED + (80,), width=1)

    ang = math.radians(i * 20)
    d.line((cx, cy, cx + math.cos(ang)*128, cy + math.sin(ang)*128),
           fill=COPPER_LIGHT + (70,), width=2)

    rr = 40 + int(3 * pulse)
    d.ellipse((cx-rr, cy-rr, cx+rr, cy+rr),
              fill=(14, 14, 15, 225), outline=WHITE + (75,), width=1)
    d.ellipse((cx-23, cy-23, cx+23, cy+23),
              outline=COPPER + (175,), width=2)
    d.text((cx, cy-9), "AZ", font=font(18, True, True),
           fill=WHITE + (245,), anchor="mm")

    # Command identity + signature systems.
    d.rounded_rectangle((760, 32, 1156, 78), radius=9,
                         fill=BG + (190,), outline=WARM_GRAY + (60,), width=1)
    d.text((782, 48), "PERSONAL COMMAND INTERFACE",
           font=font(8, True, True), fill=MUTED + (255,))
    d.text((782, 65), "MODE / ENGINEERING",
           font=font(8, True, True), fill=COPPER_LIGHT + (255,))

    d.rounded_rectangle((744, 350, 1160, 401), radius=9,
                         fill=BG + (190,), outline=WARM_GRAY + (60,), width=1)
    d.text((765, 365), "SIGNATURE SYSTEMS",
           font=font(7, True, True), fill=MUTED + (255,))
    d.text((765, 386), "AGENT HQ   ·   CRETIQ   ·   VIRTUAL LAB",
           font=font(8, True, True), fill=WHITE + (235,))

    # One restrained scanning sweep.
    sy = 82 + ((i * 17) % (H - 170))
    d.line((40, sy, 1160, sy), fill=COPPER_LIGHT + (27,), width=1)

    d.text((40, 415), "REAL DATA · TRACEABLE · VERIFIABLE",
           font=font(7, True, True), fill=MUTED + (220,))
    d.text((1160, 415), "NO FAKE TELEMETRY",
           font=font(7, True, True), fill=COPPER + (220,), anchor="ra")

    frames.append(img.quantize(colors=64, method=Image.Quantize.MEDIANCUT))

frames[0].save(
    "assets/profile-hud.gif",
    save_all=True,
    append_images=frames[1:],
    duration=130,
    loop=0,
    optimize=True,
)
